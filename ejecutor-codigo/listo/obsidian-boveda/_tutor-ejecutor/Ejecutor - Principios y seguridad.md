---
tags: [tipo/ejecutor, estado/en-curso]
creado: 2026-09-14
---

# Principios y seguridad

Criterios **por defecto** para crear o modificar código. Aplican en cualquier lenguaje. Si
`contexto-proyecto.md` o el usuario indican otra cosa para un proyecto, manda eso.

## Principios de arquitectura

- **Diseño antes que código.** En algo nuevo o grande, primero estructura, flujo y datos;
  después el código (modo `crear-script`).
- **Modular siempre.** Lo reutilizable va en módulos compartidos (por ejemplo, una carpeta
  `Comun\` con configuración, soporte y conexión a sistemas). Cada proceso tiene su propia
  configuración (por ejemplo, su `Config.ini`). Las constantes de un proceso no se mezclan en la
  configuración global.
- **El lenguaje se elige por el problema**, no por costumbre. Referencia del ecosistema del
  usuario cuando aplica:
  - **Python** como orquestador (lógica, datos, APIs, integración).
  - **VBA** para trabajar dentro de Excel.
  - **AutoIt** como respaldo para automatizar ventanas cuando no hay API o scripting.
  - Cualquier otro lenguaje cuando el contexto lo pida; dilo y explica por qué.
- **IA solo para lo no determinista**: clasificar, redactar, interpretar texto libre. La
  navegación y la ejecución deterministas (clics, transacciones, cálculos) nunca se delegan a IA.
- **Revisión humana obligatoria** en procesos de nómina o SAP antes de cualquier ejecución
  automatizada.
- **Trazabilidad.** Los procesos que modifican datos dejan log con fecha y hora: qué hicieron,
  sobre qué y con qué resultado.
- **Re-ejecutable sin daño** cuando sea posible: correr dos veces no debe duplicar ni corromper.

## Reglas de seguridad

- **Nada sensible en archivos versionados o compartidos**: credenciales, contraseñas, tokens,
  rutas reales, servidores, configuración de la empresa en SAP ni datos internos.
- **Credenciales fuera del código**: se leen al ejecutar desde configuración externa
  (`Config.ini`, `.env`, variables de entorno). Nunca compiladas dentro de un `.exe` ni subidas a Git.
- **`.gitignore` antes del primer commit.** Configura qué se ignora (configuración con secretos,
  datos, logs) **antes** de agregar archivos.
- **Datos reales en chats**: antes de subir archivos a un chat (Proyecto de Claude o ChatGPT),
  sugiere **anonimizar** muestras: nombres, RFC, CURP, números de empleado, cuentas y montos
  reales. Para analizar estructura bastan pocas filas ficticias.
- **Ejemplos de configuración** siempre con valores ficticios (`usuario = TU_USUARIO`).

## Revisión `seguridad` (checklist)

Cuando el usuario pida `seguridad`, o antes de proponer subir algo a Git, revisa y reporta:

| Revisión | Qué buscar |
|---|---|
| Secretos | `password`, `pwd`, `token`, `api_key`, `secret`, cadenas de conexión, encabezados `Authorization` |
| Rutas y equipos | Rutas absolutas (`C:\Users\…`, unidades de red), nombres de servidor, IPs internas |
| Datos | Nombres reales, RFC, CURP, cuentas, montos, correos internos |
| Git | ¿`.gitignore` cubre configuración, datos y logs? ¿Hay archivos sensibles ya rastreados? |
| Ejecución | Operaciones destructivas sin confirmación, sin respaldo o sin prueba en seco |

Formato del reporte: **hallazgo → archivo y línea → riesgo → corrección propuesta** (la
corrección sigue la regla de aprobación).
