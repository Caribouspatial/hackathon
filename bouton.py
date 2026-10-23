from machine import Pin
import time

boutons = [
    Pin(2, Pin.IN, Pin.PULL_UP),
    Pin(3, Pin.IN, Pin.PULL_UP),
    Pin(4, Pin.IN, Pin.PULL_UP),
]

# LEDs : sorties
leds = [
    Pin(10, Pin.OUT),
    Pin(11, Pin.OUT),
    Pin(12, Pin.OUT),
]

# Au démarrage, tout est éteint
for led in leds:
    led.value(0)

while True:
    for i, bouton in enumerate(boutons):
        if bouton.value() == 0:  # bouton i appuyé
            for j, led in enumerate(leds):
                led.value(1 if j == i else 0)
            time.sleep(1)