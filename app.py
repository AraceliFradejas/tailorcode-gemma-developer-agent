"""A beginner-friendly replay of the recorded Codex price correction."""
import streamlit as st
from demo.engine import compare, patch, run_checks, sources
from demo.skill_downloads import render_skill_downloads

st.set_page_config(page_title='tAilorCode · Corrige y aprende', page_icon='🧵', layout='wide')
st.markdown("""
<style>
.st-key-case_selector {
    background: color-mix(in srgb, #8b5cf6 13%, var(--background-color, #0e1117));
    border: 2px solid #8b5cf6;
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.5rem;
}
.st-key-case_selector [role="radiogroup"] {
    gap: 1rem 2rem;
    flex-wrap: wrap;
}
.st-key-case_selector [data-testid="stRadio"] label p {
    font-size: 1.1rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)
with st.container(border=True, key='case_selector'):
    st.subheader('Empieza aquí: elige un caso')
    st.caption('Tres situaciones cotidianas. Pulsa una opción para explorar su fallo y su solución.')
    labels = {
        'Un producto gratis': '🏷️  1. Un producto gratis',
        'Dos cestas que se mezclan': '🛒  2. Dos cestas que se mezclan',
        'El último día se queda fuera': '💧  3. El último día se queda fuera',
    }
    example = st.radio('Elige un ejemplo', list(labels), format_func=labels.get,
                       horizontal=True, label_visibility='collapsed', key='selected_case')
if example == 'Dos cestas que se mezclan':
    from demo.basket_view import render_baskets
    render_baskets()
    st.stop()

if example == 'El último día se queda fuera':
    from demo.range_view import render_range
    render_range()
    st.stop()

st.markdown('**tAilorCode · Corrige y aprende**')
st.title('Es gratis. ¿Por qué me cobran 20 €?')
st.write('Imagina que estás probando la caja de una tienda. Un producto está marcado como gratuito, '
         'pero al pasar por caja aparece un cobro de 20 €. Vamos a entender y comprobar el arreglo.')
st.caption('No necesitas saber Python para seguir el ejemplo. Corrección real guardada de Codex; sin generación nueva de IA.')

with st.sidebar:
    st.header('Tu recorrido')
    st.write('1. Elige una situación.\n\n2. Compara lo que cobra la caja.\n\n3. Comprueba el arreglo.')
    st.divider()
    st.write('Proyecto de Araceli Fradejas Muñoz')
    render_skill_downloads()
    st.markdown('[Ver proyecto en GitHub](https://github.com/AraceliFradejas/tailorcode-gemma-developer-agent)')

st.subheader('1. Elige qué producto pasa por caja')
st.write('**Regla de esta tienda ficticia:** se cobra el precio registrado. Solo si no hay precio registrado, '
         'se aplica el importe de reserva de 20 €. Un precio de 0 € sí está registrado: significa gratis.')
scenario = st.selectbox('Situación', ['Producto gratuito · 0 €', 'Producto con precio · 12,50 €', 'Producto sin precio registrado'])
price = {'Producto gratuito · 0 €': 0, 'Producto con precio · 12,50 €': 12.5,
         'Producto sin precio registrado': None}[scenario]
before, after = compare(price, 20)
expected = 20 if price is None else price
money = lambda value: f'{value:g} €'.replace('.', ',')
st.write(f'**Lo que debería cobrar:** {money(expected)}')
a, b = st.columns(2)
a.metric('La caja antes del arreglo cobra', money(before))
b.metric('La caja después del arreglo cobra', money(after))
if before != expected:
    st.error('Aquí está el fallo: el producto es gratis, pero la caja cobra 20 €. Después del arreglo cobra 0 €, como debe.')
else:
    st.info('En esta situación las dos versiones cobran lo esperado. Vuelve al producto gratuito para ver dónde estaba el fallo.')

explain_tab, tests_tab, code_tab = st.tabs(['Entender el ejemplo', 'Comprobar el arreglo', 'Ver el código · opcional'])
with explain_tab:
    st.subheader('2. ¿Qué estaba confundiendo el programa?')
    st.write('La caja trataba estas dos situaciones como si fueran iguales:')
    st.markdown('- **Precio 0 €:** sabemos el precio y el producto es gratis.\n'
                '- **Sin precio registrado:** no sabemos el precio y usamos los 20 € de reserva.')
    st.write('**La corrección:** preguntar si falta el precio, en lugar de interpretar el cero como si faltara.')
    st.subheader('Una pregunta para ti')
    answer = st.radio('Un producto tiene un precio registrado de 0 €. ¿Cuánto debería cobrar la caja?',
                      ['0 €', '20 €'], index=None)
    if answer == '0 €':
        st.success('Eso es: sabemos que es gratis. No necesitamos el importe de reserva.')
    elif answer is not None:
        st.info('Fíjate en la diferencia: no falta el precio, está registrado como cero. Cero significa gratis.')
    st.write('**Idea clave:** «vale cero» y «no sé cuánto vale» son cosas distintas.')

with tests_tab:
    st.subheader('3. ¿Cómo sabemos que el arreglo funciona?')
    st.write('Una prueba automática hace lo mismo que tú: introduce un precio y comprueba si la caja cobra lo esperado.')
    st.markdown('**Ejemplo:** introducir 0 € → esperar 0 €. Si la caja devuelve 20 €, la prueba detecta el fallo.')
    st.write('El botón ejecuta ahora las pruebas sobre las dos versiones. También comprueba que sigan funcionando '
             'el precio sin registrar y otros valores.')
    if st.button('Comprobar el arreglo', type='primary'):
        with st.spinner('Comprobando las dos versiones…'):
            try:
                st.session_state['checks'] = run_checks()
            except Exception as error:
                st.session_state.pop('checks', None)
                st.error(f'No se pudo completar la comprobación: {error}')
    if 'checks' in st.session_state:
        result = st.session_state['checks']
        reproduced = result['before']['exit_code'] != 0 and 'AssertionError' in result['before']['output']
        passed = result['after']['exit_code'] == 0
        if reproduced:
            st.warning('ANTES: la prueba detecta que el producto gratis se cobra a 20 €. Esto confirma el fallo.')
        else:
            st.error('No se ha reproducido el fallo esperado. Revisa los detalles.')
        if passed:
            st.success('DESPUÉS: pasan las 3 pruebas. El producto gratis cuesta 0 € y los otros casos comprobados siguen funcionando.')
        else:
            st.error('El arreglo no pasa las pruebas. Hay que revisarlo.')
        with st.expander('Ver la salida técnica de las pruebas · opcional'):
            st.markdown('**Antes**')
            st.code(result['before']['output'], language='text')
            st.markdown('**Después**')
            st.code(result['after']['output'], language='text')
        st.caption('Son tres pruebas de este ejemplo, no una garantía para todos los programas.')
    else:
        st.info('Pulsa el botón para ejecutar la comprobación. Aún no se ha ejecutado en esta sesión.')

with code_tab:
    st.subheader('El cambio en Python')
    original, corrected = sources()
    a, b = st.columns(2)
    with a:
        st.markdown('**Antes**')
        st.code(original, language='python')
    with b:
        st.markdown('**Después · corrección guardada de Codex**')
        st.code(corrected, language='python')
    st.write('`price` es el precio y `fallback` el importe de reserva. `None` significa que no hay precio registrado. '
             'El operador `or` también considera falso el cero; `is None` comprueba únicamente si falta el dato.')
    with st.expander('Ver exactamente la línea modificada'):
        st.code(patch(), language='diff')
    st.download_button('Descargar el cambio', patch(), file_name='tailorcode-zero-price.patch', mime='text/plain')
