import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo
import base64
from lib import ruthinit
import pandas as pd
import json

st.set_page_config(page_title="Search", page_icon= "static/ruthlogo.png")

add_logo('static/ruthsmall.png', height=100)
st.sidebar.header("Search")
image = Image.open('static/team.png')

database = ruthinit.database
container = ruthinit.container


# search_input = st.text_input('Search for incidents')
search_state = False
search_container = st.container()
items = container.read_all_items()

search_results = []
with search_container:
    with st.form(key='search', clear_on_submit=True):
        user_input = st.text_area("Search keywords", key='keyword', height=10)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        search_state = True
        for item in items:
            if user_input in json.dumps(item, indent=True):
                search_results.append(item["id"])
        
    for i in range(len(search_results)):
        existing_item = container.read_item(
        item= search_results[i],
        partition_key="61dba35b-4f02-45c5-b648-c6badc0cbd79",)
        for existing_item in existing_items:
            with st.expander(f'''Incident Name: {existing_item["incidentName"]}                                              Date Uploaded: {item["incidentDate"]}
            '''):
                search_rca_details_df = pd.DataFrame(eval(existing_item["rcaDetails"]))
                st.write("Root Cause")
                st.write(search_rca_details_df.iloc[0, 0])
                st.write("RCA Executive Summary")
                st.write(search_rca_details_df.iloc[0, 1])
                st.write("Investigation & Resolution")
                st.write(search_rca_details_df.iloc[0, 2])

                st.write("Action Items")
                search_action_items_df =  pd.DataFrame(eval(existing_item["actionItems"]))
                st.table(search_action_items_df)

                st.write("Incident Timeline")
                search_incident_timeline_df = pd.DataFrame(eval(existing_item["incidentTimeline"]))
                st.table(search_incident_timeline_df)

                st.write("RCA 5 WHYs")
                st.write(existing_item["rca5WHYs"])


if search_state is False:
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
        