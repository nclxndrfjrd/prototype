import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

# Title of the app
st.title("🌪️ Live Wind Speed Logger")

# Initialize or load data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Date', 'Time', 'Wind Speed (m/s)'])

placeholder = st.empty()

# Start button to begin logging
if st.button('Start Logging'):
    st.success('Logging started... Press Stop to end.')
    
    # Loop to continuously generate random wind speed and display data
    while True:
        now = datetime.now()
        date_today = now.strftime("%Y-%m-%d")
        time_now = now.strftime("%H:%M:%S")
        wind_speed = round(random.uniform(0, 5), 2)

        # Add new data to the session state using concat instead of append
        new_row = pd.DataFrame({'Date': [date_today], 'Time': [time_now], 'Wind Speed (m/s)': [wind_speed]})
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

        # Update the table
        placeholder.dataframe(st.session_state.data)

        # Pause for 1 second before next data point
        time.sleep(1)

elif st.button('Stop Logging'):
    st.warning('Logging stopped.')
    st.stop()
