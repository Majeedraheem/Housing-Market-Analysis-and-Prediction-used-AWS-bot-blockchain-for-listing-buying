import streamlit as st
import pandas as pd
import requests
from geopy.geocoders import Nominatim
import pydeck as pdk
from dotenv import load_dotenv

load_dotenv()

geolocator = Nominatim(user_agent="streamlit_maps_geopy1")
url = 'https://us1.locationiq.com/v1/search'
prev_address = 'Toronto'
# lat = 43.6532
# lon = 79.3832

# with st.form('address_form'):
#     address = st.text_input('Enter an address')
#     submitted = st.form_submit_button('Submit')
address = st.text_input('Find Location', prev_address, autocomplete='street-address')


if address == '':
    address = prev_address
else:
    prev_address = address

try:
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    address_found = location.address
except:
    data = {
        'key': os.getenv("LOCATIONIQ_KEY"),
        'q':address,
        'format': 'json'
    }
    response = requests.get(url, params=data)
    data = response.json()
    lat = float(data[0]['lat'])
    lon = float(data[0]['lon'])
    address_found = float(data[0]['display_name'])

st.write(f"Using Address: {address_found}")

map_df = pd.DataFrame(
    [[lat, lon]],
    columns=['lat', 'lon'])

view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=16, pitch=0)

scatter_layer = pdk.Layer('ScatterplotLayer',
                          data=map_df,
                          get_position='[lon, lat]',
                          get_color='[200, 30, 0, 160]',
                          # radiusUnits='pixels',
                          # maxPixelRadius=20,
                          # minPixelRadius=20,
                          get_radius=5,
                          # get_radius=view_state.zoom,
                          # radiusScale=1,
                          # radiusScale=2**(view_state.zoom/3),
                         )
# scatter_layer.get_radius = "1 / view_state.zoom"
deck = pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v12',
    initial_view_state=view_state,
    layers=[scatter_layer],
    map_provider='mapbox',
    # onViewStateChange
)
st.pydeck_chart(deck)