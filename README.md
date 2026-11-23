# Real-Time Vehicle Tracking and Density Estimator using YOLOv8

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange.svg)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated video surveillance and traffic telemetry pipeline that performs multi-class vehicle detection, centroid tracking, and bi-directional traffic density estimation in real time using YOLOv8 and OpenCV.

---

## Technical Highlights

1. **Object Detection:** Utilizes pretrained YOLOv8 models for accurate detection of multi-class vehicles (cars, motorcycles, buses, trucks).
2. **Centroid-Based Tracking:** Custom \Track\ class mapping Euclidean coordinate transitions between successive frames, maintaining target ID persistence and handling temporary occlusion.
3. **Virtual Boundary Triggering:** Dynamically monitors coordinate offsets across customizable spatial threshold lines to count incoming and outgoing vehicle flows without manual intervention.
4. **Visual Telemetry:** Real-time trajectory overlays, bounding box visualization, and dynamic traffic count dashboards rendered directly onto video feeds.

---

## Repository Structure

`	ext
vehicle-tracking-yolov8/
├── track_and_count.py       # Main detection and tracking pipeline
├── yolov8n.pt               # Lightweight YOLOv8 nano model
├── requirements.txt
├── .gitignore
└── README.md
`

---

## Quickstart

### 1. Installation
\\\ash
git clone https://github.com/muhammad7865/vehicle-tracking-yolov8.git
cd vehicle-tracking-yolov8
pip install -r requirements.txt
\\\

### 2. Run on Video Feed
\\\ash
python track_and_count.py
\\\

---

## Author
**Muhammad Awais Mohsin**  
COMSATS University Islamabad | Cybersecurity & AI Systems Engineer  
- GitHub: [@muhammad7865](https://github.com/muhammad7865)  
- LinkedIn: [muhammad-awais-mohsin-b1250026a](https://linkedin.com/in/muhammad-awais-mohsin-b1250026a)
