import streamlit as st
import os
import tkinter,tkinter.filedialog, tkinter.messagebox
import hashlib
import sys
import os.path
import magic
import string
import subprocess


def strings(filename, min=4):
    with open(filename, errors="ignore") as f:  # Python 3.x
    # with open(filename, "rb") as f:           # Python 2.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result


def read_bytes(filename, chunksize=8192):
    # バイナリファイルをバイトごとに抽出
    try:
        with open(filename, "r+b") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    for b in chunk:
                        #print(type(b))
                        #print(b)
                        yield b
                else:
                    break
    except IOError:
        print("")
        print("Error - The file provided can't open")
        print("")
        sys.exit(0)

def is_character_printable(s):
    ## asciiの英数字・記号の文字列かどうかを判別し、真偽値を返します。
    if s < 126 and s >= 33:
        return True 

def validate_byte_as_printable(byte):
    ## ascii 文字列化をチェック. asciiでなければ '.' を返す ##
    if is_character_printable(byte):
        return byte
    else:
        return 46



if __name__ == '__main__':
   # タイトル
    st.title('Malware Analyze stella')

    
    #exeファイルをアップロード
    st.sidebar.markdown('## select .exe file')

    if st.sidebar.button('upload'):
        #guiで処理ファイルを開く
        #参考https://qiita.com/miyatomo1122/items/1b64aa91dcd45ad91540
        fTyp = [("","*.exe")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        malware_file_name = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        #ファイルを開く
        st.write('解析対象'+malware_file_name)

        #各ハッシュ値
        md5hs = hashlib.md5(malware_file_name.encode()).hexdigest()
        sha256hs = hashlib.sha256(malware_file_name.encode()).hexdigest()
        sha1hs = hashlib.sha1(malware_file_name.encode()).hexdigest()
        #各ハッシュ値の表示
        st.write('MD5 : '+md5hs)
        st.write('sha256 : '+sha256hs)
        st.write('sha1 : '+sha1hs)

        #各マルウェア解析サイトへのリンク
        hybrid_analysis_link = 'https://www.hybrid-analysis.com/search?query='+md5hs
        virus_total_link = 'https://www.virustotal.com/gui/search/'+md5hs

        #ファイルの種類判別
        st.write('このファイルは、'+magic.from_file(malware_file_name))

        #バイナリの可読部
        sl = list(strings(malware_file_name))
        st.write(sl)

        #flossの実行
        output = subprocess.getoutput("ls")
        print(output)









    

 