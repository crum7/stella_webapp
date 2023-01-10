from tempfile import NamedTemporaryFile
import streamlit as st
import speech_recognition as sr
import numpy
import ffmpeg
import pydub
import youtube_dl
import math
import os
import wave
import struct
from scipy import fromstring, int16
from pydub import AudioSegment

DURATION = 180  # 300 秒ごとに分割する

# 動画の再生時間(秒)を返却する ※小数点は切り上げる
def get_playback_seconds_of_movie(fpath):
    return math.ceil(float(ffmpeg.probe(fpath)['streams'][0]['duration']))




def cut_wav2(filename,duration):

    # wavファイルの読み込み
    sound = AudioSegment.from_file(filename, format="wav")
    original_len = duration

    #秒をmsに直す
    stom = 1000
    current = 0
    idx = 1

    while original_len-current>=0:
        
        #通常に3分に分割
        if original_len-current >= 180:
            sound1 = sound[current:180*stom]
        #動画の一番最後で3分に満たない
        else:
            sound1 = sound[current*stom:]
        #ファイルの場所
        outf = video_file_path[:-4]+'/output/' + str(idx) + '.wav'
        # 抽出した部分を出力
        sound1.export(outf, format="wav")

        idx += 1
        current += 180





















uploaded_file = st.file_uploader("File upload", type=['wav','mp4','mp3'])



if uploaded_file:

    #mp4→wav
    if str(uploaded_file.name)[-3:] == 'mp4':
        with st.spinner('Wait for it...'):
            with NamedTemporaryFile(dir='.', suffix='.mp4') as f:
                f.write(uploaded_file.getbuffer())
                video_file_path = f.name

                #ここで変換
                stream = ffmpeg.input(video_file_path)
                stream = ffmpeg.output(stream, video_file_path+'.wav')
                ffmpeg.run(stream,overwrite_output=True)

                wav_file_path = video_file_path+'.wav'

                #動画の長さ
                duration = get_playback_seconds_of_movie(wav_file_path)

                #動画が、3分以上のときに行う
                if duration >180: 
                    #ディレクトリを生成
                    os.makedirs(video_file_path[:-4]+'/output/')

                    #動画を3分ずつに分割
                    f_name = wav_file_path
                    cut_time = 180
                    cut_wav2(f_name,duration)

                    #分割した動画を保存してあるパスへのリンク
                    saved_splited_wav_path = os.listdir(video_file_path[:-4]+'/output/')
                    new_list_reverse = sorted(saved_splited_wav_path)
                
                    for fname in new_list_reverse:
                        #取得したパスを基に音声認識をする
                        r = sr.Recognizer()
                        with sr.AudioFile(video_file_path[:-4]+'/output/'+fname) as source2:
                            audio2 = r.record(source2)
                        text_from_video = r.recognize_google(audio2, language='ja-JP')
                        st.write(text_from_video+'\n')

                #動画が3分以内
                else:
                    #取得したパスを基に音声認識をする
                    r = sr.Recognizer()
                    with sr.AudioFile(video_file_path+'.wav') as source2:
                        audio2 = r.record(source2)
                    text_from_video = r.recognize_google(audio2, language='ja-JP')
                    st.write(text_from_video)

        st.success('Done!')



    #mp3→wavにする
    elif str(uploaded_file.name)[-3:] == 'mp3':
        with st.spinner('Wait for it...'):
            #streamlitのuploaderは、ByteIOなのでそれを.wav形式に直す。
            #フルパスをvideo_file_pathに入れている
            with NamedTemporaryFile(dir='.', suffix='.mp3') as f:
                f.write(uploaded_file.getbuffer())
                video_file_path = f.name
                
                wav_file_path = video_file_path+'.wav'

                #動画の長さ
                duration = get_playback_seconds_of_movie(wav_file_path)

                #動画が、3分以上のときに行う
                if duration >180: 
                    #ディレクトリを生成
                    os.makedirs(video_file_path[:-4]+'/output/')

                    #動画を3分ずつに分割
                    f_name = wav_file_path
                    cut_time = 180
                    cut_wav2(f_name,duration)

                    #分割した動画を保存してあるパスへのリンク
                    saved_splited_wav_path = os.listdir(video_file_path[:-4]+'/output/')
                    new_list_reverse = sorted(saved_splited_wav_path)
                
                    for fname in new_list_reverse:
                        #取得したパスを基に音声認識をする
                        r = sr.Recognizer()
                        with sr.AudioFile(video_file_path[:-4]+'/output/'+fname) as source2:
                            audio2 = r.record(source2)
                        text_from_video = r.recognize_google(audio2, language='ja-JP')
                        st.write(text_from_video+'\n')

                #動画が3分以内
                else:
                    #取得したパスを基に音声認識をする
                    r = sr.Recognizer()
                    with sr.AudioFile(video_file_path+'.wav') as source2:
                        audio2 = r.record(source2)
                    text_from_video = r.recognize_google(audio2, language='ja-JP')
                    st.write(text_from_video)
                    
        st.success('Done!')









    #wav
    else:
        with st.spinner('Wait for it...'):
            #streamlitのuploaderは、ByteIOなのでそれを.wav形式に直す。
            #フルパスをvideo_file_pathに入れている
            with NamedTemporaryFile(dir='.', suffix='.wav') as f:
                f.write(uploaded_file.getbuffer())
                video_file_path = f.name
                

                #取得したパスを基に音声認識をする
                r = sr.Recognizer()
                with sr.AudioFile(video_file_path) as source2:
                    audio2 = r.record(source2)
                text_from_video = r.recognize_google(audio2, language='ja-JP')
                st.write(text_from_video)
        st.success('Done!')


#youtubeからダウンロード
youtube_link = st.text_input(label='Input Youtube Link',value='')
st.write('input: ', youtube_link)

#テキストボックスが空じゃないとき
if youtube_link!='':
    with st.spinner('Download...'):
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
    st.success('Done!')

    #mp3をwavに
    #ここで変換
    with st.spinner('Wait for it...'):
        sound = pydub.AudioSegment.from_file(output_file_path +'.mp3')
        sound.export(output_file_path+".wav", format="wav")
        

        #取得したパスを基に音声認識をする
        r = sr.Recognizer()
        with sr.AudioFile(output_file_path+'.wav') as source2:
            audio2 = r.record(source2)
        text_from_video = r.recognize_google(audio2, language='ja-JP')
        st.write(text_from_video)
    st.success('Done!')

