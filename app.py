"""Streamlit portfolio demo of the recorded Codex price correction."""
import streamlit as st
from demo.engine import compare, patch, run_checks, sources

st.set_page_config(page_title='tAilorCode · Corrige y aprende', page_icon='🧵', layout='wide')
st.markdown('**tAilorCode** / laboratorio de aprendizaje')
st.title('Un cero también tiene valor.')
st.write('Descubre un fallo de Python, explora la corrección y comprueba por qué funciona.')
st.caption('Caso real corregido con Codex · explicación preparada · sin llamadas nuevas a IA')

with st.sidebar:
    st.header('Corrige · comprueba · aprende')
    st.write('Proyecto de Araceli Fradejas Muñoz')
    st.markdown('**Caso 01 — Un producto gratuito**')
    st.write('Un precio de 0 debe conservarse. Solo un precio ausente (`None`) permite usar el precio de reserva.')
    st.divider()
    st.write('Esta demo reproduce un resultado guardado. No analiza código nuevo ni genera respuestas con un modelo.')
    st.markdown('[Ver el proyecto en GitHub](https://github.com/AraceliFradejas/tailorcode-gemma-developer-agent)')

st.subheader('1. Prueba el comportamiento')
left, middle, right = st.columns(3)
with left:
    missing = st.checkbox('El precio está ausente (None)', value=False)
    entered_price = st.number_input('Precio del producto', value=0.0, step=1.0, disabled=missing)
with middle:
    fallback = st.number_input('Precio de reserva', value=20.0, step=1.0)
with right:
    st.write('Prueba cero, un número negativo o un precio ausente. Los resultados cambian al instante.')
price = None if missing else entered_price
before, after = compare(price, fallback)
a, b = st.columns(2)
a.metric('Código original devuelve', f'{before:g}')
b.metric('Código corregido devuelve', f'{after:g}')
if before != after:
    st.warning('El código original sustituye un precio válido por el de reserva.')
else:
    st.info('Con esta entrada coinciden. Que un caso pase no significa que el programa esté libre de fallos.')

code_tab, tests_tab, learn_tab = st.tabs(['El cambio', 'Las pruebas', 'Lo que aprendes'])
with code_tab:
    st.subheader('2. Una corrección de una línea')
    original, corrected = sources()
    a, b = st.columns(2)
    with a:
        st.markdown('**Antes**')
        st.code(original, language='python')
    with b:
        st.markdown('**Después · resultado guardado de Codex**')
        st.code(corrected, language='python')
    st.write('`or` elige el segundo valor cuando el primero se considera falso. En Python, eso incluye el cero. '
             'La condición `is None` pregunta únicamente si falta el precio: conserva cero y los negativos.')
    st.code(patch(), language='diff')
    st.download_button('Descargar el parche', patch(), file_name='tailorcode-zero-price.patch', mime='text/plain')

with tests_tab:
    st.subheader('3. Comprueba el arreglo por tu cuenta')
    st.write('Este botón ejecuta ahora las tres pruebas originales sobre el código antes y después. '
             'No usa un modelo ni modifica tus archivos de trabajo.')
    st.caption('Casos: cero, precio ausente y valores no nulos (12,5 y −3).')
    if st.button('Ejecutar pruebas antes y después', type='primary'):
        with st.spinner('Ejecutando las pruebas locales…'):
            try:
                st.session_state['checks'] = run_checks()
            except Exception as error:
                st.session_state.pop('checks', None)
                st.error(f'No se pudieron completar las pruebas: {error}')
    if 'checks' in st.session_state:
        result = st.session_state['checks']
        a, b = st.columns(2)
        with a:
            st.markdown('**Antes**')
            if result['before']['exit_code'] != 0 and 'AssertionError' in result['before']['output']:
                st.warning('El fallo del caso original se reproduce.')
            else:
                st.error('La reproducción no coincide con lo esperado; revisa la salida.')
            st.code(result['before']['output'], language='text')
        with b:
            st.markdown('**Después**')
            if result['after']['exit_code'] == 0:
                st.success('Verificado con las tres pruebas del ejemplo.')
            else:
                st.error('La corrección no pasa las pruebas.')
            st.code(result['after']['output'], language='text')
        st.caption('Esto verifica los casos del ejemplo; no garantiza el comportamiento de cualquier programa.')
    else:
        st.info('Pruebas aún no ejecutadas en esta sesión. Pulsa el botón para comprobar el resultado.')

with learn_tab:
    st.subheader('4. ¿Puedes anticipar el resultado?')
    st.write('Si el precio es −3 y el de reserva es 20, ¿qué debería devolver la versión corregida?')
    answer = st.radio('Elige una respuesta', ['−3', '20', 'None'], index=None)
    if answer == '−3':
        st.success('Exacto: un precio negativo sigue siendo un valor presente. Solo None activa la reserva.')
    elif answer is not None:
        st.info('Pista: la condición comprueba si falta el precio, no si es positivo. Puedes probarlo arriba.')
    st.markdown('**Idea que te llevas:** ausencia y cero son estados distintos. Elige una condición que exprese '
                'la regla del problema, y prueba los valores que podrían confundirse.')
    st.caption('El caso se resolvió también sin la skill. No hemos demostrado que tAilorCode mejore a Codex; '
               'esta demo hace visible el arreglo, su explicación y sus pruebas.')
