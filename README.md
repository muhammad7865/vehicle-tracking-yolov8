<div align="center">

# Real-Time Vehicle Tracking & Traffic Flow Density Estimator

**An edge-ready Computer Vision pipeline combining YOLOv8 multi-class object detection, centroid trajectory tracking, and bi-directional virtual boundary traffic telemetry.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=flat-square&logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

</div>

---

## 📌 Overview

Automated traffic surveillance and telemetry are vital components of modern Intelligent Transportation Systems (ITS). This project delivers an automated, real-time pipeline to detect, track, and quantify vehicle flow across complex roadway scenarios without requiring expensive infrastructure sensors.

By pairing **YOLOv8 object detection** with a custom **Euclidean coordinate tracker**, this system maintains persistent vehicle identities, tracks motion vectors across consecutive frames, and measures directional volume using virtual crossing triggers.

---

## ✨ Key Capabilities

* **Multi-Class Vehicle Detection:** Detects cars, buses, trucks, and motorcycles in variable lighting conditions using optimized YOLOv8 weights.
* **Persistent Centroid Tracking:** Custom `Track` state-machine tracking object centroids $(c_x, c_y)$ and bounding-box coordinates to maintain tracking continuity across frames.
* **Occlusion & Disappearance Recovery:** Frame-distance heuristics prevent duplicate counting when vehicles undergo brief visual occlusions.
* **Virtual Boundary Counting Line:** Synthesizes bidirectional counting lines across roadways, computing crossing transitions to estimate directional traffic volume in real time.
* **Live Video Telemetry Dashboard:** Overlays tracking bounding boxes, object IDs, motion vectors, and cumulative counters directly onto output video feeds.

---

## 🏗️ Architecture & Pipeline Flow

```text
Input Video Stream (MP4/RTSP)
             │
             ▼
   [ Frame Extraction ]
             │
             ▼
   [ YOLOv8 Inference ] ───► Extract Bounding Boxes [x1, y1, x2, y2, conf, class]
             │
             ▼
  [ Centroid Calculation ] ──► Bottom Center Coordinate (cx, bottom_y)
             │
             ▼
  [ Track State Machine ] ───► Associate with Existing Track ID or Initialize New Track
             │
             ▼
[ Boundary Crossing Logic ] ──► Check Transition (prev_bottom_y < Line <= current_bottom_y)
             │
             ├──► Trigger Vehicle Count Increment (counted = True)
             ▼
  [ Frame Annotation ] ─────► Render IDs, Bounding Boxes, and Analytics Dashboard
             │
             ▼
Output Video Stream / File Storage
```

---

## 📊 Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **Object Detector** | YOLOv8 Nano (`yolov8n.pt`) / Medium (`yolov8m.pt`) |
| **Input Resolution** | Dynamic (Tested on 1080p and 720p 30 FPS video feeds) |
| **Tracking Algorithm** | Centroid-based Euclidean Distance Mapping |
| **Target Classes** | Car (class 2), Motorcycle (class 3), Bus (class 5), Truck (class 7) |
| **Inference Framework** | PyTorch / Ultralytics |
| **Telemetry Outputs** | Total Inflow / Outflow Count, Real-Time FPS, Annotated Video (`.mp4`) |

---

## 📁 Repository Structure

```text
vehicle-tracking-yolov8/
├── track_and_count.py       # Main real-time detection, tracking, and counting pipeline
├── yolov8n.pt               # Lightweight pretrained YOLOv8 nano model weights
├── requirements.txt         # Production dependencies
├── .gitignore               # Excludes raw video feeds and build caches
└── README.md                # Project documentation and benchmarks
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/muhammad7865/vehicle-tracking-yolov8.git
cd vehicle-tracking-yolov8
```

### 2. Environment Setup
Create a virtual environment and install the required dependencies:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Tracking on Video Feed
Place your test video in the root directory (e.g., `traffic.mp4`) and run:
```bash
python track_and_count.py
```
Annotated frames and telemetry output will be compiled directly into `runs/track/yolo_output.mp4`.

---

## 👤 Author

**Muhammad Awais Mohsin**  
*COMSATS University Islamabad — Cybersecurity & Applied AI Systems Engineer*  
* GitHub: [@muhammad7865](https://github.com/muhammad7865)  
* LinkedIn: [Muhammad Awais Mohsin](https://linkedin.com/in/muhammad-awais-mohsin-b1250026a)  
* Portfolio: [miihammadawais.vercel.app](https://miihammadawais.vercel.app)