# same as main_V1, but uses picamera instead of picamzero

### UNTESTED CODE ###
### records video with USB camera and PI camera simultaneously

import cv2
import picamera2
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
        self.cam = picamera.PiCamera() # picamera setup

    def record(self):
      self.cam.start_recording('my_video.h264')
      #TODO put in timestamps
      # old from picamzero:  self.cam.record_video(f"./", duration=120)

    def preview(self):
        self.cam.start_preview() #TODO change?


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

    while True:
        x = ser.readline()
        if x != b'':
            if (b"start" in x) and (not recording):
                recording = True

            elif (b"stop" in x) and (recording):
                recording = False
                usb.stop()
                piStarted = False
                # does picamera stop?


        if recording:
            usb.record_frame()
            if not piStarted:
                pi.record()
                piStarted = True