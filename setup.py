import requests
import json
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

##### THEME ##### 
primaryColor="#6a6bfb"
backgroundColor="#141519"
secondaryBackgroundColor="#0b0d1f"
textColor="#ffffff"

color1="#a0a1fc"
color2="e668ea"
color3="6a6bfb"
color4="efe84a"
color5="86e29b"
color6="ff9f4a"

# add sidebar
st.sidebar.title("Remosto Analytics")

# Fetching data from the feedback URL
url_feedback = 'https://backend-remosto-ujrltkkgyq-et.a.run.app/feedback'
response_feedback = requests.get(url_feedback)
data = response_feedback.json()

# Extracting data from the "data" attribute
feedback_data = data["data"]

# Creating DataFrame
feedback_df = pd.DataFrame(feedback_data, columns=["id", "section", "star", "categories", "desc", "timestamp"])
# Setting the "id" column as the index
feedback_df.set_index("id", inplace=True)
reversed_feedback_df = feedback_df[::-1]


# Main Section Property

##############
# ROW A MAIN #
##############
   
# Define functions outside the blocks
def home_page():
    st.write("")

def page_one():
    st.write("Page 1")

def page_two():
    st.write("Page 2")

# st.markdown("<h1 style='text-align: center;'>Remosto Analytics</h1>", unsafe_allow_html=True)
# st.markdown("")
# st.markdown("")

url_clickstream = 'https://backend-remosto-ujrltkkgyq-et.a.run.app/analytics/range'
payload_clickstream = {"start": "2023-11-01T09:06:09Z", "end": "2023-11-24T09:06:09Z"}
headers_clickstream = {'Content-Type': 'application/json'}
response_clickstream = requests.post(url=url_clickstream, data=json.dumps(payload_clickstream), headers=headers_clickstream)
data = response_clickstream.json()
clickstream_data = data["data"]
clickstream_df = pd.DataFrame(clickstream_data, columns=['id', 'timestamp', 'visited_url'])

# Pisah kolom
max_cols = 20
for i in range(max_cols):
    col_name = f'clicked{i+1}'
    clickstream_df[col_name] = clickstream_df['visited_url'].apply(lambda x: x[i] if len(x) > i else None)

# Count Value
columns_to_count = ['clicked1', 'clicked2', 'clicked3', 'clicked4', 'clicked5', 
                    'clicked6', 'clicked7', 'clicked8', 'clicked9', 'clicked10', 
                    'clicked11', 'clicked12', 'clicked13', 'clicked14', 'clicked15', 
                    'clicked16', 'clicked17', 'clicked18', 'clicked19', 'clicked20']
total_count = clickstream_df[columns_to_count[0]].value_counts()
for column in columns_to_count[1:]:
    count_column = clickstream_df[column].value_counts()
    total_count = total_count.add(count_column, fill_value=0)
    
df_total = pd.DataFrame(list(total_count.items()), columns=['Path', 'Count'])
df_total = df_total[df_total['Path'].isin(['/feedback', '/informasi', '/maps', '/tempat-makan'])]


# Displaying metrics with custom styling
st.markdown("""
    <style>
        .metric-container {
            text-align: left;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            background: #21242d;
            padding: 25px;
            border-radius: 8px;
        }
        .metric-label {
            font-size: 18px;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)
a1, a2, a3 = st.columns((10/3, 10/3, 10/3))

url_feedback = 'https://backend-remosto-ujrltkkgyq-et.a.run.app/feedback'
response_feedback = requests.get(url_feedback)
data = response_feedback.json()
feedback_data = data["data"]
feedback_df = pd.DataFrame(feedback_data, columns=["id", "section", "star", "categories", "desc", "timestamp"])
feedback_df.set_index("id", inplace=True)
reversed_feedback_df = feedback_df[::-1]

root_feedback_data = reversed_feedback_df[reversed_feedback_df['section'] == "Root"]
root_feedback_data_subset = root_feedback_data.loc[:, ['star', 'categories', 'desc', 'timestamp']]

counts = root_feedback_data_subset['star'].value_counts()
index_max_count = df_total['Count'].idxmax()
page_with_max_count = df_total.loc[index_max_count, 'Path']
with a1:
    st.markdown('<div class="metric-container">Jumlah Pengunjung:<br>{}<br><span class="metric-label">Orang</span></div>'.format(clickstream_df.shape[0]), unsafe_allow_html=True)
with a2:
    st.markdown('<div class="metric-container">Overall Feedback:<br>{}<br><span class="metric-label">Star</span></div>'.format(counts.idxmax()), unsafe_allow_html=True)
with a3:
    st.markdown('<div class="metric-container">Most Clicked:<br>{}<br><span class="metric-label">Page</span></div>'.format(page_with_max_count), unsafe_allow_html=True)

st.title("")
fig = px.bar(df_total, 
            x='Path', 
            y='Count',
            text_auto='.3s',
            category_orders={'Path': ['/informasi', '/maps', '/tempat-makan', '/feedback']},
            title='Most Clicked Page'
            )

fig.update_layout(
    width=600,
    height=400,
    title_text="Most Clicked Page",
    title_x=0.35,
    title_y=0.98, 
    title_font=dict(size=35),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=10, r=10, t=110, b=0)
)

fig.update_xaxes(title_text=None)
fig.update_yaxes(title_text=None)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

    
st.title("Gembira Loka")
st.markdown("")
st.markdown("")

# Create the columns
b1, b2, b3, b4 = st.columns((2.5, 2.5, 2.5, 2.5))

pages1 = ["Home", "Zona Kucing", "Zona Anjing", "Zona Burung"]
pages2 = ["Home", "Gerai Zoovenir", "Presentasi Edukasi Mamalia", "Presentasi Edukasi Aves"]
pages3 = ["Petting zoo", "Terapi Ikan", "Interaksi Gajah", "ATV", "Bumber Boat", "Speed Boat", "Kolam Tangkap", "Zoolahraga"]
pages4 = ["zoo Mart", "Kantin O-utan", "Kantin Flamingo", "Gajah Resto"]
pages = ["Home", pages1, pages2]

with b1:
    st.write("click stream Satwa")
    
    # Menentukan jumlah maksimal kolom yang dibutuhkan (misalnya, 5 kolom)
    max_cols = 20

    # Membuat kolom-kolom baru dengan menggunakan apply dan lambda
    for i in range(max_cols):
        col_name = f'clicked{i+1}'
        clickstream_df[col_name] = clickstream_df['visited_url'].apply(lambda x: x[i] if len(x) > i else None)
    
    columns_to_count = ['clicked1', 'clicked2', 'clicked3', 'clicked4', 'clicked5', 
                    'clicked6', 'clicked7', 'clicked8', 'clicked9', 'clicked10', 
                    'clicked11', 'clicked12', 'clicked13', 'clicked14', 'clicked15', 
                    'clicked16', 'clicked17', 'clicked18', 'clicked19', 'clicked20']

    total_count = clickstream_df[columns_to_count[0]].value_counts()

    for column in columns_to_count[1:]:
        count_column = clickstream_df[column].value_counts()
        total_count = total_count.add(count_column, fill_value=0)
    
    df_total = pd.DataFrame(list(total_count.items()), columns=['Path', 'Count'])
    
    df_yyy = df_total[df_total['Path'].str.startswith('/informasi/detail/')]
    df_yyy['zona'] = 'lainnya'  # default value

    # Extract the numeric value after "/informasi/detail/"
    df_yyy['zona'] = df_yyy['Path'].str.extract(r'/informasi/detail/(\d+)')

    # Replace NaN values with 'lainnya'
    df_yyy['zona'].fillna('lainnya', inplace=True)
    
    # Assuming df_yyy is your DataFrame
    df_yyy['zona_desc'] = 'lainnya'  # default value

    # Define conditions
    condition_kucing = df_yyy['zona'].isin(["1","2","3","4","5","16","17","18","19","20","21","22","23"])
    condition_anjing = df_yyy['zona'].isin(["6","7","8","9","10"])
    condition_burung = df_yyy['zona'].isin(["11","12","13","14","15"])

    # Assign values based on conditions
    df_yyy.loc[condition_kucing, 'zona_desc'] = 'kucing'
    df_yyy.loc[condition_anjing, 'zona_desc'] = 'anjing'
    df_yyy.loc[condition_burung, 'zona_desc'] = 'burung'
    
    # Group by 'zona' and 'zona_desc', and sum the 'Count' column
    result_df = df_yyy.groupby(['zona', 'zona_desc'], as_index=False)['Count'].sum()
    
    result_df_grouped = result_df.groupby('zona_desc', as_index=False)['Count'].sum()
    
    fig = px.bar(result_df_grouped, x='zona_desc', y='Count', color='zona_desc')
    fig.update_xaxes(title_text=None)
    fig.update_yaxes(title_text=None)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    width=600,
    height=400)
    
    st.plotly_chart(fig, use_container_width=True)

    selected_page = st.selectbox("", ["Home", "Zona Kucing", "Zona Anjing", "Zona Burung"])

    # Conditional rendering based on the selected page
    if selected_page == "Home":
        home_page()
    elif selected_page == "Zona Kucing":
        # bar chart result_df if zona_desc == kucing
        fig = px.bar(result_df[result_df['zona_desc'] == 'kucing'], x='zona', y='Count', title='Kucing')
        st.plotly_chart(fig, use_container_width=True)
    elif selected_page == "Zona Anjing":
        fig = px.bar(result_df[result_df['zona_desc'] == 'anjing'], x='zona', y='Count', title='Anjing')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(result_df[result_df['zona_desc'] == 'burung'], x='zona', y='Count', title='Burung')
        st.plotly_chart(fig, use_container_width=True)
    
    url = "https://backend-remosto-ujrltkkgyq-et.a.run.app/animal-categories/"
    

with b2:
    st.write("click stream Fasilitas (belum ada)")
    selected_page2 = st.selectbox("", ["Home", "Page 3", "Page 4"])

    # Conditional rendering based on the selected page
    if selected_page2 == "Home":
        home_page()
    elif selected_page2 == "Page 1":
        page_one()
    elif selected_page2 == "Page 2":
        page_two()

with b3:
    st.write("click stream Wahana (belum ada)")
    selected_page3 = st.selectbox("", ["Home", "Page 5", "Page 6"])

    # Conditional rendering based on the selected page
    if selected_page3 == "Home":
        home_page()
    elif selected_page3 == "Page 1":
        page_one()
    elif selected_page3 == "Page 2":
        page_two()

with b4:
    st.write("click stream Resto/Kantin")
    
    all_food = df_total[df_total['Path'].str.startswith("/tempat-makan/detail/")]
    
    # Assuming df_yyy is your DataFrame
    all_food['storeType'] = 'lainnya'  # default value

    # Extract the numeric value after "/informasi/detail/"
    all_food['storeType'] = all_food['Path'].str.extract(r'/tempat-makan/detail/(\d+)')

    # Replace NaN values with 'lainnya'
    all_food['storeType'].fillna('lainnya', inplace=True)
    
    all_food['type'] = 'lainnya'  # default value

    # Define conditions
    storeType1 = all_food['storeType'].isin(["4","5","11","12","15","16","17","18","19","1","2","3","22","14","24","25","23","21","20","27","26","13"])
    storeType2 = all_food['storeType'].isin(["6","7","8","9","10"])

    # Assign values based on conditions
    all_food.loc[storeType1, 'type'] = 'storeType1'
    all_food.loc[storeType2, 'type'] = 'storeType2'
    
    fig = px.bar(all_food, x='type', y='Count')
    fig.update_xaxes(title_text=None)
    fig.update_yaxes(title_text=None)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    width=600,
    height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    selected_page = st.selectbox("", ["Home", "storeType1", "storeType2"])

    # Conditional rendering based on the selected page
    if selected_page == "Home":
        home_page()
    elif selected_page == "storeType1":
        # bar chart result_df if zona_desc == kucing
        fig = px.bar(all_food[all_food['type'] == 'storeType1'], x='storeType', y='Count', title='storeType1')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(all_food[all_food['type'] == 'storeType2'], x='storeType', y='Count', title='storeType2')
        st.plotly_chart(fig, use_container_width=True)

# Displaying DataFrame in Streamlit
# show feedback_df where section == root
root_feedback_data = reversed_feedback_df[reversed_feedback_df['section'] == "Root"]
root_feedback_data_subset = root_feedback_data.loc[:, ['star', 'categories', 'desc', 'timestamp']]

# # Split categories separated by comma and create a new DataFrame
# categories_df = (
#     root_feedback_data_subset['categories']
#     .str.split(',', expand=True)
#     .stack()
#     .reset_index(level=1, drop=True)
#     .to_frame('category')
# )

# # Drop empty values
# categories_df = categories_df[categories_df['category'] != '']

# root_feedback_data_subset_split = root_feedback_data_subset.drop('categories', axis=1).join(categories_df)

# # Reset index
# root_feedback_data_subset_split = root_feedback_data_subset_split.reset_index(drop=True)

# # Custom styling function based on categories
# def highlight_categories(val):
#     categories_colors = {
#         "Pelayanan Robot": "color: red",
#         "Pelayanan Petugas": "color: red",
#         "Fasilitas Umum": "color: green",
#         "Kebersihan Lingkungan": "color: blue",
#         "Lainnya": "color: yellow"
#     }
    
#     # Menggunakan get() untuk menghindari KeyError
#     return categories_colors.get(val, "color: default_color")

# # Apply the styling functions to the DataFrame
# styled_df = root_feedback_data_subset_split.style.applymap(highlight_categories, subset=['category'])

# # Display the styled DataFrame in Streamlit
# st.table(styled_df)

st.title("Feedback")
st.markdown("")
st.markdown("")

url_feedback = 'https://backend-remosto-ujrltkkgyq-et.a.run.app/feedback'
response_feedback = requests.get(url_feedback)
data = response_feedback.json()
feedback_data = data["data"]
feedback_df = pd.DataFrame(feedback_data, columns=["id", "section", "star", "categories", "desc", "timestamp"])
feedback_df.set_index("id", inplace=True)
reversed_feedback_df = feedback_df[::-1]

feedback_page = ["Home Page", "Feedback Informasi", "Feedback Tempat Makan", "Feedback Pelayanan Petugas", "Feedback Robot"]
selected_feedback = st.selectbox("", ["Home Page", "Feedback Informasi", "Feedback Tempat Makan", "Feedback Pelayanan Petugas", "Feedback Robot"])

if selected_feedback == "Home Page":
    root_feedback_data = reversed_feedback_df[reversed_feedback_df['section'] == "Root"]
    root_feedback_data_subset = root_feedback_data.loc[:, ['star', 'categories', 'desc', 'timestamp']]
    st.table(root_feedback_data_subset)
elif selected_feedback == "Feedback Informasi":
    informasi_feedback_data = reversed_feedback_df[reversed_feedback_df['section'] == "Informasi"]
    informasi_feedback_data_subset = informasi_feedback_data.loc[:, ['star', 'categories', 'desc', 'timestamp']]
    st.table(informasi_feedback_data)
elif selected_feedback == "Feedback Tempat Makan":
    tm_feedback_data = reversed_feedback_df[reversed_feedback_df['section'] == "Tempat Makan"]
    tm_feedback_data_subset = tm_feedback_data.loc[:, ['star', 'categories', 'desc', 'timestamp']]
    st.table(tm_feedback_data_subset)
elif selected_feedback == "Feedback Pelayanan Petugas":
    pelayanan_feedback_data = reversed_feedback_df[reversed_feedback_df['section'] == "Pelayanan Petugas"]
    pelayanan_feedback_data_subset = pelayanan_feedback_data.loc[:, ['star', 'categories', 'desc', 'timestamp']]
    st.table(pelayanan_feedback_data_subset)
else:
    robot_feedback_data = reversed_feedback_df[reversed_feedback_df['section'] == "robot"]
    robot_feedback_data_subset = robot_feedback_data.loc[:, ['star', 'categories', 'desc', 'timestamp']]
    st.table(robot_feedback_data_subset)