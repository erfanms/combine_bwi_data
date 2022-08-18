import streamlit as st
import pandas as pd
st.title(“A Simple Streamlit Web App”)
name = st.text_input(“Enter your name”, ‘’)
st.write(f”Hello {name}!”)
