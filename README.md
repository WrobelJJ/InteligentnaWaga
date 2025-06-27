# Projekt Smart Scale

Ten projekt składa się z trzech głównych komponentów: backendu (FastAPI), symulatora danych (Python) oraz prostego frontendu (HTML/CSS/JavaScript).

## Spis treści
- [Opis Projektu](#opis-projektu)
- [Użyte Technologie](#użyte-technologie)
- [Struktura Projektu](#struktura-projektu)
- [Konfiguracja Azure Blob Storage](#konfiguracja-azure-blob-storage)
- [Uruchomienie Projektu](#uruchomienie-projektu)
  - [Ręczne Uruchomienie](#ręczne-uruchomienie)
  - [Uruchomienie z Docker Compose (Opcjonalnie)](#uruchomienie-z-docker-compose-opcjonalnie)
- [Przepływ Danych](#przepływ-danych)

## Opis Projektu
Projekt "Smart Scale" symuluje działanie inteligentnej wagi, która wysyła dane pomiarowe (waga, procent tkanki tłuszczowej, procent wody) do backendu. Backend zapisuje te dane w Azure Blob Storage. Frontend umożliwia pobieranie i wyświetlanie historii pomiarów dla konkretnego użytkownika.

## Użyte Technologie

### Backend
- **Python 3.9+**
- **FastAPI**: Szybki framework webowy do budowania API.
- **Uvicorn**: Serwer ASGI do uruchamiania aplikacji FastAPI.
- **Pydantic**: Walidacja danych i zarządzanie ustawieniami.
- **Azure Storage Blob SDK**: Do interakcji z Azure Blob Storage.
- **python-dotenv**: Do ładowania zmiennych środowiskowych z pliku `.env`.

### Symulator
- **Python 3.9+**
- **Requests**: Biblioteka do wykonywania zapytań HTTP.

### Frontend
- **HTML5**: Struktura strony.
- **CSS3**: Stylizacja.
- **JavaScript**: Logika po stronie klienta do komunikacji z API i wyświetlania danych.

### Inne
- **Docker / Docker Compose**: Do konteneryzacji i orkiestracji usług (opcjonalnie).

## Struktura Projektu

smart-scale/
├── backend/
│   ├── .env
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── simulator/
│   ├── simulator.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── docker-compose.yml
└── README.md


## Konfiguracja Azure Blob Storage

Projekt wymaga konta Azure Storage i kontenera blob. Backend używa `AZURE_STORAGE_CONNECTION_STRING` do połączenia się z Azure Blob Storage.

1.  **Utwórz konto Azure Storage** (jeśli jeszcze go nie masz).
2.  **Utwórz kontener blob** o nazwie `smartscale-data` w ramach swojego konta Storage.
3.  **Pobierz Connection String** dla swojego konta Storage.
4.  **Utwórz plik `.env`** w katalogu `backend/` (`backend/.env`) i dodaj do niego swój Connection String w formacie:
    ```
    AZURE_STORAGE_CONNECTION_STRING="Twoj_Connection_String_Azure"
    ```
    Zastąp `"Twoj_Connection_String_Azure"` rzeczywistym Connection Stringiem.

## Uruchomienie Projektu

### Ręczne Uruchomienie

1.  **Wymagania wstępne:**
    - Python 3.9+ zainstalowany.
    - `pip` (menedżer pakietów Pythona).

2.  **Zainstaluj zależności dla backendu:**
    Otwórz terminal i przejdź do katalogu `backend`:
    ```bash
    cd backend
    ```
    Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Zainstaluj zależności dla symulatora:**
    Otwórz **nowy terminal** i przejdź do katalogu `simulator`:
    ```bash
    cd simulator
    ```
    Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uruchom backend:**
    W terminalu, w którym jesteś w katalogu `backend`, uruchom:
    ```bash
    uvicorn main:app
    ```
    Backend będzie nasłuchiwał na `http://127.0.0.1:8000`.

5.  **Uruchom symulator:**
    W **drugim terminalu**, w którym jesteś w katalogu `simulator`, uruchom:
    ```bash
    python simulator.py
    ```
    Symulator zacznie generować i wysyłać dane do backendu.

6.  **Otwórz frontend:**
    Przejdź do katalogu `frontend` i otwórz plik `index.html` w swojej przeglądarce internetowej.
    ```
    frontend/index.html
    ```
    Wpisz `user_id` (np. `user1`, `user2`) i kliknij "Pobierz dane", aby zobaczyć historię pomiarów.

### Uruchomienie z Docker Compose (Opcjonalnie)

1.  **Wymagania wstępne:**
    - Docker Desktop zainstalowany i uruchomiony.

2.  **Upewnij się, że plik `.env`** w katalogu `backend/` zawiera poprawny `AZURE_STORAGE_CONNECTION_STRING` (patrz sekcja [Konfiguracja Azure Blob Storage](#konfiguracja-azure-blob-storage)).

3.  **Przejdź do głównego katalogu projektu** (`smart-scale`):
    ```bash
    cd .
    ```

4.  **Uruchom Docker Compose:**
    ```bash
    docker compose up --build
    ```
    To polecenie zbuduje obrazy Docker dla backendu i symulatora, a następnie uruchomi oba serwisy. Backend będzie dostępny na `http://localhost:8000`.

5.  **Otwórz frontend:**
    Przejdź do katalogu `frontend` i otwórz plik `index.html` w swojej przeglądarce internetowej.
    ```
    frontend/index.html
    ```
    Wpisz `user_id` (np. `user1`, `user2`) i kliknij "Pobierz dane", aby zobaczyć historię pomiarów.

## Przepływ Danych
1.  **Symulator** generuje losowe dane pomiarowe i wysyła je do backendu FastAPI za pomocą żądań HTTP POST.
2.  **Backend** odbiera dane, dodaje do nich znacznik czasu (timestamp) i zapisuje je jako pliki JSON w kontenerze `smartscale-data` w Azure Blob Storage.
3.  **Frontend** umożliwia użytkownikowi wprowadzenie `user_id`. Po kliknięciu przycisku, wysyła żądanie HTTP GET do backendu.
4.  **Backend** pobiera wszystkie pliki JSON dla danego `user_id` z Azure Blob Storage, przetwarza je i zwraca jako listę pomiarów do frontendu.
5.  **Frontend** wyświetla otrzymane dane w czytelnej formie, konwertując znacznik czasu na polską strefę czasową (UTC+2).