# 2/22/2025

import time
import serial
import picamera2

recording = False
cam = picamera2.PiCamera()

if not recording:
    cam.start_recording('test_recording.h264')
    recording = True
    print("start")

    time.sleep(6) # will be replaced with event of xbee stop in real code
else:
    cam.stop_recording()
    recording = False
    print("stop")