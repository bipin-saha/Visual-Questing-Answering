import streamlit as st
import os
import pathlib
import textwrap
import google.generativeai as genai
from PIL import Image



from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image, prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
   
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="Gemini Image Analysis")
st.header("Visual Question Answering")

input = st.text_input("Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "png", "jpeg", "webp"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Generate")

input_prompt = """
                You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


                """

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image, input)
    st.subheader("Response : ")
    st.write(response)