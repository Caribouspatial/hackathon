from machine import Pin, PWM
import time

# --- CONFIGURATION DES MOTEURS (3 Moteurs via PmodHB5 ou similaires) ---
# Moteur 1
pin_dir1 = Pin(17, Pin.OUT)
pin_en1 = PWM(Pin(18))
pin_en1.freq(1000)

# Moteur 2 (Exemple sur GP19 et GP20)
pin_dir2 = Pin(19, Pin.OUT)
pin_en2 = PWM(Pin(20))
pin_en2.freq(1000)

# Moteur 3 (Exemple sur GP21 et GP22)
pin_dir3 = Pin(21, Pin.OUT)
pin_en3 = PWM(Pin(22))
pin_en3.freq(1000)

# --- CONFIGURATION DES BOUTONS ET DES LEDS (Broches 4 à 15) ---
# Levier morse (Actionneur global)
bouton_morse = Pin(16, Pin.IN, Pin.PULL_UP)

# Boutons de sélection (1, 2, 3)
btn_sel1 = Pin(4, Pin.IN, Pin.PULL_UP)
btn_sel2 = Pin(6, Pin.IN, Pin.PULL_UP)
btn_sel3 = Pin(8, Pin.IN, Pin.PULL_UP)

# LEDS témoins (1, 2, 3)
led1 = Pin(5, Pin.OUT)
led2 = Pin(7, Pin.OUT)
led3 = Pin(9, Pin.OUT)
#Cloche
dir_pin = Pin(14, Pin.OUT)   # DIR du PmodHB5
en_pin = Pin(15, Pin.OUT) # EN du PmodHB5
def cloche_switch():
    NB_TRANSITIONS = 2         # nombre de coups (le sens change à chaque coup)
    DUREE_IMPULSION_S = 0.2     # durée du 12 V pour chaque coup
    PAUSE_S = 0.09              # coupure entre deux coups

    dir_pin = Pin(14, Pin.OUT)   # DIR du PmodHB5
    en_pin = Pin(15, Pin.OUT)    # EN du PmodHB5

    dir_pin.value(0)
    en_pin.value(0)              # au repos : sortie coupée
    time.sleep(0.5)                # petit délai au démarrage pour te laisser le temps

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

        print("start")

# Puissance des moteurs (25%)
puissance_pourcentage = 25
duty_cycle = int((puissance_pourcentage / 100) * 65535)

def cloche_de_jeu(times, moteur_pin):
    NB_TRANSITIONS = times         # nombre de coups (le sens change à chaque coup)
    DUREE_IMPULSION_S = 0.5      # durée du 12 V pour chaque coup
    PAUSE_S = 0.1              # coupure entre deux coups
    dir_pin.value(0)
    en_pin.value(0)              # au repos : sortie coupée
    time.sleep(0.7)                # petit délai au démarrage pour te laisser le temps

    sens = 0
    moteur_pin.duty_u16(duty_cycle)
    try:
        for i in range(NB_TRANSITIONS):
            dir_pin.value(sens)      # EN est à 0 : changement de DIR sans danger
            time.sleep(0.01)
            print("Coup", i + 1, "- DIR =", sens)
            en_pin.value(1)          # 12 V sur M+ / M-
            time.sleep(DUREE_IMPULSION_S)
            en_pin.value(0)          # coupure AVANT de changer DIR
            sens = 1 - sens          # on inverse la polarité pour le coup suivant
            time.sleep(PAUSE_S)
    finally:
        en_pin.value(0)
        moteur_pin.duty_u16(0)

# Variables pour mémoriser l'état des boutons (anti-rebond / bascule)
dernier_etat_btn1 = 1
dernier_etat_btn2 = 1
dernier_etat_btn3 = 1
dernier_etat_morse = 1

# Numéro du moteur actuellement sélectionné (0 = aucun, 1, 2 ou 3)
moteur_actif = 0
moteur_precedent = 0

try:
    # Initialiser le sens des moteurs (sens 1)
    pin_dir1.value(1)
    pin_dir2.value(1)
    pin_dir3.value(1)
    time.sleep(0.01)

    print("Système à 3 moteurs prêt.")

    while True:
        etat_b1 = btn_sel1.value()
        etat_b2 = btn_sel2.value()
        etat_b3 = btn_sel3.value()
        etat_morse = bouton_morse.value()
        # Front descendant du levier (1 -> 0) : une seule cloche par tirage
        levier_actionne = dernier_etat_morse == 1 and etat_morse == 0

        # --- Gestion du Bouton 1
        if dernier_etat_btn1 == 1 and etat_b1 == 0:
            if moteur_actif == 1:
                moteur_actif = 0  # Désélectionne si on rappuie dessus
            else:
                moteur_actif = 1  # Sélectionne le moteur 1
            time.sleep(0.2)

        # --- Gestion du Bouton 2 ---
        if dernier_etat_btn2 == 1 and etat_b2 == 0:
            if moteur_actif == 2:
                moteur_actif = 0
            else:
                moteur_actif = 2
            time.sleep(0.2)

        # --- Gestion du Bouton 3 ---
        if dernier_etat_btn3 == 1 and etat_b3 == 0:
            if moteur_actif == 3:
                moteur_actif = 0
            else:
                moteur_actif = 3
            time.sleep(0.2)

        dernier_etat_btn1 = etat_b1
        dernier_etat_btn2 = etat_b2
        dernier_etat_btn3 = etat_b3

        # On coupe d'abord tout par sécurité, puis on active uniquement le bon
        pin_en1.duty_u16(0)
        pin_en2.duty_u16(0)
        pin_en3.duty_u16(0)
        led1.value(0)
        led2.value(0)
        led3.value(0)

        if moteur_actif == 1:
            led1.value(1)
            if levier_actionne:
                cloche_de_jeu(2, pin_en1)

        elif moteur_actif == 2:
            led2.value(1)
            if levier_actionne:
                cloche_de_jeu(2, pin_en2)

        elif moteur_actif == 3:
            led3.value(1)
            if levier_actionne:
                cloche_de_jeu(2, pin_en3)

        if moteur_actif != moteur_precedent:
            cloche_switch()
            moteur_precedent = moteur_actif

        dernier_etat_morse = etat_morse
        time.sleep(0.05)

except KeyboardInterrupt:
    # Arrêt propre de tous les moteurs et LEDs
    pin_en1.duty_u16(0)
    pin_en2.duty_u16(0)
    pin_en3.duty_u16(0)
    pin_en1.deinit()
    pin_en2.deinit()
    pin_en3.deinit()
    led1.value(0)
    led2.value(0)
    led3.value(0)
    print("\nArrêt du programme.")
