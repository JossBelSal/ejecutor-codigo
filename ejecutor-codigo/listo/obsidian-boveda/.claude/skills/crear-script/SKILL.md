---
name: crear-script
description: 'Ejecutor: crea un script o proceso nuevo en cualquier lenguaje, con configuración externa, log y manejo de errores. Usar al pedir crear un script suelto.'
---

> **En esta bóveda**, los archivos que se nombran abajo están aquí:
> `metodo-ejecutor.md` → `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` ·
> `principios-y-seguridad.md` → `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md` ·
> `trampas-conocidas.md` → la sección `## Trampas` de `<Lenguaje>/Referencia/` (ahí se anotan
> las nuevas) · `contexto-proyecto.md` → `Proyectos/<Nombre>/<Nombre>.md`.

# Modo: crear script

Objetivo: construir algo nuevo que funcione a la primera, sea mantenible y respete los principios
del usuario. **Diseño antes que código.** Sigue `metodo-ejecutor.md`.

## 0. Dónde vive el script

Un script suelto **no merece repositorio propio**, pero tampoco vive dentro de la bóveda de
Obsidian. El reparto es:

| Qué | Dónde |
|---|---|
| El archivo ejecutable (`.py`, `.au3`, `.bas`, `.ps1`…) | El repo `scripts` del usuario, o la carpeta de trabajo donde se usa |
| **Qué hace, cuándo usarlo y sus gotchas** | Una nota en `<Lenguaje>/Referencia/` de la bóveda |
| Trampas nuevas que salgan | La sección `## Trampas` de esa misma nota |

Así el saber queda donde ya lo buscas y lo ejecutable donde se ejecuta.

**La excepción son los ejercicios de estudio** (`<Lenguaje>/Aprendizaje/`,
`Python/python_udemy/`): esos son del tutor. Si lo que te piden es practicar y no un entregable,
dilo y pásalo al tutor.

Si el script crece —varias piezas, configuración propia, vida propia— **no es un script: es un
proyecto.** Dilo y pasa al modo `crear-proyecto`.

## 1. Requisitos

Pregunta solo lo que falte, **máximo 5 preguntas en un solo mensaje**:

- Objetivo: qué problema resuelve y cómo se ve "terminado".
- Entradas y salidas: archivos, formatos, pantallas, sistemas.
- Entorno: sistema operativo, versiones, permisos, ¿hay SAP, Excel, red?
- Quién lo ejecuta y con qué frecuencia.
- Restricciones: sin instalar librerías, sin permisos de administrador, tiempo límite, etc.

## 2. Lenguaje

Si el usuario no lo definió, **recomienda uno** con el porqué en 1-2 líneas, usando los
principios (Python orquesta, VBA dentro de Excel, AutoIt para ventanas sin API, u otro si el
contexto lo pide). Si hay dos opciones razonables, di cuál y por qué.

## 3. Diseño (propuesta)

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

## 4. Bloques típicos

Ajusta al caso, pero en general:

1. **Configuración y utilidades**: lectura de configuración, log, manejo de errores común.
2. **Lógica central**: el cálculo, la transformación o la automatización principal.
3. **Entrada y salida**: lectura de archivos o sistemas y escritura de resultados.
4. **Orquestador**: el punto de entrada que une todo, con modo `DRY_RUN` si aplica.
5. **Pruebas**: casos de prueba (entrada → salida esperada) y, si aplica, código de prueba.

Cada bloque: código completo con nombre de archivo → verificación (§4 del método) → formato
**HECHO** → **espera OK** antes del siguiente.

## 5. Entrega final

- **Cómo instalar y ejecutar**, paso a paso.
- **Ejemplo de configuración** con valores ficticios.
- Resultado de la revisión **`seguridad`** (sin secretos, `.gitignore` sugerido).
- Ofrece `documentar-proceso` para dejar el README.

**Y la nota de la bóveda, que no es opcional** (§0): una nota en `<Lenguaje>/Referencia/` con qué
hace el script, cuándo usarlo, el snippet de la pieza reutilizable y sus gotchas. Usa la plantilla
`99-Plantillas/Plantilla - Referencia.md`. Si no puedes escribir en la bóveda, entrégala en un
bloque `markdown` para pegar.

Sin esa nota, el script se pierde: dentro de seis meses nadie recuerda que existía.
