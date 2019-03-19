from django.db import models
import cv2
from os import listdir
from os.path import isfile, join
import threading

class Recorder(threading.Thread):
    __NULL_FRAME_EXCEPTION = Exception('Video frame null')
    
    def __init__(self):
      threading.Thread.__init__(self)
      self.__cap = cv2.VideoCapture(0)
      self.__current_frame = None
      self.__reading = True
      self.__recording = False
      self.__fourcc = cv2.VideoWriter_fourcc(*'X264')
      self.__outs = {}
      
    def run(self):
        while(self.__reading):
            if not self.__cap.isOpened():
                self.__cap.open(0)
            success, self.__current_frame = self.__cap.read()
            if success:
                for k in self.__outs:
                    self.__outs[k].write(self.__current_frame)
                
    def __del__(self):
        print("Releasing webcam")
        self.__cap.release()

    def getFrame(self):
        if self.__current_frame is None:
            raise Recorder.__NULL_FRAME_EXCEPTION
        else:
            ret, jpeg = cv2.imencode('.jpg', self.__current_frame)
            return jpeg.tobytes()

    def startRecording(self, name):
        if self.__current_frame is None:
            raise Recorder.__NULL_FRAME_EXCEPTION
        else:
            h, w, _ = self.__current_frame.shape
            self.__outs[name] = cv2.VideoWriter(name, self.__fourcc, 30, (w, h), True)

    def stopRecording(self, name):
        del self.__outs[name]
                 
    def stopReading(self):
        self.__reading = False
        
class Video(models.Model):
    PUBLIC_PATH="couch/videos/"
    VIDEOS_PATH="trainer/static/" + PUBLIC_PATH
    
    abstract = True
    __instance = 0
    __recorder = None

    def __init__(self, name=""):
        self.__video_name = name
        self.__using_recorder = not isfile(self.local_path)
            
        if self.__using_recorder:
            if Video.__instance == 0:
                Video.__recorder = Recorder()
                Video.__recorder.start()
            Video.__instance += 1
            if name != "":
                Video.__recorder.startRecording(self.local_path)

    def __del__(self):
        print("Destroing video")
        if self.__using_recorder:
            Video.__instance -= 1
            if Video.__instance == 0:
                print("Stoping recorder")
                Video.__recorder.stopReading()
                Video.__recorder.join()
                print("Recorder stoped")
                Video.__recorder = None

    @property
    def public_path(self):
        return Video.PUBLIC_PATH + self.__video_name

    @property
    def local_path(self):
        return Video.VIDEOS_PATH + self.__video_name

    @staticmethod
    def all():
        return [Video(f) for f in listdir(Video.VIDEOS_PATH) if isfile(join(Video.VIDEOS_PATH, f))]
        
    def get_frame(self):
        return Video.__recorder.getFrame()
