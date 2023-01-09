from tempfile import NamedTemporaryFile
import streamlit as st
import speech_recognition as sr
import numpy
import ffmpeg
import pydub
uploaded_file = st.file_uploader("File upload", type=['wav','mp4','mp3'])


if uploaded_file:
    st.write(uploaded_file.name)
    #mp4をwavにかける

    if str(uploaded_file.name)[-3:] == 'mp4':
        st.write('this is mp4 file')
        with NamedTemporaryFile(dir='.', suffix='.mp4') as f:
            f.write(uploaded_file.getbuffer())
            video_file_path = f.name
            st.write(video_file_path)
            stream = ffmpeg.input(video_file_path)
            stream = ffmpeg.output(stream, video_file_path+'.wav')
            ffmpeg.run(stream,overwrite_output=True)

            audio_file = open(video_file_path+'.wav', 'rb')
            audio_bytes = audio_file.read()
            #wav化して再生する
            st.audio(audio_bytes, format='audio/wav')

            #取得したパスを基に音声認識をする
            r = sr.Recognizer()
            with sr.AudioFile(video_file_path+'.wav') as source2:
                audio2 = r.record(source2)
            text_from_video = r.recognize_google(audio2, language='ja-JP')
            st.write(text_from_video)


    elif str(uploaded_file.name)[-3:] == 'mp3':
        #streamlitのuploaderは、ByteIOなのでそれを.wav形式に直す。
        #フルパスをvideo_file_pathに入れている
        with NamedTemporaryFile(dir='.', suffix='.mp3') as f:
            f.write(uploaded_file.getbuffer())
            video_file_path = f.name
            st.write(f.name)

            sound = pydub.AudioSegment.from_mp3(video_file_path)
            sound.export(video_file_path+".wav", format="wav")

                        #取得したパスを基に音声認識をする
            r = sr.Recognizer()
            with sr.AudioFile(video_file_path+'.wav') as source2:
                audio2 = r.record(source2)
            text_from_video = r.recognize_google(audio2, language='ja-JP')
            st.write(text_from_video)


    else:
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
