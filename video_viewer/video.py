"""Video display component using opencv.

https://stackoverflow.com/a/67856716

Author: Romain Fayat, January 2022
"""
import cv2
import numpy as np


class VideoCamera(cv2.VideoCapture):
    "Handle video reading with opencv and conversion to bytes."

    def get_frame(self):
        "Grab the next frame from the video and return it as as bytes."
        _, image = self.read()
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class RandomImageGenerator(VideoCamera):
    "Simulate a video reader returning random frames."

    def __init__(self, width=255, height=255):
        "Create the object and store the wished resolution as attributes."
        self.width = width
        self.height = height

    def read(self):
        "Simulate an opencv video capture reading data from a video."
        image = np.random.random((self.height, self.width, 3)) * 255
        return True, image.astype(np.uint8)
