import streamlit as st
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from pathlib import Path
import pandas as pd
import json
import tempfile

def welcome_message():
    res = """
    Welcome to Epiclear, we are working on figuring out your skincare concerns!
    """
    return res

def display_skill_data(skin_data):
    """Display the skill data in a table."""
    if skin_data:
        df = pd.DataFrame(list(skin_data.items()), columns=["Feature", "Value"])
        st.table(df)


def get_skincare_issues(file_path: Path):

    genai.configure(api_key="AIzaSyB0_RyrVWUPT56zSz-JzTveau1hs6h_P1U")
    model = genai.GenerativeModel(model_name="gemini-pro-vision")
    
    sample_file = genai.upload_file(path=file_path, display_name="Face Image")
    
    response = model.generate_content(["""
                    within this image, identify the following skin concerns, and return a carefully examined output. 
                    1. skin type - dry, oily, normal
                    2. acne - none, moderate, severe
                    3. dark circles - yes, no
                    4. acne scarring - yes, no
                    5. wrinkles - yes, no
                    6. pores - yes, no

                    Your output should be a python list containing one accurate option. The selected options should be correct in regards to the skin concerns of the image. Do not include any extra special characters. 
                    """, sample_file] ,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
        # HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE
    }
    )
    text = str(response.parts[0])
    start_index = text.find('[')
    end_index = text.find(']') + 1
    list_string = text[start_index:end_index]
    match = re.search(r'\[.*\]', text)
    if match:
        list_string = match.group()
    else:
        list_string = ''
        
    extracted_list = []
    if list_string:
        try:
            extracted_list = re.findall(r'[\w]+', list_string)
        except ValueError as e:
            print(f"Error parsing list: {e}")

    # Define the keys for the dictionary
    keys = ['skin type', 'acne', 'dark circles', 'acne scarring', 'wrinkles', 'pores']

# Create the dictionary
    result_dict = {}
    if len(extracted_list) == len(keys):
        result_dict = dict(zip(keys, extracted_list))
        
    return result_dict

        
    
    
def main():
# Title of the app
    st.title("EpiClear: Your Skincare Assistant")

    # Step 1: Image Upload
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.image(image, caption='Uploaded Image', width = 400)
        # st.image(image, caption='Uploaded Image', width = 400)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_file_path = tmp_file.name

        # Initialize chat session
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        response = welcome_message()
        st.session_state.messages.append({"role": "assistant", "content": response})
                    
        with st.chat_message("assistant"):
            st.markdown(response)
            
        skin_data = get_skincare_issues(file_path = temp_file_path)
        st.session_state.messages.append({"role": "assistant", "content": skin_data})
        with st.chat_message("assistant"):
            st.markdown(display_skill_data(skin_data))
            
            
                
if __name__ =='__main__':
    main()
