import streamlit as st
import pandas as pd
import requests

# ==============================================================================
# 1. IMPOR FUNGSI API & KONSTANTA (Person 1)
# ==============================================================================
try:
    from app import ambil_data_dari_api
except ImportError:
    st.error("Error: Gagal mengimpor fungsi API. Pastikan app.py berada di root folder.")
    def ambil_data_dari_api(endpoint, params=None): 
        return {} 

GAMBAR_PREFIX = "https://image.tmdb.org/t/p/w500" 
GAMBAR_PREFIX_ACTOR = "https://image.tmdb.org/t/p/w200"

# ==============================================================================
# 2. CSS KUSTOM (UI Deep Contrast & TAJAM) (Person 2)
# ==============================================================================

st.markdown("""
<style>
/* 1. SETUP DASAR & BACKGROUND GELAP */
.stApp { background-color: #121212; color: #E0E0E0; }
header[data-testid="stHeader"] { display: none; }

/* 2. CARD UTAMA KONTEN */
.main-content-card {
    background: #1E1E2F; padding-bottom: 2rem; margin: 20px auto;
    border-radius: 10px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); 
    overflow: hidden;
}

/* 3. JUDUL FILM */
.movie-title-bar { background-color: #0e1530; padding: 20px; text-align: center; margin-bottom: 30px;}
.main-title-text-fixed { font-size: 2.5rem; color: white; font-weight: 800; }

/* 4. GRID AKTOR (DIMODIFIKASI UNTUK KLIK) */
.actor-section { padding: 0 4rem; margin-bottom: 3rem; }
.actor-card-wrapper { 
    padding: 10px; margin-bottom: 10px; border-radius: 8px;
    background-color: #282844; box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    transition: transform 0.3s;
    cursor: pointer; /* Menunjukkan elemen bisa diklik */
}
.actor-card-wrapper:hover {
    background-color: #383858; 
    transform: translateY(-3px);
}
.actor-name-text { color: #E0E0E0; font-weight: bold; }
.actor-role-text { color: #A0A0A0; }
.actor-img-box { width: 100%; aspect-ratio: 2/3; overflow: hidden; border-radius: 6px; margin-bottom: 5px; }

/* 5. STYLING SECTION HEADERS */
h3 { border-left: 5px solid #E04444; padding-left: 15px; color: #E0E0E0; }
/* 6. GARIS PEMBATAS */
hr { background-color: #333; height: 1px; border: none; }
/* 7. METRIC STYLE */
[data-testid="stMetricValue"] { color: #E04444 !important; }
/* 8. TOMBOL KEMBALI */
div.stButton > button { background-color: #991b1b; color: white; border-radius: 5px; padding: .5rem 1.5rem; }

/* 9. CSS HACK UNTUK MEMBUAT CARD BISA DIKLIK (Person 3) */
/* Pastikan tombol Streamlit berada di atas card dan transparan */
div[data-testid="stVerticalBlock"] > div > div:nth-child(2) {
    margin-top: -100%; /* Pindahkan tombol ke atas card */
    height: 100%;
    position: relative;
    z-index: 5; /* Agar tombol berada di atas card-wrapper */
}
div[data-testid="stVerticalBlock"] > div > div:nth-child(2) > button {
    background: rgba(0,0,0,0); /* Transparan */
    color: rgba(0,0,0,0);
    border: none;
    padding-top: 100%; /* Agar area klik menutupi card */
    height: 100%;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. FUNGSI VISUALISASI F9 (Person 3 - Dihilangkan)
# ==============================================================================
def generate_actor_productivity_chart(credits_data):
    pass 


# ==============================================================================
# 4. FUNGSI RENDER AKTOR (Person 3 - DIMODIFIKASI UNTUK KLIK)
# ==============================================================================

def handle_actor_click(actor_id):
    """Fungsi yang dipanggil saat tombol aktor diklik."""
    # Menetapkan ID aktor yang dipilih ke session state
    st.session_state.selected_actor_id = actor_id
    # Memaksa navigasi segera terjadi
    st.switch_page("pages/hal3.py") 

def render_actor_grid(data_kredit):
    """F3: Merender tampilan 20 aktor dalam grid 6 kolom yang dapat diklik."""
    
    if data_kredit and 'cast' in data_kredit:
        aktor_utama = data_kredit['cast'][:20] 
        NUM_COLS = 6 
        
        st.markdown('<div class="actor-section">', unsafe_allow_html=True)

        for row_start in range(0, len(aktor_utama), NUM_COLS):
            row_actors = aktor_utama[row_start : row_start + NUM_COLS]
            cols = st.columns(NUM_COLS) 
            
            for i, aktor in enumerate(row_actors):
                # NOTE: Mengubah struktur loop zip/enumerate agar konsisten dengan Python
                # NOTE: Memastikan semua kolom diisi
                with cols[i]: 
                    actor_id = aktor['id']
                    path = aktor.get('profile_path')
                    
                    if path:
                        img_html = f'<img src="{GAMBAR_PREFIX_ACTOR}{path}" class="actor-img-element">'
                    else:
                        img_html = '<div style="font-size:2rem; text-align:center; height:100px;">👤</div>'
                    
                    # Tombol Streamlit (Disembunyikan secara visual) untuk menangkap klik
                    # NOTE: st.button ditempatkan sebelum st.markdown untuk CSS Hack
                    if st.button(f"Lihat Detail {aktor['name']}", key=f"actor_btn_{actor_id}", use_container_width=True):
                        handle_actor_click(actor_id)
                        
                    # Tampilan Card Aktor
                    st.markdown(f"""
                        <div class="actor-card-wrapper" 
                             title="Klik untuk detail {aktor['name']}">
                            <div class="actor-img-box">{img_html}</div>
                            <div class="actor-name-text">{aktor['name']}</div>
                            <div class="actor-role-text">{aktor['character'].split(' / ')[0]}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) 
    else:
        st.warning("Data aktor tidak tersedia.")


# ==============================================================================
# 5. FUNGSI UTAMA TAMPILAN (Person 2 & 3)
# ==============================================================================

def tampilkan_detail_film(movie_id):
    """Fungsi utama yang menampilkan semua komponen halaman detail."""
    
    data_film = ambil_data_dari_api(f"movie/{movie_id}")
    data_kredit = ambil_data_dari_api(f"movie/{movie_id}/credits")

    if not data_film or 'title' not in data_film:
        st.error("Gagal memuat detail film.")
        return
    
    # --- WRAPPER UTAMA: MAIN CONTENT CARD ---
    st.markdown('<div class="main-content-card">', unsafe_allow_html=True)

    # 1. JUDUL FILM 
    st.markdown(f"""
        <div class="movie-title-bar">
            <h1 class="main-title-text-fixed">{data_film["title"]}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. GRID AKTOR (Person 3)
    render_actor_grid(data_kredit)
    
    # 3. GARIS PEMBATAS
    st.markdown("---") 
    
    # 4. DETAIL FILM & SINOPSIS (Person 2)
    st.subheader("Detail Film & Sinopsis")

    col_spacer_left, col_poster, col_info, col_spacer_right = st.columns([0.5, 1.5, 3.5, 0.5])
    
    with col_poster:
        poster_path = data_film.get('poster_path')
        if poster_path:
            st.image(f"{GAMBAR_PREFIX}{poster_path}", use_container_width=True)
        else:
            st.write("No Image")

    with col_info:
        overview = data_film.get('overview', 'Sinopsis tidak tersedia.')
        release_date = data_film.get('release_date', '-')
        rating = round(data_film.get('vote_average', 0), 1)

        st.markdown('<h4 class="detail-header-text">Sinopsis</h4>', unsafe_allow_html=True)
        st.write(overview)
        st.markdown('<br>', unsafe_allow_html=True)
        
        st.metric(label="Tanggal Rilis", value=release_date)
        st.metric(label="Rating TMDb", value=f"{rating} / 10")
    
    # 5. TOMBOL KEMBALI
    if st.button("⬅️ Kembali ke Pencarian", key='back_btn'):
        st.session_state.selected_movie_id = None
        st.switch_page("app.py")
    
    # --- TUTUP MAIN CONTENT CARD ---
    st.markdown('</div>', unsafe_allow_html=True) 


# ==============================================================================
# LOGIKA EKSEKUSI HALAMAN (Person 1)
# ==============================================================================

if __name__ == "__main__":
    
    # Inisialisasi state aktor agar tidak ada error di awal
    if 'selected_actor_id' not in st.session_state:
        st.session_state.selected_actor_id = None 

    if 'selected_movie_id' not in st.session_state or st.session_state.selected_movie_id is None:
        st.warning("Silakan pilih film terlebih dahulu.")
        st.switch_page("app.py")
    else:
        st.set_page_config(layout="wide", page_title="Detail Film")
        tampilkan_detail_film(st.session_state.selected_movie_id)