import cv2
import time
import pymsgbox
slouch = False
count = 0
session_end = False
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

time.sleep(0.1)
t_last = time.time()
class Posture():
    def __init__(self, cap):
        self.video_capture = cap
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def startPost(self):
        while True:
            ret, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # use appropriate flag based on version of OpenCV
            if int(cv2.__version__.split('.')[0]) >= 3:
                cv_flag = cv2.CASCADE_SCALE_IMAGE
            else:
                cv_flag = cv2.cv.CV_HAAR_SCALE_IMAGE

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv_flag
            )
            # for each face, draw a green rectangle around it and append to the image
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                if y > 250:
                    print('slouch')
                    global slouch
                    slouch = True
                else:
                    slouch = False
                    print("No slouching detected")
            global t_last
            if slouch == True and time.time() - t_last > 10:
                global count
                cv2.imwrite("frame%d.jpg" % count, frame)
                count = count + 1
                pymsgbox.alert('Stop Slouching!', 'PostureFix')
                t_last = time.time()

            # display the resulting image
            cv2.imshow('PostureFix', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.5)

    def stopPost(self):
        global session_end;
        session_end = True

if __name__ == '__main__':
    Posture.startPost(self= None)