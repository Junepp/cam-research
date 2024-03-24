import RPi.GPIO as GPIO
import time

servoAzimPin = 12
servoElevPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoAzimPin, GPIO.OUT)
GPIO.setup(servoElevPin, GPIO.OUT)


pulseFreq = 50  # based on MG996R datasheet
servoAzim = GPIO.PWM(servoAzimPin, pulseFreq)
servoElev = GPIO.PWM(servoElevPin, pulseFreq)

if __name__ == "__main__":
    servoAzim.start(7.5)  # 7.5 dutyRatio = 90 degree
    servoElev.start(7.5)  # 7.5 dutyRatio = 90 degree
    time.sleep(3)

    servoAzim.ChangeDutyCycle(2.5)
    servoElev.ChangeDutyCycle(2.5)
    time.sleep(3)

    servoAzim.ChangeDutyCycle(12.5)
    servoElev.ChangeDutyCycle(12.5)  # 7.5 dutyRatio = 90 degree
    time.sleep(3)

    servoAzim.ChangeDutyCycle(7.5)
    servoElev.ChangeDutyCycle(7.5)  # 7.5 dutyRatio = 90 degree
    time.sleep(3)
