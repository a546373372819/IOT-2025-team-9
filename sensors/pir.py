import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

class PIR:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)
        self.last_state = False

    def detect_motion(self):
        return GPIO.input(self.pin)

    def check_for_event(self):
        current_state = self.detect_motion()

        if current_state != self.last_state:
            self.last_state = current_state
            if current_state:
                return "motion_detected"
            else:
                return "motion_stopped"
        return None

def run_pir_loop(pir, callback, stop_event):
    while not stop_event.is_set():
        event = pir.check_for_event()
        if event:
            callback(event)
        time.sleep(0.1)