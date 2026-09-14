# Ejecutor de código — fuente única, cuatro destinos

Un mismo ejecutor para **Claude Code**, **Proyectos de Claude**, **Proyectos de ChatGPT** y la
**bóveda de Obsidian**. Analiza, crea, modifica, depura, documenta y migra código **en cualquier
lenguaje**. Analizar es directo; **cualquier cambio va primero como propuesta** y se ejecuta solo
con tu aprobación, bloque por bloque.

## La frontera, que es lo que hay que entender primero

El ejecutor produce **dos cosas que van a lugares distintos**:

```
              LA BÓVEDA (conocimiento y diseño)
   Proyectos/<Nombre>/       ← diseño, decisiones, bitácora
   <Lenguaje>/Referencia/    ← trampas y snippets  ← COPIA MAESTRA
            │                              ▲
   alimenta │                              │ devuelve diseño y trampas nuevas
            ▼                              │
      ┌───────────────────────────────────────┐
      │            EL EJECUTOR                │
      └───────────────────────────────────────┘
                       │
                       └── escribe CÓDIGO ──▶ su propio repositorio
                                              ❌ nunca la bóveda
```

**El código nunca se escribe dentro de la bóveda.** Es una base de conocimiento: si se llena de
`.py`, se vuelve lenta, Dataview se contamina con archivos que no son notas y el historial mezcla
apuntes con código.

## Qué hay aquí

```text
ejecutor-codigo/
├── LEEME.md
├── armar_paquete.py              ← regenera listo/ desde las fuentes
├── pruebas/                      ← unittest de las funciones puras del build
│
├── nucleo/                       FUENTE compartida
│   ├── metodo-ejecutor.md        ← aprobación, nivel protegido, calidad, entrega
│   ├── principios-y-seguridad.md ← arquitectura y reglas de seguridad
│   ├── contexto-proyecto.md      ← plantilla por proyecto
│   ├── trampas-extra.md          ← trampas sin carpeta en la bóveda todavía
│   └── trampas-conocidas.md      ← GENERADO desde la bóveda (no editar a mano)
├── skills/                       FUENTE: los 7 modos
│   ├── analizar-codigo/   crear-proyecto/   crear-script/   modificar-codigo/
│   └── depurar-error/     documentar-proceso/   migrar-lenguaje/
├── adaptadores/                  FUENTE: lo específico de cada destino
│   ├── claude-code/   claude-proyecto/
│   └── chatgpt-proyecto/   obsidian-boveda/
│
└── listo/                        SALIDA generada — no editar a mano
```

**Regla de oro:** solo editas `nucleo/` (menos `trampas-conocidas.md`), `skills/` y
`adaptadores/`. Después corres `python armar_paquete.py`.

Ya no depende de tu memoria: `python armar_paquete.py --check` falla si `listo/` quedó desfasado,
y el CI lo corre en cada push.

## Los siete modos

| Modo | Se activa cuando pides… |
|---|---|
| `analizar-codigo` | entender código sin cambiarlo |
| `crear-proyecto` | un proyecto, arquitectura o sistema completo |
| `crear-script` | un script suelto, que cabe en un archivo |
| `modificar-codigo` | corregir, mejorar o refactorizar lo que ya existe |
| `depurar-error` | resolver un error o un comportamiento raro |
| `documentar-proceso` | README o manual de operación |
| `migrar-lenguaje` | pasar código de un lenguaje a otro |

`crear-proyecto` es el que diseña primero en la bóveda, pregunta **dónde va el código**, y solo
entonces genera el andamiaje por bloques.

## Trampas conocidas: la bóveda es la fuente

`nucleo/trampas-conocidas.md` es **generado**. La copia maestra son las secciones `## Trampas` de
las notas `<Lenguaje>/Referencia/` de la bóveda.

Cuando `depurar-error` encuentre una causa que valga la pena recordar:

1. Anótala en la nota del lenguaje, en su sección `## Trampas`.
2. Corre `python armar_paquete.py --boveda <ruta a obsidian-jbs>`.
3. Vuelve a copiar o subir lo que cambió.

Una trampa se anota **una vez**, donde ya la buscas cuando trabajas ese lenguaje. Si la escribes
en `trampas-conocidas.md`, el siguiente build la borra.

Los temas que aún no tienen carpeta en la bóveda (JavaScript, PowerShell) viven en
`nucleo/trampas-extra.md` hasta que les toque carpeta propia.

## Montaje

### Bóveda de Obsidian

Copia el contenido de `listo/obsidian-boveda/` sobre la raíz de la bóveda:

| Qué | A dónde |
|---|---|
| `.claude/agents/ejecutor.md` | `.claude/agents/` |
| `.claude/skills/` | `.claude/skills/` |
| `99-Plantillas/Plantilla - Proyecto.md` | `99-Plantillas/` (reemplaza) |
| `_tutor-ejecutor/` | `Logica/_tutor-ejecutor/` |
| `AGENTS-ejecutor.md` | pegar entre `<!-- ejecutor:inicio -->` y `<!-- ejecutor:fin -->` de `AGENTS.md` |

**Nunca toques `Proyectos/` ni `<Lenguaje>/Referencia/`:** ahí vive tu contenido real.

### Claude Code (en cada repositorio de trabajo)

1. Copia el contenido de `listo/claude-code/` a la **raíz** del repo: `CLAUDE.md`,
   `contexto-proyecto.md`, `gitignore-sugerido.txt` y la carpeta `.claude/`.
2. **Pega `gitignore-sugerido.txt` en tu `.gitignore` ANTES del primer `git add`.**
   `contexto-proyecto.md` lleva estructura y sistemas del proyecto: no debe subirse.
3. Si el repositorio ya tenía `CLAUDE.md`, no lo reemplaces: agrega al inicio del tuyo

   ```text
   @.claude/ejecutor/metodo-ejecutor.md
   @.claude/ejecutor/principios-y-seguridad.md
   @contexto-proyecto.md
   ```

4. Llena `contexto-proyecto.md` **sin datos sensibles**.

### Proyecto de Claude (claude.ai)

1. Pega `listo/claude-proyecto/instrucciones.md` en las instrucciones del proyecto.
2. Sube **sueltos** los 5 archivos de `listo/claude-proyecto/archivos-del-proyecto/`.
3. **Skills:** en **Personalizar → Skills**, sube cada `.zip` de `skills-para-subir/` sin
   descomprimir. Sus descripciones empiezan con `Ejecutor:` para no chocar con las del tutor.

### Proyecto de ChatGPT

Pega `listo/chatgpt-proyecto/instrucciones.md` y sube **sueltos** los 5 archivos de
`archivos-del-proyecto/`. No hay skills: los 7 modos van en `modos-ejecutor.md`.

## Cómo pedir

| Quieres… | Escribe algo como |
|---|---|
| Entender un script | "analiza esto" + el código |
| Un proyecto nuevo | "crea un proyecto que…" → diseño → "sí" → bloques |
| Algo suelto | "crea un script que…" |
| Un cambio | "cambia X para que Y" → propuesta → "sí" |
| Resolver un error | el mensaje exacto o la captura + el código |
| Documentar | "documenta este proceso" |
| Migrar | "pasa esto de VBA a Python" |

**Atajos:** `rápido` · `plan` · `diff` · `completo` · `explica` · `prueba` · `seguridad` ·
`contexto`

### Datos reales

Antes de subir archivos a un chat, **anonimiza**: nombres, RFC, CURP, números de empleado, cuentas
y montos. Para analizar la estructura bastan pocas filas ficticias.

## Mantenimiento

1. Edita la fuente (`nucleo/`, `skills/` o `adaptadores/`); las trampas, en la bóveda.
2. Corre las pruebas: `python -m unittest discover -s pruebas`.
3. Corre `python armar_paquete.py` (Python 3.9+), con `--boveda <ruta>` si tocaste trampas.
4. Vuelve a copiar o subir **solo lo que cambió**.
5. Antes de commitear: `python armar_paquete.py --check`.

### Notas

- Los ZIP son **reproducibles**: misma fuente, mismo byte. Si un `.zip` cambia en el diff, es
  porque cambió el contenido.
- El build **avisa** cuando una descripción de skill pasa de 180 caracteres: el tope de claude.ai
  es 200 y conviene dejar margen para editar.
- **Nunca copies `contexto-proyecto.md` de `listo/` encima de uno ya lleno:** es la plantilla vacía.
