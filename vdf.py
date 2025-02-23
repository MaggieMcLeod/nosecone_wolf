# code for vdf
# no livestreaming, just xbees and recording on both

### UNTESTED CODE ###
### records video with USB camera and PI camera simultaneously

import cv2
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import serial

class USB_camera_control:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('output.avi', self.fourcc, 20.0, (640, 480))

    def stop(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

class PI_camera_control:
    def __init__(self):
        self.cam = Picamera2() # picamera setup

    def record(self):
      video_config = self.cam.create_video_configuration()
      self.cam.configure(video_config)
      encoder = H264Encoder(bitrate=10000000)
      output = "my_video.h264"
      self.cam.start_recording(encoder, output)
      #TODO put in timestamps
      # old from picamzero:  self.cam.record_video(f"./", duration=120)

    #def preview(self):
        #self.cam.start_preview()


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

 #   pi.preview()
    while True:
        x = ser.readline()
        if x != b'':
            print(x)
            if (b"start" in x) and (not recording):
                recording = True
                print("recording")

            elif (b"stop" in x) and (recording):
                recording = False
                usb.stop()
                piStarted = False
                print("recording stopped")
                # does picamera stop?


        if recording:
            #
            ret, frame = usb.cap.read()
            print("frame")
            if not ret:
                print("failed")
            usb.out.write(frame)

            # # Display the frame
            #
            if not piStarted:
                pi.record()
                piStarted = True

main()

