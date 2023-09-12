import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo
import base64

st.set_page_config(page_title="About Us", page_icon= "static/ruthlogo.png")

add_logo('static/ruthsmall.png', height=100)
st.sidebar.header("Meet the Team")
image = Image.open('static/team.png')

#st.write('Team DATAMRK')
st.image(image,caption=' ')