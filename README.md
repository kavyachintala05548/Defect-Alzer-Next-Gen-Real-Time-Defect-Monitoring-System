# Defect-Alzer-Next-Gen-Real-Time-Defect-Monitoring-System
Defect-Alzer: A Next-Gen Real-Time Defect Monitoring System** is an AI-powered defect detection project built to identify manufacturing defects in real time using computer vision and deep learning. The system is designed for automated defect monitoring, quality inspection, and report generation using YOLOv8, Python, OpenCV, and Streamlit.

## Problem Statement

Manual defect inspection in manufacturing is:
- Slow, labour‑intensive, and inconsistent
- Error‑prone due to human fatigue
- Expensive when using high‑end GPU-based AI systems
Small and medium-scale industries often find it difficult to adopt expensive real-time automated inspection systems.

## Project Objective

The objective of this project is to build a cost-effective and scalable defect detection system that:

- Detects defects in products such as PCBs, plastic bottles, and apples.
- Works efficiently on low-end hardware.
- Provides a simple web interface for image or video upload and defect analysis.
- Generates CSV-based defect reports for further analysis.
    
## Features
- Real-time defect detection using YOLOv8.
- Automated defect monitoring for industrial quality control.
- Streamlit-based user interface for easy interaction.
- Bounding box visualization with confidence scores.
- CSV report generation for detected defects.
- Downloadable processed images and results.
- Optimized for practical use on low-end hardware.
## Keywords

defect detection, real-time monitoring, automated defect monitoring, computer vision, object detection, quality control, manufacturing inspection, YOLOv8, OpenCV, Python.

## Tech Stack
- Python
- YOLOv8
- OpenCV
- Streamlit
- Pandas
- CSV
  
## Project Structure

batch3/
├── process/              # Main app, preprocessing, defect handling logic
├── test/                 # Testing scripts(image input testing)
│   └── test.py
├── test1/                # Video input testing
│   └── video_input_test.py
├── dataset/              # Dataset files
├── models/               # Trained model weights for multiple use cases
│   └── best.pt
├── images/               # Sample and test images
├── requirements.txt      # Project dependencies
└── README.md
## How to Run
1. Clone the repository:
```bash
git clone https://github.com/your-username/defect-alzer.git
cd defect-alzer
```
2. Create a virtual environment:
```bash
python -m venv venv
```
3. Activate the virtual environment:
Windows:
```bash
venv\Scripts\activate
```
Mac/Linux:
```bash
source venv/bin/activate
```
4. Install required packages:
```bash
pip install -r requirements.txt
```
5. Run the Streamlit app:
```bash
streamlit run frontend.py
```
## System Workflow

The system works in the following steps:
1. Upload or capture product images or videos.
2. Preprocess the images.
3. Run the YOLOv8 model to detect defects.
4. Draw bounding boxes and confidence scores.
5. Save the results in CSV format.
6. Display the output in a Streamlit dashboard.

## Future Scope

- Predictive maintenance based on defect patterns.
- IoT integration for real-time monitoring.
- Support for more industrial product categories.
- Improved model performance with larger datasets.

## About This Project

This project was developed as a major project titled **Defect Alzer: Next-Gen Real-Time Defect Monitoring System** for industrial quality control using AI and computer vision.

