import streamlit as st
from github import Github
import streamlit.components.v1 as components

# Sidebar awal: 'expanded' agar bisa dilihat, lalu dilipat otomatis oleh JS
st.set_page_config(page_title="Video Hub", layout="wide", initial_sidebar_state="expanded")

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
        return []

def save_links(links_list):
    content = "\n".join(links_list)
    try:
        file = repo.get_contents("links.txt")
        repo.update_file(file.path, "Update link", content, file.sha)
    except:
        repo.create_file("links.txt", "Inisialisasi", content)

menu = st.sidebar.radio("Navigasi", ["Pemutar Video", "Admin"])

if menu == "Pemutar Video":
    links = get_links()
    if links:
        video_ids = [link.split("v=")[-1] for link in links]
        playlist_ids = ",".join(video_ids)
        
        # HTML & JS untuk Fullscreen dan Melipat Sidebar
        html_code = f"""
        <iframe id="video_player" width="100%" height="900" 
        src="https://www.youtube.com/embed/?playlist={playlist_ids}&autoplay=1&loop=1" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        
        <script>
            setTimeout(function() {{
                // 1. Fullscreen
                var elem = document.getElementById('video_player');
                if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
                
                // 2. Melipat Sidebar otomatis
                // Mencari tombol lipat sidebar berdasarkan tombol panah (svg path)
                var buttons = window.parent.document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {{
                    if (buttons[i].innerHTML.includes('polyline') || buttons[i].getAttribute('aria-label') === 'Collapse sidebar') {{
                        buttons[i].click();
                        break; 
                    }}
                }}
            }}, 5000); // 5 Detik
        </script>
        """
        components.html(html_code, height=950)
    else:
        st.info("Playlist kosong. Masuk ke Admin untuk menambah link.")

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
