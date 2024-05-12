from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_output(input, image, prompt):
    response=model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config('Nutribot')
st.header("Check your Plate Nutrition Value")
input_text=st.text_input("Write your question here...")
uploaded_file=st.file_uploader("Search my query", type=["jpg", "jpeg", "png"])
img=""

if uploaded_file is not None:
    img= Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image.", use_column_width=True)

submit_button=st.button("Give Nutrition Details")    

input_prompt="""
You are an expert in understanding nutrition in a plate. We will upload a a image of food plate
and you will have to answer any questions based on the uploaded image. Make sure you only answer what's asked.
You need to tell first calories, vitamins, fat, carbs and protien in each food item and then tell total of all. Also tell if the food is healthy or unhealthy. Based on the daily recommended quantity.
"""
if submit_button:
    image_bytes = input_image_details(uploaded_file)
    response=get_gemini_output(input_prompt, image_bytes, input_text)
    st.subheader("The response is: ")
    st.write(response)




