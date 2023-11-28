import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(
    page_title="Remosto",
    layout="wide",
    initial_sidebar_state="expanded"
)

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inisialisasi session state jika belum ada
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"

def load_data(period, count):
    # Fungsi load data
    url = 'https://us-west1-remosto-2023.cloudfunctions.net/endpoint-b/get'
    payload = {'data':['expression', 'race', 'gender', 'age', 'luggage'], 'period': period, 'count': count}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    data = response.json()
    return data

def authenticate_user(email, password):
    # Fungsi autentikasi
    url = 'https://us-west1-remosto-2023.cloudfunctions.net/endpoint-b/login/'
    payload = {'email': email, 'password': password}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code == 200:
        st.session_state.is_authenticated = True  # Update session state
        st.session_state.current_page = "Dashboard"  # Pindah ke halaman dashboard setelah login
        return True  # Authentication successful
    else:
        return False

def logout():
    # Fungsi logout
    st.session_state.is_authenticated = False
    st.session_state.current_page = "Login"
    
def display_dashboard():
    # Fungsi untuk menampilkan dashboard
    pages = ["Dashboard", "Detail Usia", "Detail Gender", "Detail Ekspresi", "Detail Ras", "Detail Bawaan"]

    selected_page = st.sidebar.selectbox("Select Page", pages)

    # Widget to choose time
    selected_period = st.sidebar.selectbox('Select Period', ["week","day"])
    selected_count = st.sidebar.slider('Select Count', min_value=1, max_value=20, value=6)

    # Load data based on selected time in widget
    data = load_data(selected_period, selected_count)
    # expression
    expression_data = data['data']['expression'][:selected_count]
    expression_df = pd.DataFrame(expression_data)
    expression_df = expression_df[::-1]
    # race
    race_data = data['data']['race'][:selected_count]
    race_df = pd.DataFrame(race_data)
    race_df = race_df[::-1]
    # gender
    gender_data = data['data']['gender'][:selected_count]
    gender_df = pd.DataFrame(gender_data)
    gender_df = gender_df[::-1]
    # age
    age_data = data['data']['age'][:selected_count]
    age_df = pd.DataFrame(age_data)
    age_df = age_df[::-1]
    # luggage
    luggage_data = data['data']['luggage'][:selected_count]
    luggage_df = pd.DataFrame(luggage_data)
    luggage_df = luggage_df[::-1]

    ###########
    # CONTENT #
    ###########

    # Content for each page
    if selected_page == "Dashboard":
        st.markdown(
        f'<h1 style="text-align: center;">Dashboard</h1><br>',
        unsafe_allow_html=True)
        
        #########
        # ROW A #
        #########
        a1, a2 = st.columns((7, 3))
        
        with a1:
            age_df = age_df.iloc[:, ::-1]
            age_df.drop('number', axis=1, inplace=True)

            mean_anak = age_df['anak'].mean()
            mean_remaja = age_df['remaja'].mean()
            mean_dewasa = age_df['dewasa'].mean()
            mean_lansia = age_df['lansia'].mean()

            mean_values = [mean_anak, mean_remaja, mean_dewasa, mean_lansia]

            # Bar chart
            fig = px.bar(x=mean_values,
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
            
        with a2:
            pie_gender_df = gender_df[['pria','wanita']]
            mean_pria = pie_gender_df['pria'].mean()
            mean_wanita = pie_gender_df['wanita'].mean()

            fig_gender = px.pie(names=["Pria", "Wanita"], values=[mean_pria, mean_wanita])
            fig_gender.update_traces(marker=dict(colors=['#d60003', '#f3722c']))
            
            fig_gender.update_layout(
                title_text="Persebaran Gender",
                title_x=0.035,
                title_y=0.9,
                title_font=dict(size=27),
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=10, r=10, t=0, b=0)
                )
            
            fig_gender.update_traces(textinfo='label+percent')
            fig_gender.update_layout(showlegend=False)
            st.plotly_chart(fig_gender, use_container_width=True)
            
        #########
        # ROW B #
        #########
        b1, b2 = st.columns((3, 7))
        
        with b1: 
            mean_manusia = luggage_df['manusia'].mean()
            mean_besar = luggage_df['besar'].mean()
            mean_sedang = luggage_df['sedang'].mean()
            mean_kecil = luggage_df['kecil'].mean()

            mean_values = [mean_manusia, mean_besar, mean_sedang, mean_kecil]
            categories = ['Manusia', 'Besar', 'Sedang', 'Kecil']
            colors = ['#d60003', '#f8961e', '#f3722c', '#f9844a']

            fig = px.pie(
                names=categories,
                values=mean_values,
                hole=0.4,
                color_discrete_sequence=colors
            )

            fig.update_layout(
                title_text="Bawaan Pengunjung",
                title_x=0,
                title_y=0.9,
                title_font=dict(size=27),
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=10, r=10, t=0, b=0)
                )

            fig.update_traces(textinfo='percent+label')
            fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)
            
        with b2:
            expression_df.drop('number', axis=1, inplace=True)

            mean_marah = expression_df['marah'].mean()
            mean_risih = expression_df['risih'].mean()
            mean_takut = expression_df['takut'].mean()
            mean_senyum = expression_df['senyum'].mean()
            mean_netral = expression_df['netral'].mean()
            mean_sedih = expression_df['sedih'].mean()
            mean_terkejut = expression_df['terkejut'].mean()

            mean_values = [mean_marah, mean_risih, mean_takut, mean_senyum, mean_netral, mean_sedih, mean_terkejut]
            
            colors = ['red', 'green', 'grey', 'orange', 'lightgrey', 'blue', 'purple']

            # Bar chart
            fig = px.bar(x=['Marah', 'Risih', 'Takut', 'Senyum', 'Netral', 'Sedih', 'Terkejut'],
                        y=mean_values,
                        color=['Marah', 'Risih', 'Takut', 'Senyum', 'Netral', 'Sedih', 'Terkejut'],
                        color_discrete_sequence=colors,
                        text_auto='.2s')

            fig.update_xaxes(title_text=None)
            fig.update_yaxes(title_text=None)
            fig.update_layout(showlegend=False)
            
            fig.update_layout(
                width=600,
                height=350,
                title_text="Ekspresi Pengunjung",
                title_x=0,
                title_y=0.865, 
                title_font=dict(size=27),
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=10, r=10, t=110, b=0)
                )
            
            emoji_mapping = {
            'Marah': '😡',
            'Risih': '😒',
            'Takut': '😱',
            'Senyum': '😊',
            'Netral': '😐',
            'Sedih': '😢',
            'Terkejut': '😲'
            }
            
            for i, expression in enumerate(['Marah', 'Risih', 'Takut', 'Senyum', 'Netral', 'Sedih', 'Terkejut']):
                emoji = emoji_mapping.get(expression, '')  # Ambil emoji yang sesuai dengan ekspresi
                fig.add_annotation(
                    x=i,
                    y=mean_values[i] + 0.5,
                    text=emoji, 
                    showarrow=False,  
                    font=dict(family="Arial", size=14),
                    xanchor="center"
                    )
                
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
        #########
        #########
        
        time = race_df['number'].unique()
        races = race_df.columns[:7]

        # # Mengelompokkan data berdasarkan kolom "number" dan menghitung jumlah ekspresi untuk setiap ekspresi emosi
        grouped_data = race_df.groupby('number')[races].sum()

        # # DataFrame untuk Plotly
        race_plotly = grouped_data.reset_index()
        race_plotly['number'] = race_plotly['number'].max() - race_plotly['number'] + 1

        fig = px.line(race_plotly, x=time, y=race_plotly.columns[1:], markers=True,
                    labels={'variable': 'Race', 'value': 'Proportion'})
        
        fig.update_traces(line=dict(width=3),
                        marker=dict(size=10))

        # Atur judul
        fig.update_layout(
            title="Persebaran Ras",
            xaxis_title=selected_period
        )

        fig.data[0].name = 'Negroid'
        fig.data[1].name = 'East Asian'
        fig.data[2].name = 'Indian'
        fig.data[3].name = 'Latin'
        fig.data[4].name = 'Middle Eastern'
        fig.data[5].name = 'SEA'
        fig.data[6].name = 'Caucasian'
        
        fig.update_layout(legend=dict(title="Race"),
                        width=600,
                        height=500,
                        title_text=f"Count of races by {selected_period}",
                        title_x=0,
                        title_y=0.99,
                        title_font=dict(size=27),
                        margin=dict(l=10, r=10, t=60, b=0))

        fig.update_yaxes(title_text=None)
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        st.plotly_chart(fig, use_container_width=True)
        

    elif selected_page == "Detail Usia":
        st.markdown(
        f'<h1 style="text-align: center;">Detail Usia</h1><br>',
        unsafe_allow_html=True)
        
        #########
        #########
        age_data = age_df.iloc[:, ::-1]
        age_data = age_data.drop('number', axis=1, inplace=True)

        mean_anak = age_df['anak'].mean()
        mean_remaja = age_df['remaja'].mean()
        mean_dewasa = age_df['dewasa'].mean()
        mean_lansia = age_df['lansia'].mean()

        mean_values = [mean_anak, mean_remaja, mean_dewasa, mean_lansia]

        # Bar chart
        fig = px.bar(x=mean_values,
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
        
        #########
        #########
        
        st.subheader("")
        
        days = age_df['number'].unique()
        age = age_df.columns[:4]

        # Mengelompokkan data berdasarkan kolom "number" dan menghitung jumlah ekspresi untuk setiap ekspresi emosi
        grouped_data = age_df.groupby('number')[age].sum()

        # DataFrame untuk Plotly
        plotly_data = grouped_data.reset_index()

        plotly_data['number'] = plotly_data['number'].max() - plotly_data['number'] + 1

        fig = px.bar(plotly_data, x='number', y=age, barmode='group',
                    labels={'number': str(selected_period), 'variable': 'Gender'},
                    color_discrete_sequence=['#f49275', '#f9844a', '#f8961e','#f3722c'],
                    text_auto='.3s')

        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.35, title=""),
                        width=600,
                        height=360,
                        title_text=f"Count age by {selected_period}",
                        title_x=0,
                        title_y=0.99,
                        title_font=dict(size=27),
                        margin=dict(l=10, r=10, t=60, b=0))

        fig.update_yaxes(title_text=None)
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)
        
        st.plotly_chart(fig, use_container_width=True) 
        
        #########
        #########
        
        st.subheader("")
        st.subheader("Data Usia Pengunjung") 
        
        table = plotly_data.drop(columns=['number'])
        st.dataframe(table)
        
    elif selected_page == "Detail Gender": 
        st.markdown(
        f'<h1 style="text-align: center;">Detail Gender</h1><br><br>',
        unsafe_allow_html=True)
        
        #########
        # ROW C #
        #########
        c1, c2, c3 = st.columns((3, 5, 2))

        with c1:
            pie_gender_df = gender_df[['pria','wanita']]
            mean_pria = pie_gender_df['pria'].mean()
            mean_wanita = pie_gender_df['wanita'].mean()

            fig_gender = px.pie(names=["Pria", "Wanita"], values=[mean_pria, mean_wanita])
            fig_gender.update_traces(marker=dict(colors=['#d60003', '#f3722c']))
            
            fig_gender.update_layout(
                title_text="Persebaran Gender",
                title_x=0.035,
                title_y=0.99,
                title_font=dict(size=27),
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=10, r=10, t=10, b=0)
                )
            
            fig_gender.update_traces(textinfo='label+percent')
            fig_gender.update_layout(showlegend=False)
            st.plotly_chart(fig_gender, use_container_width=True)
            
        with c2:
            days = gender_df['number'].unique()
            genders = ['pria', 'wanita']

            grouped_data = gender_df.groupby('number')[genders].sum()
            
            # Buat DataFrame baru dengan data yang sudah diurutkan
            reversed_grouped_data = grouped_data.reset_index()
            # reversed_grouped_data = reversed_grouped_data.drop(columns=['number'])
            reversed_grouped_data['number'] = reversed_grouped_data['number'].max() - reversed_grouped_data['number'] + 1

            fig = px.bar(reversed_grouped_data, x='number', y=genders, barmode='group',
                        labels={'number': str(selected_period), 'variable': 'Gender'},
                        color_discrete_sequence=['#d60003', '#f3722c']
                        )
            
            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.35, title=""),
                            width=600,
                            height=360,
                            title_text=f"Count gender by {selected_period}",
                            title_x=0,
                            title_y=0.99,
                            title_font=dict(size=27),
                            margin=dict(l=10, r=10, t=60, b=0))
            
            fig.update_yaxes(title_text=None)
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
        with c3:
            st.subheader("")
            st.subheader("")
            st.subheader("")
            reversed_gro = reversed_grouped_data.drop(columns=['number'])
            st.dataframe(reversed_gro)
            
            
    elif selected_page == "Detail Ekspresi": 
        st.markdown(
        f'<h1 style="text-align: center;">Detail Ekspresi</h1><br>',
        unsafe_allow_html=True)
        
        #########
        # ROW D #
        #########
        
        exp_fig_1 = expression_df.drop('number', axis=1)

        mean_marah = exp_fig_1['marah'].mean()
        mean_risih = exp_fig_1['risih'].mean()
        mean_takut = exp_fig_1['takut'].mean()
        mean_senyum = exp_fig_1['senyum'].mean()
        mean_netral = exp_fig_1['netral'].mean()
        mean_sedih = exp_fig_1['sedih'].mean()
        mean_terkejut = exp_fig_1['terkejut'].mean()

        mean_values = [mean_marah, mean_risih, mean_takut, mean_senyum, mean_netral, mean_sedih, mean_terkejut]

        colors = ['red', 'green', 'grey', 'orange', 'lightgrey', 'blue', 'purple']

        # Bar chart
        fig = px.bar(x=['Marah', 'Risih', 'Takut', 'Senyum', 'Netral', 'Sedih', 'Terkejut'],
                    y=mean_values,
                    color=['Marah', 'Risih', 'Takut', 'Senyum', 'Netral', 'Sedih', 'Terkejut'],
                    color_discrete_sequence=colors,
                    text_auto='.2s')

        fig.update_xaxes(title_text=None)
        fig.update_yaxes(title_text=None)
        fig.update_layout(showlegend=False)

        fig.update_layout(
            width=600,
            height=350,
            title_text="Ekspresi Pengunjung",
            title_x=0,
            title_y=0.865, 
            title_font=dict(size=27),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=10, r=10, t=110, b=0)
            )

        emoji_mapping = {
        'Marah': '😡',
        'Risih': '😒',
        'Takut': '😱',
        'Senyum': '😊',
        'Netral': '😐',
        'Sedih': '😢',
        'Terkejut': '😲'
        }

        for i, expression in enumerate(['Marah', 'Risih', 'Takut', 'Senyum', 'Netral', 'Sedih', 'Terkejut']):
            emoji = emoji_mapping.get(expression, '')  # Ambil emoji yang sesuai dengan ekspresi
            fig.add_annotation(
                x=i,
                y=mean_values[i] + 0.5,
                text=emoji, 
                showarrow=False,  
                font=dict(family="Arial", size=14),
                xanchor="center"
                )
            
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        st.plotly_chart(fig, use_container_width=True)   
        
        #########
        #########
        
        st.subheader("")
        st.subheader("")
        
        days = expression_df['number'].unique()
        emotions = expression_df.columns[:6]

        # Mengelompokkan data berdasarkan kolom "number" dan menghitung jumlah ekspresi untuk setiap ekspresi emosi
        grouped_data = expression_df.groupby("number")[emotions].sum()

        # DataFrame untuk Plotly
        plotly_data = grouped_data.reset_index()

        plotly_data['number'] = plotly_data['number'].max() - plotly_data['number'] + 1

        # Membuat grafik bar
        fig = px.bar(plotly_data, x='number', y=emotions, barmode='group',
                    labels={'number': str(selected_period), 'variable': 'Expression'},
                    color_discrete_sequence=['red', 'green', 'grey', 'orange', 'lightgrey', 'blue', 'purple'],
                    text_auto='.3s')

        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.3, title=""),
                            width=600,
                            height=380,
                            title_text=f"Count expression by {selected_period}",
                            title_x=0,
                            title_y=0.99,
                            title_font=dict(size=27),
                            margin=dict(l=10, r=10, t=60, b=0))

        fig.update_yaxes(showticklabels=False)
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        st.plotly_chart(fig, use_container_width=True)
        
        #########
        #########
        
        st.subheader("")
        st.subheader("Data Ekspresi Pengunjung") 
        
        table = plotly_data.drop(columns=['number'])
        st.dataframe(table)
        
    elif selected_page == "Detail Ras": 
        st.markdown(
        f'<h1 style="text-align: center;">Detail Ras</h1><br><br>',
        unsafe_allow_html=True)

        #########
        #########
        
        time = race_df['number'].unique()
        races = race_df.columns[:7]

        # Mengelompokkan data berdasarkan kolom "number" dan menghitung jumlah ekspresi untuk setiap ekspresi emosi
        grouped_data = race_df.groupby('number')[races].sum()

        # DataFrame untuk Plotly
        race_plotly = grouped_data.reset_index()
        race_plotly['number'] = race_plotly['number'].max() - race_plotly['number'] + 1

        fig = px.line(race_plotly, x=time, y=race_plotly.columns[1:], markers=True,
                    labels={'variable': 'Race', 'value': 'Proportion'})
        
        fig.update_traces(line=dict(width=3),
                        marker=dict(size=10))

        # Atur judul
        fig.update_layout(
            title="Persebaran Ras",
            xaxis_title=selected_period
        )

        fig.data[0].name = 'Negroid'
        fig.data[1].name = 'East Asian'
        fig.data[2].name = 'Indian'
        fig.data[3].name = 'Latin'
        fig.data[4].name = 'Middle Eastern'
        fig.data[5].name = 'SEA'
        fig.data[6].name = 'Caucasian'
        
        fig.update_layout(legend=dict(title="Race"),
                        width=600,
                        height=500,
                        title_text=f"Count of races by {selected_period}",
                        title_x=0,
                        title_y=0.99,
                        title_font=dict(size=27),
                        margin=dict(l=10, r=10, t=60, b=0))

        fig.update_yaxes(title_text=None)
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        st.plotly_chart(fig, use_container_width=True)
            
        #########
        #########
        
        st.subheader("")
        st.subheader("Data Ras Pengunjung") 
        
        table = race_plotly.drop(columns=['number'])
        st.dataframe(table)
        
    elif selected_page == "Detail Bawaan": 
        st.markdown(
        f'<h1 style="text-align: center;">Detail Bawaan</h1><br><br>',
        unsafe_allow_html=True)
        
        f1, f2 = st.columns((3, 7))
        
        with f1: 
            mean_manusia = luggage_df['manusia'].mean()
            mean_besar = luggage_df['besar'].mean()
            mean_sedang = luggage_df['sedang'].mean()
            mean_kecil = luggage_df['kecil'].mean()

            mean_values = [mean_manusia, mean_besar, mean_sedang, mean_kecil]
            categories = ['Manusia', 'Besar', 'Sedang', 'Kecil']
            colors = ['#d60003', '#f8961e', '#f3722c', '#f9844a']

            fig = px.pie(
                names=categories,
                values=mean_values,
                hole=0.4,
                color=categories,
                color_discrete_map={'Manusia':'#d60003',
                                    'Besar':'#f8961e',
                                    'Sedang':'#f3722c',
                                    'Kecil':'#f9844a'}
            )

            fig.update_layout(
                title_text="Bawaan Pengunjung",
                title_x=0,
                title_y=1,
                title_font=dict(size=27),
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=10, r=10, t=0, b=0)
                )

            fig.update_traces(textinfo='percent+label')
            fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)
            
        with f2:
            days = luggage_df['number'].unique()
            luggage = luggage_df.columns[:4]

            # Mengelompokkan data berdasarkan kolom "number" dan menghitung jumlah ekspresi untuk setiap ekspresi emosi
            grouped_data = luggage_df.groupby('number')[luggage].sum()

            # DataFrame untuk Plotly
            plotly_data = grouped_data.reset_index()

            plotly_data['number'] = plotly_data['number'].max() - plotly_data['number'] + 1

            # Membuat grafik bar
            fig = px.bar(plotly_data, x='number', y=luggage, barmode='group',
                        labels={'number': str(selected_period), 'variable': 'Luggage'},
                        color_discrete_sequence=['#d60003', '#f8961e', '#f3722c', '#f9844a']
                        )

            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.3, title=""),
                                width=600,
                                height=370,
                                title_text=f"Count of luggage by {selected_period}",
                                title_x=0,
                                title_y=1,
                                title_font=dict(size=27),
                                margin=dict(l=10, r=10, t=60, b=0))

            fig.update_yaxes(title_text=None)
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)

            st.plotly_chart(fig, use_container_width=True)
            
        #########
        #########
        
        st.subheader("Data Bawaan Pengunjung") 
        
        table = plotly_data.drop(columns=['number'])
        st.dataframe(table)
    
def login_page():
    # Fungsi untuk menampilkan halaman login
    st.title("Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        is_authenticated = authenticate_user(email, password)
        if is_authenticated:
            st.success("Login successful!")
            display_dashboard()
        else:
            st.error("Login failed. Please check your email and password.")

# # Tampilkan halaman sesuai dengan status current_page
# if st.session_state.current_page == "Login":
#     login_page()

# elif st.session_state.current_page == "Dashboard":
#     display_dashboard()

import subprocess
def analytics():
    subprocess.run(["streamlit", "run", "setup.py"])
      
# Tampilkan halaman sesuai dengan status current_page
if st.session_state.current_page == "Login":
    login_page()
elif st.session_state.current_page == "Dashboard":
    st.sidebar.button("Logout", on_click=logout)
    st.sidebar.button("Analytics", on_click=analytics)
    display_dashboard()
    

# st.session_state.is_authenticated = False

# def load_data(period, count):
#     url = 'https://us-west1-remosto-2023.cloudfunctions.net/endpoint-b/get'
#     payload = {'data':['expression', 'race', 'gender', 'age', 'luggage'], 'period': period, 'count': count}
#     headers = {'Content-type': 'application/json'}
#     response = requests.post(url=url, data=json.dumps(payload), headers=headers)
#     data = response.json()
#     return data

# def authenticate_user(email, password):
#     url = 'https://us-west1-remosto-2023.cloudfunctions.net/endpoint-b/login/'
#     payload = {'email': email, 'password': password}
#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(url=url, json=payload, headers=headers)

#     if response.status_code == 200:
#         st.session_state.is_authenticated = True  # Update session state
#         return True  # Authentication successful
#     else:
#         return False

# def display_dashboard():
#     ###########
#     # SIDEBAR #
#     ###########

#     # Widget to choose page
#     pages = ["Dashboard", "Detail Usia", "Detail Gender", "Detail Ekspresi", "Detail Ras", "Detail Bawaan"]


#     selected_page = st.sidebar.selectbox("Select Page", pages)

#     # Widget to choose time
#     selected_period = st.sidebar.selectbox('Select Period', ["week","day"])
#     selected_count = st.sidebar.slider('Select Count', min_value=1, max_value=20, value=3)

#     # Load data based on selected time in widget
#     data = load_data(selected_period, selected_count)
#     # expression
#     expression_data = data['data']['expression'][:selected_count]
#     expression_df = pd.DataFrame(expression_data)
#     expression_df = expression_df[::-1]
#     # race
#     race_data = data['data']['race'][:selected_count]
#     race_df = pd.DataFrame(race_data)
#     race_df = race_df[::-1]
#     # gender
#     gender_data = data['data']['gender'][:selected_count]
#     gender_df = pd.DataFrame(gender_data)
#     gender_df = gender_df[::-1]
#     # age
#     age_data = data['data']['age'][:selected_count]
#     age_df = pd.DataFrame(age_data)
#     age_df = age_df[::-1]
#     # luggage
#     luggage_data = data['data']['luggage'][:selected_count]
#     luggage_df = pd.DataFrame(luggage_data)
#     luggage_df = luggage_df[::-1]

#     ###########
#     # CONTENT #
#     ###########

#     # Content for each page
#     if selected_page == "Dashboard":
#         st.markdown(
#         f'<h1 style="text-align: center;">Dashboard</h1><br>',
#         unsafe_allow_html=True)
        
#         #########
#         # ROW A #
#         #########
#         a1, a2 = st.columns((7, 3))
        
#         with a1:
#             age_df = age_df.iloc[:, ::-1]
#             age_df.drop('number', axis=1, inplace=True)

#             mean_anak = age_df['anak'].mean()
#             mean_remaja = age_df['remaja'].mean()
#             mean_dewasa = age_df['dewasa'].mean()
#             mean_lansia = age_df['lansia'].mean()

#             mean_values = [mean_anak, mean_remaja, mean_dewasa, mean_lansia]

#             # Bar chart
#             fig = px.bar(x=mean_values,
#                         y=['Anak', 'Remaja', 'Dewasa', 'Lansia'],
#                         color_discrete_sequence=['#d60003', '#d60003', '#d60003', '#d60003'],
#                         text_auto='.3s')

#             fig.update_xaxes(title_text=None)
#             fig.update_yaxes(title_text=None)
#             fig.update_layout(showlegend=False)
            
#             fig.update_layout(
#                 width=600,
#                 height=350,
#                 title_text="Persebaran Umur",
#                 title_x=0,
#                 title_y=0.865, 
#                 title_font=dict(size=27),
#                 paper_bgcolor='rgba(0, 0, 0, 0)',
#                 plot_bgcolor='rgba(0, 0, 0, 0)',
#                 margin=dict(l=10, r=10, t=110, b=0)
#                 )
#             fig.update_xaxes(showgrid=True)
#             fig.update_yaxes(showgrid=True)
            
#             st.plotly_chart(fig, use_container_width=True)
            
#         with a2:
#             pie_gender_df = gender_df[['pria','wanita']]
#             mean_pria = pie_gender_df['pria'].mean()
#             mean_wanita = pie_gender_df['wanita'].mean()

#             fig_gender = px.pie(names=["Pria", "Wanita"], values=[mean_pria, mean_wanita])
#             fig_gender.update_traces(marker=dict(colors=['#d60003', '#f3722c']))
            
#             fig_gender.update_layout(
#                 title_text="Persebaran Gender",
#                 title_x=0.035,
#                 title_y=0.9,
#                 title_font=dict(size=27),
#                 paper_bgcolor='rgba(0, 0, 0, 0)',
#                 plot_bgcolor='rgba(0, 0, 0, 0)',
#                 margin=dict(l=10, r=10, t=0, b=0)
#                 )
            
#             fig_gender.update_traces(textinfo='label+percent')
#             fig_gender.update_layout(showlegend=False)
#             st.plotly_chart(fig_gender, use_container_width=True)
        
#     st.title("Dashboard Page")
#     # Tambahkan konten halaman dashboard di sini
    
# def login_page():
#     if st.session_state.is_authenticated:
#         display_dashboard()
#         return
    
#     st.title("Login Page")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         is_authenticated = authenticate_user(email, password)
#         if is_authenticated:
#             st.session_state.is_authenticated = True  # Menandai bahwa pengguna sudah terautentikasi
#             st.success("Login successful!")
#             display_dashboard()
#         else:
#             st.error("Login failed. Please check your email and password.")

# # Inisialisasi session state jika belum ada
# if "is_authenticated" not in st.session_state:
#     st.session_state.is_authenticated = False

# # Panggil fungsi login_page
# login_page()