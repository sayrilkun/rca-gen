import mailparser
import streamlit as st
def parse_from_bytes (bytes_data):
    mail = mailparser.parse_from_bytes(bytes_data)
    return mail.text_plain