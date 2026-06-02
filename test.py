from ultralytics import YOLO
import cv2

# Load the trained model
model = YOLO("best (3).pt")

# Perform predictions on test images
results = model.predict(source="C:/Users/KAVYA/OneDrive/Desktop/BATCH3/p1.png", conf=0.25)

# Display results
for result in results:
    # Assuming results contain image-level data to visualize
    img = result.plot()  # Plot the results on the image

    # Resize the output image for display
    scale_percent = 50  # Adjust this percentage to scale the image
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    # Show the resized image
    cv2.imshow("YOLO Predictions", resized_img)

    # Wait for the 'q' key to be pressed
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()