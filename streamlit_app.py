# Import necessary libraries
import os
import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
from transformers import pipeline
from google.cloud import vision
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
import io
import base64
import logging
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import speech_recognition as sr

# Initialize API and models
GOOGLE_API_KEY = "AIzaSyAgxzRq1399TV8eUIBYT4lLvFnNWBXC9xE"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
vision_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def handle_error(error):
    logging.error(error)
    st.error(f"Error: {str(error)}")

def analyze_image(image, prompt):
    try:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        message = HumanMessage(content=[ 
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"}
        ])
        return vision_llm.invoke([message]).content
    except Exception as e:
        handle_error(e)

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp.getvalue()
    except Exception as e:
        handle_error(e)

# Define a video transformer for camera input
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.image = None

    def transform(self, frame):
        if self.image is None:  # Capture only once
            self.image = frame.to_image()  # Convert the frame to a PIL image
        return frame  # Return the frame for streaming purposes

# Function for voice activation
def listen_for_trigger():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening for trigger word: 'Hello VRS'")
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            return "hello vrs" in command
    except sr.UnknownValueError:
        st.warning("Could not understand the audio. Please try again.")
        return False
    except sr.RequestError as e:
        handle_error(e)
        return False
    except Exception as e:
        handle_error(e)
        return False

def main():
    st.set_page_config(page_title="Vision Assistant", layout="wide")
    st.title("Welcome to VRS Foundation")
    
    # Initialize image as None
    image = None

    # Create the VideoTransformer context for the webcam
    ctx = webrtc_streamer(key="camera", video_transformer_factory=VideoTransformer)

    # Check if image is captured and available
    if ctx.video_transformer and ctx.video_transformer.image:
        image = ctx.video_transformer.image  # Assign the captured image
        st.image(image, caption="Captured Image")

    # Manual image upload option
    uploaded_file = st.file_uploader("Or upload an image", type=['jpg', 'jpeg', 'png'])

    if uploaded_file:
        image = Image.open(uploaded_file)  # Assign the uploaded image to 'image'
        st.image(image, caption="Uploaded Image")

    # Ensure the image is available for analysis
    if image:
        st.write("Image successfully loaded. You can now select a feature to analyze.")

        # Feature selection and analysis
        feature = st.radio("Select Feature", ["Scene Description", "Object Detection", "Task Assistance"])

        if feature == "Scene Description" and st.button("Analyze Scene"):
            with st.spinner("Analyzing scene..."):
                description = analyze_image(image, "Provide a detailed description of this image for a visually impaired person.")
                st.write(description)
                st.audio(text_to_speech(description), format="audio/mp3")

        elif feature == "Object Detection" and st.button("Detect Objects"):
            with st.spinner("Analyzing objects..."):
                objects_info = analyze_image(image, "Identify objects and obstacles in this image.")
                st.write(objects_info)
                st.audio(text_to_speech(objects_info), format="audio/mp3")

        elif feature == "Task Assistance":
            task_type = st.selectbox("Select Task Type", ["item_identification", "label_reading", "navigation_help", "daily_tasks"])
            task_prompts = {
                "item_identification": "Identify and describe items in this image.",
                "label_reading": "Analyze labels and text in this image.",
                "navigation_help": "Provide navigation guidance for this space.",
                "daily_tasks": "Give step-by-step guidance for daily tasks in this image."
            }
            if st.button("Get Assistance"):
                with st.spinner("Generating assistance..."):
                    guidance = analyze_image(image, task_prompts[task_type])
                    st.write(guidance)
                    st.audio(text_to_speech(guidance), format="audio/mp3")

    # Voice activation
    if st.button("Activate Voice Command"):
        st.info("Voice command activated. Speak 'Hello VRS' to trigger.")
        if listen_for_trigger():
            st.experimental_rerun()

if __name__ == "__main__":
    main()
