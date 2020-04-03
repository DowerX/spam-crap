import keyboard
import mouse
import yaml
from time import sleep

class Job:
    events = []

    def Parse(self, path):
        data = None
        with open(path, "r") as f:
            data = yaml.load(f.read(), Loader=yaml.CLoader)
        for i in data:
            if i["type"] == "MouseMove":
                e = MouseMoveEvent(i["x"], i["y"], i["relative"], i["time"])
            elif i["type"] == "MouseClick":
                e = MouseClickEvent(i["button"])
            elif i["type"] == "KeyboardType":
                e = KeyboardTypeEvent(i["text"])
            elif i["type"] == "KeyboardKey":
                e = KeyboardKeyEvent(i["button"], i["position"])
            elif i["type"] == "Wait":
                e = WaitEvent(i["time"])
            self.events.append(e)

    def Execute(self):
        for i in self.events:
            i.Execute()

    def Loop(self, x):
        for i in range(x):
            self.Execute()
            
class MouseMoveEvent:
    def __init__(self, x, y, r=False, d=0.2):
        self.x = x
        self.y = y
        self.a = not r
        self.d = d

    def Execute(self):
        mouse.move(self.x, self.y, absolute=self.a, duration=self.d)

class MouseClickEvent:
    def __init__(self, btn):
        self.btn = btn

    def Execute(self):
        mouse.click(self.btn)

class KeyboardTypeEvent:

    def __init__(self, txt):
        self.txt = txt

    def Execute(self):
        keyboard.write(self.txt)

class KeyboardKeyEvent:
    def __init__(self, btn, pos):
        self.btn = btn
        self.pos = pos

    def Execute(self):
        if self.pos:
            keyboard.press(self.btn)
        else:
            keyboard.release(self.btn)

class WaitEvent:
    def __init__(self, t):
        self.t = t

    def Execute(self):
        sleep(self.t)