import cv2
import torch

# Carica il modello YOLOv5 pre-addestrato
model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# Apri il flusso video dalla telecamera
capture = cv2.VideoCapture(0)  # 0 per la prima telecamera, 1 per la seconda, ecc.

# Criteri per il conteggio delle macchine
count_threshold = 0.5  # Soglia di confidenza per considerare un'area come macchina
min_area = 1000  # Area minima per considerare un'area come macchina

# Dizionario per tracciare le macchine rilevate
tracked_cars = {}

# Contatore per le macchine rilevate
car_count = 0

while True:
    # Leggi il frame dal flusso video
    ret, frame = capture.read()
    if not ret:
        break

    # Esegui l'inferenza sugli oggetti nel frame
    results = model(frame)

    # Rileva le macchine
    for pred in results.pred:
        for item in pred:
            if item[5] == 2 and item[4] >= count_threshold:  # Supponiamo che '2' sia l'ID dell'oggetto per le macchine
                x1, y1, x2, y2, conf, _ = item
                area = (x2 - x1) * (y2 - y1)
                if area >= min_area:
                    # Verifica se la macchina è già stata tracciata
                    car_key = (int(x1), int(y1), int(x2), int(y2))
                    if car_key not in tracked_cars:
                        # Incrementa il contatore delle macchine rilevate
                        car_count += 1
                        # Traccia la macchina nel dizionario
                        tracked_cars[car_key] = True
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Disegna il bounding box intorno alla macchina

    # Visualizza il frame con i bounding box delle macchine rilevate e il numero di macchine contate
    cv2.putText(frame, f'Car Count: {car_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Cars Detection', frame)

    # Interrompi il ciclo se viene premuto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia il flusso video e chiudi le finestre di visualizzazione
capture.release()
cv2.destroyAllWindows()
