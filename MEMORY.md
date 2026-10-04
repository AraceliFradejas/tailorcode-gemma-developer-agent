# Memoria de tAilorCode — actualizada el 4 de octubre de 2026

Este documento conserva el contexto del proyecto para retomarlo y para explicar
su desarrollo. Distingue lo que se ha comprobado de lo que solo está preparado.
Los documentos técnicos y el código se mantienen en inglés; esta memoria está
en español para facilitar el relato de Araceli.

## Qué queremos construir

tAilorCode es un agente para la competición Gemma 4 Developer Agent de Kaggle.
Su objetivo es recibir una incidencia de programación, investigar el repositorio,
proponer una modificación, ejecutar pruebas y entregar un parche revisable.
Araceli dirige y es autora del proyecto, inspirado en su trabajo anterior con KelceTS.

El objetivo inmediato es más pequeño: ejecutar **una tarea pública** con el agente
y comprobar el resultado. Todavía no hemos ejecutado Gemma ni medido su capacidad
para resolver tareas. Preparar un ZIP no equivale a ejecutar al agente.

## Qué ocurrió con Kaggle

1. Se revisó el notebook anterior, que dependía de entradas externas para preparar
   el envío. Se preparó otro autocontenido, con los tres YAML y los prompts incluidos.
2. Araceli lo ejecutó y obtuvo `/kaggle/working/submission.zip`. En aquella versión
   el ZIP medía 1.683 bytes. Después se cambió el empaquetado para que fuese
   reproducible: es normal que cambien el tamaño y el hash del ZIP, aunque los YAML
   del agente sigan siendo los mismos.
3. Hubo un bloqueo previo por la configuración de Internet. Ese mensaje era distinto
   del fallo posterior de un envío ya realizado.
4. La inspección de Kaggle mostró cuatro envíos con `Kaggle Error`. El más reciente
   observado era Version 11, a las 19:18:58 de Madrid, con el ZIP en Uploaded Files.
   El mensaje describía un error de sistema y recomendaba contactar con soporte.
5. Se preparó la consulta a soporte y Araceli confirmó que la había enviado.
   Soporte respondió el 28 de septiembre: recomendó preguntar en el foro de la
   competición, sin aportar diagnóstico ni confirmar una incidencia de infraestructura.
   No se conoce la causa exacta. No se ha hecho otro envío durante esta continuación.

Referencia: [checkpoint del envío](docs/progress-2026-09-27.md).

## Decisión del 4 de octubre: continuar en Colab

- Araceli publicará personalmente la consulta preparada en el
  [foro de la competición](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion).
  No se ha confirmado la publicación ni registrado todavía un enlace al tema.
- El intento de publicación asistida se abandonó porque no se completó el acceso
  en la pestaña compartida. No se publicó ningún mensaje.
- Se continuará desarrollando y evaluando tAilorCode en Colab; no es necesario
  instalar Linux en el Mac. El entorno de Colab debe prepararse y comprobarse.
- Kaggle queda pendiente: se retomará el envío cuando se resuelva el problema o
  haya orientación concreta que justifique un nuevo intento.
- Se documentarán en GitHub los resultados y limitaciones, sin subir credenciales,
  datos de competición, pesos del modelo ni enlaces privados de Drive.
- Elegir Colab no autoriza por sí solo consumir créditos. Antes de conectar una
  máquina hay que revisar el consumo; antes de ejecutar Gemma, confirmar GPU,
  memoria, entorno e inputs, y autorizar la prueba de una tarea.

Las comprobaciones locales del 4 de octubre pasaron: 10 tests, ejecución completa
del notebook de empaquetado dos veces y comprobación de frescura. El preflight
local encontró las tres tareas y sus snapshots, pero no `swegemma` ni runtime
NVIDIA. No se ejecutó Gemma ni se obtuvo puntuación. El subset y su informe se
prepararon en una carpeta temporal fuera del repositorio; no son resultados del agente.

Araceli creó su copia privada en Colab y autorizó únicamente una comprobación CPU
de unos cinco minutos. La salida compartida mostró Python 3.12.13, Linux x86_64,
210,5 GiB de disco libre, kagglehub 1.0.0, kaggle 2.0.0, torch 2.10.0+cpu,
transformers 5.0.0 y vLLM ausente. No se comprobó acceso autenticado al modelo,
no se instalaron las dependencias de evaluación ni se ejecutó Gemma.
A las 13:38 del 4 de octubre confirmó que había guardado y desconectado.
No se verificó independientemente la eliminación del runtime ni el panel de
sesiones activas. La autorización no se extiende a otra conexión o instalación.

Después Araceli confirmó que no había sesiones activas y autorizó por separado
otra comprobación CPU de hasta unos cinco minutos. A las 13:56 compartió la
descarga correcta de `config.json` (18.711 bytes) de la versión 2 mediante
KaggleHub, solicitando solo ese archivo. Su configuración declara
`Gemma4ForConditionalGeneration`, `compressed-tensors`, estado `compressed`
y pesos enteros de 4 bits con grupos de 32 y cuantización simétrica.
Esto confirma acceso a ese archivo desde la sesión, no la descarga de todos
los pesos ni compatibilidad de ejecución. No se ejecutó el modelo.
Araceli confirmó la desconexión a las 16:09, antes de la siguiente comprobación.

A continuación autorizó otra comprobación CPU de hasta cinco minutos para
descargar solo los tres paquetes oficiales. A las 16:12 compartió resultados
correctos desde el wheelhouse versión 25: `adk-submission 0.2.11` (62.404 bytes),
`adk-eval-core 0.1.0` (89.306 bytes) y `swegemma 0.2.7` (111.548 bytes).
Los tres hashes SHA256 coinciden con el manifiesto registrado. No se instaló
ni ejecutó ninguno. Las descargas son temporales y no persisten al eliminar
la máquina; guardar sus salidas no conserva los archivos.
Falta confirmar el cierre de esta última sesión.

A las 16:18, descargar `tasks.jsonl` falló con `UnauthenticatedError`: la sesión
del navegador no autenticaba Colab. Se configuró el secreto `KAGGLE_API_TOKEN`
con acceso al notebook, sin introducir su valor en el código ni en GitHub.
KaggleHub 1.0.0 lo reconoce automáticamente; esta vía usa token API, no OAuth.
Tras autorizar otra sesión CPU de hasta cinco minutos, Araceli compartió a las
16:30 la autenticación correcta y la descarga de `tasks.jsonl` (1.984.455 bytes,
129 registros). La tarea `fastapi_14786`, el repositorio `fastapi/fastapi` y el
commit `eacbce24c9d299c6a28110d9fc8ac50f53cddb08` coincidieron con el baseline.
No se descargaron snapshots ni pesos, ni se ejecutó la tarea.
Falta confirmar el cierre de esta sesión; no prolongar su autorización.

Siguiente paso: preparar los inputs restantes de la tarea y planificar la
instalación aislada y conservación de logs antes de autorizar otro consumo.
Los detalles están en [la preparación documentada](docs/colab-setup.md).

## Qué hemos comprobado realmente

Actualización de la tarde del 4 de octubre: la primera instalación falló porque
el Python de Colab no tenía `ensurepip`. Se corrigió el instalador para usar
`virtualenv` cuando falte ese módulo, con cinco pruebas de regresión locales.
El notebook aportado por Araceli registra después código de salida 0,
`No broken requirements found.`, importaciones correctas y CUDA no disponible
en CPU. No se cargó Gemma ni se validó GPU.

Araceli pidió ordenar su copia, que acumulaba celdas al principio. La plantilla
de GitHub se reorganizó a partir de su archivo: explicaciones Markdown por etapa,
resultados históricos útiles identificados como tales, instalación después de
los preparativos y Python aislado para preflight/evaluación. Las autorizaciones
siguen desactivadas y falta preparar inputs completos. El archivo original
descargado no se modificó. Guardar el notebook no conserva el entorno temporal.

- `agents/baseline/` es la fuente de la configuración: agente principal, analista
  de código de solo lectura y presupuesto de evaluación. Ambos usan
  `gemma-4-31b-it-qat-w4a16-ct`.
- `scripts/build_submission.py` genera el notebook autocontenido y detecta si
  está desactualizado respecto a los YAML.
- El notebook de empaquetado se ejecutó dos veces en directorios temporales;
  se verificaron el contenido del ZIP y su reproducibilidad.
- Pasaron 10 pruebas automatizadas locales, que incluyen comprobaciones de
  configuración, selección de tareas, compatibilidad básica y bloqueos de ejecución.
  Son pruebas del proyecto, **no diez tareas resueltas por Gemma**.
- El compilador oficial `adk-submission 0.2.11`, con `google-adk 1.36.1`, construyó
  los objetos del agente y del subagente. Se utilizaron herramientas inertes:
  no se hicieron llamadas al modelo ni se resolvieron incidencias.
- En Colab se ejecutaron correctamente las comprobaciones de desarrollo con CPU.
  Se guardaron el notebook y sus salidas en una copia privada de Drive.
- Se localizaron las tres tareas públicas y sus snapshots en el Mac:
  `fastapi_14786`, `rich_4077` y `requests_6592`.

El informe del compilador está en
[docs/compiler-check-2026-09-27.md](docs/compiler-check-2026-09-27.md).
No se ha comprobado en esta sesión el resultado remoto de GitHub Actions, aunque
el workflow está guardado y las comprobaciones locales han pasado.

## Qué pasó en Colab y por qué aparecía un error

La primera sesión tenía Python 3.13, unos 12,7 GB de RAM y no tenía disponible
la instalación completa para evaluar con Gemma. Servía para los controles de
desarrollo, pero no demostraba que el agente pudiera ejecutarse.

Se crearon dos cuadernos privados en Drive:

- `tAilorCode - Development Checks - 2026-09-27.ipynb`: controles ya ejecutados.
- `tAilorCode - One Public Task - 2026-09-27.ipynb`: prueba de una tarea preparada,
  todavía sin ejecutar con Gemma.

El segundo cuaderno conserva `RUNTIME_COST_APPROVED = False` y `RUN_AGENT = False`.
Araceli ejecutó la primera celda y apareció un `RuntimeError` en inglés: era el
bloqueo deliberado antes de continuar, no un fallo de Gemma. La forma de mostrarlo
resultó confusa y se explicó. **No quitar ese bloqueo interpretando el mensaje
como un defecto del modelo o como autorización de consumo.**

Ejecutar esa celda sí conectó una máquina de Colab. Se terminó esa sesión y se
verificó «No hay sesiones activas». La sesión anterior de desarrollo también se
había terminado. Esto refleja el último estado observado, no una garantía sobre
sesiones que se abran más adelante.

## Costes y forma de trabajar acordada

- Araceli pidió avisar **antes de generar cargos o consumir créditos de pago**.
  No interpretar «continuamos» como autorización de un gasto todavía no explicado.
- La cuenta inspeccionada consumía unidades también con CPU. Un notebook bloqueado
  no detiene la facturación de una máquina conectada.
- Antes de conectar recursos, explicar qué se va a ejecutar, el consumo conocido,
  la incertidumbre y el límite de la prueba. Pedir la autorización correspondiente.
- Parar el servidor del modelo no desconecta Colab: hay que terminar también
  el entorno y verificar su estado. Guardar primero los archivos de resultados.
- Explicar el avance en español sencillo y a un ritmo que Araceli pueda seguir.
  Los detalles técnicos deben servir para entender las decisiones.
- Araceli indicó que podía estar hasta las 20:15 en esta sesión; es una restricción
  de esa fecha, no un horario permanente.

No se ha activado ninguna GPU, descargado el modelo ni creado recursos de Google
Cloud. No se ha contratado ningún plan nuevo.

## Lo que estamos preparando y por qué

El ejemplo oficial de Kaggle utiliza `sandbox='subprocess'`, que permite evaluar
sin un servicio Docker. La falta de Docker en el Mac no es por sí sola un bloqueo
de esta alternativa; siguen faltando el entorno Linux/GPU y sus dependencias.

Se revisaron las versiones anteriores de Colab sin conectar recursos. Primero
se identificó 2026.07 por incluir Python 3.12. Al revisar vLLM 0.19.1 se encontró
que exige PyTorch 2.10.0, mientras que 2026.07 documenta PyTorch 2.11.0.
Por eso la candidata actual es **2026.04**, que documenta Python 3.12.13 y
PyTorch 2.10.0. La selección no se guardó ni se inició una máquina.

Esto todavía no prueba compatibilidad completa: faltan resolver las dependencias,
comprobar CUDA y conocer la memoria real disponible en la GPU.

Se instaló Kaggle CLI 2.2.4 en un entorno temporal separado del Mac, en
`/tmp/tailorcode-kaggle-cli`. Permitió listar públicamente el wheelhouse oficial
y descargar dos paquetes pequeños: `swegemma` y `adk-eval-core`. El paquete
`adk-submission` ya se había descargado desde el navegador. Se inspeccionaron
sus requisitos y se registraron los hashes de los tres archivos.

La consulta de los archivos del modelo por CLI exigió autenticación y se detuvo.
No había credenciales locales configuradas. La sesión de Kaggle del navegador
no equivale a una sesión autenticada de la terminal. No se generaron tokens.

La ficha del modelo requerido, versión 2, muestra unos **23,3 GB**. Es tamaño
de archivos: no garantiza que baste una GPU con esa cantidad de memoria.

Se preparó `scripts/install_gpu_environment.py` para crear un entorno aislado,
verificar los tres paquetes oficiales e instalar las dependencias seleccionadas.
Sus comprobaciones locales de hashes y bloqueo han pasado. **La instalación
Linux/Colab no se ha realizado:** aún puede revelar conflictos.

La prueba de una tarea usa un presupuesto de agente de 5 minutos, frente a los
30 minutos del baseline. Es una prueba diagnóstica. La preparación, carga del
modelo y verificación añaden tiempo; esos 5 minutos no son un límite de coste total.

## Archivos para retomar

| Archivo | Para qué sirve |
| --- | --- |
| `agents/baseline/` | Fuente de la configuración del agente |
| `deliverables/tailorcode-submit-ready.ipynb` | Crear el ZIP para Kaggle |
| `notebooks/tailorcode-colab-checks.ipynb` | Controles de desarrollo con CPU |
| `notebooks/tailorcode-public-smoke.ipynb` | Plantilla de prueba de una tarea |
| `scripts/check_smoke_environment.py` | Detectar requisitos básicos ausentes |
| `scripts/run_public_smoke.py` | Ejecutar una tarea cuando el entorno esté listo |
| `scripts/install_gpu_environment.py` | Instalador candidato, con activación explícita |
| `requirements-gpu.txt` | Versiones principales propuestas para GPU |
| `evaluation/official-harness-wheels.json` | Procedencia, hashes y requisitos inspeccionados |
| `docs/colab-setup.md` | Pasos técnicos y limitaciones de la preparación |

Los entornos y archivos de `/tmp` son temporales y pueden desaparecer. Los
scripts, informes y documentación están respaldados en GitHub. Los enlaces
privados de Drive y las credenciales no se publican en este repositorio.

## Próximos pasos concretos

1. Autorizar y completar el acceso de Kaggle CLI si se usa esa vía para obtener
   los archivos; comprobar el acceso antes de reservar una GPU.
2. Acordar cualquier consumo de Colab antes de conectar la sesión de preparación.
3. Resolver e instalar el entorno candidato, guardar las versiones y comprobar
   importaciones y dependencias. La instalación en una máquina no persiste si
   se elimina su entorno temporal.
4. Preparar los datos y el modelo en la máquina de prueba. Todavía no están en
   Colab. En el notebook habrá que indicar las rutas reales y usar el Python del
   entorno aislado; la copia de Drive sigue siendo una plantilla.
5. Verificar GPU, memoria y consumo; autorizar por separado la ejecución.
6. Ejecutar una tarea, guardar parche, logs, tiempo y resultado de las pruebas.
   Guardar el notebook en Drive no conserva por sí solo esos archivos temporales.
7. Terminar los recursos y verificar que no quedan sesiones activas.
8. Registrar el enlace del tema y cualquier respuesta del foro cuando estén
   disponibles. La respuesta de soporte ya está incorporada; no atribuir todavía
   una causa al error de Kaggle.

## Cómo contarlo después

> Partí de un problema al enviar mi agente a Kaggle. Primero hice reproducible
> el paquete de entrega y separé ese paso de la evaluación real. Después validé
> la configuración con el compilador oficial y ejecuté controles de desarrollo
> en Colab. Al preparar la primera prueba con Gemma, detecté diferencias de
> versiones entre Colab y las dependencias de la competición. Por eso preparé
> una instalación aislada y una prueba de una sola tarea antes de consumir GPU.
> A este punto todavía no tengo una puntuación ni una tarea resuelta: tengo una
> base comprobada, documentación y un plan de evaluación reproducible.

No afirmar todavía que tAilorCode ha mejorado su precisión, resuelto las tareas
o superado el error de Kaggle. Esas conclusiones requieren resultados que aún faltan.

## Preservación del trabajo

Había cambios y borrados anteriores en el árbol de trabajo, incluida `.gitignore`.
No se han restaurado ni incluido indiscriminadamente. Añadir a Git únicamente
los archivos pertinentes; no subir los datos públicos descargados, entornos,
ZIP generados ni cambios ajenos. Mantener esta memoria actualizada cuando cambie
el estado de instalación, evaluación o soporte.
