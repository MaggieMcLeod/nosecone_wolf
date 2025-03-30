### UNTESTED CODE ###
### records video with USB camera and PI camera simultaneously

import cv2
from picamera import PiCamera
import serial

class USB_camera_control:
    def __init__(self):
        self.cap = cv2.VideoCapture(1, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('output.avi', self.fourcc, 20.0, (640, 480))

    def record_frame(self):
        _, frame = self.cap.read()

        self.out.write(frame)

        # # Display the frame
        # cv2.imshow('Recording', frame)

    def stop(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

class PI_camera_control:
    def __init__(self):
        self.cam = Camera()

    def record(self):
        self.cam.record_video(f"./", duration=120)

    def preview(self):
        self.cam.start_preview()


def main():
#    usb = USB_camera_control()
#    pi = PI_camera_control()
#    recording = False
#    piStarted = False

    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    #pi.preview()
    print("listening")
    while True:
        x = ser.readline()
        if x != b'':
            print(x)

main()

    
    
