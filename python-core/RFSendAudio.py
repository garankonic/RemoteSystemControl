import time
import sys
import RPi.GPIO as GPIO

audio_on  = '1000001011011001000011000'
audio_off = '1000001011011001000001000'
long_delay_one = 0.000335
short_delay_one = 0.000045
long_delay_zero = 0.000504
short_delay_zero = 0.000210
extended_delay = 0.004000

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay_one)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_delay_zero)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay_one)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_delay_zero)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')

