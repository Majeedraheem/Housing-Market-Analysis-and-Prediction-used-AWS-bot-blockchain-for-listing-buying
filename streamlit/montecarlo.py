import streamlit as st
#import os
import pandas as pd
#import datetime as dt
#from pathlib import Path
from MCForecastTools import MCSimulation
import warnings
warnings.filterwarnings(action='ignore')
from utils.Load_CSV import load_csv

def render_page():
    #Import data
    ontario_dataset = load_csv("ONTARIO.csv").dropna()
    #Rename column to match with MCForecastTools library
    ontario_dataset.rename(columns = {'Composite_Benchmark_SA':'close'}, inplace = True)
    #Drop unneeded columns
    ontario_dataset = ontario_dataset.drop(columns=["Composite_HPI_SA", "Single_Family_HPI_SA", "One_Storey_HPI_SA", "Two_Storey_HPI_SA", "Townhouse_HPI_SA", "Apartment_HPI_SA", "Single_Family_Benchmark_SA", "One_Storey_Benchmark_SA", "Two_Storey_Benchmark_SA", "Townhouse_Benchmark_SA", "Apartment_Benchmark_SA"])
    ontario_dataset
    #Set the index to the datetime
    ontario_dataset = ontario_dataset.set_index("Date")
    ontario_dataset.index = pd.to_datetime(ontario_dataset.index)
    ontario_dataset
    #Concatenate the data to be consumed by the library
    concat = pd.concat([ontario_dataset], axis=1, keys=["Benchmark1"]).dropna()
    concat
    #InitiaL the Monte Carlo simulation

    years = st.number_input("Years", min_value=1, max_value=10, value =2, step=1)

    num_simulations = st.number_input("Number of Simulations", min_value=1, max_value=1000, value =500, step=1)

    initial_investment = st.number_input("Initial Investment", min_value=1, max_value=100000000, value =1000000, step=1)

    if st.button("Generate Chart"):
        #years = 10 
        MC_10_year = MCSimulation(
            portfolio_data = concat, 
            weights =[1], 
            num_simulation = num_simulations, 
            num_trading_days= 12 * years # Note: Our data is monthly not daily
        )
        #Run the Monte Carlo simulation
        MC_10_year.calc_cumulative_return()

        #Show the plot of the Monte Carlo simulation
        #MC_10_year.plot_simulation()
           
        st.header(f"{years} Year Monte Carlo Simulations")

        st.line_chart(MC_10_year.plot_simulation_dataframe())

        #Calculcate the summary data
        tbl = MC_10_year.summarize_cumulative_return()
        print(tbl)
        #Analysis of the data
        #initial_investment = 1000000

        ci_lower = round(tbl[8]*initial_investment,2)
        ci_upper = round(tbl[9]*initial_investment,2)

        print(f"There is a 95% chance that an initial real estate investment of ${initial_investment:,}"
            f" over the next {years} years will end within in the range of"
            f" ${ci_lower:,} and ${ci_upper:,}")
        text = f"There is a 95% chance that an initial real estate investment of \${initial_investment:,} over the next {years} years will end within in the range of \${ci_lower:,} and \${ci_upper:,}"
        st.write(text)

        st.write("Source: https://creastats.crea.ca/en-CA/")
