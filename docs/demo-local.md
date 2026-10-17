# Demo local · Un cero también tiene valor

Esta aplicación Streamlit permite elegir tres ejemplos: el precio cero corregido
por Codex y dos cestas que se mezclan por compartir una lista y un plan de riego que
excluye el último día. Los dos últimos usan correcciones de referencia preparadas,
sin atribuirlas a un modelo. Ambos muestran
el código, la explicación y tres pruebas reales en carpetas temporales.

## Arrancar

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-demo.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1
```

Abre la URL local que muestra Streamlit, habitualmente http://127.0.0.1:8501.
Para detenerlo, pulsa Ctrl+C en la terminal. La versión pública está en
https://tailorcode-corrige-y-aprende.streamlit.app/.

## Recorrido

1. Elige “Producto gratuito · 0 €”: la pantalla muestra lo esperado, el cobro
   incorrecto de 20 € y el cobro corregido de 0 €.
2. Compara las otras dos situaciones: precio registrado y precio sin registrar.
3. Lee “Entender el ejemplo” y responde cuánto debería cobrarse por algo gratis.
4. En “Comprobar el arreglo”, pulsa el botón: se ejecutan las tres pruebas reales.
   Los resultados se explican en lenguaje sencillo; la salida técnica es opcional.
5. Abre “Ver el código” solo si quieres relacionar la explicación con Python.

El 17 de octubre se simplificó el recorrido tras indicar Araceli que no entendía
la prueba. La caja de una tienda ficticia sustituye a las entradas técnicas;
se mantiene el mismo código y las mismas pruebas. Los tres escenarios, ambas
respuestas del ejercicio y el botón pasaron las comprobaciones de interfaz.

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

## Segundo ejemplo: dos cestas que se mezclan

El selector de la parte superior permite abrir “Dos cestas que se mezclan”.
Ana y Luis añaden artículos a cestas nuevas. Antes, ambas listas comparten los
artículos; después, cada una conserva solo su compra. Cambiar los artículos inicia
una simulación nueva para no arrastrar el estado entre visitantes o ejecuciones.

El botón comprueba independencia de las listas nuevas y conservación de una lista
existente, incluida una vacía. La salida técnica y el código son opcionales. Esta
corrección se etiqueta como referencia: no se presenta como resultado de Claude.

## Si aparece un ImportError tras actualizar el código

El 17 de octubre el servidor iniciado antes de añadir las cestas conservó la
versión anterior de `demo.engine` y no encontró `basket_trace`. El fichero sí
contenía la función. Se detuvo y reinició Streamlit, y se observó la pantalla
real de las cestas en Chrome sin ese error. Las comprobaciones anteriores en
procesos nuevos no habían detectado el estado del servidor que seguía abierto.

Tras cambios estructurales de módulos, detener el servidor con Ctrl+C y volver
a ejecutar el comando de arranque. Recargar solo el navegador puede no bastar
para renovar los módulos que el servidor Python ya tiene importados.

## Tercer ejemplo: el último día se queda fuera

Selecciona “El último día se queda fuera”. El calendario ficticio riega los días
pares, incluyendo ambos extremos del periodo. Del 1 al 4 deberían regarse el
2 y el 4: antes falta el 4 y después aparece. Los días impares se muestran como
sin riego previsto, no como errores.

También se puede elegir solo el día 2 o del 1 al 5 (caso que ya funcionaba).
El botón ejecuta cuatro pruebas originales; el código y los detalles técnicos
son opcionales. Es una corrección de referencia, no un resultado de Claude.
Se verificaron los tres escenarios, el botón, el ejercicio y el cambio entre
las tres pantallas. Pasaron 37 tests locales. Se reinició el servidor para
cargar los módulos nuevos, como requiere la incidencia documentada arriba.

## Selección visible y descarga de la skill

Los tres casos se eligen mediante opciones siempre visibles dentro de un panel
destacado. La barra lateral incluye descargas ZIP reales para Codex y Claude
Code. Cada ZIP contiene solo la carpeta `tailorcode` con instrucciones y
referencias; Codex añade sus metadatos de interfaz. No incluye sesiones ni logs.
Al descomprimir, copiar esa carpeta a `.agents/skills/` o `.claude/skills/`
dentro del proyecto elegido. La interfaz muestra los pasos de instalación.
Se comprobaron ambos archivos y la presencia de las descargas en los tres casos.
