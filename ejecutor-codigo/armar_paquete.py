"""Arma los paquetes del ejecutor de código para cada plataforma a partir de las fuentes.

Fuentes (lo único que se edita a mano):
    nucleo/        metodo-ejecutor.md, principios-y-seguridad.md, contexto-proyecto.md
    nucleo/trampas-extra.md   trampas de temas que aún no tienen carpeta en la bóveda
    skills/        una carpeta por modo con su SKILL.md
    adaptadores/   lo específico de cada plataforma destino

Generado pero versionado:
    nucleo/trampas-conocidas.md   se regenera con --boveda desde <Lenguaje>/Referencia/

Salida (se regenera completa, no editar a mano):
    listo/claude-code/         contenido para copiar a la raíz de cada repositorio
    listo/claude-proyecto/     instrucciones + archivos + skills en .zip
    listo/chatgpt-proyecto/    instrucciones + archivos (modos en un solo .md)
    listo/obsidian-boveda/     lo que se copia sobre la bóveda de Obsidian

Uso:
    python armar_paquete.py                 arma el paquete
    python armar_paquete.py --check         no escribe nada; falla si listo/ está desfasado
    python armar_paquete.py --boveda RUTA   regenera trampas-conocidas.md desde la bóveda
"""

import filecmp
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
NUCLEO = RAIZ / "nucleo"
SKILLS = RAIZ / "skills"
ADAPT = RAIZ / "adaptadores"
LISTO = RAIZ / "listo"

ARCHIVOS_NUCLEO = [
    "metodo-ejecutor.md",
    "principios-y-seguridad.md",
    "trampas-conocidas.md",
    "contexto-proyecto.md",
]
# En Claude Code, la plantilla de contexto va en la raíz del repo; el resto en .claude/ejecutor/
CONTEXTO = "contexto-proyecto.md"
ARCHIVO_MODOS = "modos-ejecutor.md"
TRAMPAS = "trampas-conocidas.md"
TRAMPAS_EXTRA = "trampas-extra.md"

ORDEN_MODOS = [
    "analizar-codigo",
    "crear-proyecto",
    "crear-script",
    "modificar-codigo",
    "depurar-error",
    "documentar-proceso",
    "migrar-lenguaje",
    "revisar-seguridad",
    "escribir-tests",
]

MAX_NOMBRE = 64        # límite de claude.ai para `name`
MAX_DESCRIPCION = 200  # límite de claude.ai para `description`
AVISO_DESCRIPCION = 180  # a partir de aquí, advertir: queda poco margen para editar

# En la bóveda los archivos del paquete viven con otro nombre o se reparten en notas.
RUTAS_BOVEDA = """> **En esta bóveda**, los archivos que se nombran abajo están aquí:
> `metodo-ejecutor.md` → `Logica/_tutor-ejecutor/Ejecutor - Metodo.md` ·
> `principios-y-seguridad.md` → `Logica/_tutor-ejecutor/Ejecutor - Principios y seguridad.md` ·
> `trampas-conocidas.md` → la sección `## Trampas` de `<Lenguaje>/Referencia/` (ahí se anotan
> las nuevas) · `contexto-proyecto.md` → `Proyectos/<Nombre>/<Nombre>.md`.
"""

# Lo que el paquete de Claude Code sugiere ignorar en cada repositorio.
GITIGNORE_SUGERIDO = """# Sugerido por el ejecutor de código. Revísalo y pégalo en tu .gitignore
# ANTES del primer `git add`. El contexto del proyecto y la configuración
# suelen llevar rutas, servidores o datos internos.

contexto-proyecto.md
Config.ini
.env
*.log
logs/

# Python
__pycache__/
*.pyc
.venv/
venv/
"""


def leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def escribir(ruta: Path, texto: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")


def separar_frontmatter(texto: str) -> tuple[dict, str]:
    """Devuelve (campos del frontmatter, cuerpo). Solo acepta `clave: valor` de una línea."""
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        raise ValueError("SKILL.md sin frontmatter")
    campos = {}
    for linea in m.group(1).splitlines():
        clave, sep, valor = linea.partition(":")
        if not sep:
            raise ValueError(f"línea de frontmatter sin ':' → {linea!r}")
        valor = valor.strip()
        if valor[:1] in ('"', "[", "{", "|", ">"):
            # El parser es de una línea: mejor fallar ruidosamente que aceptar mal.
            raise ValueError(
                f"valor no soportado en '{clave.strip()}': usa texto plano o comillas simples"
            )
        if len(valor) >= 2 and valor[0] == valor[-1] == "'":
            valor = valor[1:-1].replace("''", "'")  # comillas simples de YAML
        campos[clave.strip()] = valor
    return campos, texto[m.end():]


def validar_skill(carpeta: Path, campos: dict) -> tuple[list[str], list[str]]:
    errores, avisos = [], []
    nombre = campos.get("name", "")
    desc = campos.get("description", "")
    if nombre != carpeta.name:
        errores.append(f"name '{nombre}' no coincide con la carpeta '{carpeta.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nombre):
        errores.append(f"name '{nombre}' debe ir en minúsculas con guiones")
    if len(nombre) > MAX_NOMBRE:
        errores.append(f"name mide {len(nombre)} (máx. {MAX_NOMBRE})")
    if not desc:
        errores.append("falta description")
    elif len(desc) > MAX_DESCRIPCION:
        errores.append(f"description mide {len(desc)} (máx. {MAX_DESCRIPCION})")
    elif len(desc) > AVISO_DESCRIPCION:
        avisos.append(
            f"description mide {len(desc)}: quedan {MAX_DESCRIPCION - len(desc)} caracteres "
            f"de margen ({len(desc.encode('utf-8'))} bytes)"
        )
    return errores, avisos


def bajar_titulos(cuerpo: str) -> str:
    """Quita el título '# Modo: …' y baja un nivel los demás, sin tocar bloques de código."""
    salida, en_codigo = [], False
    for linea in cuerpo.splitlines():
        if linea.lstrip().startswith(("```", "~~~")):
            en_codigo = not en_codigo
        elif not en_codigo and re.match(r"^# ", linea):
            continue  # el título lo pone el encabezado del modo
        elif not en_codigo and re.match(r"^#{2,5} ", linea):
            linea = "#" + linea
        salida.append(linea)
    return "\n".join(salida).strip() + "\n"


def extraer_trampas(nota: str) -> str:
    """Devuelve el cuerpo de la sección '## Trampas' de una nota, sin su encabezado."""
    m = re.search(r"^## Trampas\n(.*?)(?=^## |\Z)", nota, re.S | re.M)
    if not m:
        return ""
    # La cita de contexto ('> …') es para quien lee la nota, no para el paquete.
    cuerpo = "\n".join(l for l in m.group(1).splitlines() if not l.lstrip().startswith(">"))
    return cuerpo.strip()


def recolectar_trampas(boveda: Path) -> str:
    """Arma trampas-conocidas.md desde las notas <Lenguaje>/Referencia/ de la bóveda."""
    if not boveda.is_dir():
        raise ValueError(f"no encuentro la bóveda en {boveda}")
    por_lenguaje: dict[str, list[str]] = {}
    for nota in sorted(boveda.glob("*/Referencia/*.md")):
        cuerpo = extraer_trampas(leer(nota))
        if cuerpo:
            por_lenguaje.setdefault(nota.parts[-3], []).append(cuerpo)
    if not por_lenguaje:
        raise ValueError(f"ninguna nota de {boveda}/*/Referencia/ tiene sección '## Trampas'")

    partes = [
        "# Trampas conocidas\n\n"
        "Errores que ya costaron tiempo o que fallan en silencio. **Antes de entregar código** en\n"
        "un lenguaje de esta lista, revisa su sección.\n\n"
        "Formato: **trampa** — síntoma → solución.\n\n"
        "> **Archivo generado.** La copia maestra son las secciones `## Trampas` de las notas\n"
        "> `<Lenguaje>/Referencia/` de la bóveda de Obsidian. Para agregar una trampa, anótala\n"
        "> ahí y corre `python armar_paquete.py --boveda <ruta a la bóveda>`.\n"
    ]
    for lenguaje in sorted(por_lenguaje):
        partes.append(f"\n---\n\n## {lenguaje}\n\n" + "\n\n".join(por_lenguaje[lenguaje]) + "\n")

    extra = NUCLEO / TRAMPAS_EXTRA
    if extra.exists():
        partes.append("\n---\n\n" + leer(extra).strip() + "\n")
    return "".join(partes)


def envolver_nota_boveda(cuerpo: str, tags: str) -> str:
    return f"---\ntags: {tags}\ncreado: 2026-09-14\n---\n\n{cuerpo.strip()}\n"


def con_rutas_boveda(texto: str) -> str:
    """Inserta, tras el frontmatter (o al inicio si no hay), la equivalencia de los archivos
    del paquete con su ubicación en la bóveda.

    Las fuentes nombran `metodo-ejecutor.md` y compañía porque así se llaman en las demás
    plataformas. En la bóveda esos archivos no existen con ese nombre: sin esta tabla, las
    skills mandan al modelo a buscar archivos fantasma.
    """
    if texto.startswith("---\n"):
        fin = texto.index("\n---\n", 4) + len("\n---\n")
        cabeza, cuerpo = texto[:fin], texto[fin:].lstrip("\n")
        return f"{cabeza}\n{RUTAS_BOVEDA}\n{cuerpo}"
    return f"{RUTAS_BOVEDA}\n{texto}"


def escribir_zip_reproducible(destino: Path, carpeta: Path) -> None:
    """ZIP con fecha fija: el archivo solo cambia si cambia el contenido."""
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(carpeta.rglob("*")):
            if f.is_file():
                info = zipfile.ZipInfo(
                    str(Path(carpeta.name) / f.relative_to(carpeta)),
                    date_time=(1980, 1, 1, 0, 0, 0),
                )
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, f.read_bytes())


def diferencias(a: Path, b: Path, prefijo: str = "") -> list[str]:
    """Compara dos árboles por contenido. Devuelve una lista de diferencias legibles."""
    cmp = filecmp.dircmp(a, b)
    fuera = [f"{prefijo}{n}: sobra en listo/" for n in sorted(cmp.left_only)]
    fuera += [f"{prefijo}{n}: falta en listo/" for n in sorted(cmp.right_only)]
    _, distintos, errores = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    fuera += [f"{prefijo}{n}: contenido distinto" for n in sorted(distintos)]
    fuera += [f"{prefijo}{n}: no se pudo comparar" for n in sorted(errores)]
    for sub in sorted(cmp.common_dirs):
        fuera += diferencias(a / sub, b / sub, f"{prefijo}{sub}/")
    return fuera


def construir(destino_raiz: Path, skills: list, modos: str) -> None:
    """Escribe el paquete completo bajo `destino_raiz`. No toca nada fuera de ahí."""
    # 1. Claude Code (se copia a la raíz de cada repositorio de trabajo)
    cc = destino_raiz / "claude-code"
    (cc / ".claude" / "ejecutor").mkdir(parents=True)
    shutil.copy2(ADAPT / "claude-code" / "CLAUDE.md", cc / "CLAUDE.md")
    for archivo in ARCHIVOS_NUCLEO:
        destino = cc / archivo if archivo == CONTEXTO else cc / ".claude" / "ejecutor" / archivo
        shutil.copy2(NUCLEO / archivo, destino)
    for carpeta, _, _ in skills:
        shutil.copytree(carpeta, cc / ".claude" / "skills" / carpeta.name)
    # El propio paquete predica `.gitignore` antes del primer commit: que lo entregue.
    escribir(cc / "gitignore-sugerido.txt", GITIGNORE_SUGERIDO)

    # 2. Proyectos de chat (no pueden escribir archivos: los modos van en un solo .md)
    for plataforma in ["claude-proyecto", "chatgpt-proyecto"]:
        destino = destino_raiz / plataforma
        archivos = destino / "archivos-del-proyecto"
        archivos.mkdir(parents=True)
        shutil.copy2(ADAPT / plataforma / "instrucciones.md", destino / "instrucciones.md")
        for archivo in ARCHIVOS_NUCLEO:
            shutil.copy2(NUCLEO / archivo, archivos / archivo)
        escribir(archivos / ARCHIVO_MODOS, modos)

    # 3. Skills en .zip para claude.ai  (zip → carpeta-skill/SKILL.md)
    zips = destino_raiz / "claude-proyecto" / "skills-para-subir"
    zips.mkdir()
    for carpeta, _, _ in skills:
        escribir_zip_reproducible(zips / f"{carpeta.name}.zip", carpeta)

    # 4. Bóveda de Obsidian (aquí NO va código: solo el agente, las skills y las reglas)
    bov = destino_raiz / "obsidian-boveda"
    bov.mkdir(parents=True)
    origen_bov = ADAPT / "obsidian-boveda"
    shutil.copy2(origen_bov / "AGENTS-ejecutor.md", bov / "AGENTS-ejecutor.md")
    escribir(bov / ".claude" / "agents" / "ejecutor.md", leer(origen_bov / "agentes" / "ejecutor.md"))
    for carpeta, _, _ in skills:
        escribir(
            bov / ".claude" / "skills" / carpeta.name / "SKILL.md",
            con_rutas_boveda(leer(carpeta / "SKILL.md")),
        )
    escribir(
        bov / "99-Plantillas" / "Plantilla - Proyecto.md",
        leer(origen_bov / "Plantilla - Proyecto.md"),
    )
    escribir(
        bov / "_tutor-ejecutor" / "Ejecutor - Metodo.md",
        con_rutas_boveda(
            envolver_nota_boveda(
                leer(NUCLEO / "metodo-ejecutor.md"), "[tipo/ejecutor, estado/en-curso]"
            )
        ),
    )
    escribir(
        bov / "_tutor-ejecutor" / "Ejecutor - Principios y seguridad.md",
        con_rutas_boveda(
            envolver_nota_boveda(
                leer(NUCLEO / "principios-y-seguridad.md"), "[tipo/ejecutor, estado/en-curso]"
            )
        ),
    )


def main() -> int:
    argv = sys.argv[1:]
    modo_check = "--check" in argv
    boveda = None
    if "--boveda" in argv:
        i = argv.index("--boveda")
        if i + 1 >= len(argv):
            print("--boveda necesita la ruta a la bóveda")
            return 2
        boveda = Path(argv[i + 1]).expanduser().resolve()
        del argv[i:i + 2]
    sobra = [a for a in argv if a != "--check"]
    if sobra:
        print(f"Argumento no reconocido: {sobra[0]}\n"
              "Uso: python armar_paquete.py [--check] [--boveda RUTA]")
        return 2

    # 0. Regenerar trampas-conocidas.md desde la bóveda, si se pidió
    if boveda:
        try:
            texto = recolectar_trampas(boveda)
        except ValueError as e:
            print(f"ERROR: {e}")
            return 1
        if modo_check:
            if leer(NUCLEO / TRAMPAS) != texto:
                print(f"{TRAMPAS} está desfasado respecto de las notas de la bóveda.")
                print("Corre `python armar_paquete.py --boveda <ruta>` y vuelve a commitear.")
                return 1
        else:
            escribir(NUCLEO / TRAMPAS, texto)
            print(f"{TRAMPAS} regenerado desde {boveda}")

    # 1. Leer y validar skills
    skills, errores, avisos = [], [], []
    for nombre in ORDEN_MODOS:
        carpeta = SKILLS / nombre
        try:
            campos, cuerpo = separar_frontmatter(leer(carpeta / "SKILL.md"))
        except (OSError, ValueError) as e:
            errores.append(f"[{nombre}] {e}")
            continue
        errs, avs = validar_skill(carpeta, campos)
        errores += [f"[{nombre}] {e}" for e in errs]
        avisos += [f"[{nombre}] {a}" for a in avs]
        skills.append((carpeta, campos, cuerpo))
    extras = {p.name for p in SKILLS.iterdir() if p.is_dir()} - set(ORDEN_MODOS)
    if extras:
        errores.append(f"Skills sin registrar en ORDEN_MODOS: {sorted(extras)}")
    if errores:
        print("ERRORES:\n  " + "\n  ".join(errores))
        return 1
    if avisos:
        print("AVISOS:\n  " + "\n  ".join(avisos))

    # 2. modos-ejecutor.md (para las plataformas sin skills)
    partes = [
        "# Modos del ejecutor\n\n"
        "Procedimientos largos del ejecutor. Cuando un modo aplique, sigue su sección.\n"
        "Archivo generado desde `skills/` con `armar_paquete.py`: no editar a mano.\n"
    ]
    for carpeta, campos, cuerpo in skills:
        partes.append(
            f"\n---\n\n## {campos['name']}\n\n"
            f"**Cuándo usarlo:** {campos['description']}\n\n{bajar_titulos(cuerpo)}"
        )
    modos = "".join(partes)

    # 3. Construir (en un temporal si es --check, para no tocar listo/)
    if modo_check:
        with tempfile.TemporaryDirectory() as tmp:
            esperado = Path(tmp) / "listo"
            esperado.mkdir()
            construir(esperado, skills, modos)
            if not LISTO.exists():
                print("ERROR: listo/ no existe. Corre `python armar_paquete.py`.")
                return 1
            difs = diferencias(LISTO, esperado)
        if difs:
            print("listo/ está desfasado respecto de las fuentes:")
            print("  " + "\n  ".join(difs))
            print("\nCorre `python armar_paquete.py` y vuelve a commitear.")
            return 1
        print(f"listo/ está sincronizado con las fuentes ({len(skills)} modos).")
        return 0

    if LISTO.exists():
        shutil.rmtree(LISTO)
    LISTO.mkdir()
    construir(LISTO, skills, modos)

    # 4. Resumen
    print("Paquete armado en:", LISTO)
    for carpeta, campos, _ in skills:
        d = campos["description"]
        print(f"  modo {campos['name']:<20} descripción: {len(d)}/{MAX_DESCRIPCION}")
    for plataforma in ["claude-proyecto", "chatgpt-proyecto"]:
        n = len(leer(ADAPT / plataforma / "instrucciones.md"))
        print(f"  instrucciones {plataforma:<17} {n} caracteres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
