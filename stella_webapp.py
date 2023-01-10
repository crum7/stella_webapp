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

DURATION = 180  # 300 秒ごとに分割する

# 動画の再生時間(秒)を返却する ※小数点は切り上げる
def get_playback_seconds_of_movie(fpath):
    return math.ceil(float(ffmpeg.probe(fpath)['streams'][0]['duration']))


def cut_wav(filename,time,duration):  # WAVファイルを刈り奪る　形をしてるだろ？ 
    # timeの単位は[sec]

    # ファイルを読み出し
    wavf = filename
    wr = wave.open(wavf, 'r')

    #元ファイルの長さ取得
    original_len = duration

    # waveファイルが持つ性質を取得
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time) # 小数点以下切り捨て
    t = int(time)  # 秒数[sec]
    frames = int(ch * fr * t)
    num_cut = int(integer//t)

    #　確認用
    print("Channel: ", ch)
    print("Sample width: ", width)
    print("Frame Rate: ", fr)
    print("Frame num: ", fn)
    print("Params: ", wr.getparams())
    print("Total time: ", total_time)
    print("Total time(integer)",integer)
    print("Time: ", t) 
    print("Frames: ", frames) 
    print("Number of cut: ",num_cut)

    # waveの実データを取得し、数値化
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = fromstring(data, dtype=int16)
    print(X)
    
    
    current = 0
    idx = 1

    while original_len-current>=0:
        start = current
        st.write(current)
        # 出力データを生成
        outf = video_file_path[:-4]+'/output/' + str(idx) + '.wav' 
        start_cut = start*frames
        
        if original_len-current >= 180:
            end_cut = start*frames + frames
        elif original_len-current <=180:
            end_cut = original_len
        
        
        st.write('start_cut'+str(start_cut))
        st.write('end_cut'+str(end_cut))
        st.write('original_len-current:'+str(original_len-current))
        print(start_cut)
        print(end_cut)
        Y = X[start_cut:end_cut]
        outd = struct.pack("h" * len(Y), *Y)

        # 書き出し
        ww = wave.open(outf, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(outd)
        ww.close()
        
        idx += 1
        current += DURATION
        
    st.write('もとの長さ'+str(original_len))






















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
                os.makedirs(video_file_path[:-4]+'/output/')


                #動画分割
                duration = get_playback_seconds_of_movie(wav_file_path)
                current = 0
                idx = 1
                #動画が、3分以上のときに行う
                if duration >DURATION: 
                    '''
                    while current < duration:
                        start = current
                        stream = ffmpeg.input(wav_file_path, ss=start, t=60)
                        stream = ffmpeg.output(stream, video_file_path[:-4]+f'/output/{idx}.wav', c='copy')
                        ffmpeg.run(stream,overwrite_output=True)
                        idx += 1
                        current += DURATION
                        st.write(current)
                    '''
                    f_name = wav_file_path
                    cut_time = 180
                    cut_wav(f_name,cut_time,duration)



                    st.write(os.listdir(video_file_path[:-4]+'/output/'))

                    #再生
                    audio_file = open(video_file_path[:-4]+'/output/1.wav', 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/wav')
                
                    audio_file = open(video_file_path[:-4]+'/output/2.wav', 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/wav')
                





                    for fname in os.listdir(video_file_path[:-4]+'/output/'):

                        #取得したパスを基に音声認識をする
                        st.write(video_file_path[:-4]+'/output/'+fname)
                        r = sr.Recognizer()
                        with sr.AudioFile(video_file_path[:-4]+'/output/'+fname) as source2:
                            audio2 = r.record(source2)
                        text_from_video = r.recognize_google(audio2, language='ja-JP')
                        st.write(text_from_video)

                        
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
                

                #ここで変換
                sound = pydub.AudioSegment.from_mp3(video_file_path)
                sound.export(video_file_path+".wav", format="wav")


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


