from time import sleep
from apriltag_detection import ApriltagDetection
from servo_motor import ServoMotor
from beam_sensor import BeamSensor
import threading

THRESHOLD_PX = 10
DEBUG = True

atdetection = ApriltagDetection()
motor = ServoMotor()
beam = BeamSensor()

stop = False

def track():
    
    at_thread = threading.Thread(target=atdetection.run_detection, daemon=True)

    turning_CW = False
    turning_CCW = False

    at_thread.start()

    while True:
        if stop: break

        # Take a snapshot of the horiz offset value, as atdetection.horiz can change to None even after the check
        h = atdetection.horiz

        # No tags detected
        if h == None:
            # Currently moving -> stop
            if turning_CCW or turning_CW:
                if DEBUG: print("Stopping [Lost target]")
                motor.stop()

                turning_CW = False
                turning_CCW = False
            # Not moving, just nothing to see -> continue
            else:
                continue

        # Tag center within threshold -> stop
        elif (turning_CCW or turning_CW) and (h >= -THRESHOLD_PX and h <= THRESHOLD_PX):
            if DEBUG: print("Stopping [Centered]")
            motor.stop()

            turning_CW = False
            turning_CCW = False

        # Tag is to the left and camera is not currently turning -> turn CCW
        elif h < -THRESHOLD_PX and not turning_CCW:
            # If turning other direction, stop the motor and wait a bit
            if turning_CW:
                if DEBUG: print("Stopping [Sudden direction change]")
                motor.stop()
                sleep(0.01)
            
            if DEBUG: print("Turning CCW")
            threading.Thread(target=motor.turn, args=(False,), daemon=True).start()

            turning_CCW = True
            turning_CW = False

        # Tag is to the right and camera is not currently turning -> turn CW
        elif h > THRESHOLD_PX and not turning_CW:
            # If turning other direction, stop the motor and wait a bit
            if turning_CCW:
                if DEBUG: print("Stopping [Sudden direction change]")
                motor.stop()
                sleep(0.01)
            
            if DEBUG: print("Turning CW")
            threading.Thread(target=motor.turn, args=(True,), daemon=True).start()

            turning_CW = True
            turning_CCW = False

            
    atdetection.stop = True

if __name__ == "__main__":
    threading.Thread(target=track, daemon=True).start()

    input("Press enter to end tracking\n")

    stop = True

    print("Done")
    motor.cleanup()
