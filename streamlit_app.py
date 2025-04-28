import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime
import math
import altair as alt

# Title of the app
st.title("🌪️ Live Wind Speed Logger")

# Initialize or load data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Elapsed Time (s)', 'Date', 'Time', 'Wind Speed (m/s)', 'Vibration Count', 'RPM', 
                                                   'Sound Level (dB)', 'Expected Lift (N)', 'Expected Drag (N)', 
                                                   'Torque (N·m)', 'Max Stress (kPa)', 'Max Strain (%)', 
                                                   'Vibration Frequency (Hz)', 'Mechanical Power Output (W)', 
                                                   'Efficiency (%)', 'Heat Generation (°C)', 'Power Output (W)', 
                                                   'Voltage (V)', 'Current (A)'])
    st.session_state.start_time = time.time()

# Constants for the formulas
C_L = 1.2  # Lift coefficient
C_D = 0.8  # Drag coefficient
A = 10  # Blade area in m^2
Radius = 5  # Radius of the turbine in meters
C_P = 0.35  # Power coefficient
E = 210000  # Young's modulus for material (example)

# Helper function to generate realistic wind speed based on time of day
def generate_wind_speed(hour, current_wind_speed):
    # Target wind speed based on hour
    if 6 <= hour < 10:
        target_speed = 2.2
    elif 10 <= hour < 14:
        target_speed = 3.7
    elif 14 <= hour < 18:
        target_speed = 5.8
    else:
        target_speed = 1.1

    # Slowly move current speed toward target with small random noise
    change = random.uniform(-0.05, 0.05)  # small random wiggle
    new_speed = current_wind_speed + (target_speed - current_wind_speed) * 0.05 + change

    # Clamp between 0.5 m/s and 4.0 m/s to stay realistic
    new_speed = max(0.5, min(new_speed, 4.0))

    return round(new_speed, 2)

tab1, tab2 = st.tabs(["📋 Live Data Table", "📈 Performance Graphs"])

# Start logging automatically
st.success('Logging started...')

# Placeholders
with tab1:
    table_placeholder = st.empty()

with tab2:
    graph_placeholders = {
        'Wind Speed and RPM': st.empty(),
        'Aerodynamic Performance': st.empty(),
        'Structural Performance': st.empty(),
        'Mechanical Performance': st.empty(),
        'Electrical Power Performance': st.empty()
    }

# Main infinite loop
while True:
    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")
    hour = now.hour

    elapsed_time = round(time.time() - st.session_state.start_time, 2)
    # Initialize current wind speed
    current_wind_speed = 1.0

    # Generate realistic wind speed
    current_wind_speed = generate_wind_speed(hour, current_wind_speed)
    wind_speed = current_wind_speed


    # Calculations
    vibration_count = wind_speed * 0.5 + 2
    rpm = wind_speed * 60
    sound_level = 20 * math.log(rpm / 20) + 30
    expected_lift = 0.5 * C_L * A * wind_speed**2
    expected_drag = 0.5 * C_D * A * wind_speed**2
    torque = expected_lift * Radius
    max_stress = torque / 0.1
    max_strain = (max_stress / E) * 100
    vibration_frequency = rpm / 60
    mechanical_power_output = torque * rpm * (2 * math.pi / 60)
    efficiency = 0.9
    heat_generation = mechanical_power_output * 0.02
    power_output = 0.5 * C_P * A * wind_speed**3
    voltage = 12.5
    current = power_output / voltage

    # New row
    new_row = pd.DataFrame({'Elapsed Time (s)': [elapsed_time], 'Date': [date_today], 'Time': [time_now],
                            'Wind Speed (m/s)': [wind_speed], 'Vibration Count': [vibration_count], 'RPM': [rpm],
                            'Sound Level (dB)': [sound_level], 'Expected Lift (N)': [expected_lift], 
                            'Expected Drag (N)': [expected_drag], 'Torque (N·m)': [torque], 'Max Stress (kPa)': [max_stress], 
                            'Max Strain (%)': [max_strain], 'Vibration Frequency (Hz)': [vibration_frequency],
                            'Mechanical Power Output (W)': [mechanical_power_output], 'Efficiency (%)': [efficiency], 
                            'Heat Generation (°C)': [heat_generation], 'Power Output (W)': [power_output],
                            'Voltage (V)': [voltage], 'Current (A)': [current]})
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

    # Update Table
    with tab1:
        table_placeholder.dataframe(st.session_state.data)

    # Update Graphs
    with tab2:
        df = st.session_state.data

        # 1. Wind Speed and RPM
        line1 = alt.Chart(df).mark_line().encode(
            x='Elapsed Time (s)',
            y=alt.Y('Wind Speed (m/s)', axis=alt.Axis(title='Wind Speed (m/s)')),
            color=alt.value('blue')
        ) + alt.Chart(df).mark_line(strokeDash=[5,5]).encode(
            x='Elapsed Time (s)',
            y=alt.Y('RPM', axis=alt.Axis(title='RPM')),
            color=alt.value('red')
        )
        graph_placeholders['Wind Speed and RPM'].altair_chart(line1, use_container_width=True)

        # 2. Aerodynamic Performance (Lift and Drag)
        line2 = alt.Chart(df).mark_line().encode(
            x='Elapsed Time (s)',
            y=alt.Y('Expected Lift (N)', axis=alt.Axis(title='Expected Lift (N)')),
            color=alt.value('green')
        ) + alt.Chart(df).mark_line(strokeDash=[5,5]).encode(
            x='Elapsed Time (s)',
            y=alt.Y('Expected Drag (N)', axis=alt.Axis(title='Expected Drag (N)')),
            color=alt.value('orange')
        )
        graph_placeholders['Aerodynamic Performance'].altair_chart(line2, use_container_width=True)

        # 3. Structural Performance (Stress and Strain)
        line3 = alt.Chart(df).mark_line().encode(
            x='Elapsed Time (s)',
            y=alt.Y('Max Stress (kPa)', axis=alt.Axis(title='Max Stress (kPa)')),
            color=alt.value('purple')
        ) + alt.Chart(df).mark_line(strokeDash=[5,5]).encode(
            x='Elapsed Time (s)',
            y=alt.Y('Max Strain (%)', axis=alt.Axis(title='Max Strain (%)')),
            color=alt.value('pink')
        )
        graph_placeholders['Structural Performance'].altair_chart(line3, use_container_width=True)

        # 4. Mechanical Performance (Mechanical Power Output)
        line4 = alt.Chart(df).mark_line(color='teal').encode(
            x='Elapsed Time (s)',
            y=alt.Y('Mechanical Power Output (W)', axis=alt.Axis(title='Mechanical Power Output (W)'))
        )
        graph_placeholders['Mechanical Performance'].altair_chart(line4, use_container_width=True)

        # 5. Electrical Power Performance (Power Output and Current)
        line5 = alt.Chart(df).mark_line().encode(
            x='Elapsed Time (s)',
            y=alt.Y('Power Output (W)', axis=alt.Axis(title='Power Output (W)')),
            color=alt.value('brown')
        ) + alt.Chart(df).mark_line(strokeDash=[5,5]).encode(
            x='Elapsed Time (s)',
            y=alt.Y('Current (A)', axis=alt.Axis(title='Current (A)')),
            color=alt.value('black')
        )
        graph_placeholders['Electrical Power Performance'].altair_chart(line5, use_container_width=True)

    # Sleep 1 second
    time.sleep(1)
