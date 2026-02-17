import queue
import time

def run_button_simulator(callback, stop_event, btn_queue):
    while not stop_event.is_set():
        try:
            user_input = btn_queue.get(timeout=1)
            cmd = str(user_input).strip().lower()
            if cmd == "press":
                callback()
            else:
                print("Invalid command. Use 'press'.")
        except queue.Empty:
            pass
        time.sleep(0.05)
