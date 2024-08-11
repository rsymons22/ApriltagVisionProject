from time import sleep
from apriltag_detection import ApriltagDetection
from stepper_motor import StepperMotor
from beam_sensor import BeamSensor
import threading

OUTER_THRESHOLD_PX = 15
INNER_THRESHOLD_PX = 3
debug = True
DEFAULT_TAG_TO_TRACK = "1"

atdetection = ApriltagDetection(DEFAULT_TAG_TO_TRACK)
motor = StepperMotor()
beam = BeamSensor()

stop = False
pause = False

def check_sudden_dir_change(turning_other):
    """
    Check if motor is turning other direction, if so stop the motor and wait a bit.

    :param turning_other: if motor is turning in other direction
    """
    if turning_other:
        atdetection.status_msg = "Stopping [Sudden direction change]"
        if debug: print(atdetection.status_msg)
        motor.stop()
        sleep(0.01)

def track():
    
    at_thread = threading.Thread(target=atdetection.run_detection, daemon=True)

    turning_CW = False
    turning_CCW = False
    turning_slow = False

    at_thread.start()

    while True:
        if stop: break
        if pause: continue

        # Take a snapshot of the horiz offset value, as atdetection.horiz can change to None even after the check
        h = atdetection.horiz
        
        # No tags detected
        if h == None:
            # Currently moving -> stop
            if turning_CCW or turning_CW:
                atdetection.status_msg = "Stopping [Lost target]"
                if debug: print(atdetection.status_msg)
                motor.stop()

                turning_CW = False
                turning_CCW = False
            # Not moving, just nothing to see -> continue
            else:
                continue

        # Tag center within outer threshold -> slow down
        elif (turning_CCW or turning_CW) and not turning_slow and (h >= -OUTER_THRESHOLD_PX and h <= OUTER_THRESHOLD_PX):
            motor.in_outer_threshold(True)
            atdetection.status_msg = "Slowing Motor [Reached outer threshold]"
            if debug: print(atdetection.status_msg)

            turning_slow = True

        # Tag center within threshold -> stop
        elif (turning_CCW or turning_CW) and (h >= -INNER_THRESHOLD_PX and h <= INNER_THRESHOLD_PX):
            motor.stop()
            atdetection.status_msg = "Stopping [Centered]"
            if debug: print(atdetection.status_msg)

            turning_CW = False
            turning_CCW = False

        # Tag center outside outer threshold and still turning slow -> speed up
        elif (turning_CCW or turning_CW) and turning_slow and (h < -OUTER_THRESHOLD_PX or h > OUTER_THRESHOLD_PX):
            motor.in_outer_threshold(False)
            atdetection.status_msg = "Speeding up Motor [Outside outer threshold]"
            if debug: print(atdetection.status_msg)

            turning_slow = False

        # Tag is to the left and camera is not currently turning -> turn CCW
        elif h < -INNER_THRESHOLD_PX and not turning_CCW:
            check_sudden_dir_change(turning_CW)
            
            atdetection.status_msg = "Turning CCW"
            if debug: print(atdetection.status_msg)
            threading.Thread(target=motor.turn, args=(False,), daemon=True).start()

            turning_CCW = True
            turning_CW = False

        # Tag is to the right and camera is not currently turning -> turn CW
        elif h > INNER_THRESHOLD_PX and not turning_CW:
            check_sudden_dir_change(turning_CCW)
            
            atdetection.status_msg = "Turning CW"
            if debug: print(atdetection.status_msg)
            threading.Thread(target=motor.turn, args=(True,), daemon=True).start()

            turning_CW = True
            turning_CCW = False

        sleep(0.001)

            
    atdetection.stop = True

if __name__ == "__main__":

    # If not already homed
    if beam.read() == 1:
        print(f"> Homing...")
        motor.home(45, beam.read)
        print(f"> Homing complete, tracking") 
    

    threading.Thread(target=track, daemon=True).start()

    print("Commands:\n \
        \ttag id   -> track tag with given id\n \
        \tdebug    -> toggle debug\n \
        \tp        -> pause/unpause tracking\n \
        \tq        -> quit\n")
    

    while True:
        cmd = input("")

        if cmd == "q": break
        if cmd == "p":
            print(f">", "Unpausing tracking" if pause else "Pausing tracking")
            pause = not pause
        elif cmd.startswith("tag"): 
            atdetection.tag = cmd[4:]
            print(f"> Tracking tag: {cmd[4:]}")
        elif cmd == "debug":
            debug = not debug
            print("> Debug", "on" if debug else "off")

    stop = True

    print("> Done")
    motor.cleanup()
