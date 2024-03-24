import time
try:
    import RPi.GPIO as GPIO

except RuntimeError:
    print('not exists')


pinAzim = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinAzim, GPIO.OUT)

pulseFreq = 50  # based on MG996R datasheet
pulseAzim = GPIO.PWM(pinAzim, pulseFreq)

pulseAzim.start(7.5)  # 7.5 dutyRatio = 90 degree

time.sleep(3)
pulseAzim.ChangeDutyCycle(5)

time.sleep(3)
pulseAzim.ChangeDutyCycle(10)

time.sleep(3)
pulseAzim.ChangeDutyCycle(7.5)
