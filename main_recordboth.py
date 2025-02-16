### records picam, then usbcam, but not concurrently

import cv2
from datetime import datetime
import os
import shutil
from picamzero import Camera
from time import sleep

# picamera
cam = Camera()
print("recording picam")
cam.record_video('./test3.mp4', duration=5)

# usb camera

# Attempt to use the V4L2 backend explicitly
cap = cv2.VideoCapture(1, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: Could not open camera with CAP_V4L2.")
    exit()

# Set a lower resolution to reduce memory usage
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# configure timestamp for filename
current_datetime = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
print("Current date & time : ", current_datetime)
str_current_datetime = str(current_datetime)
 
# create a file object along with extension
file_name = str_current_datetime+".avi"

# Define the codec (try MJPG if XVID still causes issues)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(file_name, fourcc, 20.0, (640, 480))

print("Recording usb... Press 'q' to stop.")

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

# Move video file to USB_videos folder
### NOTE while the file naming timestamps work, moving to the video folder
# is not working. Fix this later.
source = '/home/pi/'+file_name
destination = '/home/pi/USB_videos'
 
src_path = os.path.join(source, f)
dst_path = os.path.join(destination, f)
shutil.move(src_path, dst_path)

# Clean up
cap.release()
out.release()
cv2.destroyAllWindows()
