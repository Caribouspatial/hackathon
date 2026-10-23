import time
import RPi.GPIO as GPIO

# Définition des broches (à adapter selon votre câblage)
PIN_DIR = 17  # Broche 1 (DIR)
PIN_EN = 18  # Broche 2 (EN)

# Configuration de la carte GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DIR, GPIO.OUT)
GPIO.setup(PIN_EN, GPIO.OUT)

# Initialisation : Désactiver le moteur et fixer une direction de départ
GPIO.output(PIN_EN, GPIO.LOW)
GPIO.output(PIN_DIR, GPIO.LOW)


def run_motor(direction, duration=3):
  print(
      f"Rotation dans le sens : {'Avant' if direction == GPIO.HIGH else'Arrière'}"
  )

  # 1. S'assurer que le moteur est arrêté avant de changer la direction (Sécurité)
  GPIO.output(PIN_EN, GPIO.LOW)
  time.sleep(0.05)  # Temps de la transition

  # 2. Définir la direction souhaitée
  GPIO.output(PIN_DIR, direction)
  time.sleep(0.05)

  # 3. Activer le moteur (Enable à HIGH pour pleine vitesse)
  GPIO.output(PIN_EN, GPIO.HIGH)

  # Laisser tourner pendant la durée spécifiée
  time.sleep(duration)

  # 4. Couper le moteur à la fin
  GPIO.output(PIN_EN, GPIO.LOW)


try:
  while True:
    # Tourne dans un sens pendant 3 secondes
    run_motor(GPIO.HIGH, duration=3)

    # Petite pause entre les deux sens
    time.sleep(1)

    # Tourne dans l'autre sens pendant 3 secondes
    run_motor(GPIO.LOW, duration=3)

    # Pause avant de recommencer le cycle
    time.sleep(2)

except KeyboardInterrupt:
  # Nettoyage des broches GPIO en cas d'interruption (Ctrl+C)
  GPIO.output(PIN_EN, GPIO.LOW)
  GPIO.cleanup()
  print("\nArrêt du programme et nettoyage des GPIO.")