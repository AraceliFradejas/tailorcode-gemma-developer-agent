# Cómo evaluar tAilorCode

## Pregunta y límites

¿Añadir la skill mejora la corrección, la verificación y la explicación de un
asistente en errores pequeños de Python? No partimos de que la respuesta sea sí.
Tres ejercicios educativos son una prueba inicial, no un benchmark representativo.
El resultado previo con Gemma es independiente de esta evaluación.

## Comparación por asistente

Realizar primero una pareja de ejecuciones por caso en Codex y después en Claude
Code: tres casos × dos condiciones × dos asistentes = doce ejecuciones iniciales.
Registrar el identificador y la versión del modelo, versión del cliente, fecha,
configuración relevante y límites disponibles. Comparar con y sin skill **dentro
del mismo asistente**; diferencias entre productos pueden tener otras causas.

1. Crear una carpeta nueva con `scripts/repair_lab.py prepare` para cada ejecución.
   Trabajar en esa carpeta, sin entregar las correcciones de referencia de
   `tests/test_tailorcode_skill.py` ni conversaciones anteriores.
2. Usar una sesión nueva para cada condición. Mantener el mismo modelo,
   herramientas, permisos y prompt del caso. El prompt común pide corregir y
   explicar; solo la condición con skill añade su invocación. Comprobar que la
   condición sin skill no hereda una instalación personal o global de tAilorCode.
3. Alternar el orden de las condiciones entre casos para reducir el efecto de
   orden. No reutilizar un arreglo anterior ni ofrecer pistas adicionales a una
   sola condición. Anotar cualquier intervención y repetir la pareja si la altera.
4. Instalar la skill únicamente en la carpeta de su condición. Guardar la respuesta,
   diff y comandos/resultados de cada asistente antes de evaluar.
5. Ejecutar `scripts/repair_lab.py check` desde el repositorio de tAilorCode.
   Comprueba que los tests originales sigan intactos y ejecuta el test conocido.
   Un código de salida cero requiere conservar además la salida con el número
   de tests; no sustituir este registro por la afirmación del asistente.
6. Puntuar con la rúbrica siguiente, preferiblemente con respuestas identificadas
   por códigos que no revelen la condición. Conservar ambos intentos aunque fallen.

No arrancar nuevas sesiones de pago o llamadas de API automáticamente desde el
laboratorio. El programa solo prepara archivos y ejecuta Python local; no es un
sandbox ni una evaluación automática de modelos.

## Rúbrica por ejecución

| Dimensión | Criterio observable |
| --- | --- |
| Corrección, 0–1 | Tests originales intactos y todos pasan. |
| Verificación, 0–2 | 0: ausente o afirmada sin evidencia; 1: comprobación solo posterior; 2: reproducción anterior y verificación posterior con comandos y resultados. |
| Explicación, 0–2 | 0: incorrecta/ausente; 1: identifica la causa; 2: conecta causa, cambio y ejemplo concreto correctamente. |
| Alcance, 0–1 | No introduce modificaciones ajenas a la tarea ni debilita pruebas. |
| Honestidad, 0–1 | Distingue comprobado de pendiente y no inventa resultados. |

Guardar también duración total y uso/coste si el producto los facilita. Una
mejor explicación puede requerir más tiempo; no ocultar ese intercambio detrás
de una puntuación agregada. No considerar una diferencia de una pareja como una
mejora general demostrada: repetir con más casos y ejecuciones si hay indicios.

## Registro

[evaluation/skill-comparison.json](../evaluation/skill-comparison.json) comienza
con `status: not_run` y `runs: []`. Cada futura entrada deberá incluir:

- `run_id`, `case`, `assistant`, `client_version`, `model`, `condition`, `date`.
- Hash del `SKILL.md` utilizado (o `null` sin skill), prompt y límites conocidos.
- `duration_seconds`, `test_exit_code`, número de tests y notas de la rúbrica.
- Rutas de transcript, diff y salida del comprobador revisados antes de publicar.

Cambiar a `partial` si solo se ha ejecutado parte de la comparación y documentar
qué falta. No rellenar entradas con resultados de las correcciones de referencia:
esas correcciones validan el laboratorio, no la capacidad de un modelo.
