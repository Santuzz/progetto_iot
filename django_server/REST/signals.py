from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import sys

try:
    from config import read_increment
except ImportError:
    sys.path.append('..')
    from config import read_increment


def perform_calculations(instance):
    # Ottengo tutte le relazioni SC della street presente nella relazione SC che ha cambiato valore
    related_street_crossroads = StreetCrossroad.objects.filter(
        street=instance.street).exclude(crossroad=instance.crossroad)
    traffic_level = 0
    for rel in related_street_crossroads:
        # per ogni crossroad trovata dalle relazioni trovo le sue street
        streets_linked_to_crossroad = Street.objects.filter(
            streetcrossroad__crossroad__name=rel.crossroad
        ).distinct()
        # Trovo tutte le relazioni che hanno le street di un crossroad escudendo quelle con il crossroad stesso
        street_crossroads_excluding_initial = StreetCrossroad.objects.filter(
            street__in=streets_linked_to_crossroad).exclude(crossroad__name=rel.crossroad)
        print(traffic_level)
        for rel_s in street_crossroads_excluding_initial:
            # Per ogni street delle relazioni vado a prendere la relazione che ha con il crossroad che ci interessa, in questo modo capisco se il valore di cars delle street trovate va aggiunto oppure sottratto
            rel_original = StreetCrossroad.objects.get(street=rel_s.street, crossroad=rel.crossroad)
            if rel_original.index % 2 == 0:
                traffic_level += rel_s.cars
            else:
                traffic_level -= rel_s.cars

        result = traffic_level*read_increment()
        print(result)
        rel.crossroad.traffic_level = result
        rel.crossroad.save()


@receiver(post_save, sender=StreetCrossroad)
def handle_cars_update(sender, instance, created, **kwargs):
    if not created:  # Questo garantisce che il segnale reagisca solo agli aggiornamenti, non alla creazione
        # Esegui il calcolo solo se 'cars' è cambiato
        perform_calculations(instance)
