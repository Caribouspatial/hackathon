from machine import Pin
import time

NB_COUPS = 3        # nombre de coups par appui (1 = comportement d'avant)
PAUSE_S = 0.5       # coupure entre deux coups (la sonnerie se relâche)
# Module HB5 : DIR = direction, EN = enable
dir_pin = Pin(14, Pin.OUT)
dir_pin.value(0)    # sens fixe, ne jamais le changer pendant que EN est à 1
en_pin = Pin(15, Pin.OUT)
en_pin.value(0)     # au repos : sortie coupée
# Bouton de test : GP2 vers GND (pull-up interne)
bouton = Pin(2, Pin.IN, Pin.PULL_UP)

def sonner():
    for i in range(NB_COUPS):
        en_pin.value(1)              # le 12 V part vers la sonnerie
        time.sleep(1)         # elle charge
        en_pin.value(0)              # coupure : elle se relâche
        if i < NB_COUPS - 1:
            time.sleep(PAUSE_S)

while True:
    if bouton.value() == 0:          # bouton appuyé
        sonner()
        while bouton.value() == 0:   # attend le relâchement du bouton
            time.sleep(0.5)
        time.sleep(0.5)             # anti-rebond