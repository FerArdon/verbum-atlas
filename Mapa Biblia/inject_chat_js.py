# Código JS para el chat
chat_js = """
// ==========================================
// LÓGICA DE LEX DIVINA (CHAT IA)
// ==========================================
const chatContainer = document.getElementById('chatContainer');
const chatInput = document.getElementById('chatInput');
const sendChatBtn = document.getElementById('sendChatBtn');
const clearChatBtn = document.getElementById('clearChatBtn');

if (sendChatBtn) {
    sendChatBtn.onclick = sendMessage;
    // También enter en el textarea
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

if (clearChatBtn) {
    clearChatBtn.onclick = () => {
        if(chatContainer) chatContainer.innerHTML = '<div style="text-align:center; color:#9CA3AF; margin-top:150px;"><p>Haz una pregunta sobre las escrituras...</p></div>';
    };
}

function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    
    // UI Usuario
    addMessage(text, 'user');
    chatInput.value = '';
    
    // UI Loading
    const loadingId = addMessage("Meditando...", 'ai');
    
    // Llamada Backend (askAgent)
    if (typeof backend !== 'undefined' && backend) {
        // Contexto simple: verso actual si existe
        let context = "";
        const verseText = document.getElementById('verseContent');
        if (verseText && verseText.innerText) {
             context = "Contexto actual de lectura: " + verseText.innerText.substring(0, 1000);
        }
        
        backend.askAgent(context, text, (response) => {
            // Borrar loading
            const loadingElem = document.getElementById(loadingId);
            if (loadingElem) loadingElem.remove();
            
            // Respuesta
            addMessage(response, 'ai');
        });
    } else {
        const loadingElem = document.getElementById(loadingId);
        if (loadingElem) loadingElem.innerText = "Error: Backend no conectado.";
    }
}

function addMessage(text, sender) {
    if (!chatContainer) return;
    const div = document.createElement('div');
    const isUser = sender === 'user';
    div.id = 'msg_' + Date.now() + Math.random();
    div.style.cssText = `margin-bottom:15px; text-align:${isUser ? 'right' : 'left'};`;
    
    const bubble = document.createElement('div');
    bubble.style.cssText = `
        display:inline-block; max-width:80%; padding:12px 18px; border-radius:16px;
        background:${isUser ? '#8B5CF6' : 'white'}; color:${isUser ? 'white' : '#374151'};
        box-shadow:0 2px 5px rgba(0,0,0,0.05); border:${isUser ? 'none' : '1px solid #E5E7EB'};
        border-bottom-${isUser ? 'right' : 'left'}-radius:4px;
        word-wrap: break-word;
    `;
    bubble.innerText = text; 
    div.appendChild(bubble);
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return div.id;
}
"""

with open(r'js\app.js', 'a', encoding='utf-8') as f:
    f.write("\n" + chat_js)
    
print("✓ Lógica de Chat inyectada en app.js")
