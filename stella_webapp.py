from tempfile import NamedTemporaryFile
import streamlit as st
import speech_recognition as sr
import numpy


uploaded_file = st.file_uploader("File upload", type=['wav','mp4'])


if uploaded_file:



    
    #streamlitのuploaderは、ByteIOなのでそれを.wav形式に直す。
    #フルパスをvideo_file_pathに入れている
    with NamedTemporaryFile(dir='.', suffix='.wav') as f:
        f.write(uploaded_file.getbuffer())
        video_file_path = f.name
        st.write(f.name)

        #取得したパスを基に音声認識をする
        r = sr.Recognizer()
        with sr.AudioFile(video_file_path) as source2:
            audio2 = r.record(source2)
        text_from_video = r.recognize_google(audio2, language='ja-JP')
        st.write(text_from_video)
