### WORKS AS OF 2/9/2025
### opens a preview window for rpi cam
### while connected to the raspberry pi
### note - previously installed picamzero module

from picamzero import Camera
from time import sleep

cam = Camera()
cam.start_preview()
# Keep the preview window open for 5 seconds
sleep(5)