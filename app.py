import streamlit as st
from github import Github
import streamlit.components.v1 as components

# Konfigurasi: Sidebar langsung tertutup sejak awal agar tampilan video luas
st.set_page_config(page_title="Video Hub", layout="wide", initial_sidebar_state="collapsed")

# Koneksi ke GitHub
try:
    github_config = st.secrets["github"]
    g = Github(github_config["token"])
    repo = g.get_repo(github_config["repo"])
except Exception as e:
    st.error("Konfigurasi GitHub di secrets belum benar. Pastikan token dan nama repo sudah diatur.")
    st.stop()

# Fungsi kelola data
def get_links():
    try:
        file = repo.get_contents("links.txt")
        return file.decoded_content.decode("utf-8").splitlines()
    except:
        # Jika file belum ada, buat file kosong
        repo.create_file("links.txt", "Inisialisasi file link", "")
        return []

def save_links(links_list):
    content = "\n".join(links_list)
    try:
        file = repo.get_contents("links.txt")
        repo.update_file(file.path, "Update daftar link", content, file.sha)
    except:
        repo.create_file("links.txt", "Inisialisasi file link", content)

# Navigasi
menu = st.sidebar.radio("Navigasi", ["Pemutar Video", "Admin"])

if menu == "Pemutar Video":
    links = get_links()
    if links:
        # Mengubah link jadi ID untuk playlist
        video_ids = [link.split("v=")[-1] for link in links]
        playlist_ids = ",".join(video_ids)
        
        # HTML untuk video dengan fitur looping dan fullscreen
        html_code = f"""
        <iframe id="video_player" width="100%" height="900" 
        src="https://www.youtube.com/embed/?playlist={playlist_ids}&autoplay=1&loop=1" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        
        <script>
            // Fullscreen otomatis setelah 5 detik
            setTimeout(function() {{
                var elem = document.getElementById('video_player');
                if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
            }}, 5000);
        </script>
        """
        components.html(html_code, height=950)
    else:
        st.info("Playlist masih kosong. Silakan masuk ke menu Admin untuk menambah link.")

elif menu == "Admin":
    st.title("⚙️ Panel Admin")
    password = st.text_input("Password:", type="password")
    if password == "123":
        new_link = st.text_input("Masukkan Link YouTube:")
        if st.button("Simpan Link"):
            if new_link:
                links = get_links()
                links.append(new_link)
                save_links(links)
                st.success("Link berhasil disimpan!")
                st.rerun()
        
        st.divider()
        st.subheader("Daftar Link Saat Ini:")
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
