# Etap budowania
FROM python:3.12-alpine AS builder

WORKDIR /app

# Instalacja narzędzi do kompilacji (build-base = gcc, make itd.)
RUN apk add --no-cache build-base libffi-dev openssl-dev

COPY app.py .

# Zapisujemy zależności do requirements.txt na podstawie tego co instalujemy
RUN pip install --upgrade pip && \
    pip install --no-cache-dir flask requests && \
    pip freeze > requirements.txt

# Finalny, produkcyjny obraz
FROM python:3.12-alpine

WORKDIR /app

# Potrzebne tylko minimalne zależności (bez gcc itp.)
RUN apk add --no-cache libffi libgcc openssl

# Skopiuj aplikację
COPY --from=builder /app /app

# Skopiuj dependencies listę i zainstaluj
RUN pip install --no-cache-dir -r /app/requirements.txt

# Dodaj użytkownika i przełącz się na niego
RUN adduser -D appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]

LABEL author="Michał Zarzecki"
LABEL version="1.0"
LABEL description="Aplikacja pogodowa w Flasku"
