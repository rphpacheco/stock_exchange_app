import streamlit as st

def set():
    with open('styles.css') as f:
        st.markdown(
            f'<style>{f.read()}</style>',
            unsafe_allow_html=True
        )