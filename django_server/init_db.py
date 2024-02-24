# move to IoTWebsiteREST/djangoproject and run python3 init_db.py


import random
import datetime
from REST.models import Crossroad, Webcam, Trafficlight
import os
import django
import datetime  # Importa il modulo datetime per la gestione delle date

# Configura l'ambiente di Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')
django.setup()


def init_db():
    print("Creazione db")
    # Creare istanze di MasterIgrometri
    crossroad_1 = Crossroad(
        name="incrocio", latitude="10.10", longitude="20.20")
    crossroad_1.save()
    webcam = Webcam(crossroad=crossroad_1)
    webcam.save()

    # Creare 30 istanze di Igrometro collegate ai MasterIgrometri con ultima misurazione

    for i in range(4):
        Trafficlight(
            direction="A",
            green_probability=0.5,
            crossroad=crossroad_1
        ).save()


def erase_db():
    # Cancella tutti i dati nei modelli
    print("Cancellazione db")
    Webcam.objects.all().delete()
    Crossroad.objects.all().delete()


if __name__ == 'main':
    print("qua")
    erase_db()
    init_db()
