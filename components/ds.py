import threading
import time
from simulators.ds import run_ds_simulator
from sensors.ds import run_ds_loop, DS


def ds_callback(name, event):

    t = time.localtime()
    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("door "+event)


def run_ds(name, settings, threads, stop_event):

    if settings['simulated']:
        print("Starting DS simulator")
        ds_thread = threading.Thread(target=run_ds_simulator,
                                     args=(2,lambda event: ds_callback(name, event), stop_event))
        ds_thread.start()
        threads.append(ds_thread)
        print("DS simulator started")
    else:
        print("Starting DS sensor loop")
        ds = DS(settings['pin'])
        ds_thread = threading.Thread(target=run_ds_loop, args=(ds, lambda event: ds_callback(name, event), stop_event))
        ds_thread.start()
        threads.append(ds_thread)
        print("DS sensor loop started")
