# code for pdf

### UNTESTED CODE ###
### records video with USB camera and PI camera simultaneously, and shows picam preview window

import cv2
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import serial
from libcamera import Transform
import threading

class USB_camera_control:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('frr.avi', self.fourcc, 10.0, (640, 480))

    def stop(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

class PI_camera_control:
    def __init__(self):
        self.cam = Picamera2() # picamera setup
        self.video_config = self.cam.create_video_configuration()
        self.cam.configure(self.video_config)
        self.encoder = H264Encoder(bitrate=10000000)
        self.output = "pdf_post.h264"

    def record(self):
      self.cam.start_recording(self.encoder, self.output)
      #TODO put in timestamps
      # old from picamzero:  self.cam.record_video(f"./", duration=120)

    def preview(self):

      self.cam.configure(self.cam.create_preview_configuration(main={"size": (320, 240)}))
      self.cam.start_preview(Preview.QTGL, x=0, y=0, width=720, height=480)
                          # default values: x=100, y=200, width=800, height=600
      transform=Transform(hflip=1)
      self.cam.start()

def usb_test(usb):
    x = 0
    while True:
        x += 1
        ret, frame = usb.cap.read()
        print("frame" + str(x))
        if not ret:
            print("failed")
        usb.out.write(frame)

def main():
    usb = USB_camera_control()
    pi = PI_camera_control()
    recording = False
    piStarted = False

    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    pi.preview()
    x = b'start'
    while True:
        #x = ser.readline()
        if x != b'':
            #print(x)
            if (b"start" in x) and (not recording):
                recording = True
                print("recording")
                if not piStarted:
                    pi.record()
                    piStarted = True
                    x = threading.Thread(target=usb_test, args=(usb,), daemon = True)
                    x.start()

            elif (b"stop" in x) and (recording):
                recording = False
 #               usb.stop()
                piStarted = False
                print("recording stopped")
                # does picamera stop?
            x = b''
            # # Display the frame
            #
            

main()
