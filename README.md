# Urban Horizons

**Your travel plans, made faster.**

Urban Horizons is a Python and Streamlit project that brings together destination information and generates a suggested sightseeing itinerary. Enter a city, explore its overview, weather, attractions, restaurants and hotels, then choose the length and intensity of your trip to generate daily maps.

Originally developed as a university project in 2024, it combines browser automation, HTML parsing, geocoding and geographic clustering in a multipage application.

## Run locally

Use **Python 3.11**. The development environment used during the current project review is Python **3.11.13**. Package versions are recorded in `requirements.txt`.

Download or clone this repository, open a terminal in its root folder, and choose one environment setup below.

### Option A: Python virtual environment

On macOS or Linux, with Python 3.11 installed:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

On Windows, using PowerShell and the Python launcher:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Option B: Conda

```bash
conda create --name urban-horizons python=3.11 pip
conda activate urban-horizons
```

### Install and start

With your chosen environment active:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m streamlit run Welcome.py
```

**Chromium is installed separately.** It is a browser binary, so it does not appear as a Python package in `requirements.txt`. Playwright installs the browser build matching its installed version.

Open the local URL printed in the terminal. An internet connection is required to retrieve live information. To stop the application, use **Ctrl+C**.

Keep the repository's folders together and launch the application from the root folder so its local text and other resources can be found.

## How the scraper works

The shared scrap_on_maps() function uses Playwright to search Google Maps and interact with dynamically loaded results. Beautiful Soup extracts place details from the rendered HTML, and Geopy resolves addresses into coordinates. Collection uses bounded scrolling attempts, with errors logged for diagnosis and partial results handled by the application.

## Using the application

1. **Welcome:** read the introduction to the project.
2. **Select your city:** enter a destination and confirm it after the Wikipedia-based check.
3. **Information for your city:** view the overview, weather, attractions, restaurants and hotels. Wait for collection to finish before changing your trip preferences.
4. Choose the number of days and sightseeing intensity, then confirm your choices.
5. **Visit guide:** explore the daily maps and follow the attraction links to Google Maps.

The **Documentation** page contains the original project notes. Results are stored in Streamlit session state to reuse them when navigating between pages for the same city. Restarting the application clears that in-memory state.

## Project structure

| File or folder | Purpose |
| --- | --- |
| `Welcome.py` | Streamlit entry point and homepage |
| `pages/` | City selection, city information, visit guide and documentation pages |
| `utils/scrap_all.py` | Shared Google Maps scraper and place-display helpers |
| `utils/check_city.py` | City validation and destination-information helpers |
| `utils/map.py` | Geographic clustering and Folium map generation |
| `utils/converter_intensity_trip.py` | Converts sightseeing preferences into numeric values |
| `utils/lottie.py` | Loads animation content for homepage |
| `text_inputs/` | Longer text used by the application and documentation |
| `.streamlit/config.toml` | Streamlit appearance configuration |
| `requirements.txt` | Python dependencies and pinned versions |

## Limitations

### Live source pages

Google Maps is dynamic. Its CSS classes, accessible labels, consent flow and results layouts may change. Network delays and page-loading behavior can also affect extraction. Selectors and waiting conditions may therefore need maintenance.

Scrolling is intentionally bounded. A search may stop loading additional results, and geocoding or missing fields can further reduce the usable count. The application cannot guarantee the maximum requested **24 attractions**. Limited results alone do not establish that access has been blocked.

### English and city ambiguity

The project is designed around English Wikipedia and English page labels. City validation uses Wikipedia lookup logic and summary keywords; it is not a comprehensive geographic disambiguation system. Places with shared names may be rejected or resolved to an unintended destination.

### Geocoding and mapping

Addresses extracted from Google Maps may not resolve in OpenStreetMap's Nominatim data. Address formatting and local data coverage affect the result, and successful matches are not independently verified in this case.

Fewer available attractions can produce a shorter itinerary than requested. At least as many attractions as trip days are needed to fit that number of KMeans clusters. Duplicate coordinate values can also produce fewer distinct clusters and require additional handling.

The maps are sightseeing suggestions. They do not account for opening hours, travel duration, accessibility, booking requirements or an optimized route. Travelling-salesman route optimization was explored during the original project but is not implemented in the current output.

## Sources and tools

- [Wikipedia](https://en.wikipedia.org/) — destination information.
- [Google Maps](https://www.google.com/maps/) — searched places and links to their listings.
- [OpenStreetMap / Nominatim](https://nominatim.org/) — address geocoding.
- [Streamlit](https://streamlit.io/), [Playwright](https://playwright.dev/python/), [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/), [Geopy](https://geopy.readthedocs.io/), [scikit-learn](https://scikit-learn.org/) and [Folium](https://python-visualization.github.io/folium/) — application, extraction and mapping tools.

OpenStreetMap data attribution: **© [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)**. Public Nominatim use is subject to its [usage policy](https://operations.osmfoundation.org/policies/nominatim/), including an application-identifying user agent, a maximum of one request per second across the application, and caching results.