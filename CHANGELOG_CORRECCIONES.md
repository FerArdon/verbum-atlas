# Changelog de Correcciones - Verbum Atlas 2026

## Fecha: 5 de enero de 2026

### 🔴 CORRECCIONES CRÍTICAS (Seguridad)

#### 1. **Exposición de API Key - CORREGIDO**
- **Problema**: La clave de API de Gemini estaba hardcodeada en `run_app.py`
- **Solución**: 
  - Removida del código fuente
  - Implementada carga segura por el usuario en tiempo de ejecución
  - Agregada validación y manejo de errores en `setApiKey()`
  - Actualizado archivo `verbum atlas api.txt` con instrucciones de seguridad

#### 2. **Manejo de errores mejorado**
- **Cambios en `run_app.py`**:
  - `getDailyReading()`: Validación de entrada, errores más descriptivos
  - `getChapterText()`: Validación de parámetros, limpieza de mensajes de error
  - `askAgent()`: Límite de longitud de pregunta (5000 caracteres), validación de entrada
  - `setApiKey()`: Validación y manejo robusto de excepciones
  - `BibleMapApp.__init__()`: Mejor manejo de excepciones al cargar recursos

### 🟡 CORRECCIONES FUNCIONALES

#### 3. **Referencias HTML incorrectas - CORREGIDO**
- **Problema**: `versionSelect` apuntaba a ID incorrecto
- **Solución**: Corregido a `bibleVersion` (el ID real en HTML)

#### 4. **Selectores CSS inconsistentes - CORREGIDO**
- **Problema**: Código buscaba `.filter-chip` pero HTML usaba `.filter-btn`
- **Solución**: Actualizado selector a `.filter-btn`

#### 5. **Selectores de vistas incorrectos - CORREGIDO**
- **Problema**: Código buscaba `.view-section` pero HTML usaba `.view`
- **Solución**: Actualizado selector a `.view`

#### 6. **Callbacks en getChapterText - CORREGIDO**
- **Problema**: Método Python no soportaba callbacks pero JS intentaba usarlos
- **Solución**: Mejorado manejo con parseo y validación de respuesta JSON

### 🟠 MEJORAS DE CALIDAD

#### 7. **Protección contra XSS - IMPLEMENTADO**
- **Cambios**:
  - `renderBooks()`: Ahora crea elementos DOM de forma segura en lugar de usar innerHTML
  - `addMessage()`: Usa `textContent` en lugar de `innerHTML` para mensajes de chat
  - Sanitización de búsquedas y entradas del usuario

#### 8. **Validación de elementos DOM - IMPLEMENTADO**
- **Cambios**:
  - `setupLexDivina()`: Valida existencia de elementos antes de usarlos
  - Mejor manejo de eventos y advertencias en consola
  - Alertas más descriptivas al usuario

#### 9. **Validación de archivos JS - IMPLEMENTADO**
- **Cambios**:
  - `index.html`: Agregado check para verificar que `bibleData` está cargado
  - Error amigable si falla la carga de `data.js`

#### 10. **Manejo de errores en lectura de capítulos - IMPLEMENTADO**
- **Cambios**:
  - Mensajes de error visuales con estilos en `openReader()`
  - Try-catch mejorado con información útil en consola

### 📦 CAMBIOS EN ARCHIVOS

#### `run_app.py`
- ✅ Removida API key hardcodeada
- ✅ Mejorado manejo de errores en 5 métodos principales
- ✅ Agregada validación de entrada
- ✅ Mejor logging y mensajes informativos

#### `js/app.js`
- ✅ Corregidas referencias a IDs HTML
- ✅ Corregidos selectores CSS
- ✅ Mejorado manejo de errores en callbacks
- ✅ Implementada protección contra XSS
- ✅ Agregada validación de elementos DOM
- ✅ Mejorada función `setupLexDivina()`
- ✅ Mejorada función `addMessage()`

#### `index.html`
- ✅ Agregado check de validación para `bibleData`
- ✅ Error amigable si falla carga de scripts

#### `Verbum Atlas 2026.spec`
- ✅ Agregado `libro_mormon.db` a la lista de archivos compilados

#### `verbum atlas api.txt`
- ✅ Removida API key
- ✅ Agregadas instrucciones de seguridad

---

## Notas Importantes

### Antes de compilar/distribuir:
1. ✅ Verifica que NO haya claves API en el código
2. ✅ Prueba la carga de `data.js` en el navegador web
3. ✅ Verifica que Lex Divina pida configurar la API Key
4. ✅ Prueba la lectura de capítulos en las 3 versiones (Católica, Protestante, Mormón)

### Para usuarios:
1. La aplicación ahora pide configurar la API Key de Gemini
2. Es seguro distribuir - no contiene claves comprometidas
3. Mejor manejo de errores - mensajes más claros en la UI

### Seguridad:
- ❌ RIESGO ELIMINADO: API key hardcodeada
- ✅ IMPLEMENTADO: Validación de entrada XSS
- ✅ IMPLEMENTADO: Manejo seguro de errores
- ✅ IMPLEMENTADO: Límites de entrada en requests

---

## Testing Recomendado

```
1. Abre Verbum Atlas 2026
2. Intenta usar Lex Divina sin configurar API Key → Debe mostrar error amigable
3. Configura tu propia API Key → Debe funcionar
4. Busca un libro → Debe renderizar sin errores
5. Lee un capítulo → Debe mostrar versos correctamente
6. Cambia entre versiones → Debe funcionar sin problemas
7. Abre DevTools (F12) → No debe haber errores de console
```

---

**Todas las funcionalidades mantienen intactas. Solo se agregaron mejoras de seguridad y estabilidad.**
