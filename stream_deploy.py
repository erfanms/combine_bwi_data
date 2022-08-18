import numpy as np
import pandas as pd
import streamlit as st




uploaded_parameter_file = st.file_uploader("Upload parameter file")
if uploaded_parameter_file is not None:
    df_parameters = pd.read_excel(uploaded_parameter_file)

