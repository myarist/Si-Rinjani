import streamlit as st # type: ignore
from function import *

st.title("Data Scraping Si Rinjani BPS NTB")

# Menampilkan opsi dropdown yang diambil dari halaman web (dari session state)
if 'satker_options' in st.session_state:
    st.session_state.satker = st.selectbox("Pilih Satker", list(st.session_state.satker_options.keys()), index=None)
    st.session_state.bulan = st.selectbox("Pilih Bulan", list(st.session_state.bulan_options.keys()), index=None)
    st.session_state.tahun = st.selectbox("Pilih Tahun", list(st.session_state.tahun_options.keys()), index=None)

    # Tombol untuk mulai scraping
    if st.button("Mulai Scraping"):
        st.session_state.satker = st.session_state.satker_options[st.session_state.satker]
        st.session_state.bulan = st.session_state.bulan_options[st.session_state.bulan]
        st.session_state.tahun = st.session_state.tahun_options[st.session_state.tahun]
        with st.spinner("Sedang memproses..."):
            driver = init_driver()
            if login_and_navigate(driver, username, password, st.session_state.satker, st.session_state.bulan, st.session_state.tahun):
                st.session_state.dataset = scrape_data(driver)

st.dataframe(st.session_state.dataset, use_container_width=True)

if st.session_state.dataset is not None:
    st.markdown(generate_whatsapp_message(st.session_state.dataset, st.session_state.bulan, st.session_state.tahun))