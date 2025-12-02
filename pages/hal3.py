import streamlit as st
import requests

try:
    from app import ambil_data_dari_api
except ImportError:
    st.error("Error: Gagal mengimpor fungsi API.")
    def ambil_data_dari_api(endpoint, params=None):
        return {}

GAMBAR_PREFIX = "https://image.tmdb.org/t/p/w500"
GAMBAR_PREFIX_ACTOR = "https://image.tmdb.org/t/p/w500"

# SET PAGE CONFIG — HARUS DI LUAR IF MAIN!
st.set_page_config(layout="wide", page_title="Detail Aktor")

# ===== CSS =====
st.markdown("""<style> ... CSS kamu ... </style>""", unsafe_allow_html=True)

# ===== FUNGSI =====
def tampilkan_detail_aktor(actor_id):

    # 1. Ambil data utama aktor
    data_actor = ambil_data_dari_api(f"person/{actor_id}")

    # 2. Ambil daftar film yang pernah dimainkan
    data_movies = ambil_data_dari_api(f"person/{actor_id}/movie_credits")

    # 3. Ambil social media (Instagram, Twitter, dll)
    data_social = ambil_data_dari_api(f"person/{actor_id}/external_ids")

    if not data_actor or "name" not in data_actor:
        st.error("Gagal memuat detail aktor.")
        return

    st.markdown('<div class="main-content-card">', unsafe_allow_html=True)

    st.markdown(f'<h1 style="text-align:center; color:white;">{data_actor["name"]}</h1>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col_img, col_bio = st.columns([1, 3])

    # FOTO
    with col_img:
        path = data_actor.get('profile_path')
        if path:
            st.image(f"{GAMBAR_PREFIX_ACTOR}{path}", use_container_width=True)
        else:
            st.write("No Image Available")

    # BIO + metadata
    with col_bio:
        st.subheader("Biografi")
        st.write(data_actor.get("biography", "Biografi belum tersedia."))

        st.subheader("Lahir")
        st.write(data_actor.get("birthday", "Tidak diketahui"))

        st.subheader("Tempat Lahir")
        st.write(data_actor.get("place_of_birth", "Tidak diketahui"))

        # SOCIAL MEDIA
        st.subheader("Media Sosial")
        ig = data_social.get("instagram_id")
        tw = data_social.get("twitter_id")

        if ig:
            st.markdown(f"- Instagram: https://instagram.com/{ig}")
        if tw:
            st.markdown(f"- Twitter: https://twitter.com/{tw}")
        if not ig and not tw:
            st.write("Tidak ada data media sosial ditemukan.")

    st.markdown("---")

    # FILM-FILM YANG DIMAINKAN
    st.subheader("Film yang Pernah Diperankan")

    if data_movies and "cast" in data_movies:
        for film in data_movies["cast"][:10]:
            st.markdown(f"- **{film['title']}** ({film.get('character', 'Unknown')})")
    else:
        st.write("Tidak ada riwayat film.")

    # TOMBOL KEMBALI
    if st.button("⬅️ Kembali ke Detail Film"):
        st.switch_page("pages/hal2.py")

    st.markdown("</div>", unsafe_allow_html=True)

# ===== LOGIKA EKSEKUSI (LANGSUNG DIJALANKAN) =====
if 'selected_actor_id' not in st.session_state or st.session_state.selected_actor_id is None:
    st.warning("Silakan pilih aktor terlebih dahulu.")
    st.switch_page("pages/hal2.py")
else:
    tampilkan_detail_aktor(st.session_state.selected_actor_id)
