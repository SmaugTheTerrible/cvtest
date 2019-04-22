import cv2
import numpy
import pyautogui
import threading


def match(template, source=None, method=cv2.TM_CCOEFF_NORMED, threshold=0.95):
    if (source is None):
        source = screenshot()

    res = cv2.matchTemplate(source, template, method)
    loc = numpy.where(res >= threshold)
    return zip(*loc[::-1])


def screenshot():
    img = pyautogui.screenshot()
    return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)


def region(topLeftX, topLeftY, width, height):
    img = pyautogui.screenshot(region=(topLeftX, topLeftY, width, height))
    return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)


def fromFile(path):
    res = cv2.imread(path)
    if res is None:
        raise Exception("Cant read image from file")
    return res


def waitUntil(img,  timeout=20):
    worker = MatchWorker(img)
    worker.start()
    worker.join(timeout)
    return worker.result


def waitWhile(img, timeout=20):
    worker = MatchWorker(img, True)
    worker.start()
    worker.join(timeout)
    return worker.result


def isOnScreen(template):
    res = match(template)
    return len(res)>0


def centers(template):
    h,w,_ = template.shape
    locs = match(template)
    for loc in locs:
        x, y = loc
        loc = x+w/2, y+h/2
    return locs


def click(x, y, clicks=1):
    pyautogui.click(x,y, clicks=clicks)


class MatchWorker(threading.Thread):
    def __init__(self, template, invert=False):
        super(MatchWorker, self).__init__()
        self.template = template
        self.result = None
        self.invert = invert
    
    def run(self):
        self.result = self.matchLoop(self.template, self.invert)

    def matchLoop(self, template, invert):
        while(True):
            res = match(template)
            hasResult = len(res)>0
            condition = invert != hasResult   # xor
            if (condition): 
                break
        
        return res


class Storage():
    def __init__(self, values={}):
        self._internal = values
    

    def __getitem__(self, key):
        return self._internal[key]


    def __setitem__(self, key, value):
        self._internal[key] = value
