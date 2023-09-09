#
# Initialization
#
from distutils.command.upload import upload
import email
import sys
sys.path.append('./lib/')

#
# Imports
#
import openai
import streamlit as st
from streamlit_chat import message
from lib import docx_util
import pandas as pd
import numpy as np
import email_util
import prompts
from lib import ruthinit
from lib import filechecker
from lib import email_parser

#
# Globals
#
log = ruthinit.log
file = False

# Generate a response
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

# Open AI API Function
def prompt(user_input):
    try:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        log.info("AI responded")
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        try:
            log.info(st.session_state['generated'][1])
        except Exception as e:
            log.info(st.session_state['generated'][0])
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
st.markdown("<h1 style='text-align: center;'> 🤖 Ruth: RCA GENERATOR🤖 </h1>", unsafe_allow_html=True)
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

# Set model
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
    uploaded_file = st.file_uploader("Choose .eml file to generate Incident Timeline", type=['.eml', '.msg'])
    generate_button = st.button("Generate :rocket:", key="generate",use_container_width=True)

# INITIAL PROMPT (incident time line)
if uploaded_file != None:
    log.info(uploaded_file)

    ext = filechecker.GetFileExtension(uploaded_file.name)
    log.info(f"extension {ext}")

    if ext == '.eml':
        file = True
        log.info("Processing eml file")
        bytes_data = uploaded_file.getvalue()
        parsed_mail = email_util.parse_from_bytes(bytes_data)

    elif ext == '.msg': #v2 of parsing .msg
        file = True
        log.info("processing msg file")
        parsed_mail = email_parser.convert_msg_to_text(uploaded_file)

    # elif ext == '.msg':
    #     file = True
    #     eml = email_parser.convert_msg_to_eml(uploaded_file)
    #     parsed_mail = email_util.parse_from_bytes(eml.as_bytes())

    # INITIAL PROMPT, OTHER PROMPTS INSIDE PROMPTS.PY
    inc_timeline_prompt = f'''Shortly summarize the contents of this email one by one thread per timestamp using only one or two sentences. Summarize the contents don't just copy it. 

    {parsed_mail}
    Can you please follow this format (No special characters no \\n or whatever):

    {prompts.inc_timeline_format}

    '''
# IF BUTTON IS CLICKED
if generate_button:
    if file is True:
        log.info("Sending Message")
        log.info(inc_timeline_prompt)
        prompt(inc_timeline_prompt)
        # file = False

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
            # HIDING THE CHATBOX
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="croodles", seed="Tigger")
            message(f'XX{i}XX {st.session_state["generated"][i]} ', key=str(i), avatar_style="bottts", seed = "Sophie")
            log.info(st.session_state['generated'])
            try:
                # CONVERT THE RESPONSE TO DATAFRAME
                inc_timeline_df = pd.DataFrame(eval(st.session_state["generated"][0]))
                
            except Exception as e:
                pass

            # WRITE THE RESPONSE TO WORD DOCUMENT
            # docx_util.build_word_document(eval(st.session_state["generated"][0]))

            # SECOND PROMPT (RCA DETAILS)
        st.header("☢️ RCA Details")
        rca_details_button = st.button("Generate RCA Details :rocket:", key="rca_details",use_container_width=True)
        if rca_details_button:
            # if file is True:
            prompt(prompts.rca_details_prompt)
        #     st.write(st.session_state["generated"][1])
        #     try:
        #         rca_details_df = pd.DataFrame(eval(st.session_state["generated"][1]))
        #         # st.table(rca_details_df)

        #         st.subheader("☢️ Root Cause")
        #         st.success(rca_details_df.iloc[0, 0])

        #         st.subheader("☢️ RCA Executive Summary")
        #         st.success(rca_details_df.iloc[0, 1])

        #         st.subheader("☢️ Investigation & Resolution")
        #         st.success(rca_details_df.iloc[0, 2])

        #         st.subheader("☢️ Contributing Factors")
            
        #     except Exception as e:
        #         pass

        #     # file = False

        # st.header("☢️ Action Items")
        # action_items_button = st.button("Generate Action Items :rocket:", key="action_items",use_container_width=True)
        # if action_items_button:
        #     prompt(prompts.action_items_prompt)
        #     st.write(st.session_state["generated"][2])
        #     try:
        #         action_items_df = pd.DataFrame(eval(st.session_state["generated"][2]))
        #         st.table(action_items_df)
        #     except Exception as e:
        #             pass

        # st.header("☢️ RCA 5 WHYs")
        # five_whys_button = st.button("Generate 5 WHYs :rocket:", key="five_whys",use_container_width=True)
        # if five_whys_button:
        #     prompt(prompts.five_whys_prompt)
        #     st.write(st.session_state["generated"][3])

        st.header("☢️ Incident Timeline")
        try:
            st.table(inc_timeline_df)
        except Exception as e:
            st.write(st.session_state["generated"][0])

        # DOWNLOAD THE WORD FILE
        with open("output.docx", "rb") as file:
            btn = st.download_button(
                    label="Download Output File (DOCX) 📄",
                    data=file,
                    file_name="output.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

action_items_button = st.button("Generate Action Items :rocket:", key="action_items",use_container_width=True)
if action_items_button:
    prompt(prompts.action_items_prompt)
    # prompt("hi")
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
