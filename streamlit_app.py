# streamlit_app.py
import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.path.dirname(__file__))

# Import your actual Streamlit app
from frontend.main import *
