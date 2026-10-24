from machine import Pin, PWM
import time

# Définition des broches (GP17 pour DIR et GP18 for EN)
pin_dir = Pin(17, Pin.OUT)

# Configuration de la broche Enable (EN) en mode PWM
pin_en = PWM(Pin(18))
pin_en.freq(1000)  # Fréquence PWM à 1 kHz

try:
    # 1. Choisir d'abord le sens avant d'activer la puissance
    pin_dir.value(1)
    time.sleep(0.01)

    # 2. Définir la puissance (vitesse) en pourcentage (entre 0 et 100)
    puissance_pourcentage = 25  # Par exemple, 25% de puissance
    
    # Conversion du pourcentage en valeur brute pour le Pico (0 à 65535)
    duty_cycle = int((puissance_pourcentage / 100) * 65535)
    pin_en.duty_u16(duty_cycle)
    
    print(f"Le moteur tourne avec une puissance de {puissance_pourcentage}%...")

    # Le programme reste ici en fonctionnement
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Arrêt propre : couper le PWM, désinitialiser, puis forcer la broche à 0V
    pin_en.duty_u16(0)
    pin_en.deinit()
    
    # Sécurité matérielle : s'assurer que la broche EN est fermement à l'état bas
    pin_arret = Pin(18, Pin.OUT)
    pin_arret.value(0)
    
    print("\nArrêt du programme et moteur coupé.")