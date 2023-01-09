from tempfile import NamedTemporaryFile
import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("File upload", type='csv')
with NamedTemporaryFile(dir='.', suffix='.csv') as f:
    f.write(uploaded_file.getbuffer())
    st.write(f.name)
    df = pd.read_csv(f.name,encoding='shift_jis')
    st.write(df)
