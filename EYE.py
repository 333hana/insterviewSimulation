"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

from datetime import timedelta
import math
import time
import datetime
import numpy as np
from unittest.main import main
from numpy import size
import cv2
import dlib
from scipy.spatial import distance as dist
import eye_detection
from gaze_tracking import GazeTracking
import stopwatch
import keyboard

stop_eye = False
res ={}
class EYE():
    def __init__(self,cap):
    # to detect the facial region
     self.detector = dlib.get_frontal_face_detector()
     self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
     self.RIGHT_EYE_POINTS = list(range(36, 42))
     self.LEFT_EYE_POINTS = list(range(42, 48))
     self.EYE_AR_THRESH = 0.22
     self.EYE_AR_CONSEC_FRAMES = 2
     self.COUNTER = 0
     self.TOTAL = 0
     self.gaze = GazeTracking()
     #webcam = cv2.VideoCapture(0)
     self.timer=stopwatch.MyTimer()
     self.timer.start()
     self.session_start=time.time()
     self.time_puse= time.time() - self.session_start
     self.cap = cap


    def gaze_blinking_function(self):
     #global stop_eye  
     #stop_eye = False
     while not(stop_eye):
    # We get a new frame from the webcam
      ret = False
      while(not(ret)):
          ret,self.frame = self.cap.read()
      print("out")
   
    # We send this frame to GazeTracking to analyze it
      self.gaze.refresh(self.frame)

      self.frame = self.gaze.annotated_frame()
      text = "" 
       # convert the frame to grayscale
      gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
      rects = self.detector(gray, 0) 
      for rect in rects:
        # get the facial landmarks
        landmarks = np.matrix([[p.x, p.y] for p in self.predictor(self.frame, rect).parts()])
            # get the left eye landmarks
        left_eye = landmarks[self.LEFT_EYE_POINTS]
            # get the right eye landmarks
        right_eye = landmarks[self.RIGHT_EYE_POINTS]
            # compute the EAR for the left eye
        ear_left = eye_detection.eye_aspect_ratio(left_eye)
            # compute the EAR for the right eye
        ear_right = eye_detection.eye_aspect_ratio(right_eye)
            # compute the average EAR
        ear_avg = (ear_left + ear_right) / 2.0
            # detect the eye blink
        if ear_avg < self.EYE_AR_THRESH:
                self.COUNTER += 1
        else:
                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                    self.TOTAL += 1
                    print("Eye blinked")
                self.COUNTER = 0 
        
      if self.gaze.is_right():
         text = "Looking right"#pused
         #print("time pused")
         #print(timer.pause()) 
              
        
      elif self.gaze.is_left():
         text = "Looking left"#pused
         #print("time pused")
         #print(timer.pause())
 
        
         
      elif self.gaze.is_center():
         text = "Looking center"#running
         self.timer.resume()
         self.time_puse= time.time() - self.time_puse   
      if keyboard.is_pressed ("esc")  :
          self.images_eye()
          break   
     
     #cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)  
       #cv2.imshow("Demo", frame)
    def images_eye(self):
     # if cv2.waitKey(1) == 27:
      global res
      session_time=time.time()-self.session_start    
      eye_contact= ((self.time_puse)/(session_time))
      eye_contact=(1-eye_contact)*100

      res['eye contact']=eye_contact
      res['blinks']=self.TOTAL
      res['session time']=session_time

      
      print("session time= "+ str((session_time))+" sec")
      print("time puse ="+ str((self.time_puse))+" sec")            
      print("eye contact ="+str(math.floor(eye_contact) )+" %" )       
      print("Total blinks =  "+str(self.TOTAL))

     


         #break
    #webcam.release()
    # cv2.destroyAllWindows()

    def stop(self):
        print("ineyestop")
        global stop_eye;
        stop_eye = True
        self.images_eye();
 

if __name__== "__main__":
    e = EYE(cv2.VideoCapture(0))
    #e.stop()
    e.gaze_blinking_function()
    


