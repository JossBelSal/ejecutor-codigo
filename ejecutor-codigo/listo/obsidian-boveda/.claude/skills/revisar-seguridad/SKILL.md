---
name: revisar-seguridad
description: 'Ejecutor: revisión de seguridad a fondo (secretos, inyección, permisos, datos personales, dependencias) con hallazgos confirmados y su test. Usar al pedir "seguridad" o antes de un push.'
---

> **En esta bóveda**, los archivos que se nombran abajo están aquí:
> `metodo-ejecutor.md` → `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` ·
> `principios-y-seguridad.md` → `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md` ·
> `trampas-conocidas.md` → la sección `## Trampas` de `<Lenguaje>/Referencia/` (ahí se anotan
> las nuevas) · `contexto-proyecto.md` → `Proyectos/<Nombre>/<Nombre>.md`.

# Modo: revisar seguridad

Objetivo: encontrar lo que puede filtrar datos, dar acceso indebido o dañar información, y
demostrarlo. Es de solo lectura: va directo. Las correcciones siguen la regla de aprobación de
`metodo-ejecutor.md` (modo `modificar-codigo`).

La checklist base (secretos, rutas, datos, Git, ejecución) está en `principios-y-seguridad.md`.
**No la repitas aquí**: aplícala primero y usa este modo para ir más a fondo.

## 1. Mapa de confianza

Antes de buscar fallas, en pocas líneas:

- **Puntos de entrada**: formularios, parámetros, archivos que se leen, celdas de Excel, APIs,
  argumentos de línea de comandos, variables de entorno.
- **Fronteras de confianza**: dónde un dato externo entra al código.
- **Lo valioso**: credenciales, datos personales (nombres, RFC, CURP, cuentas, montos), escrituras
  en SAP o en bases de datos, envíos.

Si el repo es grande, entrega solo el mapa y pregunta dónde profundizar.

## 2. Qué revisar según el tipo de código

Prioriza y di por qué:

| Tipo | Lo que más pesa |
|---|---|
| Web y APIs | inyección, XSS, CSRF, control de acceso e IDOR, sesión, CORS, SSRF |
| Scripts y automatización (Python, VBA, AutoIt, PowerShell) | credenciales fijas, ejecución de comandos con datos externos, rutas, operaciones masivas, sesión SAP equivocada |
| Integraciones con IA | secretos o datos personales enviados al modelo, prompt injection desde texto externo, salida del modelo usada como comando |
| Cualquiera | dependencias con vulnerabilidades, secretos en el historial de Git, datos personales en logs |

Qué buscar en los casos que más se repiten:

- **Inyección**: datos externos concatenados en SQL, `eval`, `exec`, `subprocess(..., shell=True)`,
  `os.system`, `Shell` de VBA, `Run` de AutoIt. Corrección: consultas parametrizadas, lista de
  argumentos sin shell, listas blancas.
- **Deserialización**: `pickle.loads`, `yaml.load` sin `SafeLoader` sobre datos no confiables.
- **Tránsito**: `http://`, `verify=False`, validación de certificados desactivada.
- **Control de acceso**: un ID que llega del cliente y se usa sin verificar que el recurso es de
  ese usuario; permisos validados solo en la interfaz.

Si hay herramientas instaladas, úsalas en modo lectura: `gitleaks` (secretos), `bandit` o
`semgrep` (código), `pip-audit` o `npm audit` (dependencias). **Instalar una herramienta requiere
aprobación.** Si no puedes correrla, da el comando para que el usuario lo corra.

## 3. Confirmar antes de afirmar

Para cada sospecha, sigue el dato desde la entrada hasta el punto peligroso leyendo el código real.

- **Confirmado**: seguiste el camino completo.
- **Probable**: falta una pieza (otro archivo, configuración, cómo se despliega). Di cuál.

Nunca ataques sistemas reales. Una prueba de concepto es un **test local** con datos ficticios.

## 4. Reporte

Ordenado por severidad. Cada hallazgo:

```text
[#n] [CRÍTICO | ALTO | MEDIO | BAJO] <título> — confirmado | probable
- Ubicación: <archivo>:<línea> — <función>
- Camino: <entrada> → … → <punto vulnerable>
- Impacto: <qué puede pasar y a quién afecta>
- Corrección: <qué cambiar>, costo: bajo | medio | alto
- Test: <entrada maliciosa → resultado esperado>
```

Severidad: **crítico** = explotable sin autenticación o daña datos productivos; **alto** =
explotable con condiciones, o se pueden perder datos; **medio** = varias condiciones o impacto
limitado; **bajo** = defensa en profundidad.

Al final:

- **No revisado**: lo que quedó fuera y por qué.
- Si un secreto ya llegó a Git: **primero se cambia la credencial**, después se limpia el historial.
- Hallazgos numerados para que el usuario diga "corrige 1 y 3". Las correcciones pasan a
  `modificar-codigo`, y cada una lleva su test (modo `escribir-tests`).

Si no hay hallazgos en una severidad, no la listes. Si todo está bien, dilo en una línea: no
inventes problemas.
