import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import requests
from geopy.geocoders import Nominatim
import pydeck as pdk

# Import the helper function from the pinata.py file
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Load_Contract Function
################################################################################
def render_page():

    @st.cache_resource
    def load_contract():

        # Load the contract ABI
        with open(Path('../solidity/contracts/compiled/propertyregistry_abi.json')) as f:
            contract_abi = json.load(f)

        # Set the contract address (this is the address of the deployed contract)
        contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

        # Get the contract
        contract = w3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )

        return contract


    # Load the contract
    contract = load_contract()

    ################################################################################
    # Helper functions to pin files and json to Pinata
    ################################################################################

    def pin_property(location, first_name, last_name, user_phone, sell_price, prop_image_file):
        # Pin the file to IPFS with Pinata
        ipfs_file_hash = pin_file_to_ipfs(prop_image_file.getvalue()) # getvalue() returns file in bytes

        # Build a token metadata file for the artwork
        token_json = {
            "location": location,
            "first_name": first_name,
            "last_name": last_name,
            "phone": user_phone,
            "price": sell_price,
            "image": ipfs_file_hash
        }
        json_data = convert_data_to_json(token_json)

        # Pin the json to IPFS with Pinata
        json_ipfs_hash = pin_json_to_ipfs(json_data)

        return json_ipfs_hash, token_json


    def pin_appraisal_report(report_content):
        json_report = convert_data_to_json(report_content)
        report_ipfs_hash = pin_json_to_ipfs(json_report)
        return report_ipfs_hash

    st.title("List Your Property")
    # add form to get user info: account, name, etc.
    user_first_name = st.text_input("First Name")
    user_last_name = st.text_input("Last Name")
    user_phone = st.number_input("Phone", max_value=9999999999, min_value=0, step=1)
    accounts = w3.eth.accounts
    user_address = st.selectbox("Wallet", options=accounts)

    geolocator = Nominatim(user_agent="streamlit_maps_geopy1")
    url = 'https://us1.locationiq.com/v1/search'
    prev_address = 'Toronto'

    geo_address = st.text_input('Address', prev_address, autocomplete='street-address')

    if geo_address == '':
        geo_address = prev_address
    else:
        prev_address = geo_address

    try:
        location = geolocator.geocode(geo_address)
        lat = location.latitude
        lon = location.longitude
        address_found = location.address
    except ConnectionError:
        data = {
            'key': os.getenv("LOCATIONIQ_KEY"),
            'q':geo_address,
            'format': 'json'
        }
        response = requests.get(url, params=data)
        print(response)
        data = response.json()
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        address_found = float(data[0]['display_name'])
    except:
        st.write("Sorry, maps are not available at the moment")
        address_found = 'Toronto'
        lat = 43.7182116
        lon = -79.4604573

    st.write(f"Using Address: {address_found}")
    map_df = pd.DataFrame(
        [[lat, lon]],
        columns=['lat', 'lon'])

    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=16, pitch=0)

    scatter_layer = pdk.Layer('ScatterplotLayer',
                              data=map_df,
                              get_position='[lon, lat]',
                              get_color='[200, 30, 0, 160]',
                              get_radius=5,
                             )
    scatter_layer.get_radius = "1 / view_state.zoom"
    deck = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12',
        initial_view_state=view_state,
        layers=[scatter_layer],
        map_provider='mapbox',
        # onViewStateChange
    )
    st.pydeck_chart(deck)
    sell_price = st.number_input("How much would you like to sell for (ETH)?")
    property_type = st.text_input("What type of property is this?")

    # Use the Streamlit `file_uploader` function create the type of digital image files (jpg, jpeg, or png) that will be uploaded to Pinata.
    file = st.file_uploader("Add a picture of your house", type=["jpg", "jpeg", "png"])

    if st.button("List!"):

        # Use the `pin_artwork` helper function to pin the file to IPFS
        property_ipfs_hash, token_json = pin_property(address_found, user_first_name, user_last_name, user_phone, int(sell_price * 1e18), file)

        property_uri = f"ipfs://{property_ipfs_hash}"

        tx_hash = contract.functions.registerProperty(
            user_address,
            address_found,
            property_type,
            int(sell_price * 1e18),
            property_uri,
            token_json['image']
        ).transact({'from': user_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Property listed successfully!")
        with st.expander("Show registration receipt"):
            st.write(dict(receipt))
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{property_ipfs_hash})")
        st.markdown(f"[Artwork IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")

    st.markdown("---")