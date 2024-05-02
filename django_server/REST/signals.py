from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import sys
import paho.mqtt.client as mqtt

try:
    from config import read_increment
except ImportError:
    sys.path.append('..')
    from config import read_increment, read_mqtt


def publish_message(crossroad, message):
    client = mqtt.Client()
    mqtt_parameters = read_mqtt()
    client.connect(mqtt_parameters["BROKER"], int(mqtt_parameters["PORT"]), 60)
    topic = "data_traffic_" + crossroad.replace(" ", "_")
    client.publish(topic, message)
    client.disconnect()


def traffic_update(instance):
    # Ottengo tutte le relazioni SC della street presente nella relazione SC che ha cambiato valore
    related_street_crossroads = StreetCrossroad.objects.filter(
        street=instance.street).exclude(crossroad=instance.crossroad)
    traffic_level = 0  # plus_time nel bridge
    traffic_levels = {}
    for rel in related_street_crossroads:
        # per ogni crossroad trovata dalle relazioni trovo le sue street
        streets_linked_to_crossroad = Street.objects.filter(
            streetcrossroad__crossroad__name=rel.crossroad
        ).distinct()
        # Trovo tutte le relazioni che hanno le street di un crossroad escudendo quelle con il crossroad stesso
        street_crossroads_excluding_initial = StreetCrossroad.objects.filter(
            street__in=streets_linked_to_crossroad).exclude(crossroad__name=rel.crossroad)
        for rel_s in street_crossroads_excluding_initial:
            # Per ogni street delle relazioni vado a prendere la relazione che ha con il crossroad che ci interessa, in questo modo capisco se il valore di cars delle street trovate va aggiunto oppure sottratto
            rel_original = StreetCrossroad.objects.get(street=rel_s.street, crossroad=rel.crossroad)
            if rel_original.index % 2 == 0:
                traffic_level += rel_s.cars
            else:
                traffic_level -= rel_s.cars

        result = traffic_level*read_increment()
        rel.crossroad.traffic_level = result
        rel.crossroad.save()
        traffic_levels[rel.crossroad.name] = traffic_level
        traffic_level = 0
    # ritorno tutti gli incroci che hanno cambiato il proprio traffic_level per via del cambiamento del numero di macchine nella relazione SC iniziale
    return traffic_levels


@receiver(post_save, sender=StreetCrossroad)
def handle_cars_update(sender, instance, created, **kwargs):
    if not created:  # Questo garantisce che il segnale reagisca solo agli aggiornamenti, non alla creazione
        # Esegui il calcolo solo se 'cars' è cambiato
        traffic_levels = traffic_update(instance)
        print(traffic_levels)
        # tramite MQTT invio ad ogni incrocio ritornatoil valore aggiornato del traffic_level
        for crossroad, traffic_level in traffic_levels.items():
            publish_message(crossroad, str(traffic_level))
