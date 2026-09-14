## Sin carpeta en la bóveda todavía

Trampas de lenguajes o temas que aún no tienen su propia carpeta en la bóveda. Cuando uno de
estos se vuelva recurrente, créale su carpeta `<Lenguaje>/Referencia/`, mueve sus trampas a la
sección `## Trampas` de esa nota y bórralas de aquí.

### JavaScript

- **`==` en vez de `===`** — conversiones de tipo inesperadas (`"0" == 0` es `true`) → usa `===`.
- **`async` dentro de `forEach`** — `forEach` no espera las promesas → usa `for...of` con `await`
  o `Promise.all`.

### PowerShell

- **`try/catch` que no atrapa** — muchos errores de cmdlets no son terminales → agrega
  `-ErrorAction Stop` o ajusta `$ErrorActionPreference`.
