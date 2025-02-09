### WORKS AS OF 2/9/2025
### records video with usb cam

import cv2

# Attempt to use the V4L2 backend explicitly
cap = cv2.VideoCapture(1, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: Could not open camera with CAP_V4L2.")
    exit()

# Set a lower resolution to reduce memory usage
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define the codec (try MJPG if XVID still causes issues)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

print("Recording... Press 'q' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Write frame to file
    out.write(frame)

    # Display the frame
    cv2.imshow('Recording', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
out.release()
cv2.destroyAllWindows()
