---
name: escribir-tests
description: 'Ejecutor: diseña y escribe pruebas (normales, negativas, de regresión de un bug) o un arnés manual si el lenguaje no tiene framework. Usar al pedir "prueba" o tests.'
---

# Modo: escribir tests

Objetivo: que un cambio se pueda comprobar sin fe. Diseñar los casos va directo; crear o editar
archivos de prueba sigue la regla de aprobación de `metodo-ejecutor.md`.

## 1. Qué probar primero

No todo merece el mismo esfuerzo. Prioriza los **flujos críticos**: los que tocan dinero o datos
financieros, datos personales, permisos, escrituras masivas o irreversibles, envíos o SAP.

Si son varios, entrega primero esta tabla y pregunta por dónde empezar:

| Flujo | Por qué es crítico | Tests que ya existen | Tests que faltan |
|---|---|---|---|

## 2. Diseñar los casos

Por cada función o flujo, antes de escribir código:

- **Normal**: la entrada típica.
- **Límite**: vacío, cero, uno, el máximo, el último elemento, fechas de fin de mes.
- **Negativo**: tipo inesperado, dato faltante, formato roto (decimales, ceros a la izquierda,
  codificación), entrada maliciosa si hay frontera de confianza.
- **Dependencias que fallan**: archivo bloqueado, API caída, ventana que no aparece, sesión SAP
  ausente.

Cada caso en una línea: `entrada → resultado esperado`. Si no sabes qué debe pasar en un caso,
**pregunta**: es una decisión de negocio, no de código.

## 3. Bug: primero el test que falla

Si hay un bug:

1. Escribe el test que lo reproduce.
2. Córrelo y **muestra que falla** por la razón esperada.
3. Corrige (modo `modificar-codigo`).
4. Muestra que ahora pasa, y que los demás siguen pasando.

Si el test pasa antes de corregir, no reproduce el bug: vuelve al paso 1.

## 4. Escribir los tests según el lenguaje

| Lenguaje | Herramienta | Nota |
|---|---|---|
| Python | `pytest` (o `unittest` si no se puede instalar nada) | `unittest` viene con Python |
| JavaScript / TypeScript | el framework que ya use el proyecto | no agregues otro |
| VBA | arnés manual: un `Sub` de pruebas que compara y escribe en una hoja o con `Debug.Print` | sin datos reales |
| AutoIt | arnés manual con `ConsoleWrite` y código de salida | nada que mueva ventanas reales |
| X++ | SysTest, si el entorno lo permite; si no, pruebas documentadas | |

Reglas:

- Un test prueba **una cosa** y su nombre dice cuál.
- Nada de datos reales: ni nombres, ni RFC, ni montos, ni rutas de la empresa.
- Lo externo (SAP, APIs, archivos de red, la webcam, el mouse) se **simula**. Nunca un test
  ejecuta contra sistemas reales.
- Instalar un framework de pruebas requiere aprobación. Si no se puede instalar nada, usa lo que
  trae el lenguaje o un arnés manual.

## 5. Pruebas manuales documentadas

Cuando no se puede automatizar, entrega una tabla que el usuario pueda seguir:

| # | Paso | Entrada | Resultado esperado | ¿Pasó? |
|---|---|---|---|---|

## 6. Cierre

Cierra con el formato **HECHO**: qué tests se agregaron, cómo correrlos (comando exacto), el
resultado **real** que obtuviste (o "no pude correrlos, aquí el comando") y qué quedó sin cubrir.
Nunca digas que pasan si no los corriste.
