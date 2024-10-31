import streamlit as st
import pandas as pd
import plotly.express as px

# Set initial data with matching lengths
data = {
    "Nama Pegawai": ["Danny", "Fajar", "Teguh", "Sulung"],
    "Bidang Tugas": [
        "CRM Nikel", "CRM PBB", "CRM Rokok", "CRM Otomotif"
    ]
}

# Load initial DataFrame
df = pd.DataFrame(data)

# Streamlit setup
st.title("Dashboard Pembagian Tugas Pegawai")
st.write("Dashboard ini menampilkan pembagian tugas pegawai dengan visualisasi data berwarna biru dan kuning sesuai dengan logo Direktorat Jenderal Pajak.")

# Display the Dashboard Table
st.subheader("Pembagian Tugas Saat Ini")
st.dataframe(df)

# Form for Adding New Assignments
st.subheader("Tambah Data Pembagian Tugas")
with st.form(key="assignment_form"):
    nama_pegawai = st.selectbox("Nama Pegawai", ["Danny", "Fajar", "Teguh", "Sulung"])
    bidang_tugas = st.selectbox(
        "Bidang Tugas", 
        [
            "CRM Nikel", "CRM PBB", "CRM Rokok", "CRM Otomotif", 
            "CRM Sawit", "CRM Batu Bara", "CRM Transfer Pricing", 
            "Administrasi", "Data Engineer", "Data Scientist", 
            "Data Visualization"
        ]
    )
    submit_button = st.form_submit_button("Tambahkan Tugas")

    # Add new assignment to DataFrame
    if submit_button:
        new_data = {"Nama Pegawai": nama_pegawai, "Bidang Tugas": bidang_tugas}
        df = df.append(new_data, ignore_index=True)
        st.success(f"Tugas baru ditambahkan untuk {nama_pegawai} pada bidang {bidang_tugas}.")

# CSV Upload for Bulk Assignment Updates
st.subheader("Upload CSV untuk Pembagian Tugas")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    new_assignments = pd.read_csv(uploaded_file)
    df = pd.concat([df, new_assignments], ignore_index=True)
    st.success("Data dari CSV berhasil ditambahkan.")

# Visualizations
st.subheader("Visualisasi Pembagian Tugas")

# Task count per employee
task_count = df['Nama Pegawai'].value_counts().reset_index()
task_count.columns = ['Nama Pegawai', 'Jumlah Tugas']

# Task count per field
field_count = df['Bidang Tugas'].value_counts().reset_index()
field_count.columns = ['Bidang Tugas', 'Jumlah Pegawai']

# Colors: Blue and Yellow (for DJP theme)
colors = ["#002855", "#FFCC00"]  # Blue and Yellow

# Plot task count per employee
fig1 = px.bar(
    task_count, x="Nama Pegawai", y="Jumlah Tugas", 
    title="Jumlah Tugas per Pegawai", color_discrete_sequence=colors
)
st.plotly_chart(fig1, use_container_width=True)

# Plot task count per field
fig2 = px.pie(
    field_count, names="Bidang Tugas", values="Jumlah Pegawai", 
    title="Distribusi Tugas per Bidang", color_discrete_sequence=colors
)
st.plotly_chart(fig2, use_container_width=True)

# Display Updated Dashboard
st.subheader("Pembagian Tugas Terbaru")
st.dataframe(df)
