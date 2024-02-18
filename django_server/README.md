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
