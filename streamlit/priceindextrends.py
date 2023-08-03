# Import the required libraries and dependencies
from distutils.command import build
import pandas as pd
from pathlib import Path
import hvplot.pandas
from bokeh.models.formatters import NumeralTickFormatter
#from bokeh.models.formatters import DatetimeTickFormatter
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import holoviews as hv
hv.extension('bokeh', logo=False)
import streamlit as st
from utils.Load_CSV import load_csv

#@st.cache(allow_output_mutation=True, hash_funcs={"_hvplot_pandas.plotting.Plot": lambda x: None})
def show_graph(ontario_df, building_types_selected):
    plot = ontario_df.dropna().loc[:, building_types_selected].hvplot.line(
        label="Ontario Benchmarks 2005-2023",
        xlabel="Date",
        ylabel="Composite Benchmark SA",
        rot=90,
        width=1400,
        height=500
    ).opts(
        yformatter=NumeralTickFormatter(format="0,0"),
        fontsize={
            'title': 20,
            'labels': 14,
            'xticks': 5,
            'yticks': 10,
        }
    )
    return plot

def render_page():
    #Import Federal and Provincial Data
    ontario_df = load_csv('ONTARIO.csv')

    #Set date as index 
    ontario_df = ontario_df.set_index("Date")

    #locations = ["Bancroft and Area", "Barrie And District", "Brantford", "Cambridge", "Greater Toronto", "Grey Bruce Owen Sound", "Guelph And District", "Hamilton Burlington", "Huron Perth", "Kawartha Lakes", "Kingston And Area", "Kitchener Waterloo", "Lakelands", "London St Thomas", "Mississauga", "Niagara Region", "Northumberland Hills", "North Bay", "Oakville Milton", "Ottawa", "Peterborough And Kawarthas", "Quinte And District", "Rideau St Lawrence", "Sault Ste Marie", "Simcoe And District", "Sudbury", "Tillsonburg District" , "Windsor Essex" , "Woodstock Ingersoll"]

    building_types = ['Composite_Benchmark_SA', 'Single_Family_Benchmark_SA', 'One_Storey_Benchmark_SA', 'Two_Storey_Benchmark_SA', 'Townhouse_Benchmark_SA', 'Apartment_Benchmark_SA']

    #locations_selected = st.multiselect("Locations(s)", locations, locations)
    
    building_types_selected = st.multiselect("Building Type(s)", building_types, building_types)

    if st.button("Generate Chart"):
        if building_types_selected:
    #Show graph with Benchmark prices
            st.write("# Canadian Real Estate Association (CREA) MLS® Home Price Index (HPI) Benchmarks Seasonally Adjusted")
            graph3 = show_graph(ontario_df, building_types_selected)
            st.write(hv.render(graph3, backend='bokeh'))

            st.write("Source: https://creastats.crea.ca/en-CA/")        
