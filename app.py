import streamlit as st
from github import Github
import os
from dotenv import load_dotenv

# Load token dari .env
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

st.title("Akses Video dari GitHub Repo")

# Inisialisasi GitHub
g = Github(token)

try:
    # Mengakses repo milik Mas Lian
    repo = g.get_repo("operansangiang-rs/video_sa")
    
    # Contoh: Mengambil konten file dari repo
    # Mas Lian bisa mengganti 'video1.mp4' dengan nama file di repo
    file_content = repo.get_contents("video1.mp4")
    
    st.success("Berhasil terhubung ke GitHub!")
    
    # Menampilkan video dari URL download file di GitHub
    st.video(file_content.download_url, autoplay=True)

except Exception as e:
    st.error(f"Gagal terhubung atau file tidak ditemukan: {e}")
