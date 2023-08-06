import VisionFive.gpio as GPIO
import time

led_pin = 17
GPIO.setup(led_pin, GPIO.OUT)

def light(delay):
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(delay)

if __name__ == '__main__':
    try:
        delay_s = input("Enter delay(seconds): ")
        delay = float(delay_s)

        while True:
            light(delay)

    finally:
        GPIO.cleanup()

