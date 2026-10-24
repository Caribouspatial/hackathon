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

# Puissance des moteurs (75%)
puissance_pourcentage = 75
duty_cycle = int((puissance_pourcentage / 100) * 65535)

# Variables pour mémoriser l'état des boutons (anti-rebond / bascule)
dernier_etat_btn1 = 1
dernier_etat_btn2 = 1
dernier_etat_btn3 = 1

# Numéro du moteur actuellement sélectionné (0 = aucun, 1, 2 ou 3)
moteur_actif = 0

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

        # --- Gestion du Bouton 1 (Front descendant : 1 -> 0) ---
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

        # --- Application de la sélection (LEDs et Moteurs) ---
        # On coupe d'abord tout par sécurité, puis on active uniquement le bon
        pin_en1.duty_u16(0)
        pin_en2.duty_u16(0)
        pin_en3.duty_u16(0)
        led1.value(0)
        led2.value(0)
        led3.value(0)

        if moteur_actif == 1:
            led1.value(1)
            if etat_morse == 0:
                pin_en1.duty_u16(duty_cycle)

        elif moteur_actif == 2:
            led2.value(1)
            if etat_morse == 0:
                pin_en2.duty_u16(duty_cycle)

        elif moteur_actif == 3:
            led3.value(1)
            if etat_morse == 0:
                pin_en3.duty_u16(duty_cycle)

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