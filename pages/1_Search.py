import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo
import base64

st.set_page_config(page_title="Search", page_icon= "static/ruthlogo.png")

add_logo('static/ruthsmall.png', height=100)
st.sidebar.header("Search")
image = Image.open('static/team.png')

#st.write('Team DATAMRK')
# st.image(image,caption=' ')

title = st.text_input('Search for incidents')
# st.write('The current movie title is', title)

for i in range(5):
    with st.expander(f"Incident #{i+1}"):
        st.write(\"\"\"
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        \"\"\")
        st.image("https://static.streamlit.io/examples/dice.jpg")