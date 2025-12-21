import time
import random

def run_pir_simulator(delay, callback, stop_event):
    last_state = None

    while not stop_event.is_set():
        motion = random.choice([0, 1])

        if motion != last_state:
            if motion:
                callback("motion_detected")
            else:
                callback("motion_stopped")
            last_state = motion

        time.sleep(delay)
