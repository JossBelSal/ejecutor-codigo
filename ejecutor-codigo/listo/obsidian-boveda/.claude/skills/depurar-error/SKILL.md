---
name: depurar-error
description: 'Ejecutor: diagnostica errores desde el mensaje, una captura o un comportamiento raro: causas probables, cómo confirmarlas y corrección. Usar al compartir una falla.'
---

> **En esta bóveda**, los archivos que se nombran abajo están aquí:
> `metodo-ejecutor.md` → `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` ·
> `principios-y-seguridad.md` → `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md` ·
> `trampas-conocidas.md` → la sección `## Trampas` de `<Lenguaje>/Referencia/` (ahí se anotan
> las nuevas) · `contexto-proyecto.md` → `Proyectos/<Nombre>/<Nombre>.md`.

# Modo: depurar error

Objetivo: encontrar la **causa real** rápido, confirmarla y corregirla con el mínimo cambio. El
diagnóstico va directo; la corrección sigue la regla de aprobación de `metodo-ejecutor.md`.

## 1. Datos del error

Pide solo lo que falte, en un solo mensaje:

- Mensaje **exacto** (texto o captura) y línea donde truena.
- Código de la función involucrada.
- Entrada o dato con el que falla, y si falla **siempre o a veces**.
- Qué cambió desde la última vez que funcionó (código, datos, versión, equipo, usuario).

## 2. Leer el error

En 1-2 líneas: qué dice el mensaje en español llano y qué parte del traceback o del error importa.

## 3. Hipótesis

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

## 4. Corrección

Con la causa confirmada (o muy probable y así declarada):

- Pasa al formato de **propuesta** (qué, dónde, por qué, riesgo, nivel). Si es un cambio pequeño
  y el usuario dijo `rápido`, entrega directo.
- Entrega la función completa corregida con el formato **HECHO**.
- Si la corrección no resuelve, vuelve a la tabla de hipótesis con lo aprendido.

## 5. Prevención

Si la causa vale la pena recordarla, **propón una entrada** para `trampas-conocidas.md`:

```text
- **<trampa>** — <síntoma> → <solución>.
```

- En Claude Code: agrégala con aprobación.
- En chats: entrégala en un bloque para que el usuario la pegue en su copia maestra.
