# import streamlit as st
from streamlit_webrtc import webrtc_streamer
# import av
# import cv2

# st.title("Hello World!")

# webrtc_streamer(key="sample")

# class VideoProcessor:
#     def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
#         img = frame.to_ndarray(format="bgr24")
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         return av.VideoFrame.from_ndarray(img, format="gray")

# class VideoProcessor:
#     def recv(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_G)
#         return av.VideoFrame.from_ndarray(img, format="bgr24")

import streamlit as st
# import mediapipe as mp
# import cv2
import numpy as np
import tempfile
import time
# from PIL import Image
import pandas as pd
import random
import plotly.express as px

########################################################################
########################################################################

### DUMMY DATA ###

# Fungsi untuk membuat data dummy
def generate_dummy_data(num_rows=50):
    age_categories = ["Anak", "Remaja", "Dewasa", "Lansia"]
    gender_categories = ["Laki-laki", "Perempuan"]
    luggage_categories = ["Manusia", "Besar", "Sedang", "Kecil"]
    expression_categories = ["Marah", "Risih", "Takut", "Senyum", "Netral", "Sedih", "Terkejut"]

    data = []

    for _ in range(num_rows):
        age = random.choice(age_categories)
        gender = random.choice(gender_categories)
        luggage = random.choice(luggage_categories)
        expression = random.choice(expression_categories)

        data.append([age, gender, luggage, expression])

    columns = ["Age", "Gender", "Luggage", "Expression"]
    df = pd.DataFrame(data, columns=columns)
    return df

# Contoh membuat DataFrame dengan 20 baris
dummy_df = generate_dummy_data(50)

########################################################################
########################################################################

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

with open('style2.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.subheader('')

select_page = st.sidebar.selectbox("", ['Dashboard','Live AI'])

if select_page == 'Dashboard':
    st.header('Dashboard')
    st.subheader('')
elif select_page == 'Live AI':
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.8)
    tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.7)
    st.sidebar.markdown('---')
    
    # vid = cv2.VideoCapture(0)
    # width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps_input = int(vid.get(cv2.CAP_PROP_FPS))
    
    st.title("Live AI")
    webrtc_streamer(key="sample")
    st.title("")
    
    a1, a2, a3, a4, a5 = st.columns((2,2,2,2,2))
    
    with a1:
        st.markdown('<div class="metric-container">Visitor:<br><span class="metric-label">{}</span></div>'.format(dummy_df.shape[0]), unsafe_allow_html=True)
    with a2:
        st.markdown('<div class="metric-container">Age:<br><span class="metric-label">{}</span></div>', unsafe_allow_html=True)
    with a3:
        st.markdown('<div class="metric-container">Gender:<br><span class="metric-label">{}</span></div>', unsafe_allow_html=True)
    with a4:
        st.markdown('<div class="metric-container">Luggage:<br><span class="metric-label">{}</span></div>', unsafe_allow_html=True)
    with a5:
        st.markdown('<div class="metric-container">Ekspresi:<br><span class="metric-label">{}</span></div>', unsafe_allow_html=True)
    
    # Dashboard
    st.title("Dashboard")
    
    b1, b2 = st.columns((7, 3))
    
    with b1:
        age_df = dummy_df['Age'].value_counts().rename_axis('Age').reset_index(name='Count')
        
        # Bar chart
        fig = px.bar(age_df,
                     x='Count',
                     y=['Anak', 'Remaja', 'Dewasa', 'Lansia'],
                     color_discrete_sequence=['#d60003', '#d60003', '#d60003', '#d60003'],
                     text_auto='.3s')

        fig.update_xaxes(title_text=None)
        fig.update_yaxes(title_text=None)
        fig.update_layout(showlegend=False)
        
        fig.update_layout(
            width=600,
            height=350,
            title_text="Persebaran Umur",
            title_x=0,
            title_y=0.865, 
            title_font=dict(size=27),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=10, r=10, t=110, b=0)
            )
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
    with b2:
        gender_df = dummy_df['Gender'].value_counts().rename_axis('Gender').reset_index(name='Count')
        
        value_counts = gender_df['Gender'].value_counts()

        fig_gender = px.pie(names=value_counts.index, values=value_counts.values)
        fig_gender.update_traces(marker=dict(colors=['#d60003', '#f3722c']))
        
        fig_gender.update_layout(
            title_text="Persebaran Gender",
            width=350,
            height=350,
            title_x=0.125,
            title_y=0.865,
            title_font=dict(size=27),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=10, r=10, t=110, b=0)
            )
        
        fig_gender.update_traces(textinfo='label+percent')
        fig_gender.update_layout(showlegend=False)
        st.plotly_chart(fig_gender, use_container_width=True)
        
    
    
    
    