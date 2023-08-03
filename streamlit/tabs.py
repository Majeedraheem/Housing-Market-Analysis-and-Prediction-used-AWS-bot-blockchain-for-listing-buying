import streamlit as st
st.set_page_config(layout="wide")
#from MultiApp import MultiApp
import PriceIndexTrends 
import Geolocation
#import MonteCarlo

def use_tabs():
    listTabs = ["Trends", "Geolocation", "Monte Carlo", "Machine Learning", "Chat Bot"]
    whitespace = 28
    tab1, tab2, tab3, tab4, tab5 = st.tabs([s.center(whitespace,"\u2001") for s in listTabs])

    with tab1:
       PriceIndexTrends.render_page()

    with tab2:
       Geolocation.render_page()

    with tab3:
        st.header("Monte Carlo")
        #MonteCarlo.render_page()

    with tab4:
      st.header("Machine Learning")
    
    with tab5:
      st.header("Chat Bot")

def main():
    use_tabs();

if __name__ == '__main__':
    main()