---
name: migrar-lenguaje
description: 'Ejecutor: migra código entre lenguajes con mapa de equivalencias, lo que no tiene equivalente y entrega por bloques. Usar al pedir migrar de un lenguaje a otro.'
---

> **En esta bóveda**, los archivos que se nombran abajo están aquí:
> `metodo-ejecutor.md` → `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` ·
> `principios-y-seguridad.md` → `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md` ·
> `trampas-conocidas.md` → la sección `## Trampas` de `<Lenguaje>/Referencia/` (ahí se anotan
> las nuevas) · `contexto-proyecto.md` → `Proyectos/<Nombre>/<Nombre>.md`.

# Modo: migrar de lenguaje

Objetivo: que el código migrado haga **lo mismo** que el original, escrito de forma **idiomática**
en el lenguaje destino. Sigue la regla de aprobación de `metodo-ejecutor.md`.

## 1. Entender el original

- Declara **lenguaje origen y destino** (con versiones o entorno si importan).
- Resume el código original como en `analizar-codigo`: qué hace, flujo, piezas y dependencias.
- Si el original tiene errores, **señálalos antes**: la migración no debe copiarlos en silencio.
  Pregunta si se corrigen en la migración o se conservan tal cual.

## 2. Mapa de equivalencias

| Pieza en origen | Equivalente en destino | Notas |
|---|---|---|

Después, una lista **"Sin equivalente directo"** con la estrategia para cada caso. Ejemplos:

- Modelo de objetos de Excel desde VBA → librería de Excel en Python (openpyxl no ejecuta macros
  ni calcula fórmulas; para eso hace falta automatizar Excel, por ejemplo con pywin32).
- Automatización de ventanas de AutoIt → librería de automatización de UI, o conservar AutoIt
  para esa parte.
- `On Error GoTo` → bloques `try/except` con excepciones concretas.

Verifica en documentación oficial que la librería o función destino existe y hace lo que dices.

## 3. Diferencias que rompen en silencio

Revisa y reporta las que apliquen:

- Índices base 0 vs base 1.
- Tipos: `Variant` o tipado dinámico vs tipado estricto; enteros vs decimales.
- Paso de parámetros por referencia vs por valor.
- Redondeo y dinero (`Currency` en VBA vs `Decimal` en Python).
- Fechas y configuración regional.
- Codificación de texto (ANSI vs UTF-8).
- Manejo de errores y valores vacíos (`Empty`, `Null`, `Nothing`, `None`, `undefined`).

## 4. Propuesta

Formato de propuesta del método, más:

- **Estrategia:** **literal** (misma estructura, fácil de comparar) o **idiomática** (reescrita al
  estilo del destino, más mantenible). Recomienda una y explica por qué.
- **Dependencias** nuevas.
- **Plan de bloques** (normalmente por módulo o función).

**Espera la aprobación.**

## 5. Migrar bloque por bloque

Cada bloque: código completo con nombre de archivo → verificación (§4 del método) → formato
**HECHO** → **espera OK**.

## 6. Comprobar equivalencia

Tabla de casos de prueba que el usuario corre en **ambas versiones**:

| Caso | Entrada | Salida en origen | Salida esperada en destino |
|---|---|---|---|

Incluye al menos un caso normal, uno vacío y uno límite. Si el proceso es de **nivel protegido**,
la primera ejecución del código migrado va en prueba en seco.
