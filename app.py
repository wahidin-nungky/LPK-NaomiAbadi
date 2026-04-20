import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Gemini CPMI System",
    page_icon="✨",
    layout="wide"
)

# --- CSS UNTUK MENIRU DASHBOARD GEMINI ---
st.markdown("""
    <style>
    /* Mengatur Header Hitam seperti di Screenshot */
    header {
        background-color: #131314 !important;
        color: white !important;
    }
    
    /* Sidebar Gelap/Navy */
    [data-testid="stSidebar"] {
        background-color: #00212b !important;
        color: white !important;
    }
    
    /* Menu Active (Toska seperti EasySwara) */
    .st-emotion-cache-17l69qf {
        background-color: #00a18e !important;
        border-radius: 8px;
    }

    /* Konten Utama Putih keabu-abuan lembut */
    .stApp {
        background-color: #f0f4f9;
    }

    /* Card Putih Bersih */
    div[data-testid="stForm"], div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 20px;
        border: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        padding: 25px;
    }

    /* Font Google Sans look */
    h1, h2, h3, p {
        color: #1f1f1f;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Branding Footer */
    .footer {
        position: fixed;
        bottom: 10px;
        font-size: 12px;
        color: #888;
        padding-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
DB_FILE = "data_cpmi_v2.csv"
try:
    df = pd.read_csv(DB_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        'Nama CPMI', 'Tanggal Daftar', 'PT Penempatan', 'Agency Luar Negeri', 
        'Negara Tujuan', 'ID SISKO', 'Paspor', 'Ujian Kompetensi', 
        'Psikotest', 'MCU Full', 'Kontrak Kerja', 'Visa Kerja', 'Status Terbang', 'Sponsor'
    ])

# --- SIDEBAR (Meniru EasySwara) ---
with st.sidebar:
    st.markdown("<h2 style='color: #00f2d1;'>✨ CPMI System</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MENU", ["📋 Dashboard Progres", "➕ Registrasi Baru"])
    
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color: #888;'>Created by: Wahidin<br>powered by GEMINI</p>", unsafe_allow_html=True)

# --- LOGIN (Simple & Clean) ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        st.markdown("### 👋 Selamat Datang")
        pwd = st.text_input("Password Staf", type="password")
        if st.button("Masuk"):
            if pwd == "admin123":
                st.session_state["password_correct"] = True
                st.rerun()
    st.stop()

# --- ISI APLIKASI ---
if menu == "➕ Registrasi Baru":
    st.markdown("<h1 style='text-align: center; color: #00a18e;'>Registrasi Peserta</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Lengkapi data CPMI untuk memulai alur proses.</p>", unsafe_allow_html=True)
    
    with st.form("gemini_style_form"):
        c1, c2 = st.columns(2)
        with c1:
            nama = st.text_input("Nama Lengkap")
            tgl = st.date_input("Tanggal Daftar")
            pt = st.text_input("PT Penempatan")
            sponsor = st.text_input("Sponsor / PL")
        with c2:
            agency = st.text_input("Agency")
            negara = st.selectbox("Negara Tujuan", ["Taiwan", "Hong Kong", "Polandia", "Jepang"])
        
        if st.form_submit_button("Simpan Data Baru"):
            new_data = {
                'Nama CPMI': nama, 'Tanggal Daftar': tgl, 'PT Penempatan': pt,
                'Agency Luar Negeri': agency, 'Negara Tujuan': negara,
                'ID SISKO': '⏳ Belum', 'Paspor': '⏳ Belum', 'Ujian Kompetensi': '⏳ Belum',
                'Psikotest': '⏳ Belum', 'MCU Full': '⏳ Belum', 'Kontrak Kerja': '⏳ Belum',
                'Visa Kerja': '⏳ Belum', 'Status Terbang': 'Proses', 'Sponsor': sponsor
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Data berhasil ditambahkan ke Cloud!")

else:
    st.markdown("<h1 style='text-align: center; color: #00a18e;'>Monitoring Progres</h1>", unsafe_allow_html=True)
    
    # Metrics ala Gemini
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total CPMI", len(df))
    m2.metric("Proses Dokumen", len(df[df['Visa Kerja'] == '⏳ Belum']))
    m3.metric("Kontrak Signed", len(df[df['Kontrak Kerja'] == '✅ Signed']))
    m4.metric("Siap Terbang", len(df[df['Status Terbang'] == 'Ready']))

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabel
    search = st.text_input("🔍 Cari Peserta...")
    if search:
        display_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    else:
        display_df = df

    edited_df = st.data_editor(display_df, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Simpan Perubahan"):
        df.update(edited_df)
        df.to_csv(DB_FILE, index=False)
        st.toast("Update Berhasil!")
