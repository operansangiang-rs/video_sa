import streamlit as st
from github import Github
import streamlit.components.v1 as components

# --- Konfigurasi ---
st.set_page_config(page_title="Video Playlist Manager", layout="wide")

# Mengambil konfigurasi dari secrets Streamlit
try:
    github_config = st.secrets["github"]
    g = Github(github_config["token"])
    repo = g.get_repo(github_config["repo"])
except Exception as e:
    st.error("Konfigurasi GitHub (secrets) belum diatur dengan benar.")
    st.stop()

# --- Fungsi Pengelola Data di GitHub ---
def get_links():
    try:
        file = repo.get_contents("links.txt")
        return file.decoded_content.decode("utf-8").splitlines()
    except:
        return []

def save_links(links_list):
    content = "\n".join(links_list)
    try:
        file = repo.get_contents("links.txt")
        repo.update_file(file.path, "Update daftar link video", content, file.sha)
    except:
        repo.create_file("links.txt", "Inisialisasi file link", content)

# --- Tampilan Utama ---
menu = st.sidebar.radio("Navigasi", ["Pemutar Video", "Admin"])

if menu == "Pemutar Video":
    st.title("📺 Playlist Otomatis")
    links = get_links()
    
    if links:
        # Mengambil ID video untuk membuat playlist YouTube
        video_ids = [link.split("v=")[-1] for link in links]
        playlist_ids = ",".join(video_ids)
        
        # HTML + JS untuk auto-play dan auto-fullscreen setelah 5 detik
        html_code = f"""
        <iframe id="video_player" width="100%" height="600" 
        src="https://www.youtube.com/embed/?playlist={playlist_ids}&autoplay=1&loop=1" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen></iframe>

        <script>
            setTimeout(function() {{
                var elem = document.getElementById('video_player');
                if (elem.requestFullscreen) {{
                    elem.requestFullscreen();
                }} else if (elem.webkitRequestFullscreen) {{ 
                    elem.webkitRequestFullscreen();
                }} else if (elem.msRequestFullscreen) {{
                    elem.msRequestFullscreen();
                }}
            }}, 5000); // 5 detik
        </script>
        """
        components.html(html_code, height=650)
    else:
        st.info("Belum ada link video. Silakan hubungi admin untuk menambahkannya.")

elif menu == "Admin":
    st.title("⚙️ Panel Admin")
    password = st.text_input("Masukkan Password Admin:", type="password")
    
    if password == "123":
        st.subheader("Tambah Link YouTube Baru")
        new_link = st.text_input("Paste Link (Contoh: https://www.youtube.com/watch?v=...):")
        
        if st.button("Simpan Link"):
            if new_link:
                links = get_links()
                links.append(new_link)
                save_links(links)
                st.success("Link berhasil disimpan!")
                st.rerun()
        
        st.divider()
        st.subheader("Daftar Link Saat Ini")
        links = get_links()
        for i, link in enumerate(links):
            col1, col2 = st.columns([0.8, 0.2])
            col1.write(f"{i+1}. {link}")
            if col2.button("Hapus", key=f"del_{i}"):
                links.pop(i)
                save_links(links)
                st.rerun()
    elif password != "":
        st.error("Password Salah!")
