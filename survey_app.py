import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from PIL import Image
import numpy as np

# Konfigurasi halaman
st.set_page_config(page_title="Football Fan Survey", layout="wide")

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
        body {
            background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1b1b1b);
            background-size: 400% 400%;
            animation: gradient 10s ease infinite;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            margin-top: -30px;
            color: #FFD700;
            text-shadow: 2px 2px #000000;
        }
        .subtitle {
            text-align: center;
            font-size: 1.3em;
            color: #dddddd;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #1f7a1f;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Background Musik
st.markdown("""
    <audio autoplay loop>
        <source src="https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Scott_Holmes/Corporate__Motivational_Music/Scott_Holmes_-_Energy.mp3" type="audio/mpeg">
    </audio>
""", unsafe_allow_html=True)

# Judul Hero Section
st.markdown('<div class="title">⚽ Football Fan Survey ⚽</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bergabunglah dan beri tahu kami klub & pemain favoritmu!</div>', unsafe_allow_html=True)

# Navigasi
menu = st.sidebar.radio("📍 Navigasi", ["Isi Survei", "Statistik", "Peta", "Tentang"])

# FORMULIR
if menu == "Isi Survei":
    st.header("📋 Formulir Penggemar Sepak Bola")
    
    with st.form(key="survey_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap")
            klub = st.selectbox("Klub Favorit", ["Real Madrid", "Barcelona", "Man City", "Liverpool", "MU", "Arsenal", "Bayern", "PSG", "Juventus", "Inter Milan"])
            pemain = st.text_input("Pemain Favorit")
        with col2:
            liga = st.selectbox("Liga Favorit", ["La Liga", "Premier League", "Bundesliga", "Serie A", "Ligue 1", "Liga Indonesia"])
            sejak = st.date_input("Sejak Tahun Menyukai Sepak Bola")
            foto = st.file_uploader("Upload Foto Favorit", type=["jpg", "jpeg", "png"])

        kirim = st.form_submit_button("Kirim 🔥")
        
        if kirim:
            st.success("Terima kasih telah mengisi survei!")
            st.markdown(f"""
                **Nama:** {nama}  
                **Klub Favorit:** {klub}  
                **Pemain Favorit:** {pemain}  
                **Liga Favorit:** {liga}  
                **Sejak:** {sejak}
            """)
            if foto:
                st.image(foto, caption="Favorit Kamu", use_column_width=True)

# STATISTIK
elif menu == "Statistik":
    st.header("📊 Statistik Klub Populer")

    # Data klub sepak bola
    data = pd.DataFrame({
        'Klub': [
            "Real Madrid", "Barcelona", "Manchester United", "Liverpool",
            "Bayern Munich", "Arsenal", "Juventus", "Inter Milan",
            "Paris Saint-Germain", "AC Milan"
        ],
        'Trofi': [95, 92, 68, 65, 82, 45, 67, 55, 48, 50]
    })

    # Menampilkan Tabel Data Statistik
    st.subheader("Tabel Statistik Trofi Klub")
    st.dataframe(data)

    # Tab untuk grafik
    tab1, tab2 = st.tabs(["📈 Bar Chart", "🥧 Pie Chart"])
    with tab1:
        fig_bar = px.bar(
            data, x="Klub", y="Trofi", color="Klub",
            title="Jumlah Trofi Klub-Klub Populer",
            template="plotly_dark"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    with tab2:
        fig_pie = px.pie(
            data, names="Klub", values="Trofi",
            title="Distribusi Klub Favorit Berdasarkan Trofi",
            hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with st.expander("📈 Lihat Diagram Garis Tren Trofi"):
        # Data tren dummy
        tahun = list(range(2010, 2021))
        trend_data = pd.DataFrame({
            'Tahun': tahun,
            'Real Madrid': [60, 62, 64, 66, 69, 71, 74, 78, 82, 90, 95],
            'Barcelona': [58, 60, 63, 65, 68, 70, 73, 76, 80, 87, 92],
            'Man United': [60, 61, 61, 62, 63, 64, 65, 66, 66, 67, 68],
            'Liverpool': [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
        })

        df_melted = trend_data.melt(id_vars="Tahun", var_name="Klub", value_name="Trofi")

        fig_line = px.line(
            df_melted, x="Tahun", y="Trofi", color="Klub",
            title="Tren Jumlah Trofi Klub dari Tahun ke Tahun",
            markers=True,
            template="plotly_dark"
        )
        st.plotly_chart(fig_line, use_container_width=True)

# PETA
elif menu == "Peta":
    st.header("🌍 Lokasi Random Fans di Dunia")

    lokasi = pd.DataFrame({
        'lat': np.random.uniform(-6.5, 6.5, 100),
        'lon': np.random.uniform(95, 141, 100)
    })

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=lokasi,
        get_position='[lon, lat]',
        get_color='[0, 255, 0, 160]',
        get_radius=100,
    )

    view_state = pdk.ViewState(latitude=0, longitude=120, zoom=3)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

    st.pydeck_chart(deck)

# TENTANG
elif menu == "Tentang":
    st.header("ℹ️ Tentang Sejarah Sepak Bola Dunia")
    st.video("https://youtu.be/fn9ZQRO6F88?si=A1AvirHLTLteTa3d")
    st.markdown("""
        Aplikasi ini dibuat untuk menyatukan para penggemar sepak bola dari berbagai penjuru.  
        Tujuan kami adalah untuk melihat tren klub favorit, pemain idola, dan liga paling digemari.  
        Dibuat oleh Nahdatunnisa
    """)
