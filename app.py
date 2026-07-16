import streamlit as st
from github import Github

# Mengambil data dari secrets Streamlit
# (Jika di lokal, gunakan file .streamlit/secrets.toml)
try:
    github_config = st.secrets["github"]
    token = github_config["token"]
    repo_name = github_config["repo"]
    
    g = Github(token)
    repo = g.get_repo(repo_name)
    st.write(f"Terhubung ke repo: {repo.full_name}")
    
except Exception as e:
    st.error("Pastikan konfigurasi secrets sudah benar di Streamlit Cloud.")
