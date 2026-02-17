import threading
import time
from simulators.four_segment import run_display_simulator
from sensors.four_segment import FourDigitDisplay, run_display_loop

def display_callback(name, value, publisher, settings):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"{name}: Displaying value: {value}")
    if publisher:
        publisher.enqueue_reading(
            sensor_type=name,
            sensor_name=name,
            value=value,
            simulated=settings.get("simulated", True),
            topic=settings.get("topic"),
        )

def run_display(name, settings, threads, stop_event, display_queue, publisher=None):
    if settings.get("simulated", True):
        print(f"Starting {name} simulator")
        display_thread = threading.Thread(
            target=run_display_simulator,
            args=(lambda value: display_callback(name, value, publisher, settings), stop_event, display_queue),
        )
        display_thread.start()
        threads.append(display_thread)
        print(f"{name} simulator started")
    else:
        print(f"Starting {name} real display loop")
        display = FourDigitDisplay(settings["segment_pins"], settings["digit_pins"])
        display_thread = threading.Thread(
            target=run_display_loop,
            args=(display, lambda value: display_callback(name, value, publisher, settings), stop_event, display_queue),
        )
        display_thread.start()
        threads.append(display_thread)
        print(f"{name} real display loop started")
