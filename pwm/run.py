import pi_servo_hat
import time

# Initialize Constructor
test = pi_servo_hat.PiServoHat()
test.set_pwm_frequency(200)
print(test.frequency) #= 25000
# Restart Servo Hat (in case Hat is frozen/locked)
test.restart()

# Test Run
#########################################
# Moves servo position to 0 degrees (1ms), Channel 0
# test.move_servo_position(0, 8)
# test.move_servo_position(1, 0)

# Pause 1 sec
#time.sleep(5)

# Moves servo position to 90 degrees (2ms), Channel 0
# test.move_servo_position(0, -180)
# test.move_servo_position(0, 0)
# test.move_servo_position(0, 180)
# test.move_servo_position(0, 360)
test.move_servo_position(0, 45)
test.move_servo_position(1, 45)
test.move_servo_position(15, 0)

# Sweep
#########################################
while True:
    print('forward')
    for i in range(0, 90):
        # print(i)
        test.move_servo_position(0, i)
        test.move_servo_position(1, i)
        test.move_servo_position(15, i)
        time.sleep(.001)
    print('backward')
    for i in range(90, 0, -1):
        # print(i)
        test.move_servo_position(0, i)
        test.move_servo_position(1, i)
        test.move_servo_position(15, i)
        time.sleep(.001)
