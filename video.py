import streamlit as st
import cv2
import numpy as np
import urllib.request

ESP32_STREAM_URL = "http://172.20.10.10/"

st.title("ESP32-S3 Camera 🎥")
frame_placeholder = st.empty()

try:
    stream = urllib.request.urlopen(ESP32_STREAM_URL)
except Exception as e:
    st.error(f"Failed to connect: {e}")
    st.stop()

byte_stream = b""

while True:
    byte_stream += stream.read(1024)  # Read data in small chunks

    start = byte_stream.find(b'\xff\xd8')  # JPEG Start
    end = byte_stream.find(b'\xff\xd9')  # JPEG End

    if start != -1 and end != -1:
        jpg = byte_stream[start:end+2]
        byte_stream = byte_stream[end+2:]  # Remove processed data

        if len(jpg) == 0:
            st.warning("Empty frame received! Retrying...")
            continue  # Skip decoding empty frames

        try:
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is None:
                st.error("Failed to decode frame! Retrying...")
                continue  # Skip bad frames

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)  # ✅ Updated here

        except Exception as e:
            st.error(f"Decoding error: {e}")
