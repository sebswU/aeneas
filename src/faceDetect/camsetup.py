import picamera2
from picamera2 import Picamera2, Preview
import time
from time import sleep

def settingup():
	"""sets up the camera, do this before running any other apps"""
	picam2 = Picamera2()
	camera_config = picam2.create_preview_configuration()
	picam2.configure(camera_config)
	picam2.start_preview(Preview.QTGL)
	picam2.start()
	print("say cheese!")
	time.sleep(2)
	picam2.capture_file(f"images/startuptest.jpg")


if __name__=="__main__":
	settingup()
