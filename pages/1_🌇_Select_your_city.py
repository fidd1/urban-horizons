import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils.check_city import *

# Config page
st.set_page_config(page_title = 'Urban Horizons (UH)', page_icon = ':small_airplane:', layout = 'wide')

# Session state initialization for input city, running pw and loaded data
if 'chosen_city' not in st.session_state:
    st.session_state.chosen_city = ''

if 'playwright_running' not in st.session_state:
    st.session_state.playwright_running = False

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False    

with st.container():
    st.title('Select your city')
    st.write('Italy? Canada? Poland? Australia? Insert below the city of your desired holiday and **start dreaming**!')
    st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)

with st.container():
    # If pw is not running in the Information for your city page
    if not st.session_state.playwright_running:
        chosen_city = st.text_input('Write it here', placeholder='Turin, Vienna, Paris...')
        chosen_city = chosen_city.strip().lower()
                
        if chosen_city:
            st.write(f'Watch out! Checking data for {chosen_city.title()}...')
            
            # If it is a first time input or city input is different than the previous one
            if st.session_state.chosen_city != chosen_city:
                st.session_state.data_loaded = False  # reset data_loaded because a new city is chosen

            if not st.session_state.data_loaded:
                exists, valid_city = exists_is_city_wikipage(chosen_city)  # check if the Wikipedia page exists and it seems a city
                
                if exists:
                    st.success(f"Information for {chosen_city.title()} is available! Confirm your choice and let's start planning. :point_down:")
                    if st.button('Information for your city :information_source:'):
                        st.session_state.chosen_city = chosen_city # set the chosen city session state for navigation between pages
                        switch_page('Information for your city')

                else:
                    st.error(
                        f'We are sorry, we are struggling with finding useful information for {chosen_city.title()}. '
                        f'Are you sure that is a city? '
                        f'If yes, **please try with a different city**. '
                    )
          
            # City input is already loaded
            elif st.session_state.data_loaded:
                st.success(f'Information for {chosen_city.title()} is already loaded! Click below. :point_down:')
                if st.button('Information for your city :information_source:'):
                    switch_page('Information for your city')
    
    # Playwright is already running
    else:
        st.warning(f'Hey, wait! We are finalizing your previous trip information. Come back in a few seconds and try again or reload Urban Horizons.')
    
with st.container():
    st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)
    if st.button('Read again about us! :house:'): 
        switch_page('Welcome')

    if st.button('Read the documentation :book:'):
        switch_page('Documentation')