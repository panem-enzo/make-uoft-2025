# BikEssential: AI-Powered Blind Spot Detection for Cyclists  

## Inspiration  
Cycling in busy cities like Toronto can be dangerous due to blind spots and unpredictable traffic. Many cyclists struggle to stay aware of approaching vehicles, increasing the risk of accidents. We wanted to create a smart safety system that would help cyclists feel safer on the road by increasing their awareness of vehicles approaching from blind spots.  

## What it does  
BikEssential uses an **ESP32-CAM** with AI-powered image detection to identify vehicles approaching from a cyclist's blind spots. When a vehicle is detected, the system activates an **ultrasonic sensor** to measure the vehicle's distance. If the vehicle is too close, the system alerts the cyclist with **flashing LED lights** and a **buzzer**, providing real-time warnings and enhancing the cyclist's awareness of their surroundings. Additionally, a **web app** displays real-time camera footage for the user, enhancing the visual feedback for cyclists.  

## How we built it  
We integrated several key components into the system:  
- **ESP32-CAM** for real-time image detection and processing  
- **Cloudflare AI object detection** to identify approaching vehicles in the camera footage  
- **Arduino** to control the hardware and manage signals between components  
- **Servo motor** to adjust the position of the ultrasonic sensor based on detected vehicles  
- **Ultrasonic sensor** to measure the distance of vehicles  
- **LED lights** and **buzzer** for visual and auditory alerts  
- **Streamlit** to create a simple web app to display real-time camera footage from the ESP32-CAM  

The components were connected on a breadboard and programmed to work together seamlessly, with the ESP32-CAM processing images and triggering the Arduino-controlled sensor and alert system. The camera footage is then streamed to the web app via Streamlit, allowing users to view live footage and alerts from the system.

## Challenges we ran into  
- **Object detection accuracy**: Fine-tuning the ESP32-CAM’s image detection to reliably identify vehicles, especially in various lighting conditions, was a challenge.  
- **Hardware integration**: Ensuring smooth communication between the ESP32-CAM, Arduino, servo motor, and sensors required several adjustments to the wiring and code.  
- **Power consumption**: Managing the power requirements for real-time detection and the activation of alerts while ensuring efficiency was a concern.  
- **Web app integration**: Implementing the web app with Streamlit to seamlessly display camera footage in real-time posed some initial challenges, especially regarding data transfer and UI responsiveness.

## Accomplishments that we're proud of  
- Successfully implementing **AI-based object detection** with **Cloudflare** on the ESP32-CAM for vehicle detection  
- Building a system that alerts cyclists in real-time using visual and auditory signals  
- Creating a **web app with Streamlit** to display live camera footage, providing added safety awareness for cyclists  
- Overcoming hardware integration issues and creating a fully functional prototype  

## What we learned  
- How to integrate **Cloudflare AI** for real-time object detection with embedded hardware like the ESP32-CAM  
- The challenges of **real-time data processing** and the importance of optimizing power consumption in battery-powered devices  
- Effective **hardware integration**, especially when combining sensors, motors, and communication protocols  
- How to create a **web app using Streamlit** to display live footage and alerts from the system  

## What's next for BikEssential  
- **Smart object tracking**: Implementing advanced tracking algorithms to enhance the detection of approaching vehicles.  
- **Dual camera depth estimation**: Using **OpenCV stereo vision** and **disparity matching** for better depth perception and distance measurement of vehicles in the cyclist’s blind spots.  
- **Radar tracking**: Integrating a **24 GHz mmWave radar sensor** for real-time distance and speed measurements, and combining radar and camera systems for more robust object detection and tracking.  
- **Tracker App**: Developing an app to display **GPS tracking** for cyclists, alerting them about **danger/high-risk zones** based on their location and current cycling route.  
- Enhancing object detection to improve accuracy in more challenging conditions, like nighttime or heavy traffic  
- Adding more advanced features, such as integration with a mobile app for cyclist tracking and data analysis  
- Exploring more efficient **power management techniques** to extend battery life  
- Testing and refining the system with real-world cyclists to ensure its reliability and effectiveness  
