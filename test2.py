from picamera2 import Picamera2, Preview
import time
picam2 = Picamera2()
picam2.start_preview(Preview.QT)
picam2.start()
time.sleep(10)
