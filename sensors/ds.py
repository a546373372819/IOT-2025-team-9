try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

from sensors.dl import DL


class DS:
    def __init__(self, pin,callback,dl:DL):

        self.pin=pin
        self.callback=callback
        self.dl=dl

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _handle_event(self, channel):

        if GPIO.input(self.pin) == GPIO.LOW:  # Button pressed
            if self.callback:
                self.callback("door closed")
        else:  # Button released
            if self.callback:
                self.callback("door open")
                self.dl.turn_on()






def run_ds_loop(ds, stop_event):

    GPIO.add_event_detect(ds.pin, GPIO.RISING, callback=
    ds._handle_event(), bouncetime=100)

    while not stop_event.is_set():
       pass