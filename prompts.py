inc_timeline_format =     [
{
    "Date" : "18-November-22",
    "Time" : "22:00",
    "Contents" : "Summary of the email,"
    
},
    {
    "Date" : "21-November-22",
    "Time" : "12:00",
    "Contents" : "Summary of the email,"
    
}
]

#WORKING PROMPT
# rca_details_format = [
#     {
#         "Root Cause" : "Root Cause",
#         "RCA Executive Summary" : "RCA Executive Summary"
#     }]


# rca_details_prompt = f''' You are an Incident Analyst. 
# Identify the Root cause of the incident and make a lengthy executive summary, minimum 2 paragraphs based on the 
# given email thread. Include important events happened in the thread in your executive summary.

# I want your output to be a Python Dataframe like this format below.

# {rca_details_format}

# '''

rca_details_format = [
    {
        "Root Cause" : "Answer #1",
    },
    {
        "RCA Executive Summary" : "Answer #2"
    },
    {
        "Investigation and Resolution" : "Answer #3",
    },
    {
        "Contributing Factors" : "Answer #4"
    }
    ]
rca_details_prompt = f''' You are an Incident Analyst. I want you to answer 3 things for me based on your profession.

1. Identify the Root cause of the incident 
2. Generate a lengthy executive summary, minimum 2 paragraphs, based on the given email thread. Include important events happened in the thread in your executive summary.
3. What are the key dates that leads to investigation and resolution. Explain each dates.
4. What are the factors that contributed to the existing issue.

Please strictly follow the format below, do not create another brace. Please don't put apostrophe in your response please.

{rca_details_format}

Not multiple instance of braces just put all of them in one

'''

# SHOULD INCLUDE THIS IN RCA DETAILS SECTION, BUT RESPONSE IS ALWAYS GETTING CUT OFF 
# PROBABLY IT CANT HANDLE SUPER LONG RESPONSES. HOPEFULLY AZURE CAN DO IT.
# IF NOT, CREATE A PROMPT SEPARATELY

# "Contributing Factors" : "Answer #4"
# 4. What are the factors that contributed to the existing issue.

action_items_format = [{
    "Actions" : "Actions",
    "Description" : "Description",
    "Owner" : "Owner",
    "Date" : "21-November-22",
    "Status" : "Status"
    },
    {
    "Actions" : "Actions",
    "Description" : "Description",
    "Owner" : "Owner",
    "Date" : "21-November-22",
    "Status" : "Status"
    }
]

action_items_prompt = f''' Identify the Action Items based on the analysis of the given email thread. Follow below categories

For Actions, identify whether it is Diagnostic, Inquiry, Test, or Implementation.
Give some description. Identify the owner, the date when it started and the status if completed or not.

Can you please follow this format (No special characters no \\n or whatever):
{action_items_format}

'''

five_whys_prompt = f''' Generate a 5 whys analysis based on the given email thread. List in butllet form'''
