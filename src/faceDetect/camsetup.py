import picamera2
from picamera2 import Picamera2, Preview
import time
from time import sleep

def settingup():
	"""sets up the camera, do this before running any other apps"""
	picam2 = Picamera2()
	try:
		picam2.start_preview(Preview.QTGL)
		picam2.start()
	except: # QT instead of QTGL allows x-forwarding over ssh/VNC
		picam2.start_preview(Preview.QT)
		picam2.start()
	camera_config = picam2.create_preview_configuration()
	picam2.configure(camera_config)
	print("say cheese!")
	time.sleep(2)
	picam2.capture_file(f"images/startuptest.jpg")
	picam2.stop_preview()
	picam2.stop()

if __name__=="__main__":
	settingup()
