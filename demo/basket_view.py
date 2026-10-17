"""Explain shared mutable defaults through two fictional shopping baskets."""
import streamlit as st
from demo.engine import basket_trace, patch, run_checks, sources
from demo.skill_downloads import render_skill_downloads

CASE = 'independent-lists'


def render_baskets():
    st.markdown('**tAilorCode · Fix and learn**')
    st.title('Someone else’s shopping is in my basket.')
    st.write('Ana starts a basket and adds apples. Luis starts another and adds bread. '
             'But the program puts both purchases in the same basket. What happened?')
    st.caption('Educational example with a prepared reference correction. '
               'This correction has not yet been tested in a Codex or Claude Code skill session.')
    with st.sidebar:
        st.header('Two people, two baskets')
        st.write('**The rule:** each person starting a basket must get a new, empty list.')
        st.write('If someone continues an existing basket, that same basket is preserved.')
        st.divider()
        st.write('A project by Araceli Fradejas Muñoz')
        render_skill_downloads()

    st.subheader('1. Choose what each person buys')
    a, b = st.columns(2)
    with a:
        first = st.selectbox('Ana buys', ['Apples', 'Milk', 'Rice'], key='basket_first')
    with b:
        second = st.selectbox('Luis buys', ['Bread', 'Eggs', 'Coffee'], key='basket_second')
    trace = basket_trace(first, second)
    st.markdown(f'**Expected:** Ana has only **{first.lower()}** and Luis has only **{second.lower()}**.')
    st.write(f'First Ana adds {first.lower()}. Then Luis starts a new basket and adds {second.lower()}. '
             'Here are both baskets at the end:')
    a, b = st.columns(2)
    with a:
        st.markdown('### Before the correction')
        st.write('Ana’s basket: **' + ', '.join(trace['before']['first_final']) + '**')
        st.write('Luis’s basket: **' + ', '.join(trace['before']['second_final']) + '**')
        st.error('Both people share the same basket. Adding Luis’s item also changes Ana’s basket.')
    with b:
        st.markdown('### After the correction')
        st.write('Ana’s basket: **' + ', '.join(trace['after']['first_final']) + '**')
        st.write('Luis’s basket: **' + ', '.join(trace['after']['second_final']) + '**')
        st.success('Each person keeps their own purchase in an independent basket.')

    explain, tests, code = st.tabs(['Understand the example', 'Check the correction', 'View the code · optional'])
    with explain:
        st.subheader('2. A new basket must start empty')
        st.write('The original program prepares a single empty basket and reuses it whenever someone asks for '
                 'a new one. That is why the items get mixed.')
        st.write('**The correction:** create a fresh empty list whenever someone starts a basket. '
                 'If someone supplies an existing basket, add to it without replacing it.')
        answer = st.radio('Luis starts a new basket. What should it contain before he adds an item?',
                          ['Nothing: it should be empty', 'Ana’s shopping'], index=None, key='basket_quiz')
        if answer == 'Nothing: it should be empty':
            st.success('Exactly. A new basket is independent of earlier baskets.')
        elif answer is not None:
            st.info('Luis is starting a basket, not continuing Ana’s. He should get an empty one.')
        st.markdown('**Key idea:** calling a function again does not always create its default objects again.')
    with tests:
        st.subheader('3. Check that the baskets no longer mix')
        st.write('The button runs three real tests: new baskets are independent; an existing '
                 'basket is preserved; and a user-supplied empty basket is also preserved.')
        if st.button('Check the baskets', type='primary', key='basket_checks'):
            try:
                with st.spinner('Checking both versions…'):
                    st.session_state['basket_checks_result'] = run_checks(CASE)
            except Exception as error:
                st.session_state.pop('basket_checks_result', None)
                st.error(f'Could not complete the checks: {error}')
        result = st.session_state.get('basket_checks_result')
        if result:
            if result['before']['exit_code'] != 0 and 'AssertionError' in result['before']['output']:
                st.warning('BEFORE: the test detects items shared between new baskets.')
            else:
                st.error('The expected bug was not reproduced. Check the output.')
            if result['after']['exit_code'] == 0:
                st.success('AFTER: all 3 tests pass. New baskets are independent and existing baskets are preserved.')
            else:
                st.error('The correction fails the tests.')
            with st.expander('View technical output · optional'):
                st.markdown('**Before**')
                st.code(result['before']['output'], language='text')
                st.markdown('**After**')
                st.code(result['after']['output'], language='text')
            st.caption('The tests use generic labels for items. They verify this function; '
                       'they do not validate a complete shop or the skill inside an assistant.')
        else:
            st.info('The tests have not run in this session yet. Press the button to check.')
    with code:
        original, corrected = sources(CASE)
        a, b = st.columns(2)
        with a:
            st.markdown('**Before**')
            st.code(original, language='python')
        with b:
            st.markdown('**After · reference correction**')
            st.code(corrected, language='python')
        st.write('`labels` is the list of items and `label` is the item being added. '
                 'Python creates the default `[]` when defining the function, not on each call. '
                 'Using `None` lets us create a new list inside the function only when none was supplied.')
        with st.expander('View the changed lines'):
            st.code(patch(CASE), language='diff')
        st.download_button('Download the basket change', patch(CASE),
                           file_name='tailorcode-independent-lists.patch', mime='text/plain')
