import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils.converter_intensity_trip import converter_intensity
from utils.map import *
from streamlit_folium import folium_static

# Config page
st.set_page_config(page_title = 'Urban Horizons (UH)', page_icon = ':small_airplane:', layout = 'wide')

# Initialize final button session state if button is not pressed at the previous page
if 'final_button' not in st.session_state:
    st.session_state.final_button = False

# Retrieve the chosen city from session state
chosen_city = st.session_state.get('chosen_city', '')

# Compare final button session state with chosen city (it will not be the same if city input changes and button is not pressed at the previous page)
if st.session_state.final_button == chosen_city:

    # Retrieve trip details from session state
    days_trip = st.session_state.get('days_trip', '')
    intensity_trip = st.session_state.get('intensity_trip', '')
    
    intensity_trip = converter_intensity(intensity_trip)
    total_attractions = days_trip * intensity_trip

    attractions = st.session_state.see_images['data'] # retrieve output used in "What to see" container to create maps with attractions

    available_attractions = len(attractions)
    used_attractions = min(available_attractions, total_attractions)
    
    # If attractions are retrieved correctly, proceed with mapping output
    if attractions:

        with st.container():
            st.title(f'Have a look at your trip in {chosen_city.capitalize()}!')
            
            if days_trip == 1:
                st.write(f'You decided to **get a recommendation for a {days_trip}-day trip**!')
            else:
                st.write(f'You decided to **get a recommendation for a {days_trip}-days trip**!')
            
            if available_attractions < days_trip:
                st.warning(
                    f"We found only {available_attractions} attractions with "
                    f"location data, which is not enough to generate a "
                    f"{days_trip}-day itinerary. Please choose fewer days "
                    "or another city."
                )
                st.stop()

            if available_attractions < total_attractions:
                st.warning(
                    f"Sorry! We found {available_attractions} attractions with "
                    f"location data, fewer than the {total_attractions} "
                    f"requested for your trip. We will still generate "
                    f"a {days_trip}-day itinerary, using "
                    f"{used_attractions} attractions in total."
                )

            st.write(
                f"Your itinerary includes {used_attractions} attractions "
                f"across {days_trip} day(s). The number of attractions "
                "may differ between days because we group nearby places "
                "to reduce travel."
            )

            st.write(f"*Try to zoom out if you can't find some attractions in the map.*")

            st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)        
        
        with st.container():
            maps = create_maps(attractions, days_trip, intensity_trip)

            # Enumerate maps to have first day number and iterate through tuples of maps itself
            for day, (map, numbered_names) in enumerate(maps, start = 1): 
                st.subheader(f'Day {day}')

                # Display map and list of places on the right
                col1, col2 = st.columns([2.5, 0.5])

                with col1:
                    folium_static(map, width=800, height=400)

                with col2:
                    st.write(f'Want to know more? Learn more about our recommendation. :point_down:')
                    for numbered_name in numbered_names:
                        index, name = numbered_name.split('. ', 1) # split numbered name to look for href link in original input attractions
                        st.markdown(f"[{numbered_name}]({attractions[name]['href']})")

                st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)
        
        with st.container():
            if st.button('Different trip? :city_sunrise:'):
                switch_page('Select your city')
                    
    else:
        st.title(f'Ops...')
        st.write("Something went wrong while loading your information. If you also can't see any attractions at the information page, please **help us and reload Urban Horizons**.")

# Handling case for which button was not pressed at previous page
else:
    st.title(f'Ops...')
    st.write("No city confirmed at the information page! Please go back and **confirm your city choice first**.")

    with st.container():
        st.markdown('<hr style="margin: 0;">', unsafe_allow_html = True)
        if st.button('Select your city :city_sunrise:'):
            switch_page('Select your city')

with st.container():
    if st.button('Read again about us! :house:'): 
        switch_page('Welcome')
    
    if st.button("Read the documentation :book:"):
        switch_page('Documentation')