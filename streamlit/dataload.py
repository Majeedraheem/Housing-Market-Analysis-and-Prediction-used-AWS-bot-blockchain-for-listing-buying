# importing libraries
import streamlit as st
#import numpy as np
import pandas as pd
from pathlib import Path
import hvplot.pandas
from bokeh.models.formatters import NumeralTickFormatter
import holoviews as hv
hv.extension('bokeh', logo=False)
from utils.Load_CSV import load_csv
from utils.Load_CSV import load_csv_with_Dates

small_date_fontsize = {
            'title': 20, 
            'labels': 14, 
            'xticks': 5, 
            'yticks': 10,
        }
plot_height = 600
plot_width = 1200

def graph_all_regions(all_regions_df):
    plot = all_regions_df.hvplot.line(
        x='Date', 
        xlabel='Date', 
        ylabel='Price Index', 
        title='Benchmarks (All Ontario Regions)',
        rot=90,
        height=plot_height,
        width=plot_width,
        legend=False
    ).opts(
        fontsize=small_date_fontsize,
        yformatter=NumeralTickFormatter(format="0,0")
    )
    return plot

def import_region_data(path):
    file = Path(path)
    region_name = file.name.split('.')[0]
    #region_data_df = pd.read_csv(file, infer_datetime_format=True, parse_dates=True, index_col='Date')
    region_data_df = load_csv_with_Dates(path).copy()
    region_data_df.index = region_data_df.index.strftime('%Y-%m')
    # region_data_df['Region'] = region_name
    region_cols = region_data_df.columns.tolist()
    region_cols[0]
    region_cols_adj = [cols for cols in region_cols if cols.find('HPI') < 0]
    region_data_df = region_data_df[region_cols_adj]
    # region_cols_rename = [{col:col+'_'+region_name} 
    for col in region_data_df.columns.tolist():
        # region_data_df.rename(columns=region_cols_rename[0], inplace=True)
        region_data_df.rename(columns={col:col+'_'+region_name}, inplace=True)
    return region_data_df

def render_page():

    st.header("Objective")
    st.write("We want to create a Machine Learning model that uses CREA data to train our data and use several inputs to generate new data.")

    st.header("Training Data (CREA)")

    ontario_df = import_region_data('ONTARIO.csv')
    bancroft_df = import_region_data('BANCROFT_AND_AREA.csv')
    barrie_df = import_region_data('BARRIE_AND_DISTRICT.csv')
    brantford_df = import_region_data('BRANTFORD_REGION.csv')
    cambridge_df = import_region_data('CAMBRIDGE.csv')
    toronto_df = import_region_data('GREATER_TORONTO.csv')
    grey_bruce_owen_sound_df = import_region_data('GREY_BRUCE_OWEN_SOUND.csv')
    guelph_df = import_region_data('GUELPH_AND_DISTRICT.csv')
    hamilton_burlington_df = import_region_data('HAMILTON_BURLINGTON.csv')
    huron_perth_df = import_region_data('HURON_PERTH.csv')
    kawartha_df = import_region_data('KAWARTHA_LAKES.csv')
    kingston_df = import_region_data('KINGSTON_AND_AREA.csv')
    kitchener_waterloo_df = import_region_data('KITCHENER_WATERLOO.csv')
    lakelands_df = import_region_data('LAKELANDS.csv')
    london_st_thomas_df = import_region_data('LONDON_ST_THOMAS.csv')
    mississauga_df = import_region_data('MISSISSAUGA.csv')
    niagara_df = import_region_data('NIAGARA_REGION.csv')
    northbay_df = import_region_data('NORTH_BAY.csv')
    northumberland_df = import_region_data('NORTHUMBERLAND_HILLS.csv')
    oakville_milton_df = import_region_data('OAKVILLE_MILTON.csv')
    ottawa_df = import_region_data('OTTAWA.csv')
    peterborough_kawarthas_df = import_region_data('PETERBOROUGH_AND_KAWARTHAS.csv')
    quinte_df = import_region_data('QUINTE_AND_DISTRICT.csv')
    rideau_df = import_region_data('RIDEAU_ST_LAWRENCE.csv')
    ss_marie_df = import_region_data('SAULT_STE_MARIE.csv')
    simcoe_df = import_region_data('SIMCOE_AND_DISTRICT.csv')
    sudbury_df = import_region_data('SUDBURY.csv')
    tillsonburg_df = import_region_data('TILLSONBURG_DISTRICT.csv')
    windsor_df = import_region_data('WINDSOR_ESSEX.csv')
    woodstock_df = import_region_data('WOODSTOCK_INGERSOLL.csv')

    all_regions = [bancroft_df, barrie_df, brantford_df, cambridge_df, toronto_df, grey_bruce_owen_sound_df, guelph_df, hamilton_burlington_df, huron_perth_df, kawartha_df, kingston_df, kitchener_waterloo_df,
               lakelands_df, london_st_thomas_df, mississauga_df, niagara_df, northbay_df, northumberland_df, oakville_milton_df, ontario_df, ottawa_df, peterborough_kawarthas_df, quinte_df, rideau_df,
               ss_marie_df, simcoe_df, sudbury_df, tillsonburg_df, windsor_df, woodstock_df
              ]
    ontario_df.head()

    all_regions_df = pd.concat(all_regions, axis=1)
    all_regions_df.head()

    all_regions_df.drop_duplicates(inplace=True)
    all_regions_df.dropna()
    
    benchmark_plot = graph_all_regions(all_regions_df)
    #benchmark_plot

    st.write(hv.render(benchmark_plot, backend='bokeh'))
    st.write("Source: https://creastats.crea.ca/en-CA/")

    st.header("Sources of data")

    lumber_df = load_csv("lumber-prices-historical-chart-data.csv").copy(deep=True)
    lumber_df['date'] = pd.to_datetime(lumber_df['date'])
    lumber_df.set_index('date', inplace=True)
    lumber_grouped_df = lumber_df.groupby(pd.Grouper(freq="M")).max()
    lumber_grouped_df.index = lumber_grouped_df.index.strftime('%Y-%m')
    lumber_grouped_df = lumber_grouped_df.rename(columns={' value': 'value'})

    lumber_grouped_df.head()

    lumber_plot = lumber_grouped_df["value"].hvplot.line(
        x='date', 
        y='value', 
        xlabel='Date', 
        ylabel='Price', 
        title='Macrotrends Lumber Prices - 50 Year Historical Chart',
        line_color='blue',
        rot=90,
        height=plot_height,
        width=plot_width
    ).opts(
        fontsize=small_date_fontsize,
        yformatter=NumeralTickFormatter(format="0,0")
    )
    lumber_plot
    st.write(hv.render(lumber_plot, backend='bokeh'))
    st.write("Source: https://www.macrotrends.net/2637/lumber-prices-historical-chart-data")

    wood_df = load_csv('WOOD.csv').copy()
    wood_df['Date'] = pd.to_datetime(wood_df['Date'])
    wood_df.set_index('Date', inplace=True)
    wood_grouped_df = wood_df.groupby(pd.Grouper(freq="M")).max()
    wood_grouped_df.index = wood_grouped_df.index.strftime('%Y-%m')

    wood_grouped_df.head()

    wood_plot = wood_grouped_df["Close"].hvplot.line(
        x='Date', 
        y='Close', 
        xlabel='Date', 
        ylabel='Price', 
        title='iShares Global Timber & Forestry ETF',
        line_color='blue',
        rot=90,
        height=plot_height,
        width=plot_width
    ).opts(
        fontsize=small_date_fontsize,
        yformatter=NumeralTickFormatter(format="0,0")
    )
    wood_plot
    st.write(hv.render(wood_plot, backend='bokeh'))
    st.write("Source: https://finance.yahoo.com/quote/ITB/history?p=WOOD")

    xhb_df = load_csv('XHB.csv').copy()
    xhb_df['Date'] = pd.to_datetime(xhb_df['Date'])
    xhb_df.set_index('Date', inplace=True)
    xhb_grouped_df = xhb_df.groupby(pd.Grouper(freq="M")).max()
    xhb_grouped_df.index = xhb_grouped_df.index.strftime('%Y-%m')

    xhb_grouped_df.head()

    xhb_plot = xhb_grouped_df["Close"].hvplot.line(
        x='Date', 
        y='Close', 
        xlabel='Date', 
        ylabel='Price', 
        title='SPDR S&P Homebuilders ETF',
        line_color='blue',
        rot=90,
        height=plot_height,
        width=plot_width
    ).opts(
        fontsize=small_date_fontsize,
        yformatter=NumeralTickFormatter(format="0,0")
    )
    xhb_plot
    st.write(hv.render(xhb_plot, backend='bokeh'))
    st.write("Source: https://finance.yahoo.com/quote/ITB/history?p=XHB")

    itb_df = load_csv('ITB.csv').copy()
    itb_df['Date'] = pd.to_datetime(itb_df['Date'])
    itb_df.set_index('Date', inplace=True)
    itb_grouped_df = itb_df.groupby(pd.Grouper(freq="M")).max()
    itb_grouped_df.index = itb_grouped_df.index.strftime('%Y-%m')

    itb_grouped_df.head()

    itb_plot = itb_grouped_df["Close"].hvplot.line(
        x='Date', 
        y='Close', 
        xlabel='Date', 
        ylabel='Price', 
        title='iShares U.S. Home Construction ETF',
        line_color='blue',
        rot=90,
        height=plot_height,
        width=plot_width
    ).opts(
        fontsize=small_date_fontsize,
        yformatter=NumeralTickFormatter(format="0,0")
    )
    itb_plot
    st.write(hv.render(itb_plot, backend='bokeh'))
    st.write("Source: https://finance.yahoo.com/quote/ITB/history?p=ITB")

    #pd.read_csv(Path("Resources/1810000601-noSymbol.csv")).T.to_csv('Resources/consumerpriceindex_formatted_t.csv', header=False)
    column_header = 'Products and product groups 7'
    cpi_df = load_csv('consumerpriceindex_formatted_t.csv').copy()
    cpi_df[column_header] = pd.to_datetime(cpi_df[column_header], format='%b-%y')
    cpi_df.set_index(column_header, inplace=True)
    cpi_df.index = cpi_df.index.strftime('%Y-%m')

    cpi_df.head()

    cpi_plot = cpi_df.hvplot.line(
        x=column_header, 
        #y='VALUE',
        xlabel='Date', 
        ylabel='Price', 
        title='Consumer Price Index',
        rot=90,
        height=plot_height,
        width=plot_width,
        legend=False
    ).opts(
        fontsize=small_date_fontsize,
        yformatter=NumeralTickFormatter(format="0,0")
    )
    cpi_plot
    st.write(hv.render(cpi_plot, backend='bokeh'))
    st.write("Source: https://www150.statcan.gc.ca/")

    ir = load_csv('bankrate.csv').copy()
    ir['Rates'] = pd.to_datetime(ir['Rates'], format='%b-%y')
    ir.set_index('Rates', inplace=True)
    ir.index = ir.index.strftime('%Y-%m')

    ir_plot = ir["Bank rate"].hvplot.line(
        x='Rates', 
        y='Bank rate', 
        xlabel='Date', 
        ylabel='Price', 
        title='Bank Rate',
        line_color='blue',
        rot=90,
        height=plot_height,
        width=plot_width
    ).opts(
        fontsize=small_date_fontsize,
        yformatter=NumeralTickFormatter(format="0,0")
    )
    ir_plot
    st.write(hv.render(ir_plot, backend='bokeh'))
    st.write("Source: https://www150.statcan.gc.ca/")
    
    
    # ir = pd.read_csv(Path("Resources/lookup.csv"))
    # st.write(ir)
    
    # ir['Date'] = pd.to_datetime(ir['Date'], format='%b-%y')
    # ir.set_index('Date', inplace=True)
    # ir_grouped_df = ir.groupby(pd.Grouper(freq="M")).last()
    # ir_grouped_df = ir_grouped_df.resample('M').last().ffill()
    # new_date_range = pd.date_range(start='2004-01-01', end='2023-07-30', freq='M')
    # ir_grouped_df = ir_grouped_df.reindex(new_date_range).ffill()
    # ir_grouped_df.index = ir_grouped_df.index.strftime('%Y-%m')

    # ir_grouped_df.tail()

    # ir_plot = ir_grouped_df["V122530"].hvplot.line(
    #     x='Date', 
    #     y='V122530', 
    #     xlabel='Date', 
    #     ylabel='Price', 
    #     title='Bank Rate',
    #     line_color='blue',
    #     rot=90,
    #     height=plot_height,
    #     width=plot_width
    # ).opts(
    #     fontsize=small_date_fontsize,
    #     yformatter=NumeralTickFormatter(format="0,0")
    # )
    # ir_plot
    # st.write(hv.render(ir_plot, backend='bokeh'))
    # st.write("Source: https://www150.statcan.gc.ca/")

    #st.write(ir["Bank rate"])

    #most_values = pd.concat([all_regions_df, lumber_grouped_df, wood_grouped_df["Close"], xhb_grouped_df["Close"], itb_grouped_df["Close"], ir["Bank rate"]], axis = 1, join = 'inner')
    #cols = all_regions_df.columns.tolist()
    #cols.extend(['Lumber', 'Wood', 'XHB', 'ITB', "Bank rate"])
    #most_values.columns = cols
    
    #st.write("Most Values")
    #st.write(most_values)

    #all_values = pd.concat([most_values, cpi_df], axis =1 , join = 'inner')

    #all_values

    #all_values.index.name = 'date'

    #st.write("All Values")
    #st.write(all_values)

    #all_values.to_csv('Resources/all_values_superset.csv', index=True)
