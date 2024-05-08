import requests as rq
import pandas as pd

bron_url = "https://opendata.rijksoverheid.nl/v1/infotypes/schoolholidays?output=json"

"""Haalt lijsten met vakantiedagen op bij de rijksoverheid. Geeft een lijst met
vakantiedatums die gelden voor heel Nederland en regio midden."""
def get_vakantiedagen() -> list: 
    brondata = rq.get(bron_url).json()
    vakantie_timestamps = []

    for type in brondata:
        for content in type['content']: 
            for vacation in content['vacations']:
                for region in vacation['regions']:
                    if region['region'] in ["heel Nederland", "midden"]:
                        range = pd.date_range(region['startdate'], region['enddate'], freq='d', unit='s', inclusive='right').to_list()
                        vakantie_timestamps.extend(range)

    # de zo gevonden lijst bestaat uit timestamps. 
    # dat is onhandig vergelijken en die resolutie is niet nodig.
    vakantiedagen = []
    for ts in vakantie_timestamps:
        vakantiedagen.append(ts.date())
    
    return vakantiedagen
