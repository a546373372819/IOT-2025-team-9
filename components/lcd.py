import threading
import time
from simulators.lcd import run_lcd_simulator
from sensors.lcd import LCD, run_lcd_loop


def lcd_callback(name, value, publisher, settings):
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
            topic=settings.get("topic")
        )


def run_lcd(name, settings, threads, stop_event, lcd_queue, publisher=None):
    if settings.get("simulated", True):
        print(f"Starting {name} simulator")
        lcd_thread = threading.Thread(
            target=run_lcd_simulator,
            args=(lambda event: lcd_callback(name, event, publisher, settings),
                  stop_event,
                  lcd_queue),
            daemon=True
        )
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"{name} simulator started")
    else:
        print(f"Starting {name} real LCD loop")
        lcd = LCD(settings["i2c_address"])
        lcd_thread = threading.Thread(
            target=run_lcd_loop,
            args=(name, lcd, stop_event, lcd_queue,
                  lambda event: lcd_callback(name, event, publisher, settings)),
            daemon=True
        )
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"{name} real LCD loop started")
