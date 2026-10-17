"""Shared authorship and social links for every demo example."""
import streamlit as st


def render_footer():
    st.divider()
    st.markdown('''
<footer aria-label="Authorship and social links" style="text-align:center; padding:1rem 0 1.5rem;">
  <p style="margin-bottom:0.6rem;">© 2026 <strong>Araceli Fradejas Muñoz</strong> · tAilorCode</p>
  <p style="line-height:2; margin-bottom:0;">
    <a href="https://github.com/AraceliFradejas" target="_blank" rel="noopener noreferrer">GitHub</a>
    &nbsp;·&nbsp;
    <a href="https://www.linkedin.com/in/araceli-fradejas-munoz-transformaciondigital/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
    &nbsp;·&nbsp;
    <a href="https://twitter.com/AraceliFradejas" target="_blank" rel="noopener noreferrer">X</a>
    &nbsp;·&nbsp;
    <a href="https://medium.com/@araceli.fradejas" target="_blank" rel="noopener noreferrer">Medium</a>
    &nbsp;·&nbsp;
    <a href="https://www.youtube.com/@aracelifradejasmunoz2758" target="_blank" rel="noopener noreferrer">YouTube</a>
  </p>
</footer>
''', unsafe_allow_html=True)
