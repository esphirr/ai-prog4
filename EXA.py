import streamlit as st

txt = st.text_area(
    
)

st.write(f"You wrote {len(txt)} characters.")
