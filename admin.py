import streamlit as st
import pandas as pd
import mysql.connector
from io import BytesIO

# Fungsi untuk mengambil data dari database MySQL
def get_data_from_db():
    try:
        # Koneksi ke database MySQL
        conn = mysql.connector.connect(
            host="154.26.133.67",  # Ganti dengan host MySQL Anda
            user="remotex",        # Ganti dengan username MySQL Anda
            password="84pUcAHV",   # Ganti dengan password MySQL Anda
            database="DUDI"        # Ganti dengan nama database Anda
        )

        # Query untuk mengambil data dari tabel data_peserta
        query = "SELECT * FROM data_peserta"
        df = pd.read_sql(query, conn)

        # Menutup koneksi
        conn.close()

        return df
    except mysql.connector.Error as e:
        st.error(f"Terjadi kesalahan saat mengambil data dari database: {e}")
        return None

# Fungsi untuk mengekspor data ke file Excel dengan nama kolom yang diubah
def export_to_excel(df):
    # Mengubah nama kolom sebelum mengekspor ke Excel
    column_mapping = {
        'Pertanyaan11': 'Pelatihan yang dilakukan sudah relevan/bersangkut paut dengan pekerjaan Anda sekarang dan tujuan Anda',
        'Pertanyaan12': 'Isi Pelatihan (materi, presesntasi, dll) mudah dipahami',
        'Pertanyaan13': 'Isi Pelatihan (materi, presesntasi, dll) sudah menjelaskan topik yang Anda harapkan',
        'Pertanyaan21': 'Anda mampu menerapkan/mempraktikan Pengetahuan/Keterampilan/Sikap yang anda dapatkan dari pelatihan di tempat kerja anda',
        'Pertanyaan22': 'Anda mampu menjelaskan Pengetahuan/Keterampilan/Sikap yang anda peroleh dari orang lain',
        'Pertanyaan31': 'Pelatihan yang dilakukan sudah bermanfaat terhadap pekerjaan anda',
        'Pertanyaan32': 'Jika Setuju, Apa bentuk manfaatnya? (Optional)',
        'Pertanyaan33': 'Anda memperoleh kesempatan atau peluang baru yang disebabkan oleh pelatihan yang telah anda lakukan',
        'Pertanyaan34': 'Jika setuju, seperti apa kesempatan dan peluang barunya? (Optional)',
        'Pertanyaan35': 'Anda merasa lebih mampu dan lebih percaya diri dalam pekerjaan anda setelah ikut pelatihan',
        'Pertanyaan36': 'Jika setuju, Apa yang membuat anda lebih percaya diri? (Optional)',
        'Pertanyaan41': 'Anda memperoleh peningkatan pendapatan setelah mengikuti pelatihan',
        'Pertanyaan42': 'Jika Setuju, Berapa peningkatannya? (dalam presentase atau rupiah) - (Optional)',
        'Pertanyaan43': 'Anda memperoleh peningkatan produksi setelah mengikuti pelatihan',
        'Pertanyaan44': 'Jika Setuju, Berapa peningkatannya? (Optional)',
        'Pertanyaan51': 'Yang menurut anda paling berguna dalam pelatihan ini',
        'Pertanyaan52': 'Yang menurut anda paling tidak berguna dalam pelatihan ini',
        'Pertanyaan53': 'Saran Anda untuk pelaksanaan pelatihan ke depannya',
        'Pertanyaan54': 'Saran Anda untuk materi pelatihan ke depannya',
        'Pertanyaan55': 'Tambahan*',
        'Foto_Dokumentasi_Geotag': 'Foto Dokumentasi Geotag',
        'Foto_Dokumentasi_Non_Geotag': 'Foto Dokumentasi Non Geotag'
    }

    # Menerapkan perubahan nama kolom
    df.rename(columns=column_mapping, inplace=True)

    # Menyimpan data ke Excel di memori
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data Peserta")
    processed_data = output.getvalue()
    return processed_data

# Fungsi untuk menampilkan data dengan filter berdasarkan kabupaten
def display_data_with_filter(df):
    kabupaten_list = df['Kabupaten'].unique()
    kabupaten_choice = st.selectbox("Pilih Kabupaten untuk Filter Data", kabupaten_list)

    filtered_df = df[df['Kabupaten'] == kabupaten_choice]
    
    if not filtered_df.empty:
        jumlah_data = filtered_df.shape[0]  # Menghitung jumlah data
        st.write(f"Data Peserta dari Kabupaten {kabupaten_choice}: ({jumlah_data} data)")
        st.write(filtered_df)
    else:
        st.write("Tidak ada data untuk kabupaten yang dipilih.")
# Judul Aplikasi Admin
st.title("Admin Panel - BPPP TEGAL")

# Mengambil data dari database
df = get_data_from_db()

if df is not None and not df.empty:
    # Menampilkan data dan filter berdasarkan kabupaten
    display_data_with_filter(df)

    # Tombol untuk mengekspor data ke Excel
    if st.button("Ekspor Semua Data ke Excel"):
        # Mengekspor data ke file Excel dengan nama kolom yang diganti
        excel_data = export_to_excel(df)
        
        # Membuat file Excel untuk diunduh
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="data_peserta.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.write("Tidak ada data yang ditemukan atau terjadi kesalahan dalam mengambil data.")
