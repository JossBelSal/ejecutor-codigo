"""Pruebas de las funciones puras de armar_paquete.py.

Ahí vive el riesgo de regresión: el parser de frontmatter, la validación de skills, la
degradación de títulos y la recolección de trampas desde la bóveda.

Correr con:  python -m unittest discover -s pruebas
"""

import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from armar_paquete import (  # noqa: E402
    RUTAS_BOVEDA,
    bajar_titulos,
    con_rutas_boveda,
    escribir_zip_reproducible,
    extraer_trampas,
    recolectar_trampas,
    separar_frontmatter,
    validar_skill,
)


class SepararFrontmatter(unittest.TestCase):
    def test_lee_clave_valor_simple(self):
        campos, cuerpo = separar_frontmatter("---\nname: uno\n---\n# Título\n")
        self.assertEqual(campos["name"], "uno")
        self.assertEqual(cuerpo, "# Título\n")

    def test_desenvuelve_comillas_simples(self):
        campos, _ = separar_frontmatter("---\ndescription: 'Ejecutor: algo'\n---\nx\n")
        self.assertEqual(campos["description"], "Ejecutor: algo")

    def test_sin_frontmatter_revienta(self):
        with self.assertRaises(ValueError):
            separar_frontmatter("# Solo un título\n")

    def test_comillas_dobles_se_rechazan(self):
        with self.assertRaises(ValueError):
            separar_frontmatter('---\ndescription: "hola"\n---\nx\n')

    def test_lista_se_rechaza(self):
        with self.assertRaises(ValueError):
            separar_frontmatter("---\ntools: [Read, Grep]\n---\nx\n")

    def test_linea_sin_dos_puntos_se_rechaza(self):
        with self.assertRaises(ValueError):
            separar_frontmatter("---\nsolo-texto\n---\nx\n")


class ValidarSkill(unittest.TestCase):
    def campos(self, **kw):
        base = {"name": "modo-uno", "description": "Ejecutor: hace algo útil"}
        base.update(kw)
        return base

    def test_skill_correcta_no_da_errores(self):
        errores, avisos = validar_skill(Path("modo-uno"), self.campos())
        self.assertEqual(errores, [])
        self.assertEqual(avisos, [])

    def test_name_distinto_de_la_carpeta(self):
        errores, _ = validar_skill(Path("otra"), self.campos())
        self.assertTrue(any("no coincide con la carpeta" in e for e in errores))

    def test_name_con_mayusculas(self):
        errores, _ = validar_skill(Path("Modo-Uno"), self.campos(name="Modo-Uno"))
        self.assertTrue(any("minúsculas con guiones" in e for e in errores))

    def test_description_de_201_es_error(self):
        errores, _ = validar_skill(Path("modo-uno"), self.campos(description="x" * 201))
        self.assertTrue(any("description mide 201" in e for e in errores))

    def test_description_de_190_avisa_pero_no_falla(self):
        errores, avisos = validar_skill(Path("modo-uno"), self.campos(description="x" * 190))
        self.assertEqual(errores, [])
        self.assertTrue(any("10 caracteres de margen" in a for a in avisos))

    def test_description_holgada_no_avisa(self):
        errores, avisos = validar_skill(Path("modo-uno"), self.campos(description="x" * 150))
        self.assertEqual((errores, avisos), ([], []))


class BajarTitulos(unittest.TestCase):
    def test_quita_el_h1_y_baja_los_demas(self):
        salida = bajar_titulos("# Modo: algo\n\n## Uno\n\n### Dos\n")
        self.assertNotIn("# Modo", salida)
        self.assertIn("### Uno", salida)
        self.assertIn("#### Dos", salida)

    def test_no_toca_almohadillas_dentro_de_un_bloque(self):
        salida = bajar_titulos("## Uno\n\n```markdown\n# <Nombre>\n## Qué hace\n```\n")
        self.assertIn("### Uno", salida)
        self.assertIn("\n# <Nombre>", salida)
        self.assertIn("\n## Qué hace", salida)

    def test_respeta_bloques_con_tildes(self):
        salida = bajar_titulos("## Uno\n\n~~~text\n## adentro\n~~~\n")
        self.assertIn("\n## adentro", salida)


class Trampas(unittest.TestCase):
    NOTA = (
        "---\ntags: [lang/vba]\n---\n\n# VBA\n\n## Snippet\n\nalgo\n\n"
        "## Trampas\n\n> Cita de contexto que no viaja al paquete.\n\n"
        "- **Una trampa** — síntoma → solución.\n\n## Relacionado\n\n- x\n"
    )

    def test_extrae_solo_la_seccion(self):
        cuerpo = extraer_trampas(self.NOTA)
        self.assertIn("**Una trampa**", cuerpo)
        self.assertNotIn("Snippet", cuerpo)
        self.assertNotIn("Relacionado", cuerpo)

    def test_quita_la_cita_de_contexto(self):
        self.assertNotIn("Cita de contexto", extraer_trampas(self.NOTA))

    def test_nota_sin_seccion_devuelve_vacio(self):
        self.assertEqual(extraer_trampas("# Nota\n\n## Snippet\n\nx\n"), "")

    def test_recolecta_agrupando_por_carpeta_de_lenguaje(self):
        with TemporaryDirectory() as tmp:
            boveda = Path(tmp)
            for lenguaje in ("VBA", "Python"):
                d = boveda / lenguaje / "Referencia"
                d.mkdir(parents=True)
                (d / f"{lenguaje} - Referencia.md").write_text(self.NOTA, encoding="utf-8")
            salida = recolectar_trampas(boveda)
        self.assertIn("## Python", salida)
        self.assertIn("## VBA", salida)
        self.assertLess(salida.index("## Python"), salida.index("## VBA"))  # orden alfabético

    def test_boveda_sin_trampas_revienta(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp) / "VBA" / "Referencia"
            d.mkdir(parents=True)
            (d / "x.md").write_text("# Sin trampas\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                recolectar_trampas(Path(tmp))

    def test_ruta_inexistente_revienta(self):
        with self.assertRaises(ValueError):
            recolectar_trampas(Path("/no/existe/esta/boveda"))


class ZipReproducible(unittest.TestCase):
    def test_mismo_contenido_mismo_zip_aunque_cambie_la_mtime(self):
        import os
        with TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            skill = raiz / "modo-uno"
            skill.mkdir()
            (skill / "SKILL.md").write_text("contenido", encoding="utf-8")
            escribir_zip_reproducible(raiz / "a.zip", skill)
            os.utime(skill / "SKILL.md", (0, 0))
            escribir_zip_reproducible(raiz / "b.zip", skill)
            self.assertEqual((raiz / "a.zip").read_bytes(), (raiz / "b.zip").read_bytes())

    def test_las_rutas_van_bajo_la_carpeta_de_la_skill(self):
        with TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            skill = raiz / "modo-uno"
            skill.mkdir()
            (skill / "SKILL.md").write_text("x", encoding="utf-8")
            escribir_zip_reproducible(raiz / "a.zip", skill)
            with zipfile.ZipFile(raiz / "a.zip") as z:
                self.assertEqual(z.namelist(), ["modo-uno/SKILL.md"])


if __name__ == "__main__":
    unittest.main()


class RutasBoveda(unittest.TestCase):
    def test_va_despues_del_frontmatter(self):
        texto = con_rutas_boveda("---\nname: uno\n---\n\n# Modo\n")
        self.assertTrue(texto.startswith("---\nname: uno\n---\n\n> **En esta bóveda**"))
        campos, cuerpo = separar_frontmatter(texto)
        self.assertEqual(campos["name"], "uno")
        self.assertTrue(cuerpo.rstrip().endswith("# Modo"))

    def test_sin_frontmatter_va_al_inicio(self):
        self.assertTrue(con_rutas_boveda("# Nota\n").startswith(RUTAS_BOVEDA))

    def test_nombra_cada_archivo_del_paquete(self):
        for archivo in ["metodo-ejecutor.md", "principios-y-seguridad.md",
                        "trampas-conocidas.md", "contexto-proyecto.md"]:
            self.assertIn(f"`{archivo}`", RUTAS_BOVEDA)
