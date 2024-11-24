import os
import sys

userNum = 0

class Person():
    """
    This class is a convenient way to organize how users 
    are identified in the aeneas system. 

    Aeneas is designed to recognize up to 100 people
    Deepface parses the images/db folder to find the image 
    that best matches the captured photo. The name of the 
    jpg file that best correlates is then verified with the 
    imgID attribute.
    """
    def __init__(self, name):
        if userNum < 9:
            self.imgID = 'user0' + userNum
        else:
            self.imgID = 'user' + userNum

        self.name = name

    def getName(self):
        return self.name
    
    def getImgID(self):
        return self.imgID

    