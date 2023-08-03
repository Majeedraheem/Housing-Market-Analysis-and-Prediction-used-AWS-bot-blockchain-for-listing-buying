import streamlit as st
st.set_page_config(layout="wide")
from utils.MultiApp import MultiApp
import priceindextrends 
import montecarlo
import dataload
import machinelearning
import chatbot
import platform
import unittests
if platform.system() == 'Windows':
    import geolocation
    import chatbotdemo

def titlepage():
    st.header("Ontario Housing Market Analysis")
    st.write("Project 1: Using Canadian Real Estate Association data to predict market (using Monte Carlo).")
    st.write("Project 2: Create a Machine Learning model that uses CREA data to train our data and use several inputs to generate new data.  Chat bot to look up data.")
    st.write("Project 3: Create a website that lets users list and buy real estate properties.")

def whatsnext():
    st.header("What's Next")
    st.write("All of Canada - Not just Ontario")
    st.write("Auction selling")
    st.write("Marketplace")
    st.write("Chatbot give listing for a particular region and building type")

def technologiesused():
    st.header("Technologies Used")
    st.text("Python")
    st.text("Pandas")
    st.text("Tensorflow")
    st.text("Keras")
    st.text("Streamlit")
    st.text("Streamlit-Chat")
    st.text("boto3")
    st.text("web3")
    st.text("Ganche")
    st.text("Remix")
    st.text("Solidity")
    st.text("OpenZeppelin")
    st.text("hvplot")
    st.text("Scikit-Learn")
    st.text("Requests")
    st.text("unittests")

def main(): 
    app = MultiApp()
    app.add_app("Title", titlepage)
    #app.add_app("Technologies Used", technologiesused)
    app.add_app("Trends (Ontario)", priceindextrends.render_page)
    #app.add_app("Trends (Regional)", priceindextrendsregional.render_page)
    if platform.system() == 'Windows':
        app.add_app("Geolocation", geolocation.render_page)
    app.add_app("Monte Carlo", montecarlo.render_page)
    app.add_app("Machine Learning - Data Load", dataload.render_page)
    app.add_app("Machine Learning", machinelearning.render_page)
    if platform.system() == 'Windows':
        app.add_app("Chat Bot", chatbotdemo.render_page)
    app.add_app("Property Value", chatbot.render_page)
    app.add_app("Unit Tests", unittests.render_page)
    #app.add_app("What's Next", whatsnext)
    
    # The main app
    app.run()

if __name__ == '__main__':
    main()