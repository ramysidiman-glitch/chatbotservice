# Étape 1 : image Python 3.11
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements
COPY requirements.txt .

# --- NOUVELLE STRATÉGIE D'INSTALLATION DEPUIS LE FICHIER ---
# Installer TOUTES les dépendances, en utilisant l'index PyTorch CPU 
# comme index supplémentaire pour s'assurer que la version CPU de torch est trouvée.
RUN pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Copier le code du projet
COPY . .

# Exposer le port utilisé par gunicorn
EXPOSE 8000

# Commande pour lancer le serveur Django avec migrations
CMD ["sh", "-c", "python manage.py makemigrations --noinput && python manage.py migrate --noinput && gunicorn OurChat.wsgi:application --bind 0.0.0.0:8000"]