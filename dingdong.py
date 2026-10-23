from machine import Pin
import time

# Module HB5 : DIR = direction, EN = enable
dir_pin = Pin(14, Pin.OUT)
dir_pin.value(0)        # sens fixe, ne jamais le changer pendant que EN est à 1

en_pin = Pin(15, Pin.OUT)
en_pin.value(0)         # au repos : sortie coupée

# Bouton de test : GP2 vers GND (pull-up interne)
bouton = Pin(2, Pin.IN, Pin.PULL_UP)

def sonner():
    en_pin.value(1)             # le 12 V part vers la sonnerie
    time.sleep(1)     # 1 seconde pour qu'elle "charge"
    en_pin.value(0)             # coupure
while True:
    if bouton.value() == 0:     # bouton appuyé
        sonner()
        while bouton.value() == 0:   # attend le relâchement
            time.sleep(1)