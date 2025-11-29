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

# Installer PyTorch CPU en premier pour éviter compilation
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Installer le reste des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du projet
COPY . .

# Exposer le port utilisé par gunicorn
EXPOSE 8000

# Commande pour lancer le serveur Django avec migrations
CMD ["sh", "-c", "python manage.py makemigrations --noinput && python manage.py migrate --noinput && gunicorn OurChat.wsgi:application --bind 0.0.0.0:8000"]
