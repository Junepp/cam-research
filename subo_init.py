import RPi.GPIO as GPIO
import time

servoPin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)

pulseFreq = 50  # based on MG996R datasheet
servo = GPIO.PWM(servoPin, pulseFreq)

if __name__ == "__main__":
    servo.start(0)  # 7.5 dutyRatio = 90 degree

    time.sleep(3)
    servo.ChangeDutyCycle(5)

    time.sleep(3)
    servo.ChangeDutyCycle(10)

    time.sleep(3)
    servo.ChangeDutyCycle(7.5)
