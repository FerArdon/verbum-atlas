"use strict";

var QWebChannelMessageTypes = {
    signal: 1,
    propertyUpdate: 2,
    init: 3,
    idle: 4,
    debug: 5,
    invokeMethod: 6,
    connectToSignal: 7,
    disconnectFromSignal: 8,
    setProperty: 9,
    response: 10,
};

var QWebChannel = function (transport, initCallback) {
    if (typeof transport !== "object" || typeof transport.send !== "function") {
        console.error("The QWebChannel expects a transport object with a send function and onmessage callback property." +
            " Given is: transport: " + typeof (transport) + ", transport.send: " + typeof (transport.send));
        return;
    }

    var channel = this;
    this.transport = transport;

    this.send = function (data) {
        if (typeof (data) !== "string") {
            data = JSON.stringify(data);
        }
        channel.transport.send(data);
    }

    this.transport.onmessage = function (message) {
        var data = message.data;
        if (typeof data === "string") {
            data = JSON.parse(data);
        }
        switch (data.type) {
            case QWebChannelMessageTypes.signal:
                channel.handleSignal(data);
                break;
            case QWebChannelMessageTypes.response:
                channel.handleResponse(data);
                break;
            case QWebChannelMessageTypes.propertyUpdate:
                channel.handlePropertyUpdate(data);
                break;
            default:
                console.error("invalid message received:", message.data);
                break;
        }
    }

    this.execCallbacks = {};
    this.execId = 0;
    this.exec = function (data, callback) {
        if (!callback) {
            // if no callback is given, send directly
            channel.send(data);
            return;
        }
        if (channel.execId === Number.MAX_VALUE) {
            // wrap
            channel.execId = 0;
        }
        data.id = channel.execId++;
        channel.execCallbacks[data.id] = callback;
        channel.send(data);
    };

    this.objects = {};

    this.handleSignal = function (message) {
        var object = channel.objects[message.object];
        if (object) {
            object.signalEmitted(message.signal, message.args);
        } else {
            console.warn("Unhandled signal: " + message.object + "::" + message.signal);
        }
    }

    this.handleResponse = function (message) {
        if (!message.hasOwnProperty("id")) {
            console.error("Invalid response message received: ", message);
            return;
        }
        channel.execCallbacks[message.id](message.data);
        delete channel.execCallbacks[message.id];
    }

    this.handlePropertyUpdate = function (message) {
        for (var i in message.data) {
            var data = message.data[i];
            var object = channel.objects[data.object];
            if (object) {
                object.propertyUpdate(data.signals, data.properties);
            } else {
                console.warn("Unhandled property update: " + data.object + "::" + data.signal);
            }
        }
        channel.execCallbacks[message.id](data);
        delete channel.execCallbacks[message.id];
    }

    this.debug = function (message) {
        channel.send({ type: QWebChannelMessageTypes.debug, data: message });
    };

    channel.exec({ type: QWebChannelMessageTypes.init }, function (data) {
        for (var objectName in data) {
            var object = new QObject(objectName, data[objectName], channel);
        }
        for (var objectName in data) {
            var object = channel.objects[objectName];
            object.unwrapProperties();
        }
        if (initCallback) {
            initCallback(channel);
        }
        channel.exec({ type: QWebChannelMessageTypes.idle });
    });
};

function QObject(name, data, webChannel) {
    this.__id__ = name;
    webChannel.objects[name] = this;

    // List of callbacks that get invoked upon signal emission
    this.__objectSignals__ = {};

    // Cache of all properties, updated when a notify signal is emitted
    this.__propertyCache__ = {};

    var object = this;

    // ----------------------------------------------------------------------

    this.unwrapProperties = function () {
        for (var propertyIdx in data.properties) {
            object.unwrapProperty(data.properties[propertyIdx]);
        }
    }

    this.unwrapProperty = function (property) {
        object.__propertyCache__[property[0]] = property[1];
        object[property[0]] = property[1];
        object.__defineGetter__(property[0], function () {
            return object.__propertyCache__[property[0]];
        });
        object.__defineSetter__(property[0], function (value) {
            if (value === undefined) return;
            object.__propertyCache__[property[0]] = value;
            webChannel.exec({ type: QWebChannelMessageTypes.setProperty, object: object.__id__, property: property[0], value: value });
        });
    }

    this.unwrapSignals = function () {
        for (var signalIdx in data.signals) {
            object.unwrapSignal(data.signals[signalIdx]);
        }
    }

    this.unwrapSignal = function (signal) {
        var signalName = signal[0];
        var signalIndex = signal[1];
        object[signalName] = function () {
            var args = [];
            for (var i = 0; i < arguments.length; i++) {
                args.push(arguments[i]);
            }
            var callback = args[args.length - 1];
            if (typeof callback !== "function") {
                callback = undefined;
            } else {
                args.pop();
            }
            webChannel.exec({ type: QWebChannelMessageTypes.invokeMethod, object: object.__id__, method: signalIndex, args: args }, function (response) {
                if (response !== undefined) {
                    var result = response;
                    if (callback) {
                        callback(result);
                    }
                }
            });
        };
        object.connect = function (signalName, functor) {
            if (typeof functor !== "function") {
                console.error("connect client error: functor is not a function");
                return;
            }
            // ... (Simplified for brevity, usually connects client side logic)
        };
    }

    this.propertyUpdate = function (signals, properties) {
        // update property cache
        for (var propertyIdx in properties) {
            var property = properties[propertyIdx];
            object.__propertyCache__[property[0]] = property[1];
        }
    }

    this.signalEmitted = function (signalName, signalArgs) {
        var callback = object.__objectSignals__[signalName];
        if (callback) {
            callback.apply(object, signalArgs);
        }
    }

    // Core unwrapping logic for methods
    for (var methodIdx in data.methods) {
        var method = data.methods[methodIdx];
        var methodName = method[0];
        var methodIndex = method[1];

        object[methodName] = (function (methodIndex) {
            return function () {
                var args = [];
                var callback;
                for (var i = 0; i < arguments.length; i++) {
                    var arg = arguments[i];
                    if (typeof arg === "function") {
                        callback = arg;
                    } else {
                        args.push(arg);
                    }
                }

                webChannel.exec({
                    "type": QWebChannelMessageTypes.invokeMethod,
                    "object": object.__id__,
                    "method": methodIndex,
                    "args": args
                }, function (response) {
                    if (callback) {
                        callback(response);
                    }
                });
            };
        })(methodIndex);
    }
}
