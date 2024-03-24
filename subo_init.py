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

time.sleep(5)
pulseAzim.start(5)  # 7.5 dutyRatio = 90 degree

time.sleep(5)
pulseAzim.start(10)  # 7.5 dutyRatio = 90 degree

time.sleep(5)
pulseAzim.start(7.5)  # 7.5 dutyRatio = 90 degree
