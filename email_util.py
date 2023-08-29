import mailparser
import streamlit as st
def parse_from_bytes (bytes_data):
    mail = mailparser.parse_from_bytes(bytes_data)
    st.write(mail.text_plain)
    return mail.text_plain