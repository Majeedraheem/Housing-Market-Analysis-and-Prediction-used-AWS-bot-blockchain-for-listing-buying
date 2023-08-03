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
import math

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
    # Buy Property
    ################################################################################
    accounts = w3.eth.accounts
    st.markdown("# Buy A Property")
    tokens = contract.functions.totalSupply().call()
    # tokens = contract.functions.collectionSize().call()

    # if the collectionSize is greater than 0 then we can import the propCollection into a dictionary
    # which we'll use to create a dataframe
    prop_collection = {}

    if tokens > 0 :
        for prop in range(tokens):
            if contract.functions.propCollection(prop).call()[0] != '0x0000000000000000000000000000000000000000':
                prop_collection[prop] = {'address':contract.functions.propCollection(prop).call()[0],
                                        'geoAddress':contract.functions.propCollection(prop).call()[1],
                                        'propType':contract.functions.propCollection(prop).call()[2],
                                        'appraisalValue':contract.functions.propCollection(prop).call()[3],
                                        'propJson':contract.functions.propCollection(prop).call()[4],
                                        }
        props_df = pd.DataFrame(prop_collection).T
        selected_address = st.selectbox("Choose a property", props_df['geoAddress'])
        token_id = int(props_df.index[props_df['geoAddress'] == selected_address][0])
        st.image("https://ipfs.io/ipfs/"+contract.functions.propCollection(token_id).call()[4], caption=selected_address, width=200)
        st.write(f"Price (ETH): {math.ceil(contract.functions.propCollection(token_id).call()[3]/1e18)}")
        st.write(f"Property Type: {contract.functions.propCollection(prop).call()[2]}")
    else:
        token_id = None
        st.write("Looks like there are no listed properties. Please try back again later.")

    buyer_wallet = st.selectbox("Choose your wallet address", options=accounts)
    buy_receipt = ''
    button_stat = True if token_id==None else False
    prop_value = 0 if token_id==None else contract.functions.propCollection(token_id).call()[3]

    if st.button("Buy", disabled=button_stat):
        contract.functions.deposit().transact({'from':buyer_wallet,'value':prop_value})
        prop_owner = contract.functions.ownerOf(token_id).call()
        is_approved = contract.functions.approve(buyer_wallet, token_id).transact({'from':prop_owner})
        if is_approved:
            buy_hash = contract.functions.buyProperty(token_id).transact({'from':buyer_wallet})
            buy_receipt = w3.eth.waitForTransactionReceipt(buy_hash)
            st.write("Congratulations on your purchase!")
    with st.expander("Show purchase receipt"):
        st.write(dict(buy_receipt))