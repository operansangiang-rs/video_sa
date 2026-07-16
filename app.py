import streamlit as st
from github import Github
import streamlit.components.v1 as components

# Sidebar otomatis terlipat
st.set_page_config(page_title="Video Player", layout="wide", initial_sidebar_state="collapsed")

try:
    github_config = st.secrets["github"]
    g = Github(github_config["token"])
    repo = g.get_repo(github_config["repo"])
except Exception as e:
    st.error(f"Error Konfigurasi: {e}")
    st.stop()

def get_links():
    try:
        file = repo.get_contents("links.txt")
        return file.decoded_content.decode("utf-8").splitlines()
    except:
        # Jika file belum ada, buat file kosong di GitHub
        repo.create_file("links.txt", "Inisialisasi file", "")
        return []

def save_links(links_list):
    content = "\n".join(links_list)
    try:
        file = repo.get_contents("links.txt")
        repo.update_file(file.path, "Update link", content, file.sha)
    except:
        repo.create_file("links.txt", "Update link", content)

menu = st.sidebar.radio("Navigasi", ["Pemutar Video", "Admin"])

if menu == "Pemutar Video":
    links = get_links()
    if links:
        video_ids = [link.split("v=")[-1] for link in links]
        playlist_ids = ",".join(video_ids)
        
        html_code = f"""
        <iframe id="video_player" width="100%" height="900" 
        src="https://www.youtube.com/embed/?playlist={playlist_ids}&autoplay=1&loop=1&playlist={playlist_ids}" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        <script>
            setTimeout(function() {{
                var elem = document.getElementById('video_player');
                if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
            }}, 5000);
        </script>
        """
        components.html(html_code, height=950)
    else:
        st.info("Playlist kosong. Buka menu Admin untuk tambah link.")

elif menu == "Admin":
    st.title("⚙️ Panel Admin")
    password = st.text_input("Password:", type="password")
    if password == "123":
        new_link = st.text_input("Link YouTube:")
        if st.button("Simpan"):
            if new_link:
                links = get_links()
                links.append(new_link)
                save_links(links)
                st.rerun()
        st.divider()
        for i, link in enumerate(get_links()):
            col1, col2 = st.columns([0.8, 0.2])
            col1.write(link)
            if col2.button("Hapus", key=i):
                links = get_links()
                links.pop(i)
                save_links(links)
                st.rerun()
    elif password != "":
        st.error("Password Salah!")
