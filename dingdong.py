from machine import Pin
import time

DUREE_IMPULSION_S = 1    # on part de 1 s, comme au premier test qui avait sonné
PAUSE_S = 0.5            # coupure entre les deux sens
dir_pin = Pin(14, Pin.OUT)
en_pin = Pin(15, Pin.OUT)
bouton = Pin(2, Pin.IN, Pin.PULL_UP)
dir_pin.value(0)
en_pin.value(0)

def impulsion(sens):
    print("DIR =", sens)
    dir_pin.value(sens)        # EN est à 0 : changement de DIR sans danger
    time.sleep(0.01)
    print("EN = 1  (12 V sur M+ / M-)")
    en_pin.value(1)
    time.sleep(DUREE_IMPULSION_S)
    en_pin.value(0)
    print("EN = 0")

print("Prêt. Appuie sur le bouton.")

while True:
    if bouton.value() == 0:
        print("Bouton détecté")
        impulsion(0)           # un gong
        time.sleep(PAUSE_S)
        impulsion(1)           # l'autre gong
        while bouton.value() == 0:
            time.sleep(0.01)
        time.sleep(0.05)
    time.sleep(0.01)               # anti-rebond