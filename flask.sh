#!/bin/bash
cd flask_server
# Attiva l'ambiente virtuale (se non è già attivo)
if ! command -v venv/bin/activate &> /dev/null; then
  echo "Attivazione ambiente virtuale..."
  python -m venv venv
fi

# Attiva l'ambiente virtuale
source venv/bin/activate

# Esporta FLASK_APP (se non è già settato)
if [ -z "$FLASK_APP" ]; then
  echo "Esportazione FLASK_APP..."
  export FLASK_APP=main.py
fi

# Esegui il server Flask sulla porta 8080
echo "Esecuzione server Flask..."
flask run --port=8080
