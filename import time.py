import time
import RPi.GPIO as GPIO

# Définition des broches
PIN_DIR = 17  # Broche 1 (DIR)
PIN_EN = 18  # Broche 2 (EN)

# Configuration de la carte GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DIR, GPIO.OUT)
GPIO.setup(PIN_EN, GPIO.OUT)

try:
  # Choisir le sens (HIGH ou LOW)
  GPIO.output(PIN_DIR, GPIO.HIGH)

  # Activer le moteur pour le faire tourner
  GPIO.output(PIN_EN, GPIO.HIGH)
  print("Le moteur tourne dans un sens...")

  # Le programme reste ici en fonctionnement
  while True:
    time.sleep(1)

except KeyboardInterrupt:
  # Arrêt propre du moteur et nettoyage des broches avec Ctrl+C
  GPIO.output(PIN_EN, GPIO.LOW)
  GPIO.cleanup()
  print("\nArrêt du programme.")