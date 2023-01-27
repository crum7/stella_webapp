import streamlit as st
from audiorecorder import audiorecorder

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    #frontEnd
    
    
    #wavファイルとして保存
    wav_file = open("audio.wav", "wb")
    wav_file.write(audio.tobytes())
    
    st.audio("audio.wav")