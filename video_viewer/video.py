"""Video display component using opencv.

https://stackoverflow.com/a/67856716

Author: Romain Fayat, January 2022
"""
import cv2


class VideoCamera(cv2.VideoCapture):
    "Handle video reading with opencv and conversion to bytes."

    def get_frame(self, frame_number=None):
        "Grab the next frame from the video and return it as as bytes."
        _, image = self.read(frame_number)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def read(self, frame_number=None):
        "Read a specific frame if provided, else read the next one."
        if frame_number is not None:
            self.go_to_frame(frame_number)
        return super().read()

    def go_to_frame(self, frame_number):
        "Set a frame number to be the next one that will be read."
        if self.current_frame != frame_number:
            return super().set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        else:
            return True

    @property
    def current_frame(self):
        "Return the current frame number."
        return super().get(cv2.CAP_PROP_POS_FRAMES)
