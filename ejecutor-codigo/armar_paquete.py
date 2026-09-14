"""Arma los paquetes del ejecutor de código para cada plataforma a partir de las fuentes.

Fuentes (lo único que se edita a mano):
    nucleo/        metodo-ejecutor.md, principios-y-seguridad.md, trampas-conocidas.md,
                   contexto-proyecto.md (plantilla)
    skills/        una carpeta por modo con su SKILL.md
    adaptadores/   CLAUDE.md e instrucciones de cada proyecto

Salida (se regenera completa, no editar a mano):
    listo/claude-code/                contenido para copiar a la raíz de cada repositorio
    listo/claude-proyecto/            instrucciones + archivos + skills en .zip
    listo/chatgpt-proyecto/           instrucciones + archivos (modos en un solo .md)

Uso:  python armar_paquete.py
"""

import re
import shutil
import sys
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
ORDEN_MODOS = [
    "analizar-codigo",
    "modificar-codigo",
    "crear-script",
    "depurar-error",
    "documentar-proceso",
    "migrar-lenguaje",
]
MAX_NOMBRE = 64        # límite de claude.ai para `name`
MAX_DESCRIPCION = 200  # límite de claude.ai para `description`


def leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def escribir(ruta: Path, texto: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")


def separar_frontmatter(texto: str) -> tuple[dict, str]:
    """Devuelve (campos del frontmatter, cuerpo). Solo lee `clave: valor` de una línea."""
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        raise ValueError("SKILL.md sin frontmatter")
    campos = {}
    for linea in m.group(1).splitlines():
        clave, _, valor = linea.partition(":")
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] == "'":
            valor = valor[1:-1].replace("''", "'")  # comillas simples de YAML
        campos[clave.strip()] = valor
    return campos, texto[m.end():]


def validar_skill(carpeta: Path, campos: dict) -> list[str]:
    errores = []
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
    return errores


def bajar_titulos(cuerpo: str) -> str:
    """Quita el título '# Modo: …' y baja un nivel los demás, sin tocar bloques de código."""
    salida, en_codigo = [], False
    for linea in cuerpo.splitlines():
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
        elif not en_codigo and re.match(r"^# ", linea):
            continue  # el título lo pone el encabezado del modo
        elif not en_codigo and re.match(r"^#{2,5} ", linea):
            linea = "#" + linea
        salida.append(linea)
    return "\n".join(salida).strip() + "\n"


def main() -> int:
    # 1. Leer y validar skills
    skills, errores = [], []
    for nombre in ORDEN_MODOS:
        carpeta = SKILLS / nombre
        campos, cuerpo = separar_frontmatter(leer(carpeta / "SKILL.md"))
        errores += [f"[{nombre}] {e}" for e in validar_skill(carpeta, campos)]
        skills.append((carpeta, campos, cuerpo))
    extras = {p.name for p in SKILLS.iterdir() if p.is_dir()} - set(ORDEN_MODOS)
    if extras:
        errores.append(f"Skills sin registrar en ORDEN_MODOS: {sorted(extras)}")
    if errores:
        print("ERRORES:\n  " + "\n  ".join(errores))
        return 1

    # 2. Limpiar salida
    if LISTO.exists():
        shutil.rmtree(LISTO)

    # 3. modos-ejecutor.md (para proyectos sin skills)
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

    # 4. Claude Code  (se copia a la raíz de cada repositorio)
    cc = LISTO / "claude-code"
    (cc / ".claude" / "ejecutor").mkdir(parents=True)
    shutil.copy2(ADAPT / "claude-code" / "CLAUDE.md", cc / "CLAUDE.md")
    for archivo in ARCHIVOS_NUCLEO:
        destino = cc / archivo if archivo == CONTEXTO else cc / ".claude" / "ejecutor" / archivo
        shutil.copy2(NUCLEO / archivo, destino)
    for carpeta, _, _ in skills:
        shutil.copytree(carpeta, cc / ".claude" / "skills" / carpeta.name)

    # 5. Proyectos (Claude y ChatGPT)
    for plataforma in ["claude-proyecto", "chatgpt-proyecto"]:
        destino = LISTO / plataforma
        archivos = destino / "archivos-del-proyecto"
        archivos.mkdir(parents=True)
        shutil.copy2(ADAPT / plataforma / "instrucciones.md", destino / "instrucciones.md")
        for archivo in ARCHIVOS_NUCLEO:
            shutil.copy2(NUCLEO / archivo, archivos / archivo)
        escribir(archivos / ARCHIVO_MODOS, modos)

    # 6. Skills en .zip para claude.ai  (zip → carpeta-skill/SKILL.md)
    zips = LISTO / "claude-proyecto" / "skills-para-subir"
    zips.mkdir()
    for carpeta, _, _ in skills:
        with zipfile.ZipFile(zips / f"{carpeta.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(carpeta.rglob("*")):
                if f.is_file():
                    z.write(f, Path(carpeta.name) / f.relative_to(carpeta))

    # 7. Resumen
    print("Paquete armado en:", LISTO)
    for carpeta, campos, _ in skills:
        print(f"  skill {campos['name']:<20} descripción: {len(campos['description'])}/{MAX_DESCRIPCION}")
    for plataforma in ["claude-proyecto", "chatgpt-proyecto"]:
        n = len(leer(ADAPT / plataforma / "instrucciones.md"))
        print(f"  instrucciones {plataforma:<17} {n} caracteres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
