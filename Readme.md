<!-- write a readme for the project -->
# AVA: A phtorealistic Artificial Intelligence Bot
## This project implemented an realtime photorealistic AI bot which can take interviews
## Installation
download the the data folder from the link https://drive.google.com/drive/folders/16lxYT3RbyGuAYhs2hbYNqOFBHxIjSfVp?usp=share_link
and put it in the root directory of the project
## Usage
steps include before this one
1. HR will specify the Requirements of the job https://ava-hr.streamlit.app/
2. Candidate will fill the form https://ava-candidate.streamlit.app/
3. HR will shortlist the candidates https://ava-shortlisting.streamlit.app/
and these can also be found in the steps folder
the python version used for this is 3.8.10
it will run only on linux as it requires the ffmpeg library and it also requires an nvidia gpu
to run the project use the command
```pip install -r requirements.txt```
then
```streamlit run Ava.py```