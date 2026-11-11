import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import geopy
import certifi
import ssl
import streamlit as st
import traceback

# Run a Chromium instance to find places through Google Maps
def scrap_on_maps(category, city, num):
    with sync_playwright() as pw:
        st.session_state.playwright_running = True
        browser = pw.chromium.launch(headless = True)  # set to False to check pw fetching
        page = browser.new_page(
            viewport={"width": 1280, "height": 900},
            locale="en-GB",
            )
        try:
            maps_url = 'https://www.google.com/maps/'
            page.goto(maps_url)
        except:
            st.session_state.playwright_running = False # avoid relaunching pw if it had already ran

        cookies_button = 'button[aria-label="Accept all"]'  # look for the cookies button to deal with it
        if page.is_visible(cookies_button):
            page.click(cookies_button)
            time.sleep(3)
        
        page.fill('input', f'{category} near {city}')   # search on maps the interested category
        page.keyboard.press('Enter')

        items = []
        grades = []
        for i in range(num):
            try:
                page.wait_for_selector('.hfpxzc')   # look for items of interested category
                updated_content = page.content()
                soup = BeautifulSoup(updated_content, 'lxml')
                items = soup.select('.hfpxzc')
                grades = soup.select('.ZkP5Je')

                last_category_location = page.locator('a.hfpxzc').last  # scroll to the last item
                last_category_location.scroll_into_view_if_needed()
                time.sleep(3)

            except Exception:
                print(f"Failed collecting results: {category} near {city}", flush=True)
                traceback.print_exc()   # log the full traceback for debugging purposes
                break

        names = []  # get list of names of locations
        for elem in items:
            name = elem.get('aria-label')
            names.append(name)
        
        hrefs = {}  # get dict of urls of locations
        for elem in items:
            name = elem.get('aria-label')
            href = elem.get('href')
            hrefs[name] = href

        reviews = {}    # get dict of reviews of locations - initially scrapped but not used for the project 
        for grade, name in zip(grades, names):
            review = grade.get('aria-label')
            reviews[name] = review
        
        addresses = {}  # get dict of addresses of locations
        images = {} # get dict of images of locations
        for i in names:
            try:
                location = page.get_by_role("link", name=i, exact=True).and_(
                    page.locator(f'a[href="{hrefs[i]}"]')).first # get the link to click on the location to get the address and main photo
                location.click()
                time.sleep(2)

                html_address = page.inner_html('body')
                soup_address = BeautifulSoup(html_address, 'html.parser')
                address = soup_address.select('.Io6YTe.fontBodyMedium.kR99db')  # get the address of the location
                correct_address = str(address[0]).split(sep=">")[1].split(sep="<")[0]
                addresses[i] = str(correct_address)

                photo_button = soup_address.find('button', attrs={'aria-label': f'Photo of {i}'})   # find the button to click and get the main photo of the location

                img_tag = (
                    photo_button.find('img')
                    if photo_button is not None
                    else None
                )

                if img_tag is not None and img_tag.get('src'):
                    images[i] = img_tag['src']
                
            except Exception:
                print(f"Failed extracting details for: {i}", flush=True)
                traceback.print_exc()
                continue

        # converting extracted addresses to coordinates with geopy
        cert_path = certifi.where()
        Nominatim.DEFAULT_SENTINEL = object()
        geopy.geocoders.options.default_ssl_context = ssl.create_default_context(cafile = cert_path)
        loc = Nominatim(user_agent = 'Geopy Library')   # initialize geocoder

        coordinates = {}
        for i in addresses:
            query = addresses[i].strip()
            try:
                getLoc = loc.geocode(query, timeout=10)

                if getLoc is None:
                    print(f"No coordinates found for: {query}", flush=True)
                    continue

                coordinates[i] = (getLoc.latitude, getLoc.longitude)

            except Exception:
                print(f"Geocoding failed for: {query}", flush=True)
                traceback.print_exc()

            finally:
                time.sleep(1)
        
        # dictionary to be used in the app
        full_info = {}
        for place in images:
            if place in hrefs and place in reviews and place in coordinates:
                full_info[place] = {
                    'href': hrefs[place],
                    'image': images[place],
                    'review': reviews[place],
                    'loc': coordinates[place]
                }
        
        print(
            f"[{category}] Collected {len(names)} places; "
            f"returned {len(full_info)} usable results.",
            flush=True,
        )

        page.close()
        st.session_state.playwright_running = False

    return full_info

def what_to_see(city):
    category = 'tourist attractions'
    num = 5
    return scrap_on_maps(category, city, num)

def where_to_eat(city):
    category = 'restaurants'
    num = 3
    return scrap_on_maps(category, city, num)

def where_to_stay(city):
    category = 'hotels'
    num = 3
    return scrap_on_maps(category, city, num)

def see_container(city):
    if 'see_images' not in st.session_state or st.session_state.see_images.get('city') != city:
        see_images = what_to_see(city)
        st.session_state.see_images = {
            'city': city,
            'data': see_images
        }
    else:
        see_images = st.session_state.see_images['data']

    display_see_images = dict(list(see_images.items())[:8]) # max output 8 for streamlit page

    cols = st.columns(len(display_see_images))
    for col, (attraction, info) in zip(cols, display_see_images.items()):
        col.image(info['image'], use_column_width=True)
        col.markdown(f'[{attraction}]({info["href"]})')

def eat_container(city):
    if 'eat_images' not in st.session_state or st.session_state.eat_images.get('city') != city:
        eat_images = where_to_eat(city)
        st.session_state.eat_images = {
            'city': city,
            'data': eat_images
        }
    else:
        eat_images = st.session_state.eat_images['data']

    display_eat_images = dict(list(eat_images.items())[:8]) # max output 8 for streamlit page

    cols = st.columns(len(display_eat_images))
    for col, (attraction, info) in zip(cols, display_eat_images.items()):
        col.image(info['image'], use_column_width=True)
        col.markdown(f'[{attraction}]({info["href"]})')

def stay_container(city):
    if 'stay_images' not in st.session_state or st.session_state.stay_images.get('city') != city:
        stay_images = where_to_stay(city)
        st.session_state.stay_images = {
            'city': city,
            'data': stay_images
        }
    else:
        stay_images = st.session_state.stay_images['data']

    display_stay_images = dict(list(stay_images.items())[:8]) # max output 8 for streamlit page

    cols = st.columns(len(display_stay_images))
    for col, (attraction, info) in zip(cols, display_stay_images.items()):
        col.image(info['image'], use_column_width=True)
        col.markdown(f'[{attraction}]({info["href"]})')