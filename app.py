import streamlit as st
from steelpy import aisc

st.header('My First App')

beam_length = st.sidebar.slider('Beam Length', min_value=1, value=30)
