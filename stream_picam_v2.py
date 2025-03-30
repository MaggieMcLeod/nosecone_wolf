from picamera2 import Picamera2, Preview
from libcamera import Transform

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, x=0, y=0, width=720, height=480)
                     # default values: x=100, y=200, width=800, height=600
transform=Transform(hflip=1)
picam2.start()

while True:
    pass