import streamlit as st
import os
from subprocess import run

if os.name == 'poxis':
    run("sudo apt-get install python3-opencv")

st.set_page_config(layout="wide", page_title="Low Light Image Enhancement")

st.title("Home Page")
