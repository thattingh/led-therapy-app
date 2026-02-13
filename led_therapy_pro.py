import streamlit as st
from PIL import Image
import os
import base64

# ---------------------------
# Page Config (MUST BE FIRST)
# ---------------------------
st.set_page_config(
    page_title="LED Therapy Pro",
    page_icon="logo.png",
    layout="wide"
)

# ---------------------------
# Header with Inline Logo
# ---------------------------
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as img_file:
        encoded = base64.b64encode(i

