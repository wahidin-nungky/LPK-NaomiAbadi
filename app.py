import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Monitoring CPMI v2.2",
    page_icon="📋",
    layout="wide"
)

# --- DATABASE ---
DB_FILE = "data_cpmi_v2.csv"
try:
    df = pd.read_csv(DB_FILE)
    # Memastikan kolom Sponsor ada jika file lama belum memilikinya
    if 'Sponsor' not in df.columns:
        df['Sponsor'] = "-"
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        'Nama CPMI', 'Tanggal Daftar', 'PT Penempatan', 'Agency Luar Negeri', 
        'Negara Tujuan', 'ID SISKO', 'Paspor', 'Ujian Kompetensi', 
        'Psikotest', 'MCU Full', 'Kontrak Kerja', 'Visa Kerja', 'Status Terbang', 'Sponsor'
    ])

# --- SISTEM LOGIN ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Admin Login")
        pwd = st.text_input("Masukkan Password", type="password")
        if st.button("Masuk"):
            if pwd == "admin123":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Password Salah!")
    st.stop()

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.header("🚢 Menu Utama")
    menu = st.radio("Pilih Menu:", ["📊 Dashboard Monitoring", "➕ Tambah CPMI Baru"])
    st.divider()
    if st.button("Log Out"):
        st.session_state["password_correct"] = False
        st.rerun()

# --- MENU: TAMBAH DATA ---
if menu == "➕ Tambah CPMI Baru":
    st.title("📝 Registrasi CPMI")
    with st.form("form_baru"):
        c1, c2 = st.columns(2)
        with c1:
            nama = st.text_input("Nama Lengkap CPMI")
            tgl = st.date_input("Tanggal Pendaftaran", datetime.now())
            pt = st.text_input("Nama PT Penempatan")
            sponsor = st.text_input("Nama Sponsor / PL") # Tambahan Input Sponsor
        with c2:
            agency = st.text_input("Nama Agency Luar Negeri")
            negara = st.selectbox("Negara Tujuan", ["Taiwan", "Hong Kong", "Singapura", "Malaysia", "Polandia", "Jepang", "Korea Selatan"])
        
        if st.form_submit_button("Simpan Data"):
            new_data = {
                'Nama CPMI': nama, 'Tanggal Daftar': tgl, 'PT Penempatan': pt,
                'Agency Luar Negeri': agency, 'Negara Tujuan': negara,
                'ID SISKO': '⏳ Belum', 'Paspor': '⏳ Belum', 'Ujian Kompetensi': '⏳ Belum',
                'Psikotest': '⏳ Belum', 'MCU Full': '⏳ Belum', 'Kontrak Kerja': '⏳ Belum',
                'Visa Kerja': '⏳ Belum', 'Status Terbang': 'Proses', 'Sponsor': sponsor
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"Data {nama} (Sponsor: {sponsor}) berhasil disimpan!")

# --- MENU: DASHBOARD MONITORING ---
elif menu == "📊 Dashboard Monitoring":
    st.title("📊 Monitoring Alur Proses CPMI")
    
    # Ringkasan Statistik
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total CPMI", len(df))
    s2.metric("Proses Visa", len(df[df['Visa Kerja'] == '⏳ Belum']))
    s3.metric("Lulus MCU", len(df[df['MCU Full'] == '✅ Fit']))
    s4.metric("Siap Terbang", len(df[df['Status Terbang'] == 'Ready']))

    st.divider()

    # Search bar
    search = st.text_input("🔍 Cari (Nama, PT, Agency, Negara, atau Sponsor)")
    if search:
        display_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    else:
        display_df = df

    # Tabel Editor
    st.write("### 📋 Tabel Progress")
    edited_df = st.data_editor(
        display_df,
        column_config={
            "ID SISKO": st.column_config.SelectboxColumn("ID SISKO", options=["⏳ Belum", "✅ Selesai"]),
            "Paspor": st.column_config.SelectboxColumn("Paspor", options=["⏳ Belum", "✅ Selesai"]),
            "Ujian Kompetensi": st.column_config.SelectboxColumn("Ujian", options=["⏳ Belum", "✅ Lulus"]),
            "Psikotest": st.column_config.SelectboxColumn("Psikotest", options=["⏳ Belum", "✅ Rekomendasi", "❌ Tidak Rekom"]),
            "MCU Full": st.column_config.SelectboxColumn("MCU", options=["⏳ Belum", "✅ Fit", "❌ Unfit"]),
            "Kontrak Kerja": st.column_config.SelectboxColumn("Kontrak", options=["⏳ Belum", "✅ Signed"]),
            "Visa Kerja": st.column_config.SelectboxColumn("Visa", options=["⏳ Belum", "✅ Terbit"]),
            "Status Terbang": st.column_config.SelectboxColumn("Terbang", options=["Proses", "Ready", "✈️ Terbang"]),
            "Sponsor": st.column_config.TextColumn("Sponsor", width="medium") # Kolom Sponsor
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("💾 Simpan Perubahan Data"):
        df.update(edited_df)
        df.to_csv(DB_FILE, index=False)
        st.success("Data berhasil diperbarui!")
