import streamlit as st
from github import Github

# --- Konfigurasi Awal ---
st.set_page_config(page_title="Video Manager", layout="wide")

# Mengambil data dari secrets
try:
    github_config = st.secrets["github"]
    g = Github(github_config["token"])
    repo = g.get_repo(github_config["repo"])
except Exception as e:
    st.error("Konfigurasi GitHub tidak ditemukan. Periksa file .streamlit/secrets.toml")
    st.stop()

# --- Fungsi Manajemen Link ---
# Menyimpan link di file 'links.txt' di dalam repositori
def save_links(links_list):
    content = "\n".join(links_list)
    try:
        file = repo.get_contents("links.txt")
        repo.update_file(file.path, "Update link video", content, file.sha)
    except:
        repo.create_file("links.txt", "Buat file link baru", content)

def get_links():
    try:
        file = repo.get_contents("links.txt")
        return file.decoded_content.decode("utf-8").splitlines()
    except:
        return []

# --- Tampilan Aplikasi ---
menu = st.sidebar.radio("Menu", ["Pemutar Video", "Admin"])

if menu == "Pemutar Video":
    st.title("Pemutar Video YouTube")
    links = get_links()
    
    if links:
        pilihan = st.selectbox("Pilih video untuk diputar:", links)
        if pilihan:
            st.video(pilihan, autoplay=True)
    else:
        st.info("Belum ada link video. Silakan hubungi admin.")

elif menu == "Admin":
    st.title("Admin Panel")
    password = st.text_input("Masukkan Password Admin:", type="password")
    
    if password == "123":
        st.success("Login Berhasil!")
        new_link = st.text_input("Masukkan Link YouTube baru:")
        if st.button("Tambah Link"):
            links = get_links()
            links.append(new_link)
            save_links(links)
            st.success("Link berhasil disimpan ke GitHub!")
        
        st.subheader("Daftar Link Saat Ini")
        links = get_links()
        st.write(links)
    elif password != "":
        st.error("Password Salah!")
