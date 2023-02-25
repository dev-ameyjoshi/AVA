import requests
import streamlit as st
import PyPDF2
import re

def correct_grammar(text):
    url = "https://v1.genr.ai/api/circuit-element/correct-grammar"
    payload = {
        "text": text,
        "temperature": 0
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, json=payload)
    return response.json()['output']

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

job_title = "Software Engineer"

st.title(job_title + " Application Form")

name = st.text_input('Your Name')

email = st.text_input('Your Email')

number = st.text_input("Your Phone Number", max_chars=15)

resume = st.file_uploader("Your Resume(PDF)", type=['pdf'])

if st.button('Submit') and name and re.match(email_regex, email) and number.isnumeric() and resume:
    name = name.strip()
    email = email.strip()
    number = number.strip().replace(" ", "")

    pdfReader = PyPDF2.PdfReader(resume)

    candidate_info = ""

    for page in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[page]
        candidate_info += pageObj.extract_text()

    # divide the candidate info into chunks of 750*5 characters
    candidate_info_chunks = [candidate_info[i:i+750*5] for i in range(0, len(candidate_info), 750*5)]

    # correct the grammar of each chunk
    for i in range(len(candidate_info_chunks)):
        candidate_info_chunks[i] = correct_grammar(candidate_info_chunks[i])

    st.write(candidate_info_chunks)