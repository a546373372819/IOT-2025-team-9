try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
import time
import queue

class FourDigitDisplay:
    def __init__(self, segment_pins, digit_pins):
        self.segments = segment_pins  # tuple of 8 pins (A-G + DP)
        self.digits = digit_pins      # tuple of 4 pins
        self.num_map = {
            ' ':(0,0,0,0,0,0,0),
            '0':(1,1,1,1,1,1,0),
            '1':(0,1,1,0,0,0,0),
            '2':(1,1,0,1,1,0,1),
            '3':(1,1,1,1,0,0,1),
            '4':(0,1,1,0,0,1,1),
            '5':(1,0,1,1,0,1,1),
            '6':(1,0,1,1,1,1,1),
            '7':(1,1,1,0,0,0,0),
            '8':(1,1,1,1,1,1,1),
            '9':(1,1,1,1,0,1,1)
        }

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for seg in self.segments:
            GPIO.setup(seg, GPIO.OUT)
            GPIO.output(seg, 0)
        for dig in self.digits:
            GPIO.setup(dig, GPIO.OUT)
            GPIO.output(dig, 1)

    def display_number(self, number_str):
        # Pad number string to 4 chars
        s = str(number_str).rjust(4)
        for digit_idx in range(4):
            for seg_idx in range(7):  # ignore DP
                GPIO.output(self.segments[seg_idx], self.num_map[s[digit_idx]][seg_idx])
            GPIO.output(self.digits[digit_idx], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit_idx], 1)

    def cleanup(self):
        GPIO.cleanup()

def run_display_loop(display, callback, stop_event, display_queue, interval=0.5):
    last_value = "    "

    while not stop_event.is_set():
        try:
            value = display_queue.get(timeout=interval)
            last_value = str(value).rjust(4)
            callback(last_value)
        except queue.Empty:
            pass

        display.display_number(last_value)
        time.sleep(0.001)

    display.cleanup()

