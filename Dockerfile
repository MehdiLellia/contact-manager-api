# Utiliser une image Python légère comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Exposer le port 5000
EXPOSE 5000

# Commande par défaut pour exécuter l'application
CMD ["python", "app.py"]
