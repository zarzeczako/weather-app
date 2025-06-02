# Użycie obrazu Python 3.12 na bazie slim
FROM python:3.12-slim AS builder

# Instalacja niezbędnych narzędzi systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Wybór katalogu roboczego
WORKDIR /app

# Kopiowanie plików aplikacji do kontenera
COPY app.py .

# Instalacja zależności aplikacji, wyczyszczenie cache pip
RUN pip install --no-cache-dir flask requests

# Druga część procesu budowania (mniejszy obraz)
FROM python:3.12-slim

# Instalacja tylko wymaganych pakietów systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Wybór katalogu roboczego
WORKDIR /app

# Kopiowanie aplikacji z etapu buildera
COPY --from=builder /app /app

# Zmiana użytkownika na mniej uprzywilejowanego
RUN useradd --create-home appuser
USER appuser

# Uruchomienie aplikacji
CMD ["python", "app.py"]

# Metadane obrazu
LABEL author="Michał Zarzecki"
LABEL version="1.0"
LABEL description="Aplikacja pogodowa w Flasku"

# Określenie, że aplikacja nasłuchuje na porcie 5000
EXPOSE 5000
