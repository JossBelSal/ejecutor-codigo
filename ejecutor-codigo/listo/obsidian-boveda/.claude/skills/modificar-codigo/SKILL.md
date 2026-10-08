---
name: modificar-codigo
description: 'Ejecutor: corrige, mejora o refactoriza código existente con propuesta, aprobación y entrega bloque por bloque. Usar al pedir cambios sobre código que ya existe.'
---

> **En esta bóveda**, los archivos que se nombran abajo están aquí:
> `metodo-ejecutor.md` → `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` ·
> `principios-y-seguridad.md` → `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md` ·
> `trampas-conocidas.md` → la sección `## Trampas` de `<Lenguaje>/Referencia/` (ahí se anotan
> las nuevas) · `contexto-proyecto.md` → `Proyectos/<Nombre>/<Nombre>.md`.

# Modo: modificar código

Objetivo: aplicar exactamente el cambio que el usuario aprueba, sin romper lo demás. Sigue la
regla de aprobación de `metodo-ejecutor.md`.

## 1. Entender antes de proponer

- Lee el código afectado **completo** (la función entera y quién la llama). Si no te lo
  compartieron, **pídelo**: no supongas código que no has visto.
- Declara el lenguaje detectado.
- Identifica si toca el **nivel protegido** (nómina, SAP, datos financieros, operaciones masivas,
  envíos, credenciales).

## 2. Propuesta

Usa el formato de propuesta del método (qué, dónde, por qué, riesgo, nivel, bloques). Además:

- **Mejoras:** cada una con su **porqué** y su **costo** (legibilidad, dependencia, rendimiento,
  compatibilidad).
- **Refactor:** declara "**comportamiento igual**" y cómo comprobarlo (mismas entradas → mismas salidas).
- **Varias opciones válidas:** muestra máximo **dos**, con la regla para elegir y tu recomendación.
- **Nivel protegido:** agrega respaldo, prueba en seco, plan de reversa y confirmación separada.

**Espera la aprobación.** Si el usuario responde "ajusta", rehaz la propuesta.

## 3. Ejecutar bloque por bloque

Por cada bloque aprobado:

1. Entrega la **función o procedimiento completo** ya modificado (o `diff` si lo pidió), con el
   nombre del archivo y la ubicación exacta.
2. Respeta el estilo existente (nombres, idioma, indentación).
3. No toques nada fuera del bloque. Si ves otro problema, ponlo en **"Fuera de alcance"**.
4. Pasa la verificación del método (§4), incluidas las trampas del lenguaje.
5. Cierra con el formato **HECHO** (cambió, cómo probar, cómo revertir, siguiente).
6. **Espera** el OK o el reporte de prueba antes del siguiente bloque.

Si el usuario reporta un error, resuélvelo (modo `depurar-error`) antes de avanzar.

## 4. Al terminar todos los bloques

- Resumen de **3 líneas máximo** de lo que quedó.
- Si hubo algo en "Fuera de alcance", recuérdalo en una línea y ofrece proponerlo.
