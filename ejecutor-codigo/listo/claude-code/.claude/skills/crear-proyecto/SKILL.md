---
name: crear-proyecto
description: 'Ejecutor: diseña y genera un proyecto completo: requisitos, diseño aprobado, dónde vive el código y andamiaje por bloques. Usar al pedir un proyecto, no un script suelto.'
---

# Modo: crear proyecto

Objetivo: pasar de una idea a un proyecto con estructura, decisiones documentadas y andamiaje
funcionando. Sigue `metodo-ejecutor.md`, incluida la regla de aprobación.

**Esto no es `crear-script`.** Un script resuelve una tarea y cabe en un archivo; un proyecto
tiene varias piezas, configuración, log y vida propia. Si dudas, pregunta en una línea: *"¿esto
es un script suelto o un proyecto con varias piezas?"*.

## 0. La frontera: dónde vive el código

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

## 1. Requisitos (máximo 3 preguntas)

Pregunta solo lo que cambia el diseño, en un solo mensaje:

1. **Qué resuelve y para quién** — en una frase.
2. **Entradas y salidas** — de dónde vienen los datos y a dónde van.
3. **Frecuencia y disparador** — manual, diario, por evento; quién lo ejecuta.

Lo que no sea crítico, **asúmelo y declara el supuesto**. Si toca nómina, SAP, datos financieros
o bases productivas, dilo ya: el proyecto entero nace en **nivel protegido**.

## 2. Diseño (propuesta, antes de código)

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

## 3. Andamiaje, bloque por bloque

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

## 4. Al terminar

Dos escrituras, y ninguna es código:

**a) La nota del proyecto** en `Proyectos/<Nombre>/<Nombre>.md` de la bóveda, con la plantilla
`99-Plantillas/Plantilla - Proyecto.md`. Llena objetivo, stack, arquitectura, **decisiones y por
qué**, **dónde vive el código** (el enlace al repo) y nivel protegido. Si no puedes escribir en
la bóveda, entrégala en un bloque `markdown` para pegar.

**b) Las trampas nuevas**, si salió alguna: van a la sección `## Trampas` de
`<Lenguaje>/Referencia/` en la bóveda, **no** a `trampas-conocidas.md`, que es generado.

## 5. Qué NO hacer

- **No generes el proyecto entero de un golpe** aunque parezca chico. El andamiaje se aprueba por
  bloques como todo lo demás.
- **No metas dependencias** sin proponerlas, con su alternativa sin dependencia.
- **No inventes la estructura** de un framework que no has verificado: confirma en su
  documentación oficial y declara la versión que asumes.
- **No dejes datos reales** en la configuración de ejemplo, ni el nombre del servidor de la
  empresa en el README.
