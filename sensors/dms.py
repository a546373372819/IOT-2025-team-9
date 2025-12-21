try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
import time


class DMS:
    def __init__(self, pins):
        self.pins = pins
        self.R1 = pins[0]
        self.R2 = pins[1]
        self.R3 = pins[2]
        self.R4 = pins[3]

        self.C1 = pins[4]
        self.C2 = pins[5]
        self.C3 = pins[6]
        self.C4 = pins[7]

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readLine(self,line, characters):
        GPIO.output(line, GPIO.HIGH)
        try:
            if GPIO.input(self.C1) == 1:
                return characters[0]
            if GPIO.input(self.C2) == 1:
                return characters[1]
            if GPIO.input(self.C3) == 1:
                return characters[2]
            if GPIO.input(self.C4) == 1:
                return characters[3]
        finally:
            GPIO.output(line, GPIO.LOW)
        return None

    def check_for_event(self):
        event = self.readLine(self.R1, ["1", "2", "3", "A"])
        if event:
            return event
        event = self.readLine(self.R2, ["4", "5", "6", "B"])
        if event:
            return event
        event = self.readLine(self.R3, ["7", "8", "9", "C"])
        if event:
            return event
        event = self.readLine(self.R4, ["*", "0", "#", "D"])
        if event:
            return event
        return None


def run_dms_loop(dms, callback, stop_event):
    while not stop_event.is_set():
        event = dms.check_for_event()
        if event:
            callback(event)
        time.sleep(0.1)