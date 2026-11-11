import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Config page
st.set_page_config(page_title = 'Urban Horizons (UH)', page_icon = ':small_airplane:', layout = 'wide')

with st.container():
    st.title('About the project')
    st.warning('**Please note**: The documentation below was written in 2024 for academic purposes. Some errors have been found and corrected in the review of the project before the GitHub upload in 2026. Refer to the GitHub README for the most up-to-date information.')
    st.write('Please find below some useful notes regarding the Urban Horizons project and its functionalities.')
    st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)

with st.container():
    st.subheader(f'Project structure')
    with open('text_inputs/read_me.txt', 'r') as text:
        read_me = text.read()
        st.write(read_me)
    
    st.subheader(f'How to navigate')
    st.warning('**Please note**: to avoid re-launching Playwright when re-running streamlit pages, make sure to first wait for the session to stop running, and later move between pages, if needed.')
    with open('text_inputs/how_to_navigate.txt', 'r') as text:
        how_to_navigate = text.read()
        st.write(how_to_navigate)

    st.subheader(f'Limitations')
    with open('text_inputs/limitations.txt', 'r') as text:
        limitations = text.read()
        st.write(limitations)
    
    st.subheader(f'Sources')
    with open('text_inputs/sources.txt', 'r') as text:
        sources = text.read()
        st.write(sources)

with st.container():
    st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)
    if st.button('Read again about us! :house:'): 
        switch_page('Welcome')