# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du projet
COPY . .

# Créer les répertoires nécessaires s'ils n'existent pas
RUN mkdir -p data/cleaned data/enriched models schema

# Exposer le port 8050 (port par défaut de Dash)
EXPOSE 8050

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DASH_DEBUG=False

# Commande pour exécuter l'application avec gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--workers", "4", "--timeout", "120", "app:server"]
