---
name: analizar-codigo
description: 'Ejecutor: análisis rápido de código o archivos en cualquier lenguaje (qué hace, flujo, dependencias, riesgos, mejoras) sin modificar nada. Usar al pedir analizar o explicar código, no en estudio.'
---

# Modo: analizar código

Objetivo: entender rápido qué hace un código o un archivo y dónde está el riesgo, **sin cambiar
nada**. Es de solo lectura: va directo, sin propuesta. Sigue `metodo-ejecutor.md`.

## 1. Ubicar

- Declara el **lenguaje detectado** y, si aplica, la versión o el entorno (Excel, SAP GUI…).
- Si es mucho código (varios archivos o más de ~300 líneas), primero entrega el **mapa general**
  (secciones 2-3) y pregunta en qué parte profundizar.

## 2. Resumen

Qué hace en conjunto, en **3 líneas máximo**: entrada → proceso → salida.

## 3. Flujo y piezas

- **Flujo** en pasos numerados. Si tiene ramas o ciclos importantes, un diagrama `mermaid`.
- **Piezas** en tabla:

| Función / procedimiento | Qué hace | Recibe | Devuelve o modifica |
|---|---|---|---|

- **Dependencias externas**: librerías, archivos, objetos COM, ventanas, APIs, bases de datos,
  configuración que lee.

## 4. Hallazgos

En tres listas **separadas**, cada hallazgo con **ubicación** (archivo, función, línea) e **impacto**:

- **Error real** — va a fallar (di con qué entrada o en qué momento).
- **Riesgo** — falla en cierto caso (datos vacíos, ventana que tarda, archivo abierto, tipo
  inesperado) o incumple `principios-y-seguridad.md` (credenciales fijas, rutas reales, sin log,
  operación destructiva sin respaldo).
- **Mejora** — funciona, pero puede ser más claro, más rápido o más mantenible. Incluye el **costo**.

Revisa `trampas-conocidas.md` del lenguaje y señala las que aparezcan.

Si no hay hallazgos en una lista, escribe "Ninguno". No inventes problemas para llenar.

## 5. Archivos de datos (Excel, CSV, JSON, logs)

Si lo que se analiza es un archivo de datos:

- Estructura: hojas, columnas, tipos, número de filas.
- Calidad: vacíos, duplicados, formatos inconsistentes (fechas, ceros a la izquierda, decimales).
- Si la plataforma puede ejecutar código, **analiza el archivo de verdad** en lugar de suponer.

## 6. Cierre

- Numera las mejoras y errores para que el usuario pueda decir "aplica 1 y 3". Eso pasa al modo
  `modificar-codigo` (con propuesta y aprobación).
- Si falta información para concluir algo, dilo como **pregunta abierta**, no como afirmación.
