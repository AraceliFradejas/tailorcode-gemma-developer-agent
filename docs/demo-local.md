# Demo local · Un cero también tiene valor

Esta primera aplicación Streamlit permite explorar el caso de precio cero que
Codex corrigió el 17 de octubre. Enseña el código antes y después, explica el
cambio y ejecuta las tres pruebas originales en carpetas temporales.

## Arrancar

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-demo.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1
```

Abre la URL local que muestra Streamlit, habitualmente http://127.0.0.1:8501.
Para detenerlo, pulsa Ctrl+C en la terminal. No se ha desplegado públicamente.

## Recorrido

1. Deja el precio en cero y la reserva en 20: observa la diferencia de resultados.
2. Cambia a −3 o activa el precio ausente: comprueba cuándo coinciden.
3. Abre “El cambio” y relaciona la condición `is None` con la regla del problema.
4. En “Las pruebas”, ejecuta el botón. El código original debe fallar por la
   aserción del cero y el corregido pasar las tres pruebas. Se muestra la salida
   de esta ejecución, no una animación ni un resultado simulado.
5. En “Lo que aprendes”, responde a la pregunta y contrasta la respuesta arriba.

## Alcance y procedencia

La interfaz muestra un caso guardado y una explicación editorial preparada.
No genera correcciones nuevas ni llama a una API. Los dos intentos de Codex,
con la skill presente y sin ella, produjeron el mismo parche: no se ha demostrado
una mejora de la skill. Véase `evaluation/skill-comparison.json`.

La interacción usa números y el estado ausente; no acepta código arbitrario.
El botón solo ejecuta archivos conocidos del repositorio mediante el laboratorio
local. El resultado respalda sus casos de prueba, no garantiza cualquier entrada.

`app.py` contiene la interfaz; `demo/engine.py` conecta los valores y el comprobador;
`demo/verified_price.py` conserva la corrección mostrada. `requirements-demo.txt`
separa las dependencias de la demo de la pila GPU histórica.

## Comprobación de esta entrega

Con Streamlit 1.66.0 pasaron 33 pruebas locales y las comprobaciones de interfaz
con AppTest: cero, negativo, None, ejecución real del botón y respuesta al
ejercicio. Chrome mostró la pantalla local correctamente. Las dependencias
pasaron `pip check`. Registro en `evaluation/demo-validation-2026-10-17.json`.
