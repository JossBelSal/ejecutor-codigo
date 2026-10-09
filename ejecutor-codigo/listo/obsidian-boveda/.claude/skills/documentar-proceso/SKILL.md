---
name: documentar-proceso
description: 'Ejecutor: documenta un script o proceso: flujo, entradas y salidas, configuración y README o manual de operación. Usar al pedir documentar.'
---

> **En esta bóveda**, los archivos que se nombran abajo están aquí:
> `metodo-ejecutor.md` → `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` ·
> `principios-y-seguridad.md` → `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md` ·
> `trampas-conocidas.md` → la sección `## Trampas` de `<Lenguaje>/Referencia/` (ahí se anotan
> las nuevas) · `contexto-proyecto.md` → `Proyectos/<Nombre>/<Nombre>.md`.

# Modo: documentar proceso

Objetivo: que otra persona (o el usuario dentro de 6 meses) pueda entender, ejecutar y mantener
el proceso sin preguntar. Sigue `metodo-ejecutor.md`.

## 1. Qué se documenta

Pregunta en una línea si no está claro:

- **Script o programa** → README técnico (sección 2).
- **Proceso manual u operativo** → manual de operación (sección 3).
- **Audiencia**: quien lo mantiene (técnico) o quien lo ejecuta (operativo).

Si falta el código o la descripción del proceso, pídelo. Si ya se analizó con `analizar-codigo`,
reutiliza ese análisis.

## 2. README técnico

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

## 3. Manual de operación (proceso)

- **Pasos numerados**, cada uno con: responsable, sistema o pantalla, acción y **punto de control**
  (cómo saber que salió bien).
- **Diagrama** `mermaid` del flujo con las decisiones.
- **Excepciones**: qué hacer cuando algo no cuadra.
- **Candidatos a automatizar**: marca qué pasos son **deterministas** (automatizables con código)
  y cuáles **no deterministas** (requieren criterio o IA), según los principios.

## 4. Reglas

- **Sin datos sensibles**: valores ficticios en ejemplos; nada de rutas reales, servidores,
  credenciales ni datos de personas.
- **No inventes comportamiento**: lo que no se puede deducir del código o de lo que dijo el
  usuario se marca como `POR CONFIRMAR`.
- **Entrega:**
  - En **chats**: el documento completo en un bloque `markdown`, directo.
  - En **Claude Code**: crear o sobrescribir el archivo (`README.md`, etc.) requiere **aprobación**;
    propón nombre y ubicación antes de escribirlo.
