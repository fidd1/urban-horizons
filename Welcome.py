import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_lottie import st_lottie
from utils.lottie import load_lottieurl

# Config page
st.set_page_config(page_title = 'Urban Horizons (UH)', page_icon = ':small_airplane:', layout = 'wide')

# Incipt container
with st.container():
    st.title('Welcome :house:')
    st.write('The aim of this platform is to provide the user (**you!**) with a simple guide to plan their holiday.')
    st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)

# About us container
with st.container():
    # load text for about us description
    with open('text_inputs/about_us.txt', 'r') as text:  
        about_us_text = text.read()

    # load lottie for graphic aesthetic
    lottie_file = load_lottieurl('https://lottie.host/1e73d20b-bf25-410f-bfe1-60fbab1218cb/r8dxvWGBYo.json') 
    
    # display columns
    col1, col2 = st.columns(2)
    with col1:
        st.write(about_us_text)
        if st.button('Select your city :city_sunrise:'):
            switch_page('Select your city')
    
        if st.button('Read the documentation :book:'):
            switch_page('Documentation')

    with col2:
        st_lottie(lottie_file, height=500, key='coding')