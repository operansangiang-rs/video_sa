import streamlit as st
from github import Github

# Konfigurasi
st.set_page_config(page_title="Video Hub", layout="wide")

try:
    github_config = st.secrets["github"]
    g = Github(github_config["token"])
    repo = g.get_repo(github_config["repo"])
except Exception as e:
    st.error("Konfigurasi GitHub belum diatur.")
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
        repo.update_file(file.path, "Update daftar link", content, file.sha)
    except:
        repo.create_file("links.txt", "Inisialisasi file link", content)

# --- Tampilan Utama ---
menu = st.sidebar.radio("Navigasi", ["Pemutar Video", "Admin"])

if menu == "Pemutar Video":
    st.title("📺 Pemutar Video YouTube")
    links = get_links()
    if links:
        pilihan = st.selectbox("Pilih video yang ingin diputar:", links)
        st.video(pilihan) # Autoplay kadang diblokir browser, jadi user klik play sendiri lebih aman
    else:
        st.info("Belum ada video. Silakan hubungi admin.")

elif menu == "Admin":
    st.title("⚙️ Panel Admin")
    password = st.text_input("Password:", type="password")
    
    if password == "123":
        st.subheader("Tambah Link Baru")
        new_link = st.text_input("Paste Link YouTube di sini:")
        if st.button("Simpan Link"):
            if new_link:
                links = get_links()
                links.append(new_link)
                save_links(links)
                st.success("Link berhasil ditambah!")
                st.rerun()
        
        st.divider()
        st.subheader("Kelola Link Saat Ini")
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
