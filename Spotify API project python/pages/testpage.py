import streamlit as st
st.set_page_config(menu_items=None)
st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("testpage in pages!")