from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title = "Urban Horizons", page_icon = ":small_airplane:", layout = "wide")
img_logo = Image.open("images/logo_milano.png")
img_city = Image.open("images/city_milano.jpeg")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://lottie.host/1e73d20b-bf25-410f-bfe1-60fbab1218cb/r8dxvWGBYo.json")

#HEADER SECTION
with st.container():
    st.subheader("Your travel plans, made faster")
    st.title("Urban Horizons")
    st.write("The aim of our platform is to provide the user with a simple guide to plan their holiday.")

#IN CASE OF A WEBSITE LINK TO PUT: st.write("[Learn More >](ourwebsite here)")

# ---- ABOUT URBAN HORIZONS ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("About Urban Horizons")
        st.write("##")
        st.write(
            """
            How many times did you want to google a holiday city and open an “all-you-need-to-know” page before departure? Have you ever felt undecided in where to go or what to do? Was bad weather one of your concerns? This is why we are setting up UH for you.

The aim of our platform is to provide the user with a simple guide to plan their holiday. 

With an initial scope of 20 Italian cities, our beta will collect all the information regarding history, weather, culture, cuisine and sightseeing locations of your chosen destination.

But that’s not it.

It will then perform an analysis to let you know, according to your preferences, which is the best time to visit the city and plan for you all the days: from breakfast to evening activities.

Still not sure about it?

What if we told you that with one click it would show the best travel and accommodation arrangements, walking time, dining options and who knows more?

This is Urban Horizons: your travel plans, made faster.
            """
        )
    
    with right_column:
        st_lottie(lottie_coding, height=500, key='coding')

# ---- MILANO PROVA ----
with st.container():
    st.write("---")
    st.header("An example")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_city)
    with text_column:
        st.subheader("Milan's logo")
        st.image(img_logo, width=100)
        st.write("##")
        st.subheader("Have a look at Milan's city")
        st.write(
            """
            This is a trial
            """
        )