## Ejecutor de código

Esta sección aplica cuando el usuario **construye**: pide un proyecto, un script, un cambio en
código que ya existe, resolver un error, documentar un proceso o migrar de lenguaje. Cuando
**estudia**, manda `CLAUDE.md` y el tutor. Si no está claro cuál de los dos es, pregunta en una
línea.

### La frontera: código fuera, conocimiento dentro

**Nunca se escribe código de trabajo dentro de la bóveda.** La excepción son los ejercicios de
estudio (`<Lenguaje>/Aprendizaje/`, `Python/python_udemy/`), que escribe el tutor.

| Qué | Dónde va |
|---|---|
| Diseño, decisiones, bitácora de un proyecto | `Proyectos/<Nombre>/<Nombre>.md` |
| Trampas nuevas de un lenguaje | `<Lenguaje>/Referencia/`, sección `## Trampas` |
| Snippets reutilizables | `<Lenguaje>/Referencia/` |
| Qué hace un script suelto y cuándo usarlo | `<Lenguaje>/Referencia/` |
| **El código de un proyecto** | **Su propio repositorio** |
| **Un script suelto** | **El repo `scripts`, o la carpeta donde se usa** |

Si el usuario pide generar código aquí, dilo y propón la alternativa: la bóveda se vuelve lenta,
Dataview se llena de archivos que no son notas y el historial mezcla apuntes con código. Procede
solo si insiste, y déjalo anotado en la nota del proyecto.

`Proyectos/Mano_Mouse/` es la excepción histórica, anterior a esta regla. No es precedente.

### Qué leer antes de responder

1. `Proyectos/<Nombre>/<Nombre>.md` del proyecto en curso, si lo hay. Si el usuario da contexto en
   el chat, **ese manda** sobre la nota.
2. La sección `## Trampas` de `<Lenguaje>/Referencia/`. **Revísala antes de entregar código** en
   ese lenguaje.
3. `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md`.
4. `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` solo si hace falta el detalle.

### La regla de aprobación

| Acción | Cómo |
|---|---|
| Leer, analizar, explicar, diagnosticar; `git status`, `git diff`, `git log` | **Directo** |
| Crear, editar, mover o borrar archivos; instalar dependencias | **Propuesta → aprobación → ejecución** |
| SAP, AutoIt, macros sobre archivos reales, envíos, operaciones masivas | **Nunca las ejecutes tú.** Entrega el comando o los pasos |

**Aprobación válida:** "sí", "va", "ok", "dale", "adelante". Una pregunta nueva, un silencio o un
"mmm" **no** es aprobación. En duda, pregunta.

**Bloque por bloque:** entrega el bloque 1 y espera el OK antes del 2. **Alcance cerrado:** si ves
otro problema, repórtalo como *Fuera de alcance*, sin arreglarlo.

### Nivel protegido

Nómina · SAP productivo · datos financieros · bases productivas · operaciones masivas
(`REPLACE ALL`, `UPDATE`/`DELETE` sin `WHERE`) · envíos · credenciales.

Además de la propuesta exige: **respaldo**, **prueba en seco**, **plan de reversa**,
**confirmación separada** y **revisión humana**. El atajo `rápido` **nunca** aplica aquí.

### Calidad y seguridad

Función completa lista para pegar · respeta el estilo existente · manejo de errores donde el
fallo es probable · **nada sensible fijo en el código**: credenciales, rutas reales y servidores
van a configuración externa · `.gitignore` **antes** del primer `git add` · comentarios solo para
el porqué · dependencias nuevas solo con propuesta · **no inventes APIs**: verifica en
documentación oficial y declara la versión que asumes.

### Modos y atajos

Los procedimientos completos están en `.claude/skills/`: `analizar-codigo`, `crear-proyecto`,
`crear-script`, `modificar-codigo`, `depurar-error`, `documentar-proceso`, `migrar-lenguaje`.
Ábrelos cuando apliquen; Codex no los carga solo.

Atajos: `rápido` · `plan` · `diff` · `completo` · `explica` · `prueba` · `seguridad` · `contexto`

### Al cerrar

Actualiza la nota del proyecto (estado, próximos pasos, bitácora) y manda las trampas nuevas a
`<Lenguaje>/Referencia/`. Cada bloque entregado cierra con: **qué cambió · cómo probar · cómo
revertir · siguiente**.
