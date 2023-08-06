import VisionFive.gpio as GPIO
import time

buzz_pin = 19
ErrOutOfRange = 0

def setup():
    GPIO.setup(buzz_pin, GPIO.OUT)
    GPIO.output(buzz_pin, GPIO.HIGH)

def pitch_in_check():
    val_in = input('Enter Pitch (200 to 20000): ')
    val = float(val_in)

    if 200 <= val <= 20000:
        return val
    else:
        print('The input data is out of range(200,20000), please re-enter...')
        return ErrOutOfRange

def loop(pitch, cycle):
    delay = 1.0 / pitch
    cycle = int((cycle * pitch)/2)
    
    while cycle >= 0:
        GPIO.output(buzz_pin, GPIO.LOW)
        time.sleep(delay)
        GPIO.output(buzz_pin, GPIO.HIGH)
        time.sleep(delay)

        cycle = cycle - 1

def destroy():
    GPIO.output(buzz_pin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        pitch = pitch_in_check()
        while pitch == 0:
            pitch = pitch_in_check()

        cycle_in = input("Enter Cycle (seconds): ")
        cycle = int(cycle_in)
        
        loop(pitch, cycle)
    finally:
        destroy()


