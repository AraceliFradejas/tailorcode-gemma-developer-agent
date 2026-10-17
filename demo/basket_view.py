"""Explain shared mutable defaults through two fictional shopping baskets."""
import streamlit as st
from demo.engine import basket_trace, patch, run_checks, sources

CASE = 'independent-lists'


def render_baskets():
    st.markdown('**tAilorCode · Corrige y aprende**')
    st.title('Mi cesta tiene la compra de otra persona.')
    st.write('Ana empieza una cesta y añade manzanas. Luis empieza otra y añade pan. '
             'Pero el programa mete las dos compras en la misma cesta. ¿Qué ha pasado?')
    st.caption('Ejemplo educativo con una corrección de referencia preparada. '
               'Este segundo arreglo aún no se ha probado en una sesión de Codex o Claude Code.')
    with st.sidebar:
        st.header('Dos personas, dos cestas')
        st.write('**La regla:** cada persona que empieza una cesta debe recibir una lista nueva y vacía.')
        st.write('Si alguien continúa una cesta existente, se conserva esa misma cesta.')
        st.divider()
        st.write('Proyecto de Araceli Fradejas Muñoz')
        st.caption('No hay llamadas nuevas a IA. Las pruebas del botón sí se ejecutan en este momento.')

    st.subheader('1. Elige la compra de cada persona')
    a, b = st.columns(2)
    with a:
        first = st.selectbox('Ana compra', ['Manzanas', 'Leche', 'Arroz'], key='basket_first')
    with b:
        second = st.selectbox('Luis compra', ['Pan', 'Huevos', 'Café'], key='basket_second')
    trace = basket_trace(first, second)
    st.markdown(f'**Lo esperado:** Ana tiene solo **{first.lower()}** y Luis solo **{second.lower()}**.')
    st.write(f'Primero Ana añade {first.lower()}. Después Luis abre una cesta nueva y añade {second.lower()}. '
             'Mira cómo quedan las dos cestas al terminar:')
    a, b = st.columns(2)
    with a:
        st.markdown('### Antes del arreglo')
        st.write('Cesta de Ana: **' + ', '.join(trace['before']['first_final']) + '**')
        st.write('Cesta de Luis: **' + ', '.join(trace['before']['second_final']) + '**')
        st.error('Las dos personas comparten la misma cesta. Añadir la compra de Luis cambia también la de Ana.')
    with b:
        st.markdown('### Después del arreglo')
        st.write('Cesta de Ana: **' + ', '.join(trace['after']['first_final']) + '**')
        st.write('Cesta de Luis: **' + ', '.join(trace['after']['second_final']) + '**')
        st.success('Cada persona conserva su propia compra en una cesta independiente.')

    explain, tests, code = st.tabs(['Entender el ejemplo', 'Comprobar el arreglo', 'Ver el código · opcional'])
    with explain:
        st.subheader('2. Una cesta nueva debe empezar vacía')
        st.write('El programa original prepara una única cesta vacía y la reutiliza cada vez que alguien pide '
                 'una nueva. Por eso los artículos se mezclan.')
        st.write('**La corrección:** crear una lista vacía nueva cada vez que alguien empieza una cesta. '
                 'Si alguien entrega una cesta que ya existe, se añade a esa cesta sin reemplazarla.')
        answer = st.radio('Luis empieza una cesta nueva. ¿Qué debería contener antes de añadir su compra?',
                          ['Nada: debe estar vacía', 'La compra de Ana'], index=None, key='basket_quiz')
        if answer == 'Nada: debe estar vacía':
            st.success('Exacto. Una cesta nueva es independiente de las anteriores.')
        elif answer is not None:
            st.info('Luis está empezando una cesta, no continuando la de Ana. Debería recibir una vacía.')
        st.markdown('**Idea clave:** volver a usar una función no siempre significa que sus objetos se creen de nuevo.')
    with tests:
        st.subheader('3. Comprueba que las cestas ya no se mezclan')
        st.write('El botón ejecuta tres pruebas reales: dos cestas nuevas son independientes; una cesta '
                 'existente se conserva; y una cesta vacía entregada por el usuario también se conserva.')
        if st.button('Comprobar las cestas', type='primary', key='basket_checks'):
            try:
                with st.spinner('Comprobando ambas versiones…'):
                    st.session_state['basket_checks_result'] = run_checks(CASE)
            except Exception as error:
                st.session_state.pop('basket_checks_result', None)
                st.error(f'No se pudo completar la comprobación: {error}')
        result = st.session_state.get('basket_checks_result')
        if result:
            if result['before']['exit_code'] != 0 and 'AssertionError' in result['before']['output']:
                st.warning('ANTES: la prueba detecta que las cestas nuevas comparten artículos.')
            else:
                st.error('No se ha reproducido el fallo esperado. Revisa la salida.')
            if result['after']['exit_code'] == 0:
                st.success('DESPUÉS: pasan las 3 pruebas. Las cestas nuevas son independientes y las existentes se conservan.')
            else:
                st.error('La corrección no pasa las pruebas.')
            with st.expander('Ver la salida técnica · opcional'):
                st.markdown('**Antes**')
                st.code(result['before']['output'], language='text')
                st.markdown('**Después**')
                st.code(result['after']['output'], language='text')
            st.caption('Las pruebas usan etiquetas genéricas para los artículos. Verifican esta función; '
                       'no son pruebas de una tienda completa ni de la skill en un asistente.')
        else:
            st.info('Las pruebas aún no se han ejecutado en esta sesión. Pulsa el botón para comprobarlo.')
    with code:
        original, corrected = sources(CASE)
        a, b = st.columns(2)
        with a:
            st.markdown('**Antes**')
            st.code(original, language='python')
        with b:
            st.markdown('**Después · corrección de referencia**')
            st.code(corrected, language='python')
        st.write('`labels` representa la lista de artículos y `label` el artículo que añadimos. '
                 'Python crea el valor por defecto `[]` al definir la función, no en cada llamada. '
                 'Usar `None` permite crear una lista nueva dentro de la función solo cuando no se proporciona una.')
        with st.expander('Ver las líneas modificadas'):
            st.code(patch(CASE), language='diff')
        st.download_button('Descargar el cambio de las cestas', patch(CASE),
                           file_name='tailorcode-independent-lists.patch', mime='text/plain')
