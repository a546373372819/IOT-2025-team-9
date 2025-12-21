import random
import time

def run_ds_simulator(delay,callback, stop_event,):
    """
    Simulates door events (open/close) randomly.

    :param callback: The function to call with the door event.
    :param stop_event: A threading.Event to stop the simulator.
    :param delay: Time in seconds between each event simulation.
    """
    next_key = "open"
    last_key="close"# Initial state of the door

    while not stop_event.is_set():

        callback(next_key)
        temp=next_key
        next_key=last_key
        last_key = temp

        time.sleep(delay)

