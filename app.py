from dotenv import load_dotenv
from PIL import Image
import base64
import os
import io
import pdf2image
import streamlit as st
import google.generativeai as genai

# Configure Google API key
load_dotenv()
genai.configure(api_key='AIzaSyCuX-m1h1vDqc09jHptsoOnptmUpYg49us')

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file:
        # Convert the PDF to an image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                'mime_type': 'image/jpeg',
                'data': base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError('No file uploaded')

# Streamlit App

# Display logo and set page title
st.set_page_config(page_title='ATS Resume Expert')

# Display header
st.header('Applicant Tracking System')

input_text = st.text_area('Job Description: ', key='input')
uploaded_file = st.file_uploader('Upload your resume (PDF)...', type=['pdf'])

if uploaded_file:
    st.write('PDF Uploaded Successfully')

submit1 = st.button('Tell Me About the Resume')
submit3 = st.button('Percentage match')

input_prompt1 = '''
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
'''

input_prompt3 = '''
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then keywords missing, and lastly, final thoughts.
'''

if submit1:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.write('Please upload the resume')

elif submit3:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.write('Please upload the resume')
