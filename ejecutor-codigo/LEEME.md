# Ejecutor de código — paquete multiplataforma

Un mismo ejecutor para **Claude Code**, **Proyectos de Claude** y **Proyectos de ChatGPT**.
Analiza, crea, modifica, mejora, depura, documenta y migra código **en cualquier lenguaje**.
**Analizar es directo; cualquier cambio va primero como propuesta y se ejecuta solo con tu
aprobación**, bloque por bloque.

## Qué hay aquí

```text
ejecutor-codigo/
├── LEEME.md
├── armar_paquete.py              ← regenera listo/ desde las fuentes
│
├── nucleo/                       ← FUENTE compartida
│   ├── metodo-ejecutor.md        ← reglas: aprobación, nivel protegido, calidad, entrega
│   ├── principios-y-seguridad.md ← tu arquitectura y reglas de seguridad
│   ├── trampas-conocidas.md      ← COPIA MAESTRA de las trampas (crece con el uso)
│   └── contexto-proyecto.md      ← plantilla para llenar por proyecto
├── skills/                       ← FUENTE: los 6 modos
│   ├── analizar-codigo/
│   ├── modificar-codigo/
│   ├── crear-script/
│   ├── depurar-error/
│   ├── documentar-proceso/
│   └── migrar-lenguaje/
├── adaptadores/                  ← FUENTE: lo específico de cada plataforma
│
└── listo/                        ← SALIDA: lo que copias o subes (generado)
    ├── claude-code/
    ├── claude-proyecto/
    └── chatgpt-proyecto/
```

**Regla de oro:** solo editas `nucleo/`, `skills/` y `adaptadores/`. Después corres
`python armar_paquete.py` y usas lo que sale en `listo/`.

## Montaje

### Claude Code (en cada repositorio o carpeta de código)

Aquí **sí van carpetas**.

1. Copia el **contenido** de `listo/claude-code/` a la **raíz** de tu repositorio: `CLAUDE.md`,
   `contexto-proyecto.md` y la carpeta `.claude/` (el punto al inicio es normal).
2. **Si el repositorio ya tenía `CLAUDE.md`**, no lo reemplaces: agrega al inicio del tuyo estas
   tres líneas y copia solo `contexto-proyecto.md` y `.claude/`:

   ```text
   @.claude/ejecutor/metodo-ejecutor.md
   @.claude/ejecutor/principios-y-seguridad.md
   @contexto-proyecto.md
   ```

3. Llena `contexto-proyecto.md` **sin datos sensibles**. Si aun así lleva algo interno, agrégalo
   a `.gitignore`.
4. Abre Claude Code en la raíz y pide lo que necesites (o usa `/analizar-codigo`, etc.).

> No lo copies a tu carpeta del tutor: cada carpeta lleva su propio `CLAUDE.md` y sus propias
> skills, así no se mezclan.

### Proyecto de Claude (claude.ai)

Todo va **suelto**, sin carpetas.

1. Crea un proyecto "Ejecutor" y **pega** el texto de `listo/claude-proyecto/instrucciones.md` en
   las instrucciones del proyecto.
2. Sube **sueltos** los 5 archivos de `listo/claude-proyecto/archivos-del-proyecto/`.
3. **Skills:** en **Personalizar → Skills**, sube cada `.zip` de
   `listo/claude-proyecto/skills-para-subir/` **sin descomprimir** y actívalo (requiere la
   ejecución de código activada).
   - Las skills son de tu cuenta y conviven con las del tutor. Sus descripciones empiezan con
     "Ejecutor:" y las instrucciones de cada proyecto dicen cuáles aplican.
   - `modos-ejecutor.md` es el respaldo si una skill no se activa.

### Proyecto de ChatGPT

Todo va **suelto**, sin carpetas.

1. Crea un proyecto "Ejecutor" y **pega** el texto de `listo/chatgpt-proyecto/instrucciones.md` en
   las instrucciones del proyecto.
2. Sube **sueltos** los 5 archivos de `listo/chatgpt-proyecto/archivos-del-proyecto/` (entran en
   una sola subida).

## Uso diario

### Un proyecto general, varios sistemas

- **Opción rápida:** pega el contexto del sistema al inicio del chat (o describe el sistema en 3-4
  líneas). El chat manda sobre el archivo.
- **Opción ordenada:** ten un `contexto-<sistema>.md` por sistema en tu computadora y reemplaza
  `contexto-proyecto.md` en el proyecto cuando cambies de sistema.
- Si un sistema se vuelve recurrente, **clona el proyecto** con su contexto fijo.

### Cómo pedir

| Quieres… | Escribe algo como |
|---|---|
| Entender un script | "analiza esto" + el código o el archivo |
| Un cambio | "cambia X para que Y" → recibes propuesta → "sí" |
| Algo nuevo | "crea un script que…" → requisitos → diseño → "sí" → bloques |
| Resolver un error | el mensaje exacto o la captura + el código |
| Documentar | "documenta este proceso" |
| Migrar | "pasa esto de VBA a Python" |

**Atajos:** `rápido` · `plan` · `diff` · `completo` · `explica` · `prueba` · `seguridad` · `contexto`

### Datos reales

Antes de subir archivos a un chat, **anonimiza**: nombres, RFC, CURP, números de empleado, cuentas
y montos. Para analizar la estructura bastan pocas filas ficticias.

## Trampas conocidas: cómo crecen

Cuando `depurar-error` encuentre una causa que valga la pena recordar, te propondrá una entrada.

1. Pégala en **`nucleo/trampas-conocidas.md`** (la copia maestra).
2. Corre `python armar_paquete.py`.
3. Vuelve a subir `trampas-conocidas.md` a los proyectos y cópialo a `.claude/ejecutor/` en tus
   repositorios.

## Mantenimiento

1. Edita la fuente (`nucleo/`, `skills/` o `adaptadores/`).
2. Corre `python armar_paquete.py` (Python 3.9 o superior). Revisa que los nombres y las
   descripciones de las skills cumplan los límites de claude.ai (64 y 200 caracteres).
3. Vuelve a subir o copiar **solo lo que cambió**:
   - Una skill: su `.zip` a Claude, `modos-ejecutor.md` a ChatGPT (y a Claude) y su carpeta a
     `.claude/skills/` en tus repositorios.
   - Un archivo del núcleo: ese archivo a los tres lados.
4. **Nunca copies `contexto-proyecto.md` de `listo/` encima de uno ya lleno**: es la plantilla vacía.
