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
        "RCA Executive Summary" : "Answer #2",
        "Investigation and Resolution" : "Answer #3",
        "Contributing Factors" : "Answer #4"
    }]
rca_details_prompt = f''' You are an Incident Analyst. I want you to answer 4 things for me based on your profession.

1. Identify the Root cause of the incident 
2. Generate a lengthy executive summary, minimum 2 paragraphs, based on the given email thread. Include important events happened in the thread in your executive summary.
3. What are the key dates that leads to investigation and resolution. Explain each dates.
4. What are the factors that contributed to the existing issue.

I want your output to be a Python Dataframe like this format below. Do not cut off the response.

{rca_details_format}

'''