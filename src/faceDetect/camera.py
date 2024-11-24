from picamera2 import Picamera2, Preview
from camsetup import settingup
from time import sleep
import re
from deepface import DeepFace
from person import Person

#TODO: test all functions

def testActivate(picam2):
    """
    activate to test camera

    assumes that picam2 has already been instantiated and configured 
    """

    try:
        picam2.start_preview(Preview.QTGL)
    except:
        picam2.start_preview(True)
    picam2.start()

    print("camera has activated")
    sleep(2)
    picam2.capture_file(f"images/test.jpg")
    picam2.stop_preview()



def addFace(name, picam2):
    """
    add a user's face to the database

    assumes that picam2 has already been instantiated and configured
    """
    picam2.start_preview(Preview.QTGL)
    picam2.start()

    print("you have 5 seconds to align your head with the middle of the screen")
    sleep(5)

    name = input("what is the name: ")

    person = Person(name)

    imgID = person.getImgID()

    picam2.capture_file(f"images/db/{imgID}.jpg")
    picam2.stop_preview()
    picam2.stop()

    print(f"{name} is now saved locally on file")



def activate(picam2):
    """
    capture with camera

    assumes that picam2 has already been instantiated and configured
    """

    try:
        picam2.start_preview(Preview.QTGL)
    except:
        picam2.start_preview(True)

    picam2.start()
    print("camera has activated, you have 5 seconds to align")
    sleep(5)

    #deepface will later parse images/db to find image
    picam2.capture_file(f"images/mystery_person.jpg")
    picam2.stop_preview() 



def detectFace(picam2):
    """
    Takes picture using activate() function by itself and
    uses DeepFace VGG network to identify face

    assumes that picam2 has already been instantiated and configured
    """
    
    #take picture
    activate(picam2)

    #compare photo with db folder
    result = DeepFace.find(
    img_path = "images/mystery_person.jpg",
    db_path = "images/db",
    )

    if result[0].size > 0 and result[0].iloc[0].threshold >= .5:
        regex = r'user\d{2}'#get only the name of the image

        user = re.findall(regex, result[0].iloc[0].identity)
        print(user)





if __name__ == "__main__":
    pass