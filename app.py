"""A beginner-friendly replay of the recorded Codex price correction."""
import streamlit as st
from demo.engine import compare, patch, run_checks, sources
from demo.skill_downloads import render_skill_downloads
from demo.footer import render_footer

st.set_page_config(page_title='tAilorCode · Fix and learn', page_icon='🧵', layout='wide')
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
    st.subheader('Start here: choose a case')
    st.caption('Three everyday situations. Choose one to explore the bug and its correction.')
    labels = {
        'A free product': '🏷️  1. A free product',
        'Mixed shopping baskets': '🛒  2. Mixed shopping baskets',
        'The missing final day': '💧  3. The missing final day',
    }
    example = st.radio('Choose an example', list(labels), format_func=labels.get,
                       horizontal=True, label_visibility='collapsed', key='selected_case')
if example == 'Mixed shopping baskets':
    from demo.basket_view import render_baskets
    render_baskets()
    render_footer()
    st.stop()

if example == 'The missing final day':
    from demo.range_view import render_range
    render_range()
    render_footer()
    st.stop()

st.markdown('**tAilorCode · Fix and learn**')
st.title('It is free. Why am I being charged €20?')
st.write('Imagine testing a shop checkout. A product is marked as free, '
         'but the checkout charges €20. Let us understand the bug and check the correction.')
st.caption('No Python knowledge needed. Recorded Codex correction; no new AI generation.')

with st.sidebar:
    st.header('Your walkthrough')
    st.write('1. Choose a situation.\n\n2. Compare the checkout results.\n\n3. Check the correction.')
    st.divider()
    st.write('A project by Araceli Fradejas Muñoz')
    render_skill_downloads()
    st.markdown('[View the project on GitHub](https://github.com/AraceliFradejas/tailorcode-gemma-developer-agent)')

st.subheader('1. Choose a product for the checkout')
st.write('**Rule for this fictional shop:** charge the recorded price. Only when no price is recorded, '
         'use a fallback price of €20. A price of €0 is recorded: it means free.')
scenario = st.selectbox('Situation', ['Free product · €0', 'Recorded price · €12.50', 'No recorded price'])
price = {'Free product · €0': 0, 'Recorded price · €12.50': 12.5,
         'No recorded price': None}[scenario]
before, after = compare(price, 20)
expected = 20 if price is None else price
money = lambda value: f'€{value:g}'
st.write(f'**Expected charge:** {money(expected)}')
a, b = st.columns(2)
a.metric('Checkout before the correction', money(before))
b.metric('Checkout after the correction', money(after))
if before != expected:
    st.error('Here is the bug: the product is free, but the checkout charges €20. After the correction it charges €0, as required.')
else:
    st.info('Both versions are correct for this input. Choose the free product to see the bug.')

explain_tab, tests_tab, code_tab = st.tabs(['Understand the example', 'Check the correction', 'View the code · optional'])
with explain_tab:
    st.subheader('2. What was the program confusing?')
    st.write('The checkout treated these two situations as if they were the same:')
    st.markdown('- **Price €0:** we know the price and the product is free.\n'
                '- **No recorded price:** the price is missing, so we use the €20 fallback.')
    st.write('**The correction:** check whether the price is missing, instead of treating zero as missing.')
    st.subheader('A question for you')
    answer = st.radio('A product has a recorded price of €0. What should the checkout charge?',
                      ['€0', '€20'], index=None)
    if answer == '€0':
        st.success('Exactly: we know it is free. We do not need the fallback price.')
    elif answer is not None:
        st.info('The price is not missing: it is recorded as zero. Zero means free.')
    st.write('**Key idea:** zero value and an unknown value are different states.')

with tests_tab:
    st.subheader('3. How do we know the correction works?')
    st.write('An automated test does the same thing you do: it supplies a price and checks the charge.')
    st.markdown('**Example:** enter €0 → expect €0. If the checkout returns €20, the test detects the bug.')
    st.write('The button runs tests on both versions now. It also checks that '
             'a missing price and other values still work.')
    if st.button('Check the correction', type='primary'):
        with st.spinner('Checking both versions…'):
            try:
                st.session_state['checks'] = run_checks()
            except Exception as error:
                st.session_state.pop('checks', None)
                st.error(f'Could not complete the checks: {error}')
    if 'checks' in st.session_state:
        result = st.session_state['checks']
        reproduced = result['before']['exit_code'] != 0 and 'AssertionError' in result['before']['output']
        passed = result['after']['exit_code'] == 0
        if reproduced:
            st.warning('BEFORE: the test detects a €20 charge for a free product. This reproduces the bug.')
        else:
            st.error('The expected bug was not reproduced. Check the details.')
        if passed:
            st.success('AFTER: all 3 tests pass. The free product costs €0 and the other tested cases still work.')
        else:
            st.error('The correction fails the tests and needs another look.')
        with st.expander('View technical test output · optional'):
            st.markdown('**Before**')
            st.code(result['before']['output'], language='text')
            st.markdown('**After**')
            st.code(result['after']['output'], language='text')
        st.caption('These are three tests of this example, not a guarantee for every program.')
    else:
        st.info('Press the button to run the checks. They have not run in this session yet.')

with code_tab:
    st.subheader('The Python change')
    original, corrected = sources()
    a, b = st.columns(2)
    with a:
        st.markdown('**Before**')
        st.code(original, language='python')
    with b:
        st.markdown('**After · recorded Codex correction**')
        st.code(corrected, language='python')
    st.write('`price` is the recorded price and `fallback` is the fallback amount. `None` means no price is recorded. '
             'The `or` operator also treats zero as false; `is None` checks only whether the value is missing.')
    with st.expander('View the exact changed line'):
        st.code(patch(), language='diff')
    st.download_button('Download the change', patch(), file_name='tailorcode-zero-price.patch', mime='text/plain')

render_footer()
