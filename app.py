import streamlit as st
import serial
import numpy as np
import matplotlib.pyplot as plt
import time

# 🚀 Serial Port Configuration (Change COM port accordingly)
SERIAL_PORT = "COM7"  # Update based on your system (e.g., /dev/ttyUSB0 for Linux)
BAUD_RATE = 9600

# 📍 Streamlit Title
st.title("📡 Real-Time Radar System")
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    st.sidebar.success(f"Connected to {SERIAL_PORT} ✅")
except:
    st.sidebar.error(f"Failed to connect to {SERIAL_PORT} ❌")


@st.cache_data
def setup():
    """Setup function for initializing the serial port and radar plot"""
    # 🚦 Try connecting to Serial Port
   
    # 🔵 Radar Plot Setup
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    ax.set_ylim(0, 80)  # Radar range in cm
    ax.set_yticks([50, 100, 150, 200])   # Range markers
    ax.set_xticks(np.radians([0, 30, 60, 90, 120, 150, 180]))  # Angle markers
    ax.set_xticklabels(["0°", "30°", "60°", "90°", "120°", "150°", "180°"])
    sc = ax.scatter([], [], c='r', label="Object", s=50)

    st.pyplot(fig)
    return fig, ax, sc

"""Real-time data handling and plot updating"""
# 🔄 Live Data Loop
data_points = []
line_counter = 0
placeholder = st.empty()  # For displaying live data

fig, ax, sc = setup()  # Run setup to initialize everything

while True:
    # try:
        # Read Data from Serial
        data = ser.readline().decode().strip()
        line_counter += 1

        if line_counter % 15 == 0:
            st.write(data)

            if "," in data:
                angle, distance = data.split(",")
                angle, distance = int(angle), int(distance)
                # Store Data for Plotting
                if distance < 800:  # Ignore out-of-range values
                    data_points.append((np.radians(angle), distance))

                if len(data_points) > 3:
                    data_points.pop(0)  # Remove the oldest point

                # Update UI
                # with placeholder.container():
                #     st.write(f"**Angle:** {angle}° | **Distance:** {distance} cm")

                # 🔄 Update Radar Plot
                angles, distances = zip(*data_points) if data_points else ([], [])
                sc.set_offsets(np.c_[angles, distances])
                ax.set_title("Real-Time Radar Feed")
                ax.legend()
                placeholder.pyplot(fig)

            time.sleep(0.1)  # Refresh every 100ms
        # except:
        #     st.error("❌ Error reading from Serial. Check Connection!")
        #     break

# Main Execution
  # Start the real-time loop if setup succeeded
