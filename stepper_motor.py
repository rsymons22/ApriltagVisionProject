import RPi.GPIO as GPIO
import time

STARTING_STEP_SLEEP = 0.0001
CLOSE_TO_HOME_STEP_SLEEP = 0.01

class StepperMotor:
    def __init__(self):
        self.out1 = 17
        self.out2 = 18
        self.out3 = 27
        self.out4 = 22

        self.step_sequence = [[1,0,0,1], [1,0,0,0], [1,1,0,0], [0,1,0,0],
                        [0,1,1,0], [0,0,1,0], [0,0,1,1],[0,0,0,1]]
       
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.out1, GPIO.OUT)
        GPIO.setup(self.out2, GPIO.OUT)
        GPIO.setup(self.out3, GPIO.OUT)
        GPIO.setup(self.out4, GPIO.OUT)

        GPIO.output(self.out1, GPIO.LOW)
        GPIO.output(self.out2, GPIO.LOW)
        GPIO.output(self.out3, GPIO.LOW)
        GPIO.output(self.out4, GPIO.LOW)

        self.motor_pins = [self.out1, self.out2, self.out3, self.out4]

        self.halt = False
        self.step_sleep = STARTING_STEP_SLEEP


    def cleanup(self):
        """
        Toggle all the motor pins to low and call the GPIO.cleanup() method
        """
        GPIO.output(self.out1, GPIO.LOW)
        GPIO.output(self.out2, GPIO.LOW)
        GPIO.output(self.out3, GPIO.LOW)
        GPIO.output(self.out4, GPIO.LOW)
        GPIO.cleanup()

    def in_outer_threshold(self, in_threshold):
        """
        Slow the motor down if the tag center is within the outer threshold

        :param in_threshold: if the tag center is within the outer threshold
        """
        if in_threshold:
            self.step_sleep = CLOSE_TO_HOME_STEP_SLEEP
        else:
            self.step_sleep = STARTING_STEP_SLEEP

    def turn(self, CW):
        """
        Turn the servo motor, speed is controlled by object attribute which
        can be altered by the in_outer_threshold method. Turning can be stopped
        by calling the stop() method.
        
        :param CW: True to turn clockwise, False to turn counter clockwise
        """
        motor_step_counter = 0
        self.halt = False

        while not self.halt:
            for pin in range(0, len(self.motor_pins)):
                GPIO.output(self.motor_pins[pin], self.step_sequence[motor_step_counter][pin])

            motor_step_counter = (motor_step_counter - 1 if CW else motor_step_counter + 1) % 8
            time.sleep(self.step_sleep)

        
    def stop(self):
        """
        Tell the servo motor to stop
        """
        self.halt = True
