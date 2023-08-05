# Pineworks Labs RP2040 GPIO

## Importing

To import this package, run: `import pineworkslabs.GPIO as GPIO`

## Connecting to the GPIO

When the package is imported, the setup code will find a compatible GPIO board on a connected COM port.

### Example: blink an LED

```
import time
GPIO.setmode(GPIO.PINEWORKS)

pin = 20

while True:
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.25)
    except KeyboardInterrupt:
        GPIO.cleanup()
```

## Acknowledgements

We are indebted to the work of the [telemetrix](https://pypi.org/project/telemetrix-rpi-pico/) team for connectivity between the PC and the GPIO board.