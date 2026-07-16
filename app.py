import streamlit as st
from github import Github
import streamlit.components.v1 as components

# --- Konfigurasi ---
st.set_page_config(page_title="Video Hub", layout="wide")

# Menyembunyikan sidebar secara default jika diinginkan bisa dengan config, 
# tapi di sini kita akan buat script untuk melipatnya setelah 5 detik.

try:
    github_config = st.secrets["github"]
    g = Github(github_config["token"])
    repo = g.get_repo(github_config["repo"])
except Exception as e:
    st.error("Konfigurasi GitHub belum diatur.")
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
    # Judul dihapus agar space lebih lega
    links = get_links()
    
    if links:
        video_ids = [link.split("v=")[-1] for link in links]
        playlist_ids = ",".join(video_ids)
        
        html_code = f"""
        <iframe id="video_player" width="100%" height="900" 
        src="https://www.youtube.com/embed/?playlist={playlist_ids}&autoplay=1&loop=1" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen></iframe>

        <script>
            // 1. Fullscreen setelah 5 detik
            setTimeout(function() {{
                var elem = document.getElementById('video_player');
                if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
            }}, 5000);

            // 2. Melipat sidebar setelah 5 detik
            // Mencari tombol menu/sidebar dan melakukan klik otomatis
            setTimeout(function() {{
                var buttons = window.parent.document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {{
                    // Tombol untuk melipat sidebar biasanya memiliki ikon atau posisi tertentu
                    if (buttons[i].getAttribute('aria-label') === 'Collapsed') {{
                        continue;
                    }}
                    // Mencoba menekan tombol yang melipat sidebar
                    buttons[i].click();
                }}
            }}, 5000);
        </script>
        """
        components.html(html_code, height=950)
    else:
        st.info("Belum ada link video.")

elif menu == "Admin":
    st.title("⚙️ Panel Admin")
    password = st.text_input("Password:", type="password")
    if password == "123":
        new_link = st.text_input("Link YouTube:")
        if st.button("Simpan"):
            links = get_links()
            links.append(new_link)
            save_links(links)
            st.rerun()
        
        for i, link in enumerate(get_links()):
            col1, col2 = st.columns([0.8, 0.2])
            col1.write(link)
            if col2.button("Hapus", key=i):
                links = get_links()
                links.pop(i)
                save_links(links)
                st.rerun()
