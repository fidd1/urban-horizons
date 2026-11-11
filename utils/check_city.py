import wikipediaapi
import re
import requests
import streamlit as st

# Identify project and language (set to en for the sake of the project - no handling of different languages)
user_agent = 'UrbanHorizons (https://github.com/fidd1/urban-horizons)'
wiki = wikipediaapi.Wikipedia(
    user_agent = user_agent,
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    language='en'
)

# Check if Wikipedia page exists for the chosen city value and it seems also a city
def exists_is_city_wikipage(city):
    
    def check_page(city):
        # set a list of words to detect if it is a city or not
        city_keywords = ['city', 'town', 'capital',
                     'population', 'located in',
                     'municipality', 'urban area',
                     'suburban area', 'metropolitan area']

        page = wiki.page(city)

        if page.exists():
            summary = page.summary[:200].lower()
            return any(keyword in summary for keyword in city_keywords)
        
        return False # if input does not have a Wikipedia page
    
    if check_page(city):
        return True, city
    
    if check_page(f'{city}_city'):
        return True, f'{city}_city' # avoid disambiguation case
    
    return False, city  # if input is likely not a city

# Get first sentences of the Wikipedia summary to output in "Information for your city"
def get_basic_info(city):
    exists, valid_city = exists_is_city_wikipage(city)
    summary = wiki.page(valid_city).summary

    # split summary into sentences
    wiki_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
    sentences = re.split(wiki_pattern, summary)

    # get first 6 sentences to output
    basic_info = ' '.join(sentences[:6])
    
    return basic_info

# Get weather information
def get_weather_info(city):
    try:
        url = f'https://wttr.in/{city}?format=j1'
        response = requests.get(url)

        weather_data = response.json()
        current_condition = weather_data['current_condition'][0]

        temp = current_condition['temp_C']
        feels_temp = current_condition['FeelsLikeC']
        weather = current_condition['weatherDesc'][0]['value']
        wind = current_condition['windspeedKmph']
        humidity = current_condition['humidity']

        weather_info = [temp, feels_temp, weather, wind, humidity]

        st.session_state.weather_info = {
                    'city': city,
                    'weather': [temp, feels_temp, weather, wind, humidity]
                }

        return weather_info
    
    except:
        return None