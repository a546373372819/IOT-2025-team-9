import queue

def run_lcd_simulator(callback, stop_event, lcd_queue, interval=0.5):
    while not stop_event.is_set():
        try:
            user_input = lcd_queue.get(timeout=interval)
            if user_input.lower().startswith("lcd "):
                value = user_input[4:].strip()
                if value:
                    callback(value)
            else:
                print("Invalid command. Use 'lcd <value>'")
        except queue.Empty:
            pass
