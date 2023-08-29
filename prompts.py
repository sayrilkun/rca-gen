sample_format =     [
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
instruction = f'''Shortly summarize the contents of this email one by one thread per timestamp using only one or two sentences. Summarize the contents don't just copy it. 

{mail.text_plain}

I want your output to be a Python Dataframe like this format below.

{sample_format}

'''
