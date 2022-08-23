import numpy as np
import pandas as pd
import streamlit as st
import datetime as dt

def dttime(i):
    if '/' in str(i):
        return pd.to_datetime(i)
    else:
        return pd.to_datetime(str(i),format='%Y-%d-%m %H:%M:%S')



uploaded_parameter_file = st.file_uploader("Upload parameter file")
if uploaded_parameter_file is not None:
    df_parameters = pd.read_excel(uploaded_parameter_file)

    uploaded_loss_file = st.file_uploader("Upload loss_file")
    if uploaded_loss_file is not None:
        df_loss = pd.read_excel(uploaded_loss_file,sheet_name= 'Sheet3')


        #df_parameters.DATE = df_parameters.DATE.apply(dttime)
        df_parameters = df_parameters[df_parameters.THICKNESS == 12]
        df_parameters.loc[((df_parameters.DATE.dt.hour > 5) | (df_parameters.DATE.dt.hour < 14)),'Shift'] = 'A'
        df_parameters.loc[((df_parameters.DATE.dt.hour > 13) | (df_parameters.DATE.dt.hour < 22)),'Shift'] = 'B'
        df_parameters.loc[((df_parameters.DATE.dt.hour > 21) | (df_parameters.DATE.dt.hour < 6)),'Shift'] = 'C'
        df_parameters = df_parameters.set_index('DATE')
        df_parameters.loc[df_parameters.between_time('06:00','14:00',include_end = False).index,'Shift'] = 'A'
        df_parameters.loc[df_parameters.between_time('14:00','22:00',include_end = False).index,'Shift'] = 'B'
        df_parameters.loc[df_parameters.between_time('22:00','6:00',include_end = False).index,'Shift'] = 'C'
        df_parameters = df_parameters.reset_index()

        df_loss['Time'] = pd.to_datetime(df_loss['Time'].apply(lambda x: str(x))).dt.time
        df_loss['Merge'] = df_loss['Date'].dt.date.apply(lambda x: str(x)) + ' ' + df_loss['Shift'] + ' ' + df_loss['Time'].apply(lambda x: str(x))
        df_loss['Loss (distributed)'] = df_loss['Loss (distributed)'].fillna(0)

        df_parameters['Merge'] = df_parameters['DATE'].dt.date.apply(lambda x: str(x)) + ' ' + df_parameters['Shift'] + ' '  + df_parameters['DATE'].dt.time.apply(lambda x: str(x))
        df_combined = df_parameters.merge(df_loss,on='Merge',how='inner')


        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df_combined)

        st.download_button(
             label="Download combined data as CSV",
             data=csv,
             file_name='large_df.csv',
             mime='text/csv',
         )
