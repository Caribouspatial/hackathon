from machine import Pin
import time

NB_COUPS = 4          # nombre de coups par appui (un coup = un sens)
PAUSE_S = 0.5         # coupure entre deux coups
DELAI_DIR_S = 0.01    # délai de sécurité entre le changement de DIR et le retour de EN
# Module HB5 : DIR = direction, EN = enable
dir_pin = Pin(14, Pin.OUT)
dir_pin.value(0)
en_pin = Pin(15, Pin.OUT)
en_pin.value(0)       # au repos : sortie coupée
# Bouton de test : GP2 vers GND (pull-up interne)
bouton = Pin(2, Pin.IN, Pin.PULL_UP)
def sonner():
    sens = 0
    for i in range(NB_COUPS):
        # EN est à 0 ici : on peut changer DIR sans danger
        dir_pin.value(sens)
        time.sleep(DELAI_DIR_S)
        en_pin.value(1)              # le 12 V part, polarité selon DIR
        time.sleep(1)         # la cloche charge
        en_pin.value(0)              # coupure AVANT de changer DIR
        sens = 1 - sens              # on inverse le sens pour le coup suivant
        if i < NB_COUPS - 1:
            time.sleep(PAUSE_S)
while True:
    if bouton.value() == 0:          # bouton appuyé
        sonner()
        while bouton.value() == 0:   # attend le relâchement du bouton
            time.sleep(0.01)
        time.sleep(0.05)             # anti-rebond
    time.sleep(0.01)