import cv2

# Apri il flusso video dalla telecamera
capture = cv2.VideoCapture(0)  # 0 per la prima telecamera, 1 per la seconda, ecc.

# Crea un rilevatore di blob
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000  # Area minima per considerare un blob come macchina
detector = cv2.SimpleBlobDetector_create(params)

# Inizializza il tracciamento degli oggetti
tracker = cv2.TrackerCSRT_create()

# Contatore per le macchine rilevate
car_count = 0

while True:
    # Leggi il frame dal flusso video
    ret, frame = capture.read()
    if not ret:
        break

    # Rileva i blob nell'immagine
    keypoints = detector.detect(frame)

    # Traccia i blob e conta le macchine
    for keypoint in keypoints:
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        w, h = int(keypoint.size), int(keypoint.size)
        bbox = (x, y, w, h)

        # Inizia il tracciamento del blob
        ok = tracker.init(frame, bbox)
        if ok:
            car_count += 1

        # Disegna un rettangolo intorno al blob
        cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)

    # Visualizza il frame con i bounding box delle macchine rilevate e il numero di macchine contate
    cv2.putText(frame, f'Car Count: {car_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Cars Detection', frame)

    # Interrompi il ciclo se viene premuto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia il flusso video e chiudi le finestre di visualizzazione
capture.release()
cv2.destroyAllWindows()
