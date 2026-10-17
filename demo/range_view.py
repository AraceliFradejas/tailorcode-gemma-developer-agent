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
                st.markdown(f'**Day {day}**')
                if day in actual:
                    st.write('💧 Water')
                elif day % 2 == 0:
                    st.write('❌ Missing water')
                else:
                    st.caption('No watering scheduled')


def render_range():
    st.markdown('**tAilorCode · Fix and learn**')
    st.title('The final day gets no water.')
    st.write('You requested a plan from day 1 through day 4, both included. The plants are watered '
             'on even days: 2 and 4. But the program only schedules day 2.')
    st.caption('Educational example with a prepared reference correction; no new AI response.')
    with st.sidebar:
        st.header('A calendar missing a day')
        st.write('**Example rule:** water on even days within the chosen period, including the final day.')
        st.write('No watering is scheduled on odd days. That is correct.')
        st.divider()
        st.write('A project by Araceli Fradejas Muñoz')
        render_skill_downloads()

    st.subheader('1. Choose the planning period')
    scenario = st.selectbox('Period', ['Day 1 through day 4', 'Day 2 only', 'Day 1 through day 5'])
    start, end = {'Day 1 through day 4': (1, 4), 'Day 2 only': (2, 2), 'Day 1 through day 5': (1, 5)}[scenario]
    expected = [day for day in range(start, end + 1) if day % 2 == 0]
    trace = range_trace(start, end)
    st.markdown('**Expected watering days: ' + ', '.join(map(str, expected)) + '.**')
    a, b = st.columns(2)
    with a:
        st.markdown('### Before the correction')
        calendar(start, end, trace['before'])
    with b:
        st.markdown('### After the correction')
        calendar(start, end, trace['after'])
    if trace['before'] != expected:
        st.error(f'Day {end} is missing from the original plan, although it is included in the requested period.')
    else:
        st.info('Both plans are correct here: the final day is odd, so no watering is scheduled. '
                'Choose “Day 1 through day 4” to see the bug.')

    explain, tests, code = st.tabs(['Understand the example', 'Check the correction', 'View the code · optional'])
    with explain:
        st.subheader('2. “Through day 4” must include day 4')
        st.write('The program used a count that stops just before the final number. '
                 'When asked for days 1 through 4, it checked only days 1, 2 and 3.')
        st.write('**The correction:** make the count check the final day too. '
                 'Then select the even days, just as before.')
        answer = st.radio('If the plan starts and ends on day 2, should that day be watered?',
                          ['Yes, day 2 is included', 'No, the plan is empty'], index=None, key='range_quiz')
        if answer == 'Yes, day 2 is included':
            st.success('Exactly. A period can last just one day, and that day counts too.')
        elif answer is not None:
            st.info('Both boundaries are included: day 2 through day 2 means one day, not zero.')
        st.markdown('**Key idea:** checking boundaries prevents accidentally omitting the first or last item.')
    with tests:
        st.subheader('3. Check the period boundaries')
        st.write('The button runs four original tests: an included even final day, a single-day period, '
                 'an odd final day, and negative values or reversed ranges as technical cases.')
        if st.button('Check the calendar', type='primary', key='range_checks'):
            try:
                with st.spinner('Checking both versions…'):
                    st.session_state['range_checks_result'] = run_checks(CASE)
            except Exception as error:
                st.session_state.pop('range_checks_result', None)
                st.error(f'Could not complete the checks: {error}')
        result = st.session_state.get('range_checks_result')
        if result:
            if result['before']['exit_code'] != 0 and 'AssertionError' in result['before']['output']:
                st.warning('BEFORE: the tests detect the excluded final day.')
            else:
                st.error('The expected bug was not reproduced. Check the details.')
            if result['after']['exit_code'] == 0:
                st.success('AFTER: all 4 tests pass. The final day is included and the other cases are preserved.')
            else:
                st.error('The correction fails the tests.')
            with st.expander('View technical output · optional'):
                st.markdown('**Before**')
                st.code(result['before']['output'], language='text')
                st.markdown('**After**')
                st.code(result['after']['output'], language='text')
            st.caption('The calendar illustrates an even-number function, not a real watering system.')
        else:
            st.info('The tests have not run in this session yet. Press the button to check.')
    with code:
        before, after = sources(CASE)
        a, b = st.columns(2)
        with a:
            st.markdown('**Before**')
            st.code(before, language='python')
        with b:
            st.markdown('**After · reference correction**')
            st.code(after, language='python')
        st.write('`range(start, end)` excludes the final boundary. `range(start, end + 1)` includes it. '
                 '`number % 2 == 0` selects even numbers: the watering days in this example.')
        with st.expander('View the changed line'):
            st.code(patch(CASE), language='diff')
        st.download_button('Download the calendar change', patch(CASE),
                           file_name='tailorcode-inclusive-range.patch', mime='text/plain')
