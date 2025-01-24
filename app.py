import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt= """You are a Youtube Video summarizer,You will be taking the transcript text and sumaarizing the entire video and providing the important summary in points within 250 words.Please provide the summary of the text given here :  """





## getting the transcript data from the video
def extract_content(ytvideo_url):
    try:
        video_id=ytvideo_url.split('=')[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        main_text=""
        for i in transcript_text:
            main_text+=" "+i["text"]
        return main_text    
    except Exception as e:
        raise e
    

## getting summary from prompt  
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("Youtube Transcript Summary")
youtube_link=st.text_input("Enter Youtube Link")
if youtube_link:
    video_id=youtube_link.split('=')[1]
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(thumbnail_url, caption="YouTube Video Thumbnail", use_column_width=True)

if st.button("Get Summary"):
    transcript_text=extract_content(youtube_link)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("Detailed Summary")
        st.write(summary)
    

