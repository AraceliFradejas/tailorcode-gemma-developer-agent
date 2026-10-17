# tAilorCode · Corrige y aprende

**Una skill para corregir pequeños errores de Python y entender por qué funciona
el arreglo.** Proyecto de portfolio creado y dirigido por **Araceli Fradejas Muñoz**.

El usuario abre su proyecto en Codex o Claude Code, describe un fallo y recibe
una corrección revisable, una explicación y evidencia de las comprobaciones.
La primera versión está preparada para instalarse en ambos asistentes; hay una primera prueba guiada en Codex con el arreglo comprobado
independientemente. Falta completar las pruebas de compatibilidad y comparación.

## Demo local interactiva

La demo permite explorar tres casos: un producto gratis que se cobra a 20 €,
dos cestas que mezclan sus artículos y un calendario que excluye el último día. Incluye explicación, cambio y pruebas
reales. El precio usa un resultado guardado de Codex; las cestas y el calendario, correcciones
de referencia preparadas. No genera correcciones nuevas ni hace llamadas de IA.

```bash
python3 -m pip install -r requirements-demo.txt
python3 -m streamlit run app.py --server.address 127.0.0.1
```

[Guía de la demo y sus límites](docs/demo-local.md).

## Por qué cambió el proyecto

Empecé desarrollando un agente para el reto Gemma de Kaggle. El 16 de octubre de
2026 logré ejecutar Gemma en una A100 y resolver una tarea pública de FastAPI.
Sin embargo, preparar el entorno consumió mucho más esfuerzo que el resultado
visible, y decidí no continuar hacia un envío al reto. Mi objetivo era aprender
y crear algo comprensible y útil para mi portfolio.

Por eso tAilorCode evoluciona hacia una herramienta reutilizable que combina
**corregir, comprobar y explicar**. Conserva lo aprendido del agente, pero utiliza
el modelo y las herramientas del asistente donde se instala. No incluye Gemma
ni necesita Kaggle o una GPU para funcionar; el uso del asistente está sujeto a
su propia cuenta, disponibilidad y límites.

La decisión, sus motivos y el plan están en la
[memoria del cambio de enfoque](docs/cambio-de-enfoque-2026-10-16.md).

## Cómo interactúa el usuario

En Codex:

> Usa $tailorcode para corregir este error de Python. Explícame la causa, muestra
> el cambio y comprueba el resultado con las pruebas disponibles.

En Claude Code:

> /tailorcode Corrige este error de Python y explícame cómo comprobar el arreglo.

La skill inspecciona el código y busca una reproducción, aplica una corrección
acotada cuando se ha solicitado, ejecuta las comprobaciones pertinentes y explica
el resultado. También respeta peticiones de diagnóstico sin modificar archivos.
Distingue **verificado con pruebas**, **solo sintaxis**, **sin verificar** y
**sin resolver**. Una propuesta plausible no se presenta como una corrección probada.

## Probar el primer ejercicio

Requiere Python 3.10 o superior. Desde la raíz de este repositorio:

```bash
python3 scripts/repair_lab.py prepare --case zero-price --workspace /tmp/tailorcode-zero-price
python3 scripts/install_tailorcode_skill.py --target codex --project /tmp/tailorcode-zero-price
```

Para Claude Code, sustituye `--target codex` por `--target claude`. Después abre
**esa carpeta** en el asistente; inicia una sesión nueva si no aparece la skill.
Lee `prompt.md` y envía su contenido junto con la invocación anterior. El
instalador conserva cualquier instalación existente: no la sobrescribe.

Después de la reparación, desde este repositorio:

```bash
python3 scripts/repair_lab.py check --case zero-price --workspace /tmp/tailorcode-zero-price
```

Antes de reparar, ese comando debe fallar por una aserción. Después, permitirá
comprobar si se cumplen los requisitos. Ejecuta Python local de la carpeta:
**no es un sandbox para código desconocido**. Estos ejemplos son ejercicios
propios y no descargan datos ni llaman a una API.

El instalador copia la fuente única de [la skill](skills/tailorcode/SKILL.md) en
`.agents/skills/tailorcode/` para Codex o `.claude/skills/tailorcode/` para Claude
Code, dentro del proyecto elegido. No modifica la configuración global.
Las ubicaciones se basan en la documentación oficial de
[Codex](https://learn.chatgpt.com/docs/build-skills) y
[Claude Code](https://code.claude.com/docs/en/skills), consultada el 16 de octubre.

La [guía de la primera demo](docs/skill-quickstart.md) desarrolla este recorrido
paso a paso, desde el fallo inicial hasta su comprobación independiente.

La [guía de Claude Code](docs/claude-quickstart.md) explica cómo probar la misma
skill en ese asistente. Instalación comprobada; ejecución en Claude pendiente.

## Tres casos reproducibles

| Caso | Comportamiento que debe conservar el arreglo |
| --- | --- |
| `independent-lists` | Llamadas sin lista crean listas independientes; una lista proporcionada mantiene su identidad. |
| `zero-price` | Cero es un precio válido; solo `None` activa el valor de reserva. |
| `inclusive-range` | Los pares incluyen ambos extremos; un intervalo invertido está vacío. |

La [validación local registrada](evaluation/skill-lab-validation-2026-10-16.json)
conserva el hash de la skill y los resultados del laboratorio sin invocar modelos.

Los casos están en [examples/repair-lab](examples/repair-lab/). El mismo comando
`prepare` sirve para cualquiera de ellos, usando una carpeta nueva. Los tests
originales deben conservarse para que el comprobador acepte el resultado.

## Qué está comprobado y qué falta

| Elemento | Estado |
| --- | --- |
| Skill y metadatos | Creados y validados estructuralmente. |
| Instalación para ambos asistentes | Copias verificadas en carpetas temporales; no sobrescriben instalaciones. |
| Tres ejercicios | Fallan antes y pasan con correcciones de referencia; esto comprueba el laboratorio. |
| Primera prueba guiada en Codex | Caso `zero-price` corregido; tres tests comprobados independientemente. Invocación comunicada por la usuaria, sin traza de herramientas. |
| Claude Code y descubrimiento automático | Pendientes de comprobar. |
| Comparación exploratoria con/sin skill | `zero-price`: mismo parche y tres tests pasan en ambas condiciones; sin ventaja funcional observada. Configuración y activación no confirmadas con trazas. [Registro parcial](evaluation/skill-comparison.json). |
| Demo local con Streamlit | Tres ejemplos interactivos: precio cero, cestas compartidas y último día excluido. Pruebas reales; sin generación nueva ni despliegue público. |

Validación local del proyecto:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 scripts/build_submission.py --check
python3 scripts/check_submission_notebook.py
```

Las dos últimas comprobaciones conservan la reproducibilidad del trabajo previo
de Kaggle; no ejecutan modelos ni prueban la nueva skill.

La [primera prueba guiada del 17 de octubre](evaluation/skill-guided-demo-2026-10-17/result.json)
conserva el parche y la verificación independiente. No es una comparación con/sin skill.

## Evidencia de la etapa anterior

El resultado real de Gemma fue `resolved: true` para `fastapi_14786`, con código
de salida de pruebas 0, seis llamadas registradas y 43,65 segundos de evaluación.
Es una tarea pública de desarrollo, no una puntuación de Kaggle ni una validación
de esta nueva skill. La GPU quedó desconectada.

- [Resultado estructurado](evaluation/public-smoke-2026-10-16.json).
- [Memoria técnica de la sesión](docs/memoria-2026-10-16.md).
- [Colab limpio conservado](notebooks/tailorcode-colab-limpio.ipynb).
- [Historia de Kaggle y Gemma](docs/historia-kaggle.md).
- [Memoria general para retomar el proyecto](MEMORY.md).

Las capturas originales y los diagnósticos con enlaces privados se conservan
localmente y están excluidos de Git.

## Autoría

**Araceli Fradejas Muñoz** · [GitHub](https://github.com/AraceliFradejas)

Proyecto desarrollado con asistencia de IA. El diseño del flujo, los scripts,
las pruebas y la evaluación constituyen el trabajo del proyecto; no se ha
entrenado un modelo propio ni demostrado una mejora general sobre otros agentes.
