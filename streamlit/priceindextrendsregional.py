# Import the required libraries and dependencies
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
import requests
from io import StringIO

def load_csv(name):
    url = 'https://raw.githubusercontent.com/JamieMellway/FintechBootcampProject3/main/streamlit/Resources/' + name
    response = requests.get(url)
    data = StringIO(response.text)
    return pd.read_csv(data)

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
        #Show graph with Benchmark prices
        st.write("# Show graph with Benchmark prices")
        graph3 = ontario_df.dropna().loc[:, building_types_selected].hvplot.line(
            label="Ontario Benchmarks 2005-2023",
            xlabel="Date",
            ylabel="Composite Benchmark SA",
            rot=90,
            width=1400,
            height = 500
        ).opts(
            yformatter=NumeralTickFormatter(format="0,0"),
            fontsize={
                'title': 20, 
                'labels': 14, 
                'xticks': 5, 
                'yticks': 10,
            }
        )
        st.write(hv.render(graph3, backend='bokeh'))

    # #Show graph of Ontario Composite HPI for 2005-2023
    # st.write("# Show graph of Ontario Composite HPI for 2005-2023")
    # graph1=ontario_df["Composite_HPI_SA"].dropna().hvplot.line(
    #     label="Ontario Composite House Price Index 2005-2023",
    #     xlabel="Date",
    #     ylabel="Composite House Price Index",
    #     rot=90,
    #     width=1400,
    #     height = 500
    # ).opts(
    #     yformatter=NumeralTickFormatter(format="0,0"),
    #     fontsize={
    #         'title': 20, 
    #         'labels': 14, 
    #         'xticks': 5, 
    #         'yticks': 10,
    #     }
    # )
    # st.write(hv.render(graph1, backend='bokeh'))

    # #Show graph of all House Price Indicies
    # st.write("# Show graph of all House Price Indicies")
    # graph2 = ontario_df.dropna().loc[:, ['Composite_HPI_SA', 'Single_Family_HPI_SA', 'One_Storey_HPI_SA', 'Two_Storey_HPI_SA', 'Townhouse_HPI_SA', 'Apartment_HPI_SA']].hvplot.line(
    #     label="Ontario HPI 2005-2023",
    #     xlabel="Date",
    #     ylabel="Composite Benchmark SA",
    #     rot=90,
    #     width=1400,
    #     height = 500
    # ).opts(
    #     yformatter=NumeralTickFormatter(format="0,0"),
    #     fontsize={
    #         'title': 20, 
    #         'labels': 14, 
    #         'xticks': 5, 
    #         'yticks': 10,
    #     }
    # )
    # st.write(hv.render(graph2, backend='bokeh'))

    # #Show graph with Benchmark prices
    # st.write("# Show graph with Benchmark prices")
    # graph3 = ontario_df.dropna().loc[:, ['Composite_Benchmark_SA', 'Single_Family_Benchmark_SA', 'One_Storey_Benchmark_SA', 'Two_Storey_Benchmark_SA', 'Townhouse_Benchmark_SA', 'Apartment_Benchmark_SA']].hvplot.line(
    #     label="Ontario Benchmarks 2005-2023",
    #     xlabel="Date",
    #     ylabel="Composite Benchmark SA",
    #     rot=90,
    #     width=1400,
    #     height = 500
    # ).opts(
    #     yformatter=NumeralTickFormatter(format="0,0"),
    #     fontsize={
    #         'title': 20, 
    #         'labels': 14, 
    #         'xticks': 5, 
    #         'yticks': 10,
    #     }
    # )
    # st.write(hv.render(graph3, backend='bokeh'))