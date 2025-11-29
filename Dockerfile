# Étape 1 : image Python 3.11 slim
FROM python:3.11-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Mise à jour pip
RUN pip install --upgrade pip

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Exposer le port pour Gunicorn
EXPOSE 8000

# Logs en temps réel
ENV PYTHONUNBUFFERED=1

# Lancer Django avec migrations puis Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn OurChat.wsgi:application --bind 0.0.0.0:8000"]
