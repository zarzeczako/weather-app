# Weather App – Aplikacja pogodowa w Dockerze (CI/CD + Trivy)


Zdjęcia potwierdzające działanie:

https://ibb.co/pjFjdXMj
https://ibb.co/B2DxkW56
https://ibb.co/d4KCQsTt
https://ibb.co/wFHxF7B5
https://ibb.co/WWhnbhZ6


Reszta repozytorium zawiera aplikację pogodową napisaną w Pythonie z użyciem frameworka Flask, opakowaną w kontener Docker oraz automatycznie budowaną i wypychaną do GitHub Container Registry przy użyciu GitHub Actions.

## Zrealizowane wymagania zadania

✔️ Aplikacja budowana jest w ramach workflow GitHub Actions  
✔️ Obraz wspiera dwie architektury: `linux/amd64` oraz `linux/arm64`   (https://ibb.co/d4KCQsTt)
✔️ Używany jest cache (`registry` jako eksporter i backend)  
✔️ Cache przechowywany jest na publicznym repozytorium DockerHub  
✔️ Przeprowadzany jest test CVE za pomocą Trivy  
✔️ Publikacja obrazu następuje tylko, gdy **brak jest zagrożeń HIGH lub CRITICAL**

---

## Tagowanie obrazów i cache

- Obraz kontenera: tag `latest`
- Cache budowania: identyfikowany przez `buildx-cache` (trwały w DockerHub)
- Cache Trivy: `trivy-binary-*`, `cache-trivy-*` (trwały w GitHub Actions)

**Uzasadnienie**:
- Użycie tagu `latest` pozwala zawsze odnosić się do aktualnej wersji obrazu
- Cache budowania warstw w DockerHub przyspiesza kolejne buildy (źródło: [Docker Buildx cache backend](https://docs.docker.com/build/cache/backends/))
- Trivy wybrano jako skaner CVE ze względu na:
  - prostotę integracji z GitHub Actions,
  - dobre wsparcie dla obrazu Alpine,
  - możliwość zablokowania procesu push w razie błędów.

---

## Pipeline GitHub Actions (build + scan + deploy)

Plik YAML 

- budowanie obrazu z użyciem `buildx`
- uruchomienie skanera CVE (Trivy)
- warunkowe wypchnięcie do `ghcr.io` tylko przy "czystym" obrazie
- obsługę cache (`--cache-to`, `--cache-from`) z publicznego DockerHub

---

## Wnioski

Workflow został uruchomiony i zakończył się sukcesem.  

Zrzut ekranu z udanego skanowania i wypchnięcia obrazu można znaleźć na górze.  


## Uruchomienie lokalne

```bash
docker build -t weather-app:test .
docker run -p 5000:5000 weather-app:test
