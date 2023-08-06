import time
import VisionFive.gpio as GPIO

led_pin = 17

GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.HIGH)

p = GPIO.PWM(led_pin, 10)
p.start(0)

try:
    while True:
        for dc in range(0, 101, 5):
            p.ChangeDutyRatio(dc)
            time.sleep(1)
        for dc in range(100, -1, -5):
            p.ChangeDutyRatio(dc)
            time.sleep(1)
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup(led_pin)
