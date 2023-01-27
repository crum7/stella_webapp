import streamlit as st
from audiorecorder import audiorecorder
from pydub import AudioSegment
from pydub.silence import split_on_silence

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    #frontEnd
    #st.audio(audio.tobytes())
    
        # wavデータの分割（無音部分で区切る）
    chunks = split_on_silence(audio.tobytes(), min_silence_len=2000, silence_thresh=-40, keep_silence=600)

    # 分割したデータ毎にファイルに出力
    for i, chunk in enumerate(chunks):
        chunk.export("output" + str(i) +".wav", format="wav")
        st.audio("output" + str(i) +".wav")
