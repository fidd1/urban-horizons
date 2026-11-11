import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils.check_city import *
from utils.scrap_all import *

# Config page
st.set_page_config(page_title = 'Urban Horizons (UH)', page_icon = ':small_airplane:', layout = 'wide')

# Session state initialization for playwright running, days trip, intensity trip and final button
if 'playwright_running' not in st.session_state:
    st.session_state.playwright_running = False

if 'days_trip' not in st.session_state:
    st.session_state.days_trip = 0

if 'intensity_trip' not in st.session_state:
    st.session_state.days_trip = ''

if 'final_button' not in st.session_state:
    st.session_state.final_button = False

# Retrieve the chosen city from session state
chosen_city = st.session_state.get('chosen_city', '')

with st.container():
    if chosen_city:
        st.title(f'A quick glance at {chosen_city.title()}!')
        st.write(f'Here you will find some brief information about **{chosen_city.title()}**. It is for you, to decide wheter to **keep organize your trip or change the city**!')
        # disclaimer for user
        st.success(f'We are loading some information for you... please wait, **do not leave this page** and see below! :point_down:')
        st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)

        # Brief overview
        with st.container():
            st.subheader(f'An introduction')
            st.write(get_basic_info(chosen_city))   # condition for the function is already checked at the previous page

        # Weather information
        with st.container():
            st.subheader(f'What about the weather?')
            weather_info = get_weather_info(chosen_city)    # if data found
            if weather_info:
                temp, feels_temp, weather, wind, humidity = weather_info

                col1, col2, col3, col4, col5  = st.columns(5)
                col1.metric(label = 'Temperature :thermometer:', value = f'{temp} °C')
                col2.metric(label = 'Feels more like :thermometer:', value = f'{feels_temp} °C')
                col3.metric(label = 'Weather :mostly_sunny:', value = f'{weather}')
                col4.metric(label = 'Wind speed :wind_blowing_face:', value = f'{wind} km/h')
                col5.metric(label = 'Humidity :fog:', value = f'{humidity} %')

            # if not found
            else:
                st.warning(f"Looks like we can't find this specific information in our sources.")

            st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)

        # Attractions, restaurants and hotels information
        with st.container():
            
            with st.container():
                st.subheader(f'What to see')
                try:
                    see_container(chosen_city)
                except:
                    st.warning(f"Looks like we can't find this specific information in our sources. We will struggle with showing you a visit guide. Sorry!")

            with st.container():
                st.subheader(f'Where to eat')
                try:
                    eat_container(chosen_city)
                except:
                    st.warning(f"Looks like we can't find this specific information in our sources.")

            with st.container():
                st.subheader(f'Where to stay')
                try:
                    stay_container(chosen_city)
                except:
                    st.warning(f"Looks like we can't find this specific information in our sources.")

        # Last input from user to store preferences and re-direct to the Visit guide
        with st.container():    
            st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)
            st.subheader('Ready? We need some more information from you!')

            col1, col2, col3 = st.columns([0.5, 1, 1]) # more compact view of col1 and col2
            
            with col1:
                days_trip = st.slider(label = f'Select the amount of days you would like to spend in {chosen_city.capitalize()}',
                        min_value = 1, max_value = 3, step = 1)
            with col2:
                intensity_trip = st.radio(label = f'How intense of a traveller are you?',
                                        options = ['Relaxed tourist (~3 attractions per day)',
                                                   'Average tourist (~5 attractions per day)',
                                                   'Pro tourist (~8 attractions per day)']
                                                   )   

            if st.button("Confirm and let's go! :world_map:"):
                st.session_state.days_trip = days_trip
                st.session_state.intensity_trip = intensity_trip
                st.session_state.final_button = chosen_city
                switch_page('Visit guide')

        with st.container():
            st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)
            if st.button('Different trip? :city_sunrise:'):
                switch_page('Select your city')

    else:
        st.title(f'Ops...')
        st.write('No city confirmed at the select page! Please go back and **confirm your city choice first**.')

        with st.container():
            st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)
            if st.button('Select your city :city_sunrise:'):
                switch_page('Select your city')

with st.container():
    if st.button('Read again about us! :house:'): 
        switch_page('Welcome')

    if st.button('Read the documentation :book:'): 
        switch_page('Documentation')
