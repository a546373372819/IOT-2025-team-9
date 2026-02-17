import time
try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

class Button:
    def __init__(self, pin=None, simulated=False):
        self.simulated = simulated
        self.pin = pin

        if not simulated and GPIO:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        return GPIO.input(self.pin) == GPIO.LOW


def run_button_loop(button, stop_event, callback, cooldown = 0.2):
    last_press_time = 0
    while not stop_event.is_set():
        if button.is_pressed():
            current_time = time.time()
            if current_time - last_press_time > cooldown:
                callback()
                last_press_time = current_time
        time.sleep(0.05)