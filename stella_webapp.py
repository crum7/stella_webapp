from tempfile import NamedTemporaryFile
import streamlit as st
import speech_recognition as sr
import numpy
import ffmpeg
import pydub
import youtube_dl


uploaded_file = st.file_uploader("File upload", type=['wav','mp4','mp3'])


if uploaded_file:
    st.write(uploaded_file.name)

    #mp4→wav
    if str(uploaded_file.name)[-3:] == 'mp4':
        st.write('this is mp4 file')
        with NamedTemporaryFile(dir='.', suffix='.mp4') as f:
            f.write(uploaded_file.getbuffer())
            video_file_path = f.name
            st.write(video_file_path)

            #ここで変換
            stream = ffmpeg.input(video_file_path)
            stream = ffmpeg.output(stream, video_file_path+'.wav')
            ffmpeg.run(stream,overwrite_output=True)
            
            #wav化して再生する
            audio_file = open(video_file_path+'.wav', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')

            #取得したパスを基に音声認識をする
            r = sr.Recognizer()
            with sr.AudioFile(video_file_path+'.wav') as source2:
                audio2 = r.record(source2)
            text_from_video = r.recognize_google(audio2, language='ja-JP')
            st.write(text_from_video)

    #mp3→wavにする
    elif str(uploaded_file.name)[-3:] == 'mp3':
        #streamlitのuploaderは、ByteIOなのでそれを.wav形式に直す。
        #フルパスをvideo_file_pathに入れている
        with NamedTemporaryFile(dir='.', suffix='.mp3') as f:
            f.write(uploaded_file.getbuffer())
            video_file_path = f.name
            st.write(f.name)

            #ここで変換
            sound = pydub.AudioSegment.from_mp3(video_file_path)
            sound.export(video_file_path+".wav", format="wav")

            #wav化して再生する
            audio_file = open(video_file_path+'.wav', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')

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


#youtubeからダウンロード
youtube_link = st.text_input(label='Input Youtube Link',value='')
st.write('input: ', youtube_link)

#テキストボックスが空じゃないとき
if youtube_link!='':
    output_file_path = '/app/stella_webapp/'+youtube_link[-5:]
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':  output_file_path + '.mp3',   # 出力先パス
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',                # 出力ファイル形式
            'preferredquality': '192'},             # 出力ファイルの品質
        ],
    }
    url = youtube_link

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    # 指定したパスに音声ファイルが格納される
    info_dict = ydl.extract_info(url, download=True)

    #mp3で大丈夫か再生する
    audio_file = open(output_file_path+'.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')


    #mp3をwavに
    #ここで変換
    sound = pydub.AudioSegment.from_mp3(output_file_path + '.mp3')
    sound.export(output_file_path+".wav", format="wav")
    #wav化して再生する
    audio_file = open(output_file_path+'.wav', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')
    #取得したパスを基に音声認識をする
    r = sr.Recognizer()
    with sr.AudioFile(output_file_path+'.wav') as source2:
        audio2 = r.record(source2)
    text_from_video = r.recognize_google(audio2, language='ja-JP')
    st.write(text_from_video)
