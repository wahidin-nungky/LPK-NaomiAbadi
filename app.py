import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CPMI System - Dark Mode",
    page_icon="🙋‍♀️",
    layout="wide"
)

# --- CUSTOM CSS UNTUK DARK MODE ELEGAN ---
st.markdown("""
    <style>
    /* Mengubah seluruh latar belakang menjadi gelap */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Styling Sidebar agar tetap kontras */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Mengubah warna teks judul dan label */
    h1, h2, h3, h4, label, .stMarkdown {
        color: #e6edf3 !important;
    }

    /* Styling Metric Cards agar menonjol di background gelap */
    div[data-testid="stMetric"] {
        background-color: #1c2128;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
    }
    
    div[data-testid="stMetricValue"] {
        color: #58a6ff !important;
    }

    /* Mempercantik Input Box */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }

    /* Footer Branding */
    .branding {
        font-size: 13px;
        color: #8b949e;
        margin-top: 50px;
        border-top: 1px solid #30363d;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
DB_FILE = "data_cpmi_v2.csv"
try:
    df = pd.read_csv(DB_FILE)
    if 'Sponsor' not in df.columns:
        df['Sponsor'] = "-"
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        'Nama CPMI', 'Tanggal Daftar', 'Masuk LPK', 'PT Penempatan', 'Agency Luar Negeri', 
        'Negara Tujuan', 'ID SISKO', 'Paspor', 'Ujian Kompetensi', 
        'Psikotest', 'MCU Full', 'Kontrak Kerja', 'Visa Kerja', 'Status Terbang', 'Sponsor'
    ])

# --- SISTEM LOGIN ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🔒Login")
        pwd = st.text_input("Password Staf", type="password")
        if st.button("Masuk ke Sistem", use_container_width=True):
            if pwd == "admin123":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Password salah.")
    st.stop()

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.markdown("### 😎 Admin")
    st.markdown("`Night Mode Active` 🌙")
    st.divider()
    
    menu = st.radio("MENU UTAMA", ["📊 Monitoring Progres", "➕ Registrasi Baru"])
    
    st.divider()
    if st.button("🔓 Keluar"):
        st.session_state["password_correct"] = False
        st.rerun()
    
    st.markdown(f"""
        <div class="branding">
            <b>Created by: LPK NAOMI ABADI</b><br>
            <i>powered by GEMINI</i>
        </div>
    """, unsafe_allow_html=True)

# --- MENU: TAMBAH DATA ---
if menu == "➕ Registrasi Baru":
    st.markdown("### ➕ Input Data CPMI Baru")
    with st.form("form_baru", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap")
            tgl = st.date_input("Tanggal Daftar", datetime.now())
            pt = st.text_input("PT Penempatan")
            sponsor = st.text_input("Sponsor / PL")
        with col2:
            agency = st.text_input("Agency Luar Negeri")
            negara = st.selectbox("Negara Tujuan", ["Taiwan", "Hong Kong", "Singapura", "Malaysia", "Polandia", "Jepang", "Korea Selatan", "Selandia Baru", "Slovakia"])
        
        if st.form_submit_button("Daftarkan Sekarang", use_container_width=True):
            new_data = {
                'Nama CPMI': nama, 'Tanggal Daftar': tgl, 'PT Penempatan': pt,
                'Agency Luar Negeri': agency, 'Negara Tujuan': negara,
                'ID SISKO': '⏳ Belum', 'Paspor': '⏳ Belum', 'Ujian Kompetensi': '⏳ Belum',
                'Psikotest': '⏳ Belum', 'MCU Full': '⏳ Belum', 'Kontrak Kerja': '⏳ Belum',
                'Visa Kerja': '⏳ Belum', 'Status Terbang': 'Proses', 'Sponsor': sponsor
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Data berhasil tersimpan!")

# --- MENU: DASHBOARD ---
elif menu == "📊 Monitoring Progres":
    st.markdown("### 📊 CPMI LPK NAOMI ABADI")
    
    # Header Statistics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total CPMI", len(df))
    m2.metric("Proses MCU", len(df[df['MCU Full'] == '⏳ Belum']))
    m3.metric("Kontrak Signed", len(df[df['Kontrak Kerja'] == '✅ Signed']))
    m4.metric("Siap Terbang", len(df[df['Status Terbang'] == 'Ready']))

    st.divider()

    # Search bar
    search = st.text_input("🔍 Filter Nama / PT / Sponsor", placeholder="Ketik di sini...")
    
    if search:
        display_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    else:
        display_df = df

    # Data Editor
    st.write("#### 📑 Progress Tracking Table")
    edited_df = st.data_editor(
        display_df,
        column_config={
            "ID SISKO": st.column_config.SelectboxColumn("SISKO", options=["⏳ Belum", "✅ Selesai"]),
            "Paspor": st.column_config.SelectboxColumn("Paspor", options=["⏳ Belum", "✅ Selesai"]),
            "Ujian Kompetensi": st.column_config.SelectboxColumn("Ujian", options=["⏳ Belum", "✅ Lulus"]),
            "Psikotest": st.column_config.SelectboxColumn("Psikotest", options=["⏳ Belum", "✅ Rekom", "❌ No Rekom"]),
            "MCU Full": st.column_config.SelectboxColumn("MCU", options=["⏳ Belum", "✅ Fit", "❌ Unfit"]),
            "Kontrak Kerja": st.column_config.SelectboxColumn("Kontrak", options=["⏳ Belum", "✅ Signed"]),
            "Visa Kerja": st.column_config.SelectboxColumn("Visa", options=["⏳ Belum", "✅ Terbit"]),
            "Status Terbang": st.column_config.SelectboxColumn("Status", options=["Proses", "Ready", "✈️ Terbang"]),
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("💾 Simpan Perubahan Data", use_container_width=True):
        df.update(edited_df)
        df.to_csv(DB_FILE, index=False)
        st.toast("Database Berhasil Diperbarui!", icon="🌙")
