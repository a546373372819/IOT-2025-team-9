import random
import time

def run_uds_simulator(callback, stop_event, delay=3):
    while not stop_event.is_set():
        simulated_distance = random.uniform(10, 200)
        callback(simulated_distance)
        time.sleep(delay)
