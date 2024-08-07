import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

#load environment variables
load_dotenv()

#configure streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini Pro",
    page_icon="brain:",
    layout="centered",
)