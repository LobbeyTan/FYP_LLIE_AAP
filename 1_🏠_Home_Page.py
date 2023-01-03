import streamlit as st
import os
from subprocess import run

if 'posix' in os.name:
    run("pip uninstall opencv-python")

st.set_page_config(layout="wide", page_title="Low Light Image Enhancement")

st.title("Home Page")
