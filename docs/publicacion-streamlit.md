# Publicación de la demo en Streamlit Community Cloud

## Estado

Publicada y verificada el **17 de octubre de 2026**.

**URL pública:** https://tailorcode-corrige-y-aprende.streamlit.app/

El despliegue inicial utilizó el commit `2239242`, con Python 3.12. La aplicación
local `127.0.0.1:8501` es independiente de esta dirección pública.

## Configuración del despliegue

- Repositorio: `AraceliFradejas/tailorcode-gemma-developer-agent`.
- Rama: `main`.
- Archivo principal: `app.py`.
- Python: **3.12**, como el entorno local comprobado.
- Subdominio propuesto: `tailorcode-corrige-y-aprende` (asignado y funcionando).
- Secretos: ninguno; esta demo no llama a APIs ni descarga modelos.

El `requirements.txt` de la raíz incluye solo `requirements-demo.txt`, que fija
Streamlit 1.66.0. No utiliza `requirements-gpu.txt`. El archivo
`.streamlit/config.toml` configura el tema oscuro, el acento violeta y la
telemetría de Streamlit desactivada. Los secretos locales quedan excluidos de Git.

La [documentación oficial de despliegue](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
explica cómo seleccionar repositorio, rama, archivo y versión de Python. El
[archivo de dependencias reconocido](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
es `requirements.txt`; `requirements-demo.txt` por sí solo no es el nombre
que detecta automáticamente el servicio.

## Comprobación después del despliegue

Verificar desde la URL pública las tres pantallas y los resultados esperados:
precio cero (tres tests), cestas (tres tests) y calendario (cuatro tests).
Descargar ambos ZIP, comprobar su contenido y revisar el footer y el diseño
en una pantalla estrecha. Guardar la URL real en el README solo cuando esté
comprobada. Conservar capturas revisadas para no publicar elementos de la cuenta.

## Presentación acordada

“Disponible para descargar e instalar en Codex y Claude Code.”

En la documentación se mantiene: prueba de uso realizada en Codex; validación
en Claude Code pendiente. Los ejemplos visuales están preparados, no generan
respuestas nuevas de IA. No se afirma una mejora demostrada sobre Codex.

## Resultado de las comprobaciones públicas

Se abrió la aplicación real en Chrome desde su URL de Streamlit y se ejecutaron
los tres botones: el precio pasó 3 tests; las cestas, 3; y el calendario, 4.
También se abrió la URL en una ventana nueva de incógnito: la aplicación se
mostró sin iniciar sesión.

Cada pantalla mostró primero el fallo original y después las pruebas aprobadas
de su corrección. No son nuevas evaluaciones de modelos.

Ambos ZIP se descargaron desde la aplicación y se inspeccionaron: Codex contiene
`SKILL.md`, la referencia y sus metadatos de interfaz; Claude Code contiene las
instrucciones y la referencia portable. No se incluyeron sesiones ni credenciales.

Las cuatro capturas se tomaron mediante CUA de la aplicación publicada, con las
barras del navegador ocultas. No se editaron ni generaron. Se revisaron las
imágenes antes de publicarlas. El footer muestra la firma y los enlaces sociales.

- [Caso del precio](images/demo/01-precio.png).
- [Caso de las cestas](images/demo/02-cestas.png).
- [Caso del calendario](images/demo/03-calendario.png).
- [Evidencia de pruebas y footer](images/demo/04-pruebas-cestas.png).

El [registro estructurado](../evaluation/publication-2026-10-17.json) conserva
resultados y hashes de las capturas. La validación de la skill dentro de Claude
Code sigue pendiente; la publicación de su paquete no cambia ese estado.
