import time
import queue

def run_display_simulator(callback, stop_event, display_queue, interval=0.5):
    while not stop_event.is_set():
        try:
            user_input = display_queue.get(timeout=interval)
            if user_input.lower().startswith("disp "):
                value = user_input[5:].strip()
                if value:
                    callback(value)
            else:
                print("Invalid command. Use 'disp <value>'")
        except queue.Empty:
            pass
