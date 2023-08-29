import openai
import streamlit as st
from streamlit_chat import message
# import mailparser
import docx_util
import pandas as pd
import numpy as np
import email_util
import prompts
# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


def prompt(user_input):
    try:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        # st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        cost = total_tokens * 0.002 / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

    except openai.error.InvalidRequestError:
        st.warning('Invalid Request. Restart app and try again')

# Setting page title and header

st.set_page_config(page_title="Ruth", page_icon= ":flower:")
st.markdown("<h1 style='text-align: center;'> 🤖 Ruth: RCA GENERATOR fgd🤖 </h1>", unsafe_allow_html=True)
st.markdown("""---""")


# Set org ID and API key
openai.organization = st.secrets.secrets["openai"]["organization"][0]
openai.api_key = st.secrets.secrets["openai"]["api_key"][0]


# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
# if 'model_name' not in st.session_state:
#     st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Team DATAMRK")
counter_placeholder = st.sidebar.empty()
# counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

    
model = "gpt-3.5-turbo"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    # st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


file_container = st.container()
file=False
st.markdown("##")


with file_container:
    message("Hi, My name is Ruth, please upload your email file so I can start generating your RCA! 😎", key="intro", avatar_style="bottts", seed = "Sophie")
    uploaded_file = st.file_uploader("Choose .eml file to generate Incident Timeline")
    generate_button = st.button("Generate :rocket:", key="generate",use_container_width=True)

if uploaded_file != None:
    file = True
    bytes_data = uploaded_file.getvalue()
    parsed_mail = email_util.parse_from_bytes(bytes_data)

    # INITIAL PROMPT, OTHER PROMPTS INSIDE PROMPTS.PY
    inc_timeline_prompt = f'''Shortly summarize the contents of this email one by one thread per timestamp using only one or two sentences. Summarize the contents don't just copy it. 

    {parsed_mail}
    I want your output to be a Python Dataframe like this format below.

    {prompts.inc_timeline_format}

    '''
if generate_button:
    if file is True:
        prompt(inc_timeline_prompt)



# container for chat history
response_container = st.container()
# container for text box
container = st.container()

#chat box
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        prompt(user_input)

#chat conversation
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            # message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="croodles", seed="Tigger")
            message(st.session_state["generated"][i], key=str(i), avatar_style="bottts", seed = "Sophie")
            try:
                inc_timeline_df = pd.DataFrame(eval(st.session_state["generated"][0]))
                
            except Exception as e:
                continue
    
            docx_util.build_docx(st.session_state["generated"][i])

        st.header("☢️ RCA Details")
        rca_details_button = st.button("Generate RCA Details :rocket:", key="rca_details",use_container_width=True)
        if rca_details_button:
            if file is True:
                prompt(prompts.rca_details_prompt)
                st.write(st.session_state["generated"][1])
                rca_details_df = pd.DataFrame(eval(st.session_state["generated"][1]))
                st.table(rca_details_df)


        st.subheader("☢️ Root Cause")
        st.subheader("☢️ RCA Executive Summary")
        st.subheader("☢️ Investigation & Resolution")

        st.subheader("☢️ Contributing Factors")

        st.header("☢️ Action Items")

        st.header("☢️ RCA 5 WHYs")

        st.header("☢️ Incident Timeline")
        st.table(inc_timeline_df)

        with open("output.docx", "rb") as file:
            btn = st.download_button(
                    label="Download Output File 📄",
                    data=file,
                    file_name="output.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:'Made by Team DATAMRK'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 1px;
            }
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)