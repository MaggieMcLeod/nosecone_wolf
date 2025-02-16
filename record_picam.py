### WORKS AS OF 2/16/2025
### opens a preview window for rpi cam
### while connected to the raspberry pi
### note - previously installed picamzero module

from picamzero import Camera
from time import sleep
#from datetime import datetime

# TODO timestamp filenames don't work

# # configure timestamp for filename
# current_datetime = datetime.now().strftime("/%Y-%m-%d, %H:%M:%S")
# print("Current date & time : ", current_datetime)
# str_current_datetime = str(current_datetime)
 
# # create a file object along with extension
# file_name = str_current_datetime+".mp4"

cam = Camera()
cam.record_video('./test3.mp4', duration=5)
# Keep the preview window open for 5 seconds
