from django.db import models
import time
import cv2

class Video(models.Model):
    abstract = True

    def __init__(self, record=False):
        self.video = cv2.VideoCapture(0)
        self.__record = record
        if self.__record:
            self.__output_file = "trainer/static/couch/videos/" + time.strftime("%Y%m%d-%H%M%S") + ".avi"
            self.__fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            self.__is_begin = True

    def __del__(self):
        print("Releasing webcam")
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if image is not None:
            if self.__record:
                if self.__is_begin:
                    h, w, _ = image.shape
                    self.__out = cv2.VideoWriter(self.__output_file, self.__fourcc, 30, (w, h), True)
                    self.__is_begin = False
                self.__out.write(image)
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        else:
            return None
