# Django basics
Note per fare cose su django che possono sempre tornare utili
## Creazione progetto
1. creare la cartella del progetto
2. Controlliamo di avere pipenv ```pipenv —version```
	1. Installare pipenv se non c’è  ```pip3 install pipenv ```
3. Installiamo django nel virtual enviroment ```pipenv install django```
4. Attiviamo il virtual enviroment ```pipenv shell```
5. Creiamo il nostro progetto ```django-admin startproject NOME_PROGETTO ./```
6. Per lanciare il progetto ```python manage.py runserver```

## Applicazioni
1. Crea una nuova app ```python manage.py startapp NOME_APP```  
	NOTA: i template di quell’app dovranno essere messi all’interno di una sottodirectory che ha lo stesso nome dell’app. In questo modo si fa meno confusione quando bisogna richiamare i template
2. Registrare l’app nel file settings.py del progetto dentro a INSTALLED_APPS
3. Aggiurgere il file urls.py nell’app
4. includere l’urls.py creato nell’urls.py del progetto
	```from django.urls import path, include```
	and ```path('api/', include('REST.urls')),```

## Migrazioni
1. Crea una migrazione per un app ```python manage.py makemigrations NOME_APP```
2. Aggiungi le migrazioni al DB ```python manage.py migrate```


# REST framework

## Serializer
Quando arriva una richiesta con dei dati che dovrebbero rappresentare un oggetto vanno serializzati  
```serializer = WebcamSerializer(data=request.data)```  
In questo modo django crea un oggetto che diventerà una nuova instance del db con la funzione save.  
```instance = serializer.save()``` 
Con il serializer si definisce la nuova instance attraverso un modello e i fields che deve avere.  
I fileds possono anche essere output di metodi, in questo caso si utilizza *SerializerMethodField* definendone il comportamento attraverso una nuova funzione in cui la nuova instance è vista attraverso la variabile *obj* passata alla funzione.  
```python
class WebcamSerializer(serializers.ModelSerializer):
    crossroad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Webcam
        fields = [
            'id',
            'cars_count',
            'active',
            'crossroad'
        ]

    def get_crossroad(self, obj):
        if not isinstance(obj, Webcam):
            return None
        return obj.get_crossroad()
```
## Generics
La struttura generale per un generics prevede la definizione di un *queryset* e di una *serializer_class*.
```python
class WebcamCreateView(generics.CreateAPIView):
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer

    # if you don't want to use the default queryset
    def get_queryset():
        return Webcam.objects.all()

```



