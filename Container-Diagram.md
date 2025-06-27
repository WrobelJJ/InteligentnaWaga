```mermaid
C4Container
    title Smart Scale System - Container Diagram
    
    %% Actors and External Systems
    Person(user, "Użytkownik", "Osoba chcąca sprawdzić historię pomiarów")
    System_Ext(azure_blob, "Azure Blob Storage", "Przechowuje dane pomiarowe w plikach JSON")

    %% System Boundary and Containers
    System_Boundary(c1, "Smart Scale System") {
        Container(frontend, "Frontend Web App", "HTML/CSS/JavaScript", "Interfejs użytkownika do przeglądania historii pomiarów")
        Container(backend, "Backend API", "FastAPI/Python", "Obsługuje żądania HTTP, zarządza danymi pomiarowymi")
        Container(simulator, "Data Simulator", "Python/Requests", "Symuluje dane z inteligentnej wagi")
    }

    %% Relationships
    Rel(user, frontend, "Używa", "HTTPS")
    Rel(frontend, backend, "Pobiera dane", "HTTP GET /api/measurements/{user_id}")
    Rel(simulator, backend, "Wysyła pomiary", "HTTP POST /api/measurements")
    Rel(backend, azure_blob, "Zapisuje/odczytuje dane", "Azure SDK")
