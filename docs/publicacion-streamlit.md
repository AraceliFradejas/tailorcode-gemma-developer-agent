# Publicación de la demo en Streamlit Community Cloud

## Estado

Preparación del repositorio completada el 17 de octubre de 2026. Despliegue
pendiente de completar en el panel de Streamlit y de verificar la URL resultante.
No confundir la dirección local `127.0.0.1:8501` con una URL pública.

## Configuración del despliegue

- Repositorio: `AraceliFradejas/tailorcode-gemma-developer-agent`.
- Rama: `main`.
- Archivo principal: `app.py`.
- Python: **3.12**, como el entorno local comprobado.
- Subdominio propuesto: `tailorcode-corrige-y-aprende` (disponibilidad pendiente).
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
