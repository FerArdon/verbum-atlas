console.log("=== DIAGNÓSTICO VERBUM ATLAS ===");
console.log("1. bibleData existe?", typeof bibleData !== 'undefined');
console.log("2. bibleData es array?", Array.isArray(bibleData));
console.log("3. Cantidad de libros:", bibleData ? bibleData.length : 0);
console.log("4. Primer libro:", bibleData ? bibleData[0] : null);
console.log("5. Elemento #booksGrid existe?", document.getElementById('booksGrid') !== null);
console.log("6. Elemento #bibleVersion existe?", document.getElementById('bibleVersion') !== null);
console.log("7. Backend conectado?", typeof backend !== 'undefined' && backend !== null);
