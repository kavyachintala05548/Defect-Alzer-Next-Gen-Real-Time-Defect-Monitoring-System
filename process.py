'''import streamlit as st
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO

# Mapping categories to model filenames
model_paths = {
    "Apples": "best (app).pt",
    "Plastic Bottles": "best (4).pt",
    "PCBs": "best (pcb).pt"
}

# Define class names for each category
category_classes = {
    "Apples": ["Defect Apple", "Good Apple"],
    "Plastic Bottles": ["Bottle", "Defective Cap", "Defective Label", "Dirt", "Good Cap", "Good Label", "Low Level", "Water Level"],
    "PCBs": ["Good PCB", "Missing Hole", "Mouse Bite", "Open Circuit", "Short", "Spurious Copper"]
}

# Title of the application
st.title("🔍 Defective Object Detection")

# Step 1: Choose Product Category
st.header("Step 1: Choose a Product Category")
categories = list(model_paths.keys())  # Get category names dynamically
category = st.selectbox("Select the category of the product:", categories)

# Set the corresponding model and class names
model_path = model_paths[category]
class_names = category_classes[category]  # Get class names based on category

st.write(f"📌 Using model: {model_path}")
model = YOLO(model_path)  # Load YOLO model

# Step 2: Upload an Image
st.header("Step 2: Upload an Image")
uploaded_file = st.file_uploader("Upload a product image for defect detection", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption=f"Uploaded Image: {category}", use_column_width=True)

    # Convert the image to a format suitable for OpenCV
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Step 3: Select Class for Detection (Specific to Category)
    st.header("Step 3: Select Class for Detection")
    selected_class = st.selectbox("Select the specific defect to detect:", class_names)

    # Button to perform defect detection
    if st.button("Run Defect Detection"):
        st.write("🔍 Running defect detection using YOLOv8...")

        # Perform YOLOv8 prediction
        results = model.predict(source=image_bgr,save=True, conf=0.25, verbose=False)

        detected = False  # Flag to check if any relevant defect is found

        for result in results:
            if result.boxes:  # If bounding boxes are detected
                img_with_predictions = result.plot()
                img_rgb = cv2.cvtColor(img_with_predictions, cv2.COLOR_BGR2RGB)
                st.image(img_rgb, caption="Defect Detection Results", use_column_width=True)

                # Display details of detected defects
                st.write("⚙ Results Summary:")

                for box in result.boxes:
                    class_index = int(box.cls.item())  # Get class index
                    class_label = class_names[class_index]  # Get class name

                    # **Display only if it matches the selected defect**
                    if class_label == selected_class:
                        detected = True
                        st.write(f"- Class: **{class_label}**, Confidence: **{box.conf.item():.2f}**")

        # If no relevant defect was detected
        if not detected:
            st.success(f"✅ No defects of type '{selected_class}' found!")
            st.write("Classification: **Nondefective** ✅")

# Sidebar Information
st.sidebar.title("📌 Project Info")
st.sidebar.write("""
This interface detects defective objects in:
- 🍏 Apples
- 🏭 Plastic Bottles
- 🔌 PCBs

Upload an image and select a defect to analyze.
""")
'''
'''import streamlit as st
from PIL import Image
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO

# Mapping categories to model filenames
model_paths = {
    "Apples": "best (app).pt",
    "Plastic Bottles": "best (4).pt",
    "PCBs": "best (pcb).pt"
}

# Define class names for each category
category_classes = {
    "Apples": ["Defect Apple", "Good Apple"],
    "Plastic Bottles": ["Bottle", "Defective Cap", "Defective Label", "Dirt", "Good Cap", "Good Label", "Low Level", "Water Level"],
    "PCBs": ["Good PCB", "Missing Hole", "Mouse Bite", "Open Circuit", "Short", "Spurious Copper"]
}

# Data storage for defect reports
defect_data = []

# Title of the application
st.title("🔍 Defective Object Detection")

# Step 1: Choose Product Category
st.header("Step 1: Choose a Product Category")
categories = list(model_paths.keys())  # Get category names dynamically
category = st.selectbox("Select the category of the product:", categories)

# Set the corresponding model and class names
model_path = model_paths[category]
class_names = category_classes[category]  # Get class names based on category

st.write(f"📌 Using model: `{model_path}`")
model = YOLO(model_path)  # Load YOLO model

# Step 2: Upload an Image
st.header("Step 2: Upload an Image")
uploaded_file = st.file_uploader("Upload a product image for defect detection", type=["jpg", "jpeg", "png"])

# Sidebar settings
st.sidebar.header("⚙ Settings")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.4, 0.8, 0.6, 0.05)

if uploaded_file is not None:
    # Load and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption=f"Uploaded Image: {category}", use_column_width=True)

    # Convert the image to a format suitable for OpenCV
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Step 3: Select Class for Detection (Specific to Category)
    st.header("Step 3: Select Class for Detection")
    selected_class = st.selectbox("Select the specific defect to detect:", class_names)

    # Button to perform defect detection
    if st.button("🔍 Run Defect Detection"):
        st.write("🔎 Processing image...")

        # Perform YOLO prediction
        results = model.predict(source=image_bgr, conf=confidence_threshold, verbose=False)

        detected = False  # Flag to check if any relevant defect is found
        defect_data.clear()  # Clear previous defect data

        for result in results:
            if result.boxes:  # If bounding boxes are detected
                img_with_predictions = result.plot()
                img_rgb = cv2.cvtColor(img_with_predictions, cv2.COLOR_BGR2RGB)
                st.image(img_rgb, caption="🛠 Defect Detection Results", use_column_width=True)

                # Display details of detected defects
                st.write("📌 **Detection Summary:**")

                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                    conf = float(box.conf[0])  # Confidence score
                    class_index = int(box.cls[0])  # Class index
                    class_label = class_names[class_index]  # Get class name

                    # Display only if it matches the selected defect
                    if class_label == selected_class:
                        detected = True
                        st.write(f"- **Class:** `{class_label}` | **Confidence:** `{conf:.2f}`")
                        defect_data.append([category, class_label, x1, y1, x2, y2, conf])

        # If no relevant defect was detected
        if not detected:
            st.success(f"✅ No defects of type '{selected_class}' found!")
            st.write("✔ Classification: *Nondefective*")

        # Export defect records if defects were found
        if defect_data:
            df = pd.DataFrame(defect_data, columns=["Category", "Class", "X1", "Y1", "X2", "Y2", "Confidence"])
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Defect Report", csv, "defect_records.csv", "text/csv", key="download-csv")

# Sidebar Information
st.sidebar.title("📌 Project Info")
st.sidebar.write("""
This interface detects defective objects in:
- 🍏 Apples
- 🏭 Plastic Bottles
- 🔌 PCBs

Upload an image and select a defect to analyze.
""")'''
'''import streamlit as st
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import io
from ultralytics import YOLO

# Define save directories
SAVE_DIR = "detected_files"
LOG_FILE = "defect_detection_log.csv"
os.makedirs(SAVE_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename="defect_detection.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Model paths and class names
model_paths = {
    "Apples": "best (app).pt",
    "Plastic Bottles": "best (4).pt",
    "PCBs": "best (pcb).pt"
}

category_classes = {
    "Apples": ["Defect Apple", "Good Apple"],
    "Plastic Bottles": ["Bottle", "Defective Cap", "Defective Label", "Dirt", "Good Cap", "Good Label", "Low Level",
                        "Water Level"],
    "PCBs": ["Good PCB", "Missing Hole", "Mouse Bite", "Open Circuit", "Short", "Spurious Copper"]
}

defective_classes = ["Defect Apple", "Defective Cap", "Defective Label", "Dirt", "Low Level", "Missing Hole",
                     "Mouse Bite", "Open Circuit", "Short", "Spurious Copper"]

# Load previous log data
if os.path.exists(LOG_FILE):
    log_data = pd.read_csv(LOG_FILE)
else:
    log_data = pd.DataFrame(columns=["Timestamp", "Category", "Class", "Confidence"])


# Function to log detections
def log_detection(category, detected_class, confidence):
    new_log = pd.DataFrame([[pd.Timestamp.now(), category, detected_class, confidence]],
                           columns=["Timestamp", "Category", "Class", "Confidence"])
    new_log.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)


# Function to calculate evaluation metrics
def calculate_metrics(log_data, class_names):
    tp = sum((log_data["Class"].isin(class_names)) & (log_data["Confidence"] >= confidence_threshold))
    fp = sum((log_data["Class"].isin(class_names)) & (log_data["Confidence"] < confidence_threshold))
    fn = sum(~log_data["Class"].isin(class_names))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0

    return accuracy, precision, recall, f1_score


# Streamlit App Title
st.title("🔍 AI-Powered Defect Detection & Dashboard")

# Sidebar Settings
st.sidebar.title("📊 Dashboard & Settings")
view_dashboard = st.sidebar.checkbox("📈 View Dashboard")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.4, 0.8, 0.6, 0.05)

if view_dashboard:
    st.header("📊 Defect Detection Analysis")
    if not log_data.empty:
        total_images = log_data["Category"].count()
        st.metric(label="Total Images Processed", value=total_images)
        defect_counts = log_data["Class"].value_counts()

        # 📊 Bar Chart - Defect Type Distribution
        st.subheader("🛠 Defect Type Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=defect_counts.index, y=defect_counts.values, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # 📌 Confidence Score Analysis
        st.subheader("📌 Confidence Score Analysis")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(log_data["Confidence"], bins=10, kde=True, ax=ax)
        st.pyplot(fig)

        # 📊 Evaluation Metrics
        accuracy, precision, recall, f1_score = calculate_metrics(log_data,
                                                                  category_classes["Apples"] + category_classes[
                                                                      "Plastic Bottles"] + category_classes["PCBs"])
        st.subheader("📊 Model Evaluation Metrics")
        st.metric("✔️ Accuracy", f"{accuracy:.2%}")
        st.metric("🎯 Precision", f"{precision:.2%}")
        st.metric("🔍 Recall", f"{recall:.2%}")
        st.metric("⚖️ F1-score", f"{f1_score:.2%}")

    else:
        st.write("No data available. Run detections to generate reports.")
else:
    st.header("🛠 Detect Defects in Products")
    category = st.selectbox("Select Product Category:", list(model_paths.keys()))
    model_path = model_paths[category]
    class_names = category_classes[category]

    try:
        model = YOLO(model_path)
        st.write(f"📌 Using Model: {model_path}")
        logging.info(f"Loaded YOLO model: {model_path}")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        logging.error(f"Model loading failed: {e}")

    uploaded_file = st.file_uploader("Upload a product image for defect detection", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded Image: {category}", use_column_width=True)
        image_np = np.array(image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        st.header("Step 3: (Optional) Select a Specific Defect")
        selected_class = st.selectbox("Select a defect to detect (leave blank to detect all):",
                                      ["Detect All"] + class_names)

        if st.button("🔍 Run Defect Detection"):
            st.write("🔎 Processing image...")
            results = model.predict(source=image_bgr, conf=confidence_threshold, verbose=False)
            detected_defects = []
            is_defective = False

            for result in results:
                if result.boxes:
                    img_with_predictions = result.plot()
                    img_rgb = cv2.cvtColor(img_with_predictions, cv2.COLOR_BGR2RGB)
                    save_path = os.path.join(SAVE_DIR, f"detected_{uploaded_file.name}")
                    cv2.imwrite(save_path, cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
                    st.image(img_rgb, caption="🛠 Defect Detection Results", use_column_width=True)
                    pil_image = Image.fromarray(img_rgb)
                    st.write("📌 **Detection Summary:**")

                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        class_index = int(box.cls[0])
                        class_label = class_names[class_index]

                        if selected_class == "Detect All" or class_label == selected_class:
                            detected_defects.append([category, class_label, x1, y1, x2, y2, conf])
                            st.write(
                                f"- **Class:** `{class_label}` | **Confidence:** `{conf:.2f}` | 📍 **Location:** ({x1}, {y1}) → ({x2}, {y2})")
                            if class_label in defective_classes:
                                is_defective = True
                            log_detection(category, class_label, conf)

            if is_defective:
                st.error("⚠️ **Defective Product Detected!**")
            else:
                st.success("✅ **No Defects Found – Product is Good!**")

            if detected_defects:
                df = pd.DataFrame(detected_defects, columns=["Category", "Class", "X1", "Y1", "X2", "Y2", "Confidence"])
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Defect Report (CSV)", csv, "defect_records.csv", "text/csv")'''


import streamlit as st
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import io
from ultralytics import YOLO

# Setup
SAVE_DIR = "detected_files"
LOG_FILE = "defect_detection_log.csv"
os.makedirs(SAVE_DIR, exist_ok=True)

model_paths = {
    "Apples": "best (app).pt",
    "Plastic Bottles": "best (4).pt",
    "PCBs": "best (pcb).pt"
}

category_classes = {
    "Apples": ["Defect Apple", "Good Apple"],
    "Plastic Bottles": ["Bottle", "Defective Cap", "Defective Label", "Dirt", "Good Cap", "Good Label", "Low Level", "Water Level"],
    "PCBs": ["Good PCB", "Missing Hole", "Mouse Bite", "Open Circuit", "Short", "Spurious Copper"]
}

defective_classes = ["Defect Apple", "Defective Cap", "Defective Label", "Dirt", "Low Level", "Missing Hole",
                     "Mouse Bite", "Open Circuit", "Short", "Spurious Copper"]

if os.path.exists(LOG_FILE):
    log_data = pd.read_csv(LOG_FILE)
else:
    log_data = pd.DataFrame(columns=["Timestamp", "Category", "Class", "Confidence"])

def log_detection(category, detected_class, confidence):
    new_log = pd.DataFrame([[pd.Timestamp.now(), category, detected_class, confidence]],
                           columns=["Timestamp", "Category", "Class", "Confidence"])
    new_log.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)

st.title("🔍 AI-Powered Defect Detection & Dashboard")
st.sidebar.title("📊 Dashboard & Settings")

view_dashboard = st.sidebar.checkbox("📈 View Dashboard")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.4, 0.8, 0.6, 0.05)

if view_dashboard:
    st.header("📊 Defect Detection Analysis")
    if not log_data.empty:
        st.metric("Total Images Processed", log_data["Category"].count())
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=log_data["Class"].value_counts().index, y=log_data["Class"].value_counts().values, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.histplot(log_data["Confidence"], bins=10, kde=True, ax=ax2)
        st.pyplot(fig2)
    else:
        st.write("No data available.")
else:
    st.header("🛠 Detect Defects in Products")
    category = st.selectbox("Select Product Category:", list(model_paths.keys()))
    model_path = model_paths[category]
    class_names = category_classes[category]

    model = YOLO(model_path)

    st.subheader("Upload Image or Video")
    media_file = st.file_uploader("Choose a file (image or video)", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

    selected_class = st.selectbox("Select a defect to detect (leave blank to detect all):",
                                  ["Detect All"] + class_names)

    if media_file and st.button("🔍 Run Defect Detection"):
        file_bytes = media_file.read()
        file_type = media_file.type

        if "image" in file_type:
            image = Image.open(io.BytesIO(file_bytes))
            image_np = np.array(image)
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            results = model.predict(source=image_bgr, conf=confidence_threshold, verbose=False)

            for result in results:
                img_with_predictions = result.plot()
                img_rgb = cv2.cvtColor(img_with_predictions, cv2.COLOR_BGR2RGB)
                st.image(img_rgb, caption="Detection Result", use_column_width=True)
                pil_image = Image.fromarray(img_rgb)

                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    class_index = int(box.cls[0])
                    class_label = class_names[class_index]

                    if selected_class == "Detect All" or class_label == selected_class:
                        st.write(f"- **Class:** `{class_label}` | **Confidence:** `{conf:.2f}` | 📍 Location: ({x1}, {y1}) → ({x2}, {y2})")
                        if class_label in defective_classes:
                            st.error("⚠️ Defective Product Detected!")
                        else:
                            st.success("✅ Product Looks Good")
                        log_detection(category, class_label, conf)

        elif "video" in file_type:
            video_path = os.path.join(SAVE_DIR, media_file.name)
            with open(video_path, 'wb') as f:
                f.write(file_bytes)

            cap = cv2.VideoCapture(video_path)
            stframe = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                results = model.predict(source=frame, conf=confidence_threshold, verbose=False)
                for result in results:
                    frame = result.plot()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stframe.image(frame_rgb, channels="RGB")
            cap.release()
