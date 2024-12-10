"""
This is the main Streamlit application that runs the document parser.
It provides a simple user interface for uploading a PDF or image file,
and then displays the parsed document in JSON format.
"""
import streamlit as st
import json
from t_parser import parse_document
import os
import logging

# Import the logger
from init import logger

# Load configuration
from config import supported_file_types, supported_image_types, model_name, num_portions_per_page

st.title("Document Parser")

uploaded_file = st.file_uploader("Choose a PDF or image file", type=supported_file_types)

if uploaded_file is not None:
    try:
        with st.spinner('Processing...'):
            temp_file_path = "temp_file" + os.path.splitext(uploaded_file.name)[1]
            logger.info(f"Saving uploaded file to {temp_file_path}")
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            result = parse_document(temp_file_path)
            logger.info("Document parsed successfully")
            os.remove(temp_file_path)

        st.subheader("Parsed Document:")
        st.json(json.dumps(result, indent=4))
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        st.error(f"An error occurred while processing the document: {e}")