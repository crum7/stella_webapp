import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder()
speak_data_dict = {}
stop_flag =0
if audio_bytes:
    
    # To save audio to a file:
    wav_file = open("audio.wav", "wb")
    wav_file.write(audio_bytes.tobytes())

    st.audio("audio.wav", format="audio/wav")
    
