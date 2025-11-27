# etatcivil/context_processors.py
from .models import ParametreMairie

def mairie_parametres(request):
    parametre = ParametreMairie.objects.first()  # récupère le premier enregistrement
    return {'parametre': parametre}
