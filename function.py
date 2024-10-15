import streamlit as st # type: ignore
import pandas as pd # type: ignore
import time
import math

from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import Select # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from datetime import datetime

username = "bps5271"
password = "antara52"

@st.dialog("Persiapan Si Rinjani", width = "large")
def load_data():
    if username and password:
        if 'satker_options' not in st.session_state:  
            with st.spinner("Sedang memproses..."):
                driver = init_driver()
                satker_options, bulan_options, tahun_options = get_dropdown_options(driver)
                st.write("✅ Selesai")
                driver.quit()

                st.session_state.satker_options = satker_options
                st.session_state.bulan_options = bulan_options
                st.session_state.tahun_options = tahun_options 
                st.session_state.logged_in = True

        if 'satker_options' in st.session_state:
            if st.button("Lanjut"):
                time.sleep(1)
                st.rerun()
    else:
        st.error("Mohon masukkan username dan password.")

@st.fragment
def login():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height: 10vh; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
        st.image('assets/Login.png', width=600, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns([1, 0.5, 1])
    col5.button("Mari Kita Mulai", on_click=load_data, use_container_width=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.dataset = False
    st.rerun()

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")  # Mode headless baru diperkenalkan sejak Chrome 109
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=400,1015")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--hide-scrollbars")  # Menyembunyikan scrollbar
    chrome_options.add_argument("--mute-audio")  # Mematikan audio

    # Mengatur agar Chrome sepenuhnya invisible tanpa jendela
    chrome_options.add_argument("--disable-infobars")  # Nonaktifkan infobars
    chrome_options.add_argument("--disable-popup-blocking")  # Nonaktifkan blokir popup
    chrome_options.add_argument("--start-maximized")  # Mulai dengan ukuran maksimal
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Fungsi untuk mengambil opsi dari dropdown di halaman
def get_dropdown_options(driver):
    wait = WebDriverWait(driver, 10)
    driver.get('https://sirinjani.bpsntb.id/login')
    st.write("✅ Berhasil membuka SiRinjani")
    
    # Proses login (sesuaikan dengan username dan password yang diperlukan)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_field.send_keys(username)  # ganti dengan username sebenarnya

    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(password)  # ganti dengan password sebenarnya

    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    st.write("✅ Berhasil login ke sistem")

    # Navigasi ke halaman dengan dropdown Satker, Bulan, dan Tahun
    navbar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-link.nav-toggler.d-block.d-md-none.waves-effect.waves-dark")))
    navbar_button.click()

    laporan_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.has-arrow.waves-effect.waves-dark[aria-expanded='false'] > i.ti-layout-media-right-alt")))
    laporan_button.click()

    kegiatan_kabkota_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Kegiatan Kabkota')]")))
    kegiatan_kabkota_button.click()

    bulanan_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Bulanan') and contains(@href, 'kabkota/bulanan')]")))
    bulanan_button.click()

    # Mengambil opsi dari dropdown Satker
    satker_dropdown = wait.until(EC.presence_of_element_located((By.ID, "unit")))
    satker_options = Select(satker_dropdown).options
    satker_values = {option.text: option.get_attribute("value") for option in satker_options}
    st.write("✅ Berhasil mendapatkan isian satker")

    # Mengambil opsi dari dropdown Bulan
    bulan_dropdown = wait.until(EC.presence_of_element_located((By.ID, "bulan")))
    bulan_options = Select(bulan_dropdown).options
    bulan_values = {option.text: option.get_attribute("value") for option in bulan_options}
    st.write("✅ Berhasil mendapatkan isian bulan")

    # Mengambil opsi dari dropdown Tahun
    tahun_dropdown = wait.until(EC.presence_of_element_located((By.ID, "tahun")))
    tahun_options = Select(tahun_dropdown).options
    tahun_values = {option.text: option.get_attribute("value") for option in tahun_options}
    st.write("✅ Berhasil mendapatkan isian tahun")

    # Kembalikan opsi dropdown
    return satker_values, bulan_values, tahun_values

# Fungsi login dan navigasi dengan pilihan dari dropdown yang diambil dari halaman web
def login_and_navigate(driver, username, password, satker_value, bulan_value, tahun_value):
    wait = WebDriverWait(driver, 10)
    
    # Login ke sistem
    driver.get('https://sirinjani.bpsntb.id/login')
    try:
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(username)

        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(password)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()
        st.write("✅ Berhasil login ke sistem")
    except Exception as e:
        st.error(f"Gagal login: {e}")
        return False

    try:
        # Navigasi ke halaman sesuai Satker
        navbar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-link.nav-toggler.d-block.d-md-none.waves-effect.waves-dark")))
        navbar_button.click()

        laporan_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.has-arrow.waves-effect.waves-dark[aria-expanded='false'] > i.ti-layout-media-right-alt")))
        laporan_button.click()

        kegiatan_kabkota_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Kegiatan Kabkota')]")))
        kegiatan_kabkota_button.click()

        bulanan_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Bulanan') and contains(@href, 'kabkota/bulanan')]")))
        bulanan_button.click()

        # Pilih Satker
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "unit")))
        select = Select(dropdown)
        select.select_by_value(satker_value)
        st.write(f"✅ Berhasil memilih Satker {satker_value}")

        # Pilih Bulan
        bulan_dropdown = wait.until(EC.presence_of_element_located((By.ID, "bulan")))
        select_bulan = Select(bulan_dropdown)
        select_bulan.select_by_value(str(bulan_value))
        st.write(f"✅ Berhasil memilih Bulan {bulan_value}")

        # Pilih Tahun
        tahun_dropdown = wait.until(EC.presence_of_element_located((By.ID, "tahun")))
        select_tahun = Select(tahun_dropdown)
        select_tahun.select_by_value(str(tahun_value))
        st.write(f"✅ Berhasil memilih Tahun {tahun_value}")

        # Klik Filter
        filter_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success")))
        filter_button.click()
        st.write("✅ Berhasil mengklik tombol Filter")
        return True

    except Exception as e:
        st.error(f"Gagal melakukan navigasi: {e}")
        return False

bulan_mapping = {
    "Jan": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr", "Mei": "May", "Jun": "Jun",
    "Jul": "Jul", "Agu": "Aug", "Sep": "Sep", "Okt": "Oct", "Nov": "Nov", "Des": "Dec"
}

def replace_bulan(tanggal):
    for indo, eng in bulan_mapping.items():
        tanggal = tanggal.replace(indo, eng)
    return tanggal

def angka_ke_bulan(angka_bulan):
  try:
    nama_bulan = datetime.date(1900, angka_bulan, 1).strftime('%B')
    return nama_bulan
  except ValueError:
    return "Angka bulan tidak valid"

# Tambahkan kolom keterangan berdasarkan kondisi yang diberikan
def keterangan(row):
    if row['Dikirim'] == 0:
        return '🔴 Belum Dikerjakan'
    elif row['Dikirim'] != 0 and row['Dikirim'] < row['Target'] and row['Diterima'] == 0:
        return '🟠 Belum Lengkap'
    elif row['Dikirim'] >= row['Target'] and row['Diterima'] == 0:
        return '🟡 Belum Dinilai'
    elif (row['Dikirim'] >= row['Target'] and 
          row['Diterima'] != 0 and 
          row['Diterima'] < row['Target'] and 
          row['Nilai'] < 5.00):
        return '🟣 Nilai Belum Selesai'
    elif ((row['Dikirim'] >= row['Target'] and 
           row['Diterima'] >= row['Target'] and 
           row['Nilai'] < 5.00) or 
          (row['Dikirim'] != 0 and 
           row['Dikirim'] < row['Target'] and 
           row['Diterima'] == row['Dikirim'])):
        return '🔵 Nilai Belum Sempurna'
    elif row['Dikirim'] >= row['Target'] and row['Diterima'] >= row['Target'] and row['Nilai'] == 5.00:
        return '🟢 Nilai Sempurna'
    else:
        return ''

def scrape_data(driver):
    wait = WebDriverWait(driver, 10)
    all_data = []

    try:
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        bulan = rows[1].find_elements(By.TAG_NAME, "td")[0].text

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 8:
                link = cols[1].find_element(By.TAG_NAME, "a").get_attribute("href")
                kegiatan = cols[1].text
                tgl_mulai = replace_bulan(cols[2].text)
                tgl_berakhir = replace_bulan(cols[3].text)
                target = int(cols[4].text)
                dikirim = int(cols[5].text)
                diterima = int(cols[6].text)
                nilai = float(cols[7].text.replace(',', '.'))
            else:
                link = cols[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                kegiatan = cols[0].text
                tgl_mulai = replace_bulan(cols[1].text)
                tgl_berakhir = replace_bulan(cols[2].text)
                target = int(cols[3].text)
                dikirim = int(cols[4].text)
                diterima = int(cols[5].text)
                nilai = float(cols[6].text.replace(',', '.'))
            
            all_data.append({
                "Tahun": st.session_state.tahun,
                "Bulan": bulan,
                "Link": link,
                "Kegiatan": kegiatan,
                "Tanggal Mulai": tgl_mulai,
                "Tanggal Berakhir": tgl_berakhir,
                "Target": target,
                "Dikirim": dikirim,
                "Diterima": diterima,
                "Nilai": nilai
            })

        st.write("✅ Data berhasil di-scrape.")

        df = pd.DataFrame(all_data)

        df['Tanggal Mulai'] = pd.to_datetime(df['Tanggal Mulai'], format='%d %b %Y')
        df['Tanggal Berakhir'] = pd.to_datetime(df['Tanggal Berakhir'], format='%d %b %Y')
        df['Keterangan'] = df.apply(keterangan, axis=1)

        return df

    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame()

# Fungsi untuk membuat template pesan WhatsApp
def generate_whatsapp_message(df, month, year):
    # Filter data untuk bulan tertentu
    
    # Hitung jumlah kegiatan berdasarkan keterangan
    keterangan_counts = df['Keterangan'].value_counts()
    
    # Hitung total kegiatan
    total_kegiatan = len(df)
    
    # Dapatkan tanggal sekarang
    current_date = datetime.now().strftime('%d %B %Y %H:%M:%S')
    
    # Buat template pesan
    message = f"📊 Laporan Kegiatan BPS Kota Mataram Bulan {month} {year} 📊\n\n"
    message += f"🗓️ {current_date}\n\n"
    message += f"Terdapat {total_kegiatan} kegiatan yang terbagi menjadi:\n"
    
    for keterangan, count in keterangan_counts.items():
        message += f"{keterangan}: {count} kegiatan\n"
    
    # Tambahkan daftar kegiatan "Belum Dikerjakan" dan "Belum Lengkap"
    belum_dikerjakan = df[df['Keterangan'] == '🔴 Belum Dikerjakan'].sort_values(by='Tanggal Berakhir')
    belum_lengkap = df[df['Keterangan'] == '🟠 Belum Lengkap'].sort_values(by='Tanggal Berakhir')
    
    def calculate_days_left(deadline):
        days_left = math.ceil((deadline - datetime.now()).total_seconds() / (3600 * 24))
        if days_left > 0:
            return f"🏳️ Kurang {days_left} hari lagi"
        elif days_left < 0:
            return f"⚠️ Terlambat {-days_left} hari dari seharusnya"
        else:
            return "🚩 Batas waktunya hari ini"

    def group_activities_by_deadline(df):
        grouped = df.groupby('Tanggal Berakhir')
        grouped_activities = []
        for deadline, group in grouped:
            days_left = calculate_days_left(deadline)
            activities = "\n".join([f"- {row['Kegiatan']} \n Kerjakan 👉🏻 {row['Link']}" for index, row in group.iterrows()])
            grouped_activities.append(f"({days_left})\n{activities}")
        return grouped_activities

    if not belum_dikerjakan.empty:
        message += "\n🔴 Kegiatan yang Belum Dikerjakan:\n"
        grouped_activities = group_activities_by_deadline(belum_dikerjakan)
        message += "\n\n".join(grouped_activities)
    
    if not belum_lengkap.empty:
        message += "\n\n🟠 Kegiatan yang Belum Lengkap:\n"
        grouped_activities = group_activities_by_deadline(belum_lengkap)
        message += "\n\n".join(grouped_activities)
    
    message += "\n\n🌐 Untuk data selengkapnya, silakan cek tautan berikut:\n"
    message += f"https://sirinjani.bpsntb.id/laporan/kabkota/bulanan?unit=52710&bulan={datetime.now().month}&tahun={year}\n"
    message += "\nTerima kasih atas perhatian dan kerjasamanya."
    
    return message