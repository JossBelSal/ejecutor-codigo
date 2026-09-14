# Ejecutor de código — Claude Code

Las reglas de comportamiento están en el método compartido (el mismo de los Proyectos de Claude y
ChatGPT). Síguelo completo, junto con los principios y el contexto de este proyecto:

@.claude/ejecutor/metodo-ejecutor.md
@.claude/ejecutor/principios-y-seguridad.md
@contexto-proyecto.md

## Lo específico de Claude Code

### Archivos

```text
<tu-proyecto>/
├── CLAUDE.md                 ← este archivo
├── contexto-proyecto.md      ← contexto de ESTE proyecto (llénalo)
└── .claude/
    ├── ejecutor/
    │   ├── metodo-ejecutor.md
    │   ├── principios-y-seguridad.md
    │   └── trampas-conocidas.md   ← léelo antes de escribir código en un lenguaje listado
    └── skills/               ← los 6 modos del ejecutor
```

### Aprobación con acceso real a archivos

Aquí **sí puedes leer, crear, editar y ejecutar**. Por eso la regla de aprobación es estricta:

| Acción | Cómo |
|---|---|
| Leer, buscar, listar; `git status`, `git diff`, `git log`; pruebas que no escriben nada | **Directo** |
| Crear, editar, mover o borrar archivos; instalar dependencias; comandos que modifican algo | **Solo con la propuesta aprobada** |
| Ejecutar automatizaciones de SAP, scripts de AutoIt, macros sobre archivos reales, envíos, operaciones masivas | **Nunca las ejecutes tú.** Entrega el comando o los pasos para que el usuario los corra |

- **Antes de editar**, revisa `git status`. Si hay cambios sin commit, avísalo y sugiere commit o
  rama antes de seguir (obligatorio en nivel protegido).
- **Después de cada bloque**, muestra un resumen del `git diff` además del formato **HECHO**.
- Si el modo plan de Claude Code está disponible, úsalo para la propuesta.

### Modos

Los modos son skills en `.claude/skills/`. El usuario también puede llamarlos con
`/analizar-codigo`, `/modificar-codigo`, `/crear-script`, `/depurar-error`, `/documentar-proceso`
y `/migrar-lenguaje`.

### Trampas conocidas

Cuando `depurar-error` proponga una trampa nueva y el usuario la apruebe, agrégala a
`.claude/ejecutor/trampas-conocidas.md` y avisa que también conviene copiarla a la versión maestra
del paquete (`nucleo/trampas-conocidas.md`) para que llegue a las otras plataformas.
