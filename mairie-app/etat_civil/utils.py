from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .models import Registre
from datetime import datetime

def generer_numero(type_acte):
    annee = datetime.now().year

    registre, created = Registre.objects.get_or_create(
        type_acte=type_acte,
        annee=annee,
        defaults={"dernier_numero": 0}
    )

    registre.dernier_numero += 1
    registre.save()

    numero_formate = str(registre.dernier_numero).zfill(4)  # ex : 0001, 0235

    return f"{numero_formate}/{annee}"


def envoyer_sms(numero, message):
    if not numero:
        return

    client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_FROM,
        to=numero
    )

def envoyer_email(dest, sujet, message):
    if not dest:
        return
    send_mail(
        sujet,
        message,
        None,
        [dest],
        fail_silently=False,
    )
