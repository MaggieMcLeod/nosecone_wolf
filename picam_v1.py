# 02/22/2025 - using Python 3.9.2
# testing with picamera instead of picamzero

import time
import serial
import picamera2

recording = False
cam = picamera.PiCamera()

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

while 1:
	x=ser.readline()
	if x != b'':
		if (b"start" in x) and (not recording):
			cam.start_recording('recording.h264')
			#TODO stick in timestamp to "recording.h264"
			recording = True
			print("start")
		elif (b"stop" in x) and (recording):
			cam.stop_recording()
			recording = False
			print("stop")
	#ser.write(str.encode("~\x00}1\x90\x00}3\xa2\x00BI\x0bg\x00\x00\x02recording\x8d"))
	#time.sleep(3)
	#print("sent")
