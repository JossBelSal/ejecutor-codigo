# Trampas conocidas

Errores que ya costaron tiempo o que fallan en silencio. **Antes de entregar código** en un
lenguaje de esta lista, revisa su sección.

Formato: **trampa** — síntoma → solución.

## Cómo crece este archivo

Cuando en `depurar-error` se encuentre una causa que valga la pena recordar, propón una entrada
nueva con el formato de arriba:

- En **Claude Code**: con aprobación, agrégala en la sección del lenguaje (créala si no existe).
- En **chats**: entrega la entrada en un bloque para que el usuario la pegue en su copia maestra.

---

## Del usuario (aprendidas en sus proyectos)

### VBA

- **`Find()` sin parámetros explícitos** — falla de forma intermitente porque Excel hereda la
  configuración de la búsqueda anterior, incluso de un Ctrl+F manual → especifica siempre
  `LookIn`, `LookAt` y `MatchCase` en cada llamada.
- **Última fila con filas de control o totales debajo de los datos** —
  `ws.Cells(ws.Rows.Count, "A").End(xlUp).Row` devuelve la fila de control, no la del último
  dato → usa `ws.Range("A3").End(xlDown).Row` desde la primera fila de datos (ojo: este se
  detiene en la primera celda vacía dentro de los datos).
- **`Public a, b, c As Integer`** — solo `c` queda como `Integer`; `a` y `b` quedan `Variant` →
  declara el tipo de cada variable.

### AutoIt

- **`Opt()` / `AutoItSetOption()` o `WinTitleMatchMode` a mitad del script** — no afectan a lo
  que ya se configuró o se ejecutó antes → ponlos al inicio del script (idealmente en `Config.au3`).
- **Cierre de popups con coincidencia parcial de título** — cierra ventanas equivocadas → dentro
  de la función que cierra popups usa coincidencia exacta (modo 1), `ControlClick`/`ControlSend`
  para interactuar en segundo plano y `Return` en cuanto cierres el primer popup encontrado.
- **`.Children($i)` al recorrer objetos COM de SAP** — resultados poco confiables → usa
  `.Children.ElementAt($i)`.

### FoxPro

- **`REPLACE ALL` es irreversible** — no hay deshacer → siempre `COPY TO respaldo.dbf` antes.

### Git

- **Primer commit sin `.gitignore`** — se suben configuración y datos sensibles → configura
  `.gitignore` (y usa `git stash` si hace falta) **antes** de hacer `git add`.

---

## Generales

### Python

- **Argumento por defecto mutable** (`def f(x, lista=[])`) — la lista se comparte entre llamadas
  → usa `lista=None` y créala dentro.
- **Dinero con `float`** — `0.1 + 0.2 != 0.3`, errores de redondeo → usa `decimal.Decimal` y
  redondea explícitamente.
- **Rutas de Windows en cadenas normales** — `"C:\nuevo"` convierte `\n` en salto de línea → usa
  `pathlib.Path` o cadenas crudas `r"C:\nuevo"`.
- **`except:` sin tipo** — también atrapa `KeyboardInterrupt` y oculta errores reales → atrapa
  excepciones concretas, o `Exception` como mínimo, y regístralas en el log.
- **Modificar una lista mientras se recorre** — se saltan elementos → recorre una copia o arma una
  lista nueva.
- **openpyxl y fórmulas** — openpyxl no calcula fórmulas; con `data_only=True` solo lee el último
  valor que guardó Excel (en archivos creados por openpyxl ese valor es `None`) → calcula en Python
  o abre y guarda con Excel.
- **CSV para Excel con acentos** — Excel muestra caracteres raros → escribe con `encoding="utf-8-sig"`.

### Datos (Excel / CSV)

- **Ceros a la izquierda** (números de empleado, cuentas, códigos) — se pierden al leer como
  número → léelos como texto (`dtype=str` en pandas, formato texto en Excel).
- **Fechas como texto** — se interpretan distinto según la configuración regional (día/mes vs
  mes/día) → conviértelas con un formato explícito.

### VBA (general)

- **`On Error Resume Next` sin `On Error GoTo 0`** — oculta todos los errores que siguen → limita
  su alcance a la línea que lo necesita y restaura el manejo de errores.
- **`Range` o `Cells` sin hoja** — en un módulo estándar apuntan a la hoja activa, que puede no
  ser la esperada → califica siempre: `ws.Range(...)`.
- **Configuración de Excel sin restaurar** (`ScreenUpdating`, `Calculation`, `EnableEvents`) — si
  la macro truena, Excel queda así → restaura en la salida de error.

### AutoIt (general)

- **`@error` revisado tarde** — otra llamada a función lo reinicia → revísalo inmediatamente
  después de la función que lo establece.
- **`StringSplit` devuelve el conteo en `[0]`** — los datos empiezan en `[1]` → tenlo en cuenta o
  usa la bandera `$STR_NOCOUNT`.

### SAP GUI Scripting

- **Scripting deshabilitado** — el script no puede conectarse → debe estar habilitado en el
  servidor (parámetro `sapgui/user_scripting`, revisable en RZ11) y en las opciones del cliente SAP GUI.
- **Asumir `Children(0)`** para conexión o sesión — con varias ventanas de SAP abiertas se
  trabaja sobre la sesión equivocada → identifica la sesión correcta antes de actuar.

### SQL

- **`UPDATE` o `DELETE` sin `WHERE`** — afecta toda la tabla → escribe primero el `SELECT` con el
  mismo `WHERE`, revisa el conteo y usa transacción.
- **Comparar con `= NULL`** — nunca es verdadero → usa `IS NULL` / `IS NOT NULL`.

### JavaScript

- **`==` en vez de `===`** — conversiones de tipo inesperadas (`"0" == 0` es `true`) → usa `===`.
- **`async` dentro de `forEach`** — `forEach` no espera las promesas → usa `for...of` con `await`
  o `Promise.all`.

### PowerShell

- **`try/catch` que no atrapa** — muchos errores de cmdlets no son terminales → agrega
  `-ErrorAction Stop` o ajusta `$ErrorActionPreference`.

### Git (general)

- **Agregar a `.gitignore` un archivo ya rastreado** — Git lo sigue rastreando → `git rm --cached
  <archivo>` y commit.
- **Secreto subido y luego borrado** — sigue en el historial → cambia la credencial de inmediato;
  limpiar el historial es secundario.
