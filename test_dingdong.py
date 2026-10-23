from machine import Pin
import time

NB_TRANSITIONS = 5         # nombre de coups (le sens change à chaque coup)
DUREE_IMPULSION_S = 0.1      # durée du 12 V pour chaque coup
PAUSE_S = 0.1              # coupure entre deux coups

dir_pin = Pin(14, Pin.OUT)   # DIR du PmodHB5
en_pin = Pin(15, Pin.OUT)    # EN du PmodHB5

dir_pin.value(0)
en_pin.value(0)              # au repos : sortie coupée
time.sleep(2)                # petit délai au démarrage pour te laisser le temps

sens = 0
for i in range(NB_TRANSITIONS):
    dir_pin.value(sens)      # EN est à 0 : changement de DIR sans danger
    time.sleep(0.01)
    print("Coup", i + 1, "- DIR =", sens)
    en_pin.value(1)          # 12 V sur M+ / M-
    time.sleep(DUREE_IMPULSION_S)
    en_pin.value(0)          # coupure AVANT de changer DIR
    sens = 1 - sens          # on inverse la polarité pour le coup suivant
    time.sleep(PAUSE_S)

print("Terminé")