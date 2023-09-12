import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo
import base64
from lib import ruthinit

st.set_page_config(page_title="Search", page_icon= "static/ruthlogo.png")

add_logo('static/ruthsmall.png', height=100)
st.sidebar.header("Search")
image = Image.open('static/team.png')

database = ruthinit.database
container = ruthinit.container


title = st.text_input('Search for incidents')

# for i in range(5):
#     with st.expander(f"Incident #{i+1}"):
#         st.write(f"Incident #{i+1}""")
#         st.image("https://static.streamlit.io/examples/dice.jpg")

items = container.read_all_items()
for item in items:
    with st.expander(f'''Incident Name: {item["incidentName"]}
    Date Uploaded: {item["incidentDate"]}
    Uploaded by: {item["uploader"]}
    
    '''):
        st.write("RCA 5 WHYs")
        st.write(item["rca5WHYs"])
        
    # print(json.dumps(item["id"], indent=True))