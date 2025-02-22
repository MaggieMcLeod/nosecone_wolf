# works as of 2/22/2025
# opens preview window for picam

from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()
picam2.start_preview(Preview.QT)