from operator import truediv
import pyautogui
import os
import shutil
import pyscreeze


import logging
import threading
from threading import Event, Thread
import time

#py -m pip install pyautogui
#py -m pip install pillow   
#py -m pip install opencv-python
class KalifastAuto :
    
    #Actions constants
    ACTION_MOVE_TO = 1
    ACTION_CLICK = 2
    ACTION_DOUBLE_CLICK = 3
    ACTION_RIGHT_CLICK = 4
    ACTION_COPY_AREA = 5

    def __init__(self):
        self.listeningImage = False;

        self.thread_stop = False;
        self.listenerThread = threading.Thread(target=self.threadFunction, args=("listeners",))
        self.listenerThread.start()

        self.eventOnVisible = Event()
        self.eventOnInvisible = Event()

        self.path_image = False


    def setListeningImage(self, path_image) :
        if os.path.exists(path_image) :
            self.path_image = path_image
            self.listeningImage = pyautogui.locateOnScreen(self.path_image, confidence=0.9)
        else :
            print("Error : image not found !")
            self.listeningImage = False

    def getLocation(self) :
        if self.listeningImage != False :
            return self.listeningImage
        else :
            print("Error : Location not found !")
            return False

    def isVisible(self) :
        if self.listeningImage != False :
            if isinstance(self.listeningImage, pyscreeze.Box) :
                return True
            else :
                return False
        else :
            print("Error : Image not found !")
            return False


    def threadFunction(self, threadName) :
        while self.thread_stop == False :
            if(self.listeningImage != False) :
                

                if self.isVisible() == True :
                    #print("v")
                    self.eventOnVisible.set()
                else :
                    #print("i")
                    self.eventOnInvisible.set()

               


                try :
                    self.listeningImage = pyautogui.locateOnScreen(self.path_image, confidence=0.9)
                except OSError as err:
                    self.listeningImage = False
                #print (self.getLocation())



    def mouseIsInImage(self ) :
        mP = pyautogui.position()
        iP = self.getLocation()

        if(self.isVisible()) :
            if mP.x >= iP.left and mP.x <= iP.left + iP.width and mP.y >= iP.top and mP.y <= iP.top+iP.height :
                return True
                
        return False 
                

    def waitVisible(self) :
       self.eventOnVisible.wait()
       
    def waitInvisible(self) :
        self.eventOnInvisible.wait()


    def clearKalifastAuto(self) :
        self.thread_stop = True


    def setClickListener(self, functionn) :
        print()

    def setDoubleClickListener(self, functionn) :
        print()

    def setMouseEnterListener(self, functionn) :
        print()

    def setMouseOutListener(self, functionn) :
        print()


    def setMouseMovedListener(self, function) :
        print()


    def doMouseAction(self, action) :
        if self.isVisible() :

            if action == self.ACTION_MOVE_TO :
                pyautogui.moveTo(self.listeningImage)
                
            if action == self.ACTION_CLICK :
                pyautogui.click(self.listeningImage, button='left')
            
            if action == self.ACTION_DOUBLE_CLICK :
                pyautogui.doubleClick(self.listeningImage, button='left')

            if action == self.ACTION_RIGHT_CLICK :
                pyautogui.click(self.listeningImage, button='right')

            if action == self.ACTION_COPY_AREA : 
                pyautogui.click(self.listeningImage)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.hotkey('ctrl', 'c')

        else :
            print("Error : image not visible")