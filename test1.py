'''from ultralytics import YOLO
import cv2
import os

# Load the trained model
model = YOLO("best (4).pt")

# Choose source: set to image or video path
source_type = "video"  # or "image"
source_path = "C:/Users/KAVYA/OneDrive/Videos/Screen Recordings/Screen Recording 2025-04-02 112143.mp4"  # change path for video

if source_type == "image":
    results = model.predict(source=source_path, conf=0.4)
    for result in results:
        img = result.plot()
        resized_img = cv2.resize(img, (800, 600))
        cv2.imshow("Image Detection", resized_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

elif source_type == "video":
    cap = cv2.VideoCapture(source_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(source=frame, conf=0.4, verbose=False)
        for result in results:
            frame = result.plot()
        cv2.imshow("Video Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
'''
'''
from ultralytics import YOLO
import cv2
import torch
from torchmetrics.detection.mean_ap import MeanAveragePrecision
import os

# Select model based on need
model_path = "best (4).pt"  # Update to "best (2).pt" if needed
model = YOLO(model_path)

# Choose source type and file path
source_type = "image"  # "image" or "video"
source_path = "C:/Users/KAVYA/OneDrive/Desktop/BATCH3/bottle5.png"  # Or video path

if source_type == "image":
    results = model.predict(source=source_path, conf=0.4)
    metric = MeanAveragePrecision()

    # Modify based on actual ground truth data
    ground_truth_boxes = [{
        "boxes": torch.tensor([[50, 50, 200, 200], [30, 30, 150, 150]]),
        "labels": torch.tensor([1, 2])
    }]

    predictions = []
    for result in results:
        img = result.plot()
        resized_img = cv2.resize(img, (800, 600))
        cv2.imshow("Image Detection", resized_img)

        pred_boxes, pred_labels, pred_scores = [], [], []
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            pred_boxes.append([x1, y1, x2, y2])
            pred_labels.append(cls)
            pred_scores.append(conf)

        predictions.append({
            "boxes": torch.tensor(pred_boxes),
            "scores": torch.tensor(pred_scores),
            "labels": torch.tensor(pred_labels),
        })

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

    # Evaluation
    metric.update(predictions, ground_truth_boxes)
    metrics = metric.compute()
    print("📊 Evaluation Metrics:")
    print(f"Precision (mAP@50): {metrics['map_50']:.4f}")
    print(f"Recall (mAP@50-95): {metrics['map_50:95']:.4f}")
    f1 = 2 * (metrics['map_50'] * metrics['map_50:95']) / (metrics['map_50'] + metrics['map_50:95'] + 1e-7)
    print(f"F1-score: {f1:.4f}")

elif source_type == "video":
    cap = cv2.VideoCapture(source_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(source=frame, conf=0.4, verbose=False)
        for result in results:
            frame = result.plot()
        cv2.imshow("Video Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    '''
from ultralytics import YOLO
import cv2
import os

# Load YOLOv8 model
model_path = "best (4).pt"  # Update with correct model file if needed
model = YOLO(model_path)

# Choose input type and path
source_type = "video"  # "image" or "video"
source_path = "C:/Users/KAVYA/OneDrive/Videos/Screen Recordings/Recording 2025-05-06 -1.mp4"  # Or video path

if source_type == "image":
    results = model.predict(source=source_path, camonf=0.4)

    for result in results:
        img = result.plot()
        resized_img = cv2.resize(img, (800, 600))
        cv2.imshow("Image Detection", resized_img)

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

elif source_type == "video":
    cap = cv2.VideoCapture(source_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=0.4, verbose=False)
        for result in results:
            frame = result.plot()

        cv2.imshow("Video Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

