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
    ax.set_ylim(0, 400)  # Radar range in cm
    ax.set_yticks([100, 200, 300, 400])   # Range markers
    ax.set_xticks(np.radians([150, 120, 90, 60, 30, 0, -30, -60, -90, -120, -150, -180]))  # Angle markers
    ax.set_xticklabels(["150", "120", "90", "60", "30", "0°", "30°", "60°", "90°", "60°", "30°", "0°"])
    sc = ax.scatter([], [], c='r', label="Object", s=50)
    # Sweeping line (initially empty)
    sweep_line, = ax.plot(-90, 400, 'g-', linewidth=2, label="Sweeping Line")
    st.pyplot(fig)
    return fig, ax, sc, sweep_line

"""Real-time data handling and plot updating"""
# 🔄 Live Data Loop
data_points = []
line_counter = 0
placeholder = st.empty()  # For displaying live data
fig, ax, sc, sweep_line = setup()  # Run setup to initialize everything

while True:
    # try:
        # Read Data from Serial
        data = ser.readline().decode().strip()
        line_counter += 1

        print(data)
        st.write(data)

        if "," in data:
            angle, distance = data.split(",")
            angle, distance = int(angle), int(distance)
            
            # Store Data for Plotting
            if distance < 800:  # Ignore out-of-range values
                data_points.append((np.radians(angle), distance))

            if len(data_points) > 3:
                data_points.pop(0)  # Remove the oldest point

            # flip data points
            if data_points:
                angles, distances = zip(*data_points)
                angles = -1* (180-np.array(angles))  # Flip angles
                distances = np.array(distances)
            else:
                angles, distances = np.array([]), np.array([])
            

            # 🔄 Update Sweeping Line
            # r_values = np.linspace(0, 400, 50)  # Full radial line
            # theta_values = np.full_like(r_values, np.radians(angle))  # Keep angle fixed
            # # Change line color based on distance
            # color = 'red' if distance < 500 else 'green'
            # sweep_line.set_data(theta_values, r_values)
            # sweep_line.set_color(color)


            # Update UI
            # with placeholder.container():
            #     st.write(f"**Angle:** {angle}° | **Distance:** {distance} cm")
            # 🔄 Update Radar Plot
            
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


