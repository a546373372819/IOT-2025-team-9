import time
import random
import queue
def run_buzzer_simulator(callback, stop_event, db_queue, delay=1):

    while not stop_event.is_set():
        try:
            user_input = db_queue.get(timeout=1)
            if user_input == "buzz":
                callback()
        except queue.Empty:
            pass 
        except KeyboardInterrupt:
            print('Stopping Door Buzzer...')
            stop_event.set()
            break

