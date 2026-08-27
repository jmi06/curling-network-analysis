import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlparse, parse_qs

SEASON = "2026" # Last year of the season
CATEGORY = "mens"
FILTER_TYPE = {
    "mens": 81,
    "womens": 82
}


def fetch_events(season, category):
    # Scrape the events page of CurlingZone
    # and save each events id and name to a 
    # DataFrame.
    url = f'https://home.curlingzone.com/schedule.php?filtertype={filtertype[category]}&eventyear={season}'
    event_data = {
        "name": [],
        "id": []
    }

    # Fetch and parse the page 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Loop through each event on the page
    for el in soup.select(".featured-title"):
        link = el.find('a').get('href') # get the anchor tag with the link to the event
        event_data['name'].append(el.find_all('a')[0].text)
        event_data['id'].append(link[link.index("eventid=")+8:]) # parse out the event id

    # Save the results as a DataFrame and write to disk
    events = pd.DataFrame(event_data)
    events.to_csv(f"data/{category}/events.csv", index=False)
        
    return events