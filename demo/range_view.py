"""Show an exclusive-boundary bug using a fictional watering calendar."""
import streamlit as st
from demo.engine import patch, range_trace, run_checks, sources
from demo.skill_downloads import render_skill_downloads

CASE = 'inclusive-range'


def calendar(start, end, actual):
    for first in range(start, end + 1, 7):
        days = list(range(first, min(first + 7, end + 1)))
        for day, column in zip(days, st.columns(len(days))):
            with column.container(border=True):
                st.markdown(f'**Día {day}**')
                if day in actual:
                    st.write('💧 Riego')
                elif day % 2 == 0:
                    st.write('❌ Falta riego')
                else:
                    st.caption('Sin riego previsto')


def render_range():
    st.markdown('**tAilorCode · Corrige y aprende**')
    st.title('El último día se queda sin riego.')
    st.write('Has pedido un plan del día 1 al día 4, ambos incluidos. Las plantas se riegan '
             'los días pares: el 2 y el 4. Pero el programa solo programa el día 2.')
    st.caption('Ejemplo educativo con corrección de referencia preparada; no es una nueva respuesta de IA.')
    with st.sidebar:
        st.header('Un calendario con un día menos')
        st.write('**Regla del ejemplo:** regar los días pares dentro del periodo elegido, incluyendo el último día.')
        st.write('Los días impares no tienen riego previsto. Eso es correcto.')
        st.divider()
        st.write('Proyecto de Araceli Fradejas Muñoz')
        render_skill_downloads()

    st.subheader('1. Elige el periodo del plan')
    scenario = st.selectbox('Periodo', ['Del día 1 al 4', 'Solo el día 2', 'Del día 1 al 5'])
    start, end = {'Del día 1 al 4': (1, 4), 'Solo el día 2': (2, 2), 'Del día 1 al 5': (1, 5)}[scenario]
    expected = [day for day in range(start, end + 1) if day % 2 == 0]
    trace = range_trace(start, end)
    st.markdown('**Días en los que debería haber riego: ' + ', '.join(map(str, expected)) + '.**')
    a, b = st.columns(2)
    with a:
        st.markdown('### Antes del arreglo')
        calendar(start, end, trace['before'])
    with b:
        st.markdown('### Después del arreglo')
        calendar(start, end, trace['after'])
    if trace['before'] != expected:
        st.error(f'Falta el día {end} en el plan original, aunque lo habíamos incluido en el periodo.')
    else:
        st.info('Aquí los dos planes son correctos: el último día es impar y no necesita riego. '
                'Elige “Del día 1 al 4” para ver el fallo.')

    explain, tests, code = st.tabs(['Entender el ejemplo', 'Comprobar el arreglo', 'Ver el código · opcional'])
    with explain:
        st.subheader('2. “Hasta el día 4” debe incluir el día 4')
        st.write('El programa usaba una cuenta que se detiene justo antes del último número. '
                 'Al pedir del 1 al 4, revisaba solo los días 1, 2 y 3.')
        st.write('**La corrección:** hacer que la cuenta revise también el último día. '
                 'Después se eligen los días pares, como antes.')
        answer = st.radio('Si el plan empieza y termina el día 2, ¿hay que regar ese día?',
                          ['Sí, el día 2 está incluido', 'No, el plan está vacío'], index=None, key='range_quiz')
        if answer == 'Sí, el día 2 está incluido':
            st.success('Exacto. El periodo puede durar un solo día, y ese día también cuenta.')
        elif answer is not None:
            st.info('El inicio y el final están incluidos: del día 2 al día 2 significa un día, no cero.')
        st.markdown('**Idea clave:** comprobar los extremos evita dejar fuera el primer o el último elemento.')
    with tests:
        st.subheader('3. Comprueba los extremos del periodo')
        st.write('El botón ejecuta cuatro pruebas originales: final par incluido, periodo de un solo día, '
                 'final impar, y valores negativos o periodos invertidos como casos técnicos.')
        if st.button('Comprobar el calendario', type='primary', key='range_checks'):
            try:
                with st.spinner('Comprobando las dos versiones…'):
                    st.session_state['range_checks_result'] = run_checks(CASE)
            except Exception as error:
                st.session_state.pop('range_checks_result', None)
                st.error(f'No se pudo completar la comprobación: {error}')
        result = st.session_state.get('range_checks_result')
        if result:
            if result['before']['exit_code'] != 0 and 'AssertionError' in result['before']['output']:
                st.warning('ANTES: las pruebas detectan que se excluye el último día.')
            else:
                st.error('No se ha reproducido el fallo esperado. Revisa los detalles.')
            if result['after']['exit_code'] == 0:
                st.success('DESPUÉS: pasan las 4 pruebas. Se incluye el último día y se conservan los otros casos.')
            else:
                st.error('La corrección no pasa las pruebas.')
            with st.expander('Ver la salida técnica · opcional'):
                st.markdown('**Antes**')
                st.code(result['before']['output'], language='text')
                st.markdown('**Después**')
                st.code(result['after']['output'], language='text')
            st.caption('El calendario ilustra una función de números pares, no un sistema real de riego.')
        else:
            st.info('Pruebas aún no ejecutadas en esta sesión. Pulsa el botón para comprobarlas.')
    with code:
        before, after = sources(CASE)
        a, b = st.columns(2)
        with a:
            st.markdown('**Antes**')
            st.code(before, language='python')
        with b:
            st.markdown('**Después · corrección de referencia**')
            st.code(after, language='python')
        st.write('`range(start, end)` excluye el límite final. `range(start, end + 1)` permite incluirlo. '
                 '`number % 2 == 0` selecciona los números pares: los días de riego de este ejemplo.')
        with st.expander('Ver la línea modificada'):
            st.code(patch(CASE), language='diff')
        st.download_button('Descargar el cambio del calendario', patch(CASE),
                           file_name='tailorcode-inclusive-range.patch', mime='text/plain')
