"""Package the portable skill for download; no local session data is included."""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

SOURCE = Path(__file__).resolve().parents[1] / 'skills/tailorcode'


def build_skill_archive(target):
    if target not in ('codex', 'claude'):
        raise ValueError('Choose codex or claude')
    paths = [SOURCE / 'SKILL.md', SOURCE / 'references/explanation.md']
    if target == 'codex':
        paths.append(SOURCE / 'agents/openai.yaml')
    output = BytesIO()
    with ZipFile(output, 'w', compression=ZIP_DEFLATED) as bundle:
        for path in paths:
            bundle.writestr('tailorcode/' + path.relative_to(SOURCE).as_posix(), path.read_bytes())
    return output.getvalue()


def render_skill_downloads():
    import streamlit as st

    st.divider()
    st.subheader('Descarga la skill')
    st.write('Prueba los ejemplos y descubre cómo corregir errores de Python paso a paso. '
             'Descarga la skill para usarla en tus proyectos.')
    st.download_button('⬇ Descargar para Codex', build_skill_archive('codex'),
                       file_name='tailorcode-codex.zip', mime='application/zip',
                       type='primary', key='download_codex_skill')
    st.download_button('⬇ Descargar para Claude Code', build_skill_archive('claude'),
                       file_name='tailorcode-claude.zip', mime='application/zip',
                       key='download_claude_skill')
    with st.expander('Cómo instalarla y usarla'):
        st.write('1. Descarga y descomprime el ZIP de tu asistente. Obtendrás una carpeta llamada `tailorcode`.')
        st.write('2. Coloca esa carpeta dentro de tu proyecto:')
        st.code('.agents/skills/tailorcode/  # Codex\n.claude/skills/tailorcode/  # Claude Code', language='text')
        st.write('3. Abre una conversación nueva en ese proyecto y pide:')
        st.code('Usa $tailorcode para corregir este error y explicarme el arreglo.', language='text')
        st.caption('En Claude Code, empieza la petición por /tailorcode. Necesitas acceso al asistente elegido.')
