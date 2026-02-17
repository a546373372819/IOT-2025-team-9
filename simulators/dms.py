import queue

def run_dms_simulator(callback, stop_event, dms_queue):
    valid_keys = {"1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"}
    while not stop_event.is_set():
        try:
            user_input = dms_queue.get(timeout=1)
            if user_input.startswith("dms "):
                key = user_input[4:].strip()
                if key in valid_keys:
                    callback(key)
            else:
                print("Invalid command. Use 'dms <key>' or 'exit'.")
        except queue.Empty:
            pass 

