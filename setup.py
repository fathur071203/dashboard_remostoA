import streamlit as st

st.set_page_config(
    page_title="Remosto Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

##### THEME ##### 
primaryColor="#4891ff"
backgroundColor="#f5f8fe"
secondaryBackgroundColor="#ffffff"
textColor="#3d4563"

# add sidebar
st.sidebar.title("Remosto Analytics")
st.sidebar.header("Navigation")
page = st.sidebar.radio("", ('Home', 'Data Exploration', 'Data Visualization', 'Data Modeling', 'About Us'))