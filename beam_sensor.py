import RPi.GPIO as GPIO

class BeamSensor:
    def __init__(self):
        self.in1 = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.IN)

    def read(self):
        """
        1 = unblocked, 0 = blocked
        """
        return GPIO.input(self.in1)