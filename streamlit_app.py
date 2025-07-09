import streamlit as st
from moviepy.editor import TextClip

st.title("MoviePy Test")
txt = TextClip("Hello", fontsize=70, color='white')
st.write("MoviePy loaded successfully ✅")
