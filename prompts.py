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

rca_details_format = [
    {
        "Root Cause" : "Root Cause",
        "RCA Executive Summary" : "RCA Executive Summary"
    }
]

rca_details_prompt = f''' You are an Incident Analyst. Identify the Root cause of the incident make an executive summary based on the given email thread. 

I want your output to be a Python Dataframe like this format below.

{rca_details_format}

'''