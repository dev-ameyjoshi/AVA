from ffpyplayer.player import MediaPlayer
import _thread as thread
import threading
import streamlit as st
from gtts import gTTS
from PIL import Image
import numpy as np
import openai
import time
import cv2
import os
# from deta import Deta
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_md")

# deta = Deta('d0t7t81b_h5omWhJECYXwDmqRpYk5CxH7koLAFx32')


def write_count(count):
    with open('generate_count.txt', 'w') as f:
        f.write(str(count))
    f.close()
    return


def write_status(status):
    with open('status.txt', 'w') as f:
        f.write(str(status))
    f.close()
    return


def read_count():
    with open('generate_count.txt', 'r') as f:
        count = f.read()
    f.close()
    return int(count)


def read_status():
    with open('status.txt', 'r') as f:
        status = f.read()
    f.close()
    return status


def read_GPT_text():
    with open('GPT_text.txt', 'r') as f:
        GPT_text = f.read()
    f.close()
    return GPT_text


def write_GPT_text(GPT_text):
    with open('GPT_text.txt', 'w') as f:
        f.write(GPT_text)
    f.close()
    return


def append_question(question):
    with open('questions.txt', 'r') as f:
        questions = f.read()
    f.close()
    if questions == "":
        questions = [question]
    else:
        questions = questions.split(';')
        if question not in questions:
            questions.append(question)
    with open('questions.txt', 'w') as f:
        f.write(';'.join(questions))
    f.close()


def read_questions():
    with open('questions.txt', 'r') as f:
        questions = f.read()
    f.close()
    if questions == "":
        questions = []
    else:
        questions = questions.split(';')
    return questions


def append_answer(answer):
    with open('answers.txt', 'r') as f:
        answers = f.read()
    f.close()
    if answers == "":
        answers = [answer]
    else:
        answers = answers.split(';')
        answers.append(answer)
    with open('answers.txt', 'w') as f:
        f.write(';'.join(answers))
    f.close()


def read_answers():
    with open('answers.txt', 'r') as f:
        answers = f.read()
    f.close()
    if answers == "":
        answers = []
    else:
        answers = answers.split(';')
    return answers


# db = deta.Base('HR-DB')
# hr = db.get('testing')

# initialize the openai api key
openai.api_key = "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"


def score_answer(question, answer):
    # Generate multiple possible answers using GPT-3
    prompt = f"{question}\n{answer}"
    model = "text-davinci-002"
    temperature = 0.5
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=1024,
        n=5,
        stop=None)

    # Score the relevance and coherence of the answer using BERT
    scores = []
    for completion in completions.choices:
        text = completion.text
        text_doc = nlp(text)
        answer_doc = nlp(answer)
        relevance_score = text_doc.similarity(answer_doc)

    # Compute the final score as the average of the relevance and coherence scores
    # final_score = sum(scores) / len(scores)
    final = int(relevance_score*100)
    if final > 100:
        final = 100

    return final


# initialize the start sequence
start_sequence = "\nAI: "
restart_sequence = "\nHuman: "

first_argument = "Hi I am AVA. It's nice to meet you."
append_question(first_argument)

GPT_text = f"The following is the conversation betweek AVA (Photorealistic Artificial Intelligence Bot) and Human. AVA, created by Om Surushe and Vaishnavi Narkhede, is a large language model trained to conduct technical and HR interviews. When starting an interview, the AI will introduce itself and greet the candidate. It will then ask a maximum of five questions based on the information provided in the candidate's skills, and will end the interview with a greeting thanking the candidate for their time. This will conclude the interview. skills = [html,css, javascript,flutter,python]  \nAI: {first_argument}"

write_GPT_text(GPT_text)


def first_video_generation(count):
    language = 'en'
    speech = gTTS(text=first_argument, lang=language, tld='ca')
    speech.save(f"./question_{count}.wav")
    generate_command = f"python3 demo.py --driving_audio ./question_{count}.wav --device cuda"
    os.system(generate_command)
    copy_command = f"cp ./results/May/question_{count}/question_{count}.avi ./question_{count}.avi"
    os.system(copy_command)
    return


def video_generation(count):
    text_feed = read_GPT_text()
    language = 'en'
    if count == 2:
        AI = "Thank you for your time we can conclude the interview. Have a nice day."
    else:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text_feed,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"])
        AI = response.choices[0].text
    write_GPT_text(read_GPT_text() + AI)
    append_question(AI)
    speech = gTTS(text=AI, lang=language, tld='ca')
    speech.save(f"./question_{count}.wav")
    generate_command = f"python3 demo.py --driving_audio ./question_{count}.wav --device cuda"
    os.system(generate_command)
    copy_command = f"cp ./results/May/question_{count}/question_{count}.avi ./question_{count}.avi"
    os.system(copy_command)
    return


# take user email
email = st.text_input('Enter your email')

candidate = email
if email:
    # check if the user with key email exists
    # db = deta.Base('Shortlist-Data')

    if 'candidate' not in st.session_state:
        st.session_state['candidate'] = email
        candidate = st.session_state['candidate']
    else:
        candidate = st.session_state['candidate']
    if candidate is None:
        st.write('Seems like you are not shortlisted for the interview')

    source = "still-face.mp4"
    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
    player = MediaPlayer(source)

    stframe = st.empty()
    im_pil = Image.open('./simple-face.jpg')
    stframe.image(im_pil)

if candidate:
    start = st.checkbox('Start')

    human = st.text_input('Your response')
    final_respnse = st.checkbox('final respnse')

    while start:
        status = read_status()
        generate_count = read_count()
        GPT_text = read_GPT_text()
        time.sleep(1/150)
        theres_a_frame, frame = cap.read()
        audio_frame, val = player.get_frame(show=True)
        # if theres a frame
        if theres_a_frame:
            frame = cv2.resize(frame, (512, 512))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(frame)
            stframe.image(im_pil)
            # this was for first video generation
            # if (generate_count == 0) and status:
            #     try:
            #         thread.start_new_thread(first_video_generation, ())
            #         with lock:
            #             global_variables["status"] = False
            #     except:
            #         print("Error: unable to start thread")
            if (generate_count > 0) and status:
                try:
                    if final_respnse:
                        final_respnse = False
                        GPT_text = GPT_text + restart_sequence + human + start_sequence
                        answer_list = read_answers()
                        if answer_list is []:
                            append_answer(human)
                        else:
                            append_answer(human)
                        write_GPT_text(GPT_text)
                        thread.start_new_thread(
                            video_generation, (generate_count,))
                        write_status(False)
                except:
                    print("Error: unable to start thread")
        else:
            if generate_count == -1:
                break
            isExist = os.path.exists(f'./question_{generate_count}.avi')
            if isExist:
                cap = cv2.VideoCapture(f'./question_{generate_count}.avi')
                player = MediaPlayer(f'./question_{generate_count}.avi')
                write_count(generate_count+1)
                if read_count() >= 3:
                    write_count(-1)
                write_status(True)
                final_respnse = False
            else:
                cap = cv2.VideoCapture(source)
                player = MediaPlayer(source)

    # this will be used after the interview is over
    player.close_player()
    cap.release()
    cv2.destroyAllWindows()

if read_count() == -1:
    st.write('Thank you for your time. Have a nice day.')
    questions = read_questions()
    questions = questions[:-1]
    answers = read_answers()
    total_score = []
    for i in range(len(questions)):
        score = score_answer(questions[i], answers[i])
        total_score.append(score)
    st.write(f'Your score is {sum(total_score)} out of {len(questions)}')
