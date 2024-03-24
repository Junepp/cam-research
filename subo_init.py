import RPi.GPIO as GPIO
import time

pinAzim = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinAzim, GPIO.OUT)

pulseFreq = 50  # based on MG996R datasheet
pulseAzim = GPIO.PWM(pinAzim, pulseFreq)

if __name__ == "__main__":
    pulseAzim.start(0)  # 7.5 dutyRatio = 90 degree

    time.sleep(3)
    pulseAzim.ChangeDutyCycle(5)

    time.sleep(3)
    pulseAzim.ChangeDutyCycle(10)

    time.sleep(3)
    pulseAzim.ChangeDutyCycle(7.5)
