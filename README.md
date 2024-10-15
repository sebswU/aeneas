# Aeneas
Room Security System


# What you'll need (physical)
* two raspberry pis (used here is 3B and 5)
* arduino uno 
* tello drone
* Components
  * depth sensor
  * pi camera
  * motion sensor
  * (optional) led strip


# What you'll need (digital)
* VSCode
* UNIX commands
* AWS Services (Mainly S3)
* SSH/SCP Protocol
* VSCode SSH extension
* Python Libraries (Not final):
  * OpenCV
  * OpenSfM
  * gpiozero (Comes with Raspbian standard)
  * boto3
  * tello


# Orientation
One raspberry pi will be right by the door. The other can be anywhere around the room.
(I really just set it up like this because the only ethernet port in the dorm room was by the door and I couldn't figure out the wifi configuration when I was setting up the first RPi.)
The RPi by the door will be connected to the motion detector/camera and the other will be 
connected to stimuli and image display peripherals like led strips, drone, an arduino
microcontroller, and an LCD monitor. The LED strips will wrap around the edges of either 
the ceiling or one of the walls.
Both RPis will be connected via VPC to Amazon AWS S3 buckets.
  

# The five stages of grief
* face detection
* stimulus
* drone image capture
* microservice communication
* display culprit


# Face Detection
The motion detector and the rpi camera will consist of the face detection module-stage.

Common libraries used would be OpenCV and gpiozero.

The RPi by the door will connect to a motion detector that scans for the opening of the door. 
it then uses a classical computer vision algo (like eigenfaces) to detect whether the face in 
the camera input is either me, my roommate, or my friend that lives across from my room.
There are three outcomes from this module:
* The face is detected to be either one of the three chosen ones
* The face is not detected to be either one of the three chosen ones and there
is a 15 second limbo in which I have to enter in a password to validate the visitor.
* Either the 15 second limbo is over or the person did not turn to look at the camera.


# Stimulus
The LED strips and the tweeter will consist of the stimulus module-stage. 

The most common library associated with this module-stage is gpiozero.

The RPi will be connected to an Arduino Uno arm that will handle more accurate signals 
to the physical peripherals.
The respective stimuli for the previous 3 outcomes are as follows:
* The LED light flashes green for about 5 seconds and nothing happens.
* The LED Light flashes yellow for 15 seconds. The tweeter will emit an exclamation.
* The LED light stays red for 2 seconds and then turns white so that the drone can capture
the culprit in better lighting conditions. The tweeter will repeatedly emit the exclamation.


# Drone
The tello drone consists of the drone module-stage.

The most common library associated with this module-stage is tello.py and gpiozero.

For the third outcome, the drone will activate and attempt to follow the culprit to at least 
the door (and maybe down the hallway, but that seems too advanced). It will take multiple 
pictures when it detects any face (using haar cascades).


# Microservice Communication
There are no physical modules associated with this section.

The most common libraries associated with this module-stage are boto3 and gpiozero.

There will be a private DNS connection over VPC for transferring images and metadata 
about the image to S3 and probably DynamoDB as well. (I haven't decided whether I will
use gateway or interface endpoint connection.) The images of the culprit from 
the drone will be the traffic. It will only be sent on there if the third outcome is true.




