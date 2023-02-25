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


# def read_GPT_text():
#     with open('GPT_text.txt', 'r') as f:
#         GPT_text = f.read()
#     f.close()
#     return GPT_text


# def write_GPT_text(GPT_text):
#     with open('GPT_text.txt', 'w') as f:
#         f.write(GPT_text)
#     f.close()
#     return


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





# take user email
email = st.text_input('Enter your email')

candidate = None

if email:
    # check if a folder with the email exists set the candidate = email
    if os.path.exists(email):
        candidate = email
        if 'candidate' not in st.session_state:
            st.session_state['candidate'] = email
            candidate = st.session_state['candidate']
        else:
            candidate = st.session_state['candidate']
        source = "still-face.mp4"
        cap = cv2.VideoCapture(source)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
        player = MediaPlayer(source)

        stframe = st.empty()
        im_pil = Image.open('./simple-face.jpg')
        stframe.image(im_pil)
    else:
        st.write('Seems like you are not shortlisted for the interview')
        candidate = None

if candidate:
    start = st.checkbox('Start')

    human = st.text_input('Your response')
    final_respnse = st.checkbox('final respnse')

    while start:
        status = read_status()
        generate_count = read_count()
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
            if final_respnse and status == False:
                final_respnse = False
                print('final response: ', human)
                # increase the count
                write_count(generate_count+1)
                write_status(True)
        else:
            if (generate_count > 0) and status:
                try:
                        isExist = os.path.exists(f'./{email}/question_{generate_count}.avi')
                        if isExist:
                            cap = cv2.VideoCapture(
                                f'./{email}/question_{generate_count}.avi')
                            player = MediaPlayer(
                                f'./{email}/question_{generate_count}.avi')
                            write_count(generate_count+1)
                            write_status(False)
                            # if read_count() >= 3:
                            #     write_count(-1)
                            final_respnse = False
                except:
                    print("Error: unable to start thread")
            # if generate_count == -1:
            #     break
            else:
                cap = cv2.VideoCapture(source)
                player = MediaPlayer(source)

    # this will be used after the interview is over
    player.close_player()
    cap.release()
    cv2.destroyAllWindows()