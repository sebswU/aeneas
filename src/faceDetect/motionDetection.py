import gpiozero
from gpiozero import MotionSensor, LED
from time import sleep
from camera import activate
"""
GPIO: 
8 -> red LED
25 -> white LED
17 -> MotionSensor
"""

pir = MotionSensor(17)
red = LED(8)
white = LED(25)

print("waiting for no motion")
#pir.wait_for_no_motion()

while True:
    white.off()
    red.on()
    print("waiting for motion")
    pir.wait_for_motion()
    print("motion detected")
    activate()
    red.off()
    white.on()
    sleep(2)
    
    
