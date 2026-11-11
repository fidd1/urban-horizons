To facilitate the understading and the navigation of the project, the structure of the submitted files is below presented.

Urban Horizons is a platform that wants to **simulate a holiday planner**. After the user inputs the name of a city, it outputs some useful information about **culture, weather, attractions, restaurants and hotels**. Later, it tries to cluster the attractions in order to give **map recommendations** for a potential holiday in the city, according to **two preferences that the user inputs**:
- **number of days of the holiday (days_trip)**, from 1 to 3 days, for the sake of the project;
- **intensity of sightseeing (intensity_trip)**, around 3, 5 or 8 attractions per day, later multiplied by total days (see *Limitations* below).

The platform is a multipage app in Streamlit. Unzipping the folder, you will find:
- **Welcome.py**, the platform homepage;
- **pages/**, a folder with the 4 sub-pages of the multipage app;
- **utils/**, a folder with some functions that are imported in the various pages when needed;
- **text_inputs/**, a folder with longer text inputs (such this one) for best practice;
- **.streamlit/**, a folder with config.toml for basic aesthetic.

If your are not doing it yet, please navigate to the Documentation page by writing "streamlit run Welcome.py" in the terminal for more.

*Note*: Please note that while debugging for the last times, I have struggled with Playwright sessions as multiple times the connection was timed out or the scrolling down was getting to the "end of the list" according to Google Maps. I believe this might be to the great number of sessions I have launched on my computer and line. If this would not be the case, the problem could influence the number of attractions collected and therefore output a smaller number of attractions even if the intensity trip is high (if retrieved less attractions than the total number calculated for the user).