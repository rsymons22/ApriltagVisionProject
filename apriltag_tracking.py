from apriltag_detection import ApriltagDetection
from servo_motor import ServoMotor
from beam_sensor import BeamSensor
import threading

THRESHOLD_PX = 10

atdetection = ApriltagDetection()
motor = ServoMotor()
beam = BeamSensor()

at_thread = threading.Thread(target=atdetection.run_detection, daemon=True)

turning_CW = False
turning_CCW = False

at_thread.start()

try:
    while True:

        if atdetection.horiz == None and not turning_CW and not turning_CCW: continue

        if atdetection.horiz < -THRESHOLD_PX and not turning_CCW:
            print("turning CCW")
            motor.stop()
            threading.Thread(target=motor.turn, args=(False,), daemon=True).start()

            turning_CCW = True
            turning_CW = False
        elif atdetection.horiz > THRESHOLD_PX and not turning_CW:
            print("turning CW")
            motor.stop()
            threading.Thread(target=motor.turn, args=(True,), daemon=True).start()

            turning_CW = True
            turning_CCW = False

        elif (turning_CCW or turning_CW) and ((atdetection.horiz >= -THRESHOLD_PX and atdetection.horiz <= THRESHOLD_PX) or atdetection.horiz == None):
            print("stopping")
            motor.stop()

            turning_CW = False
            turning_CCW = False

except KeyboardInterrupt:
    print("Done")
finally:
    print("cleaning up")
    motor.cleanup()

