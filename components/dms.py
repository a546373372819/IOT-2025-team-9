import threading
import time
from simulators.dms import run_dms_simulator
from sensors.dms import run_dms_loop, DMS

def dms_callback(name, event):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"{name}:Key pressed: {event}")

def run_dms(name, settings, threads, stop_event, dms_queue):
    if settings['simulated']:
        print("Starting DMS simulator")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(lambda event: dms_callback(name, event), stop_event, dms_queue))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS simulator started")
    else:
        print("Starting DMS sensor loop")
        dms = DMS(settings['pins'])
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, lambda event: dms_callback(name, event), stop_event))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS sensor loop started")
