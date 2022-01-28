"""Video display component using opencv.

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

    @property
    def frame_count(self):
        "Return the number of frames in the video."
        return int(self.get(cv2.CAP_PROP_FRAME_COUNT))


class SynchedVideoCamera(VideoCamera):
    "Allow frame grabing from a hashing table for synchronization purposes."

    def __init__(self, *args, synchro=None, **kwargs):
        "Create  the object, adding the synchronization as a dictionary."
        super().__init__(*args, **kwargs)
        if synchro is None:
            self.synchro = {i: i for i in range(self.frame_count)}
        else:
            self.synchro = synchro

    def get_frame_from_synchro(self, synchro_value=None):
        "Grab the frame number from the synchro and returns it as bytes."
        frame_number = self.synchro.get(synchro_value, None)
        return self.get_frame(frame_number)
