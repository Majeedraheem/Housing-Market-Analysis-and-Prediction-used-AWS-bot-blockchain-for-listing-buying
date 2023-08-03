import streamlit as st
import pandas as pd
import requests
from io import StringIO

@st.cache
def load_csv(name):
    url = 'https://raw.githubusercontent.com/JamieMellway/FintechBootcampProject3/main/streamlit/Resources/' + name
    response = requests.get(url)
    data = StringIO(response.text)
    csv = pd.read_csv(data)
    return csv.copy(deep=True)

@st.cache
def load_csv_with_Dates(name):
    url = 'https://raw.githubusercontent.com/JamieMellway/FintechBootcampProject3/main/streamlit/Resources/' + name
    response = requests.get(url)
    data = StringIO(response.text)
    csv = pd.read_csv(data, infer_datetime_format=True, parse_dates=True, index_col='Date')
    return csv.copy(deep=True)
