# Builder
FROM python:3.12-alpine AS builder

WORKDIR /app

# Potrzebne do budowania zależności Pythona (requests, flask)
RUN apk add --no-cache build-base libffi-dev openssl-dev

COPY app.py .

# Instalacja zależności
RUN pip install --upgrade pip && \
    pip install --no-cache-dir flask requests

# Finalny obraz - minimalny
FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /app /app

# Użytkownik nieuprzywilejowany
RUN adduser -D appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]

LABEL author="Michał Zarzecki"
LABEL version="1.0"
LABEL description="Aplikacja pogodowa w Flasku"
