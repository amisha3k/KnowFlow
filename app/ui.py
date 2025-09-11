import streamlit as st
import os

os.environ["STREAMLIT_CONFIG_DIR"] = "/tmp/.streamlit"
os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"



def pdf_uploader():
    return st.file_uploader(
       'upload PDF files',
       type='pdf',
       accept_multiple_files=True,
       help="upload one or more medical PDF decuments"
    )