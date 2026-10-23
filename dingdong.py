from machine import Pin
import time

# --- Réglages ---
NB_COUPS = 40              # nombre de coups par appui (40 coups = environ 2 secondes)
DEMI_PERIODE_S = 0.04      # durée d'un coup dans un sens
PAUSE_SECURITE_S = 0.005   # EN coupé autour de chaque changement de DIR
# --- Broches (numéros GPIO) ---
dir_pin = Pin(14, Pin.OUT)             # DIR du PmodHB5
en_pin = Pin(15, Pin.OUT)              # EN du PmodHB5
bouton = Pin(2, Pin.IN, Pin.PULL_UP)   # bouton vers GND : appuyé = 0
dir_pin.value(0)
en_pin.value(0)                        # au repos : sortie coupée

def sonner():
    sens = 0
    for i in range(NB_COUPS):
        dir_pin.value(sens)            # EN est à 0 : changement de DIR sans danger
        time.sleep(PAUSE_SECURITE_S)
        en_pin.value(1)                # 12 V sur M+ / M-, polarité selon DIR
        time.sleep(DEMI_PERIODE_S)     # le battant frappe
        en_pin.value(0)                # coupure AVANT de changer DIR
        time.sleep(PAUSE_SECURITE_S)
        sens = 1 - sens                # on inverse la polarité pour le coup suivant
    en_pin.value(0)                    # sécurité : on finit toujours coupé

while True:
    if bouton.value() == 0:            # bouton appuyé
        sonner()
        while bouton.value() == 0:     # attend le relâchement du bouton
            time.sleep(0.01)
        time.sleep(0.05)               # anti-rebond
    time.sleep(0.01)