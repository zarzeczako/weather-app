# Etap buildera
FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir flask requests

# Etap końcowy
FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app /app

RUN useradd --create-home appuser
USER appuser

CMD ["python", "app.py"]

LABEL author="Michał Zarzecki"
LABEL version="1.0"
LABEL description="Aplikacja pogodowa w Flasku"

EXPOSE 5000
