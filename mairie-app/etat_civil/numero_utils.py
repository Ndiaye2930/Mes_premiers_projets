# etat_civil/numero_utils.py
import random

def generer_numero(prefix=""):
    return f"{prefix.upper()}-{random.randint(1000, 9999)}"
