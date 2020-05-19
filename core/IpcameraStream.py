import cv2
import threading


class IpcameraStream:
    def __init__(self, uri):
        self.stream = cv2.VideoCapture(0)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if self.stream is None or not self.stream.isOpened():
            raise Exception("Can not open Camera")
        self.stopped = False
        self.t = None
        self.uri = uri
        self.output_frame = None

    def start(self):
        self.t = threading.Thread(target=self.update, args=())
        self.t.daemon = True
        self.t.start()
        return self

    def update(self):
        _count_restart = 0
        while not self.stopped:
            if not self.stream.isOpened():
                continue
            (grabbed, frame) = self.stream.read()

            if not grabbed:
                _count_restart += 1
                if _count_restart % 5 == 0:
                    self.__restart_stream()
                continue

            self.output_frame = frame.copy()
            _count_restart = 0

    def read(self):
        return self.output_frame

    def stop(self):
        self.stopped = True
        if self.t is not None:
            self.t.join()
        self.stream.release()

    def __restart_stream(self):
        self.stream.release()
        self.stream = cv2.VideoCapture(self.uri)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if self.stream is None or not self.stream.isOpened():
            raise Exception("Can not open Camera")
