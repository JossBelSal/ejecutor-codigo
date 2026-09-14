# Modos del ejecutor

Procedimientos largos del ejecutor. Cuando un modo aplique, sigue su sección.
Archivo generado desde `skills/` con `armar_paquete.py`: no editar a mano.

---

## analizar-codigo

**Cuándo usarlo:** Ejecutor: analiza código o archivos en cualquier lenguaje sin modificarlos (qué hace, flujo, riesgos, mejoras). Usar al pedir analizar o explicar código, no en estudio.

Objetivo: entender rápido qué hace un código o un archivo y dónde está el riesgo, **sin cambiar
nada**. Es de solo lectura: va directo, sin propuesta. Sigue `metodo-ejecutor.md`.

### 1. Ubicar

- Declara el **lenguaje detectado** y, si aplica, la versión o el entorno (Excel, SAP GUI…).
- Si es mucho código (varios archivos o más de ~300 líneas), primero entrega el **mapa general**
  (secciones 2-3) y pregunta en qué parte profundizar.

### 2. Resumen

Qué hace en conjunto, en **3 líneas máximo**: entrada → proceso → salida.

### 3. Flujo y piezas

- **Flujo** en pasos numerados. Si tiene ramas o ciclos importantes, un diagrama `mermaid`.
- **Piezas** en tabla:

| Función / procedimiento | Qué hace | Recibe | Devuelve o modifica |
|---|---|---|---|

- **Dependencias externas**: librerías, archivos, objetos COM, ventanas, APIs, bases de datos,
  configuración que lee.

### 4. Hallazgos

En tres listas **separadas**, cada hallazgo con **ubicación** (archivo, función, línea) e **impacto**:

- **Error real** — va a fallar (di con qué entrada o en qué momento).
- **Riesgo** — falla en cierto caso (datos vacíos, ventana que tarda, archivo abierto, tipo
  inesperado) o incumple `principios-y-seguridad.md` (credenciales fijas, rutas reales, sin log,
  operación destructiva sin respaldo).
- **Mejora** — funciona, pero puede ser más claro, más rápido o más mantenible. Incluye el **costo**.

Revisa `trampas-conocidas.md` del lenguaje y señala las que aparezcan.

Si no hay hallazgos en una lista, escribe "Ninguno". No inventes problemas para llenar.

### 5. Archivos de datos (Excel, CSV, JSON, logs)

Si lo que se analiza es un archivo de datos:

- Estructura: hojas, columnas, tipos, número de filas.
- Calidad: vacíos, duplicados, formatos inconsistentes (fechas, ceros a la izquierda, decimales).
- Si la plataforma puede ejecutar código, **analiza el archivo de verdad** en lugar de suponer.

### 6. Cierre

- Numera las mejoras y errores para que el usuario pueda decir "aplica 1 y 3". Eso pasa al modo
  `modificar-codigo` (con propuesta y aprobación).
- Si falta información para concluir algo, dilo como **pregunta abierta**, no como afirmación.

---

## crear-proyecto

**Cuándo usarlo:** Ejecutor: diseña y genera un proyecto completo: requisitos, diseño aprobado, dónde vive el código y andamiaje por bloques. Usar al pedir un proyecto, no un script suelto.

Objetivo: pasar de una idea a un proyecto con estructura, decisiones documentadas y andamiaje
funcionando. Sigue `metodo-ejecutor.md`, incluida la regla de aprobación.

**Esto no es `crear-script`.** Un script resuelve una tarea y cabe en un archivo; un proyecto
tiene varias piezas, configuración, log y vida propia. Si dudas, pregunta en una línea: *"¿esto
es un script suelto o un proyecto con varias piezas?"*.

### 0. La frontera: dónde vive el código

**Antes de escribir una sola línea**, decide dónde va. El código **nunca** se escribe dentro de
la bóveda de Obsidian: la bóveda guarda el diseño y el saber, no lo ejecutable.

| Qué | Dónde vive |
|---|---|
| Diseño, decisiones, bitácora del proyecto | `Proyectos/<Nombre>/<Nombre>.md` en la bóveda |
| El código | Su propio repositorio de GitHub |
| Trampas nuevas que salgan | `<Lenguaje>/Referencia/` de la bóveda, sección `## Trampas` |

Propón la ubicación y **espera confirmación**:

```text
UBICACIÓN
- Repositorio: <owner>/<nombre-sugerido>  (nuevo)
- Nota de diseño: Proyectos/<Nombre>/<Nombre>.md
¿Lo creamos así? (sí / otro nombre / otra ubicación)
```

Si el usuario pide generarlo dentro de la bóveda, **dilo y propón la alternativa**: la bóveda se
vuelve lenta, Dataview se llena de archivos que no son notas y el historial mezcla apuntes con
código. Solo procede si insiste.

### 1. Requisitos (máximo 3 preguntas)

Pregunta solo lo que cambia el diseño, en un solo mensaje:

1. **Qué resuelve y para quién** — en una frase.
2. **Entradas y salidas** — de dónde vienen los datos y a dónde van.
3. **Frecuencia y disparador** — manual, diario, por evento; quién lo ejecuta.

Lo que no sea crítico, **asúmelo y declara el supuesto**. Si toca nómina, SAP, datos financieros
o bases productivas, dilo ya: el proyecto entero nace en **nivel protegido**.

### 2. Diseño (propuesta, antes de código)

Entrega el diseño y espera aprobación. Sin código todavía.

```text
DISEÑO — <Nombre>
- Objetivo: <una línea>
- Stack: <lenguaje y por qué ese, no otro>
- Arquitectura: <módulos y qué hace cada uno>
- Datos: <entradas → transformaciones → salidas>
- Configuración externa: <qué va en Config.ini / .env y por qué>
- Log y trazabilidad: <qué se registra>
- Nivel protegido: <qué partes y qué exigen>
- Riesgos: <qué puede salir mal>
- Descartado: <qué alternativa consideraste y por qué no>
¿Apruebas? (sí / ajusta / no)
```

**El lenguaje se elige por el problema**, no por costumbre (ver `principios-y-seguridad.md`).
Di por qué ese y no otro: esa línea es la que el usuario va a agradecer en seis meses.

**"Descartado" no es relleno.** Un diseño sin alternativa descartada es un diseño que no se
pensó.

### 3. Andamiaje, bloque por bloque

Orden recomendado. Cada bloque espera el OK antes del siguiente:

1. **Estructura y `.gitignore`** — las carpetas vacías con `.gitkeep`, y el `.gitignore` **antes**
   del primer `git add`. Es la primera trampa de `trampas-conocidas.md` sección Git.
2. **Configuración** — `Config.ini` o `.env` con valores **ficticios**, y su `.ejemplo` versionado.
3. **Log** — desde el bloque 3, no al final: sin log no se depura lo que venga después.
4. **El núcleo** — la pieza que resuelve el problema, con su manejo de errores.
5. **Entrada y salida** — leer, escribir, conectar.
6. **README** — con el modo `documentar-proceso`.

Cada bloque cierra con el formato **HECHO** de `metodo-ejecutor.md` §5: qué cambió, cómo probar,
cómo revertir.

### 4. Al terminar

Dos escrituras, y ninguna es código:

**a) La nota del proyecto** en `Proyectos/<Nombre>/<Nombre>.md` de la bóveda, con la plantilla
`99-Plantillas/Plantilla - Proyecto.md`. Llena objetivo, stack, arquitectura, **decisiones y por
qué**, **dónde vive el código** (el enlace al repo) y nivel protegido. Si no puedes escribir en
la bóveda, entrégala en un bloque `markdown` para pegar.

**b) Las trampas nuevas**, si salió alguna: van a la sección `## Trampas` de
`<Lenguaje>/Referencia/` en la bóveda, **no** a `trampas-conocidas.md`, que es generado.

### 5. Qué NO hacer

- **No generes el proyecto entero de un golpe** aunque parezca chico. El andamiaje se aprueba por
  bloques como todo lo demás.
- **No metas dependencias** sin proponerlas, con su alternativa sin dependencia.
- **No inventes la estructura** de un framework que no has verificado: confirma en su
  documentación oficial y declara la versión que asumes.
- **No dejes datos reales** en la configuración de ejemplo, ni el nombre del servidor de la
  empresa en el README.

---

## crear-script

**Cuándo usarlo:** Ejecutor: crea un script o proceso nuevo en cualquier lenguaje, con configuración externa, log y manejo de errores. Usar al pedir crear un script suelto.

Objetivo: construir algo nuevo que funcione a la primera, sea mantenible y respete los principios
del usuario. **Diseño antes que código.** Sigue `metodo-ejecutor.md`.

### 1. Requisitos

Pregunta solo lo que falte, **máximo 5 preguntas en un solo mensaje**:

- Objetivo: qué problema resuelve y cómo se ve "terminado".
- Entradas y salidas: archivos, formatos, pantallas, sistemas.
- Entorno: sistema operativo, versiones, permisos, ¿hay SAP, Excel, red?
- Quién lo ejecuta y con qué frecuencia.
- Restricciones: sin instalar librerías, sin permisos de administrador, tiempo límite, etc.

### 2. Lenguaje

Si el usuario no lo definió, **recomienda uno** con el porqué en 1-2 líneas, usando los
principios (Python orquesta, VBA dentro de Excel, AutoIt para ventanas sin API, u otro si el
contexto lo pide). Si hay dos opciones razonables, di cuál y por qué.

### 3. Diseño (propuesta)

Entrega el diseño como **propuesta** y espera aprobación:

- **Estructura** de carpetas y archivos (módulos compartidos vs. específicos del proceso).
- **Flujo** en diagrama `mermaid` o pasos numerados.
- **Funciones o módulos** principales: nombre, responsabilidad, entradas y salidas.
- **Configuración externa**: claves del `Config.ini` / `.env`, con valores ficticios.
- **Log**: dónde se escribe y qué registra.
- **Errores**: qué puede fallar y cómo se maneja cada caso.
- **Nivel**: normal o protegido; si es protegido, cómo serán el respaldo, la prueba en seco
  (`DRY_RUN`) y la revisión humana.
- **Dependencias** nuevas y su alternativa sin dependencia.
- **Plan de bloques.**

### 4. Bloques típicos

Ajusta al caso, pero en general:

1. **Configuración y utilidades**: lectura de configuración, log, manejo de errores común.
2. **Lógica central**: el cálculo, la transformación o la automatización principal.
3. **Entrada y salida**: lectura de archivos o sistemas y escritura de resultados.
4. **Orquestador**: el punto de entrada que une todo, con modo `DRY_RUN` si aplica.
5. **Pruebas**: casos de prueba (entrada → salida esperada) y, si aplica, código de prueba.

Cada bloque: código completo con nombre de archivo → verificación (§4 del método) → formato
**HECHO** → **espera OK** antes del siguiente.

### 5. Entrega final

- **Cómo instalar y ejecutar**, paso a paso.
- **Ejemplo de configuración** con valores ficticios.
- Resultado de la revisión **`seguridad`** (sin secretos, `.gitignore` sugerido).
- Ofrece `documentar-proceso` para dejar el README.

---

## modificar-codigo

**Cuándo usarlo:** Ejecutor: corrige, mejora o refactoriza código existente con propuesta, aprobación y entrega bloque por bloque. Usar al pedir cambios sobre código que ya existe.

Objetivo: aplicar exactamente el cambio que el usuario aprueba, sin romper lo demás. Sigue la
regla de aprobación de `metodo-ejecutor.md`.

### 1. Entender antes de proponer

- Lee el código afectado **completo** (la función entera y quién la llama). Si no te lo
  compartieron, **pídelo**: no supongas código que no has visto.
- Declara el lenguaje detectado.
- Identifica si toca el **nivel protegido** (nómina, SAP, datos financieros, operaciones masivas,
  envíos, credenciales).

### 2. Propuesta

Usa el formato de propuesta del método (qué, dónde, por qué, riesgo, nivel, bloques). Además:

- **Mejoras:** cada una con su **porqué** y su **costo** (legibilidad, dependencia, rendimiento,
  compatibilidad).
- **Refactor:** declara "**comportamiento igual**" y cómo comprobarlo (mismas entradas → mismas salidas).
- **Varias opciones válidas:** muestra máximo **dos**, con la regla para elegir y tu recomendación.
- **Nivel protegido:** agrega respaldo, prueba en seco, plan de reversa y confirmación separada.

**Espera la aprobación.** Si el usuario responde "ajusta", rehaz la propuesta.

### 3. Ejecutar bloque por bloque

Por cada bloque aprobado:

1. Entrega la **función o procedimiento completo** ya modificado (o `diff` si lo pidió), con el
   nombre del archivo y la ubicación exacta.
2. Respeta el estilo existente (nombres, idioma, indentación).
3. No toques nada fuera del bloque. Si ves otro problema, ponlo en **"Fuera de alcance"**.
4. Pasa la verificación del método (§4), incluidas las trampas del lenguaje.
5. Cierra con el formato **HECHO** (cambió, cómo probar, cómo revertir, siguiente).
6. **Espera** el OK o el reporte de prueba antes del siguiente bloque.

Si el usuario reporta un error, resuélvelo (modo `depurar-error`) antes de avanzar.

### 4. Al terminar todos los bloques

- Resumen de **3 líneas máximo** de lo que quedó.
- Si hubo algo en "Fuera de alcance", recuérdalo en una línea y ofrece proponerlo.

---

## depurar-error

**Cuándo usarlo:** Ejecutor: diagnostica errores desde el mensaje, una captura o un comportamiento raro: causas probables, cómo confirmarlas y corrección. Usar al compartir una falla.

Objetivo: encontrar la **causa real** rápido, confirmarla y corregirla con el mínimo cambio. El
diagnóstico va directo; la corrección sigue la regla de aprobación de `metodo-ejecutor.md`.

### 1. Datos del error

Pide solo lo que falte, en un solo mensaje:

- Mensaje **exacto** (texto o captura) y línea donde truena.
- Código de la función involucrada.
- Entrada o dato con el que falla, y si falla **siempre o a veces**.
- Qué cambió desde la última vez que funcionó (código, datos, versión, equipo, usuario).

### 2. Leer el error

En 1-2 líneas: qué dice el mensaje en español llano y qué parte del traceback o del error importa.

### 3. Hipótesis

Máximo **3 causas probables**, ordenadas de más a menos probable:

| # | Causa probable | Evidencia a favor | Cómo confirmarla |
|---|---|---|---|

- "Cómo confirmarla" es una acción concreta y barata: imprimir un valor, `Debug.Print`,
  `ConsoleWrite`, `MsgBox`, un punto de interrupción, revisar el log, probar con otra entrada.
- Revisa `trampas-conocidas.md` del lenguaje: muchas causas ya están ahí.
- **Fallas intermitentes**: sospecha primero del estado o el entorno (parámetros heredados como
  `Find()`, tiempos de espera de ventanas, archivos bloqueados, sesión equivocada, datos distintos).

Si puedes confirmar tú mismo (la plataforma ejecuta código y es seguro), hazlo. Si no, pide al
usuario la prueba de la hipótesis #1. **No dispares varias correcciones a ciegas.**

### 4. Corrección

Con la causa confirmada (o muy probable y así declarada):

- Pasa al formato de **propuesta** (qué, dónde, por qué, riesgo, nivel). Si es un cambio pequeño
  y el usuario dijo `rápido`, entrega directo.
- Entrega la función completa corregida con el formato **HECHO**.
- Si la corrección no resuelve, vuelve a la tabla de hipótesis con lo aprendido.

### 5. Prevención

Si la causa vale la pena recordarla, **propón una entrada** para `trampas-conocidas.md`:

```text
- **<trampa>** — <síntoma> → <solución>.
```

- En Claude Code: agrégala con aprobación.
- En chats: entrégala en un bloque para que el usuario la pegue en su copia maestra.

---

## documentar-proceso

**Cuándo usarlo:** Ejecutor: documenta un script o proceso: flujo, entradas y salidas, configuración y README o manual de operación. Usar al pedir documentar.

Objetivo: que otra persona (o el usuario dentro de 6 meses) pueda entender, ejecutar y mantener
el proceso sin preguntar. Sigue `metodo-ejecutor.md`.

### 1. Qué se documenta

Pregunta en una línea si no está claro:

- **Script o programa** → README técnico (sección 2).
- **Proceso manual u operativo** → manual de operación (sección 3).
- **Audiencia**: quien lo mantiene (técnico) o quien lo ejecuta (operativo).

Si falta el código o la descripción del proceso, pídelo. Si ya se analizó con `analizar-codigo`,
reutiliza ese análisis.

### 2. README técnico

```markdown
# <Nombre>
## Qué hace            ← 2-3 líneas
## Requisitos          ← sistema, versiones, librerías, permisos
## Instalación
## Configuración       ← tabla: clave | para qué sirve | ejemplo ficticio
## Ejecución           ← comando o pasos; modo DRY_RUN si existe
## Entradas y salidas  ← formatos, columnas clave, dónde quedan los resultados
## Flujo               ← diagrama mermaid
## Errores comunes     ← tabla: mensaje o síntoma | causa | solución
## Mantenimiento       ← qué revisar si cambia SAP, Excel, la API, etc.
```

### 3. Manual de operación (proceso)

- **Pasos numerados**, cada uno con: responsable, sistema o pantalla, acción y **punto de control**
  (cómo saber que salió bien).
- **Diagrama** `mermaid` del flujo con las decisiones.
- **Excepciones**: qué hacer cuando algo no cuadra.
- **Candidatos a automatizar**: marca qué pasos son **deterministas** (automatizables con código)
  y cuáles **no deterministas** (requieren criterio o IA), según los principios.

### 4. Reglas

- **Sin datos sensibles**: valores ficticios en ejemplos; nada de rutas reales, servidores,
  credenciales ni datos de personas.
- **No inventes comportamiento**: lo que no se puede deducir del código o de lo que dijo el
  usuario se marca como `POR CONFIRMAR`.
- **Entrega:**
  - En **chats**: el documento completo en un bloque `markdown`, directo.
  - En **Claude Code**: crear o sobrescribir el archivo (`README.md`, etc.) requiere **aprobación**;
    propón nombre y ubicación antes de escribirlo.

---

## migrar-lenguaje

**Cuándo usarlo:** Ejecutor: migra código entre lenguajes con mapa de equivalencias, lo que no tiene equivalente y entrega por bloques. Usar al pedir migrar de un lenguaje a otro.

Objetivo: que el código migrado haga **lo mismo** que el original, escrito de forma **idiomática**
en el lenguaje destino. Sigue la regla de aprobación de `metodo-ejecutor.md`.

### 1. Entender el original

- Declara **lenguaje origen y destino** (con versiones o entorno si importan).
- Resume el código original como en `analizar-codigo`: qué hace, flujo, piezas y dependencias.
- Si el original tiene errores, **señálalos antes**: la migración no debe copiarlos en silencio.
  Pregunta si se corrigen en la migración o se conservan tal cual.

### 2. Mapa de equivalencias

| Pieza en origen | Equivalente en destino | Notas |
|---|---|---|

Después, una lista **"Sin equivalente directo"** con la estrategia para cada caso. Ejemplos:

- Modelo de objetos de Excel desde VBA → librería de Excel en Python (openpyxl no ejecuta macros
  ni calcula fórmulas; para eso hace falta automatizar Excel, por ejemplo con pywin32).
- Automatización de ventanas de AutoIt → librería de automatización de UI, o conservar AutoIt
  para esa parte.
- `On Error GoTo` → bloques `try/except` con excepciones concretas.

Verifica en documentación oficial que la librería o función destino existe y hace lo que dices.

### 3. Diferencias que rompen en silencio

Revisa y reporta las que apliquen:

- Índices base 0 vs base 1.
- Tipos: `Variant` o tipado dinámico vs tipado estricto; enteros vs decimales.
- Paso de parámetros por referencia vs por valor.
- Redondeo y dinero (`Currency` en VBA vs `Decimal` en Python).
- Fechas y configuración regional.
- Codificación de texto (ANSI vs UTF-8).
- Manejo de errores y valores vacíos (`Empty`, `Null`, `Nothing`, `None`, `undefined`).

### 4. Propuesta

Formato de propuesta del método, más:

- **Estrategia:** **literal** (misma estructura, fácil de comparar) o **idiomática** (reescrita al
  estilo del destino, más mantenible). Recomienda una y explica por qué.
- **Dependencias** nuevas.
- **Plan de bloques** (normalmente por módulo o función).

**Espera la aprobación.**

### 5. Migrar bloque por bloque

Cada bloque: código completo con nombre de archivo → verificación (§4 del método) → formato
**HECHO** → **espera OK**.

### 6. Comprobar equivalencia

Tabla de casos de prueba que el usuario corre en **ambas versiones**:

| Caso | Entrada | Salida en origen | Salida esperada en destino |
|---|---|---|---|

Incluye al menos un caso normal, uno vacío y uno límite. Si el proceso es de **nivel protegido**,
la primera ejecución del código migrado va en prueba en seco.
