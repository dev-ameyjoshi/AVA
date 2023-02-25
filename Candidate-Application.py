from gtts import gTTS
import requests
import streamlit as st
import PyPDF2
import os
import re
import shutil

from email.mime.application import MIMEApplication
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def send_email(receiver):
    subject = "Application Status Update"
    email_message = '''You can proceed for interview round
    follow the link to proceed http://localhost:8502'''
    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message['From'] = Header('vishwasocialmail@gmail.com')
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message, 'plain', 'utf-8'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login('vishwasocialmail@gmail.com', 'kuqsidknooumncji')
    text = message.as_string()
    server.sendmail('vishwasocialmail@gmail.com', receiver, text)
    server.quit()

def correct_grammar(text):
    url = "https://v1.genr.ai/api/circuit-element/correct-grammar"
    payload = {
        "text": text,
        "temperature": 0
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, json=payload)
    return response.json()['output']


def generate_questions(text):
    url = "https://v1.genr.ai/api/circuit-element/generate-questions"
    payload = {
        "text": text,
        "temperature": 0,
        "questions": 3
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

    st.write("Your resume has been submitted successfully!")

    # divide the candidate info into chunks of 750*5 characters
    candidate_info_chunks = [candidate_info[i:i+750*5]
                             for i in range(0, len(candidate_info), 750*5)]

    # correct the grammar of each chunk
    for i in range(len(candidate_info_chunks)):
        candidate_info_chunks[i] = correct_grammar(candidate_info_chunks[i])

    st.write("Information extracted from your resume successfully!")

    # generate questions from the chunks
    questions = ""

    for chunk in candidate_info_chunks:
        questions += "\n" + generate_questions(chunk)

    # convert the questions into a list of questions by \n
    questions = questions.split("\n")

    # remove the empty questions
    questions = [question for question in questions if question]

    # remove the duplicate questions
    questions = list(dict.fromkeys(questions))

    final_questions = []

    # if name is in the question, remove it
    for question in questions:
        if f"{name}'s" in question.lower():
            question = question.lower().replace(f"{name}'s", "your")
        if name in question.lower():
            question = question.lower().replace(name, "you")
        
        question = correct_grammar(question)

        final_questions.append(question)

    st.write("Questions generated successfully!")

    # remove the previous results
    if os.path.exists('./results/'):
        shutil.rmtree('./results/', ignore_errors=False, onerror=None)

    # generate the videos
    for ind,val in enumerate(final_questions):
        st.write(f"Generating video for question {ind+1}...")
        speech = gTTS(text=val, lang='en', tld='ca')
        # create a folder with the email name
        if not os.path.exists(f"./{email}"):
            os.makedirs(f"./{email}")
        speech.save(f"./{email}/question_{ind+1}.wav")
        generate_command = f"python3 demo.py --driving_audio ./{email}/question_{ind+1}.wav --device cuda"
        os.system(generate_command)
        copy_command = f"cp ./results/May/question_{ind+1}/question_{ind+1}.avi ./{email}/question_{ind+1}.avi"
        os.system(copy_command)

    st.write("Videos generated successfully!")

    # send the email
    send_email(email)