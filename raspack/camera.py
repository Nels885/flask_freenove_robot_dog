import cv2 as cv
import pytesseract
from pytesseract import Output
from picamera2 import Picamera2


class VideoCamera:

    def __init__(self, img_type=".jpg"):
        self.picam = Picamera2()
        self.picam.start()
        self.img_type = img_type

    def __del__(self):
        self.picam.stop()

    def get_frame(self):
        frame = self.picam.capture_array()
        frame = cv.resize(frame, (800, 448))
        ret, img = cv.imencode(self.img_type, frame)
        if ret:
            return img.tobytes()
        return None

    def get_recognize_text(self):
        frame = self.picam.capture_array()
        frame = cv.resize(frame, (800, 448))
        d = pytesseract.image_to_data(frame, output_type=Output.DICT)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # don't show empty text
                if text and text.strip() != "":
                    frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    frame = cv.putText(frame, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
        ret, img = cv.imencode(self.img_type, frame)
        if ret:
            return img.tobytes()
        return None


pi_camera = VideoCamera()
