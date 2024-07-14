import RPi.GPIO as GPIO
import time

class ServoMotor:
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


    def cleanup(self):
        GPIO.output(self.out1, GPIO.LOW)
        GPIO.output(self.out2, GPIO.LOW)
        GPIO.output(self.out3, GPIO.LOW)
        GPIO.output(self.out4, GPIO.LOW)
        GPIO.cleanup()


    def turn(self, CW, step_sleep=0.001):
        if step_sleep < 0.001: step_sleep = 0.001

        motor_step_counter = 0
        self.halt = False

        while not self.halt:
            for pin in range(0, len(self.motor_pins)):
                GPIO.output(self.motor_pins[pin], self.step_sequence[motor_step_counter][pin])

            motor_step_counter = (motor_step_counter - 1 if CW else motor_step_counter + 1) % 8
            time.sleep(step_sleep)

        
    def stop(self):
        self.halt = True
