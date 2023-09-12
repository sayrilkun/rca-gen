import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo
import base64
from lib import ruthinit
import pandas as pd

st.set_page_config(page_title="Search", page_icon= "static/ruthlogo.png")

add_logo('static/ruthsmall.png', height=100)
st.sidebar.header("Search")
image = Image.open('static/team.png')

database = ruthinit.database
container = ruthinit.container


title = st.text_input('Search for incidents')


items = container.read_all_items()
for item in items:
    with st.expander(f'''Incident Name: {item["incidentName"]}                                              Date Uploaded: {item["incidentDate"]}
    '''):
        search_rca_details_df = pd.DataFrame(eval(item["rcaDetails"]))
        st.write("Root Cause")
        st.write(search_rca_details_df.iloc[0, 0])
        st.write("RCA Executive Summary")
        st.write(search_rca_details_df.iloc[0, 1])
        st.write("Investigation & Resolution")
        st.write(search_rca_details_df.iloc[0, 2])

        st.write("Action Items")
        search_action_items_df =  pd.DataFrame(eval(item["actionItems"]))
        st.table(search_action_items_df)

        st.write("Incident Timeline")
        search_incident_timeline_df = pd.DataFrame(eval(item["incidentTimeline"]))
        st.table(search_incident_timeline_df)
        
        st.write("RCA 5 WHYs")
        st.write(item["rca5WHYs"])
        