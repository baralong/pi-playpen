import pi_servo_hat
import time
import math
# Initialize Constructor
pwmHat = pi_servo_hat.PiServoHat()
pwmHat.set_pwm_frequency(200)
print(pwmHat.frequency) #= 25000
# Restart Servo Hat (in case Hat is frozen/locked)
pwmHat.restart()

def pointTo(x,y):
    # points from 0 to 1
    # 0,0 = top left
    xp = (1 - max(min(x,1),0)) * 90
    yp = max(min(y,1),0) * 90
    pwmHat.move_servo_position(0, xp)
    pwmHat.move_servo_position(1, yp)


pointTo(0,0)
# time.sleep(°2)
pointTo(1,0)
pointTo(1,1)
pointTo(0,1)
# for l in range(-90, 90): 
#     pwmHat.move_servo_position(15,l)
#     time.sleep(0.1)
# for x in range(15):
#     pwmHat.move_servo_position(0,x*6)
#     time.sleep(0.5)
#     pwmHat.move_servo_position(15,90)
#     for y in range(90):
#         pwmHat.move_servo_position(1,y)
#         #time.sleep(0.1)
#     pwmHat.move_servo_position(15,0)