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
    st.subheader('Download the skill')
    st.write('Try the examples and learn how to correct Python bugs step by step. '
             'Download the skill to use it in your own projects.')
    st.download_button('⬇ Download for Codex', build_skill_archive('codex'),
                       file_name='tailorcode-codex.zip', mime='application/zip',
                       type='primary', key='download_codex_skill')
    st.download_button('⬇ Download for Claude Code', build_skill_archive('claude'),
                       file_name='tailorcode-claude.zip', mime='application/zip',
                       key='download_claude_skill')
    with st.expander('How to install and use it'):
        st.write('1. Download and extract the ZIP for your assistant. It contains a folder named `tailorcode`.')
        st.write('2. Place that folder inside your project:')
        st.code('.agents/skills/tailorcode/  # Codex\n.claude/skills/tailorcode/  # Claude Code', language='text')
        st.write('3. Start a new conversation in that project and ask:')
        st.code('Use $tailorcode to fix this bug and explain the correction.', language='text')
        st.caption('In Claude Code, start the request with /tailorcode. You need access to your chosen assistant.')
