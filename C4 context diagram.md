```mermaid
C4Context
    title Smart Scale System - Context Diagram
    
    Person(user, "Użytkownik", "Osoba korzystająca z inteligentnej wagi, chce monitorować swoje pomiary")
    
    System(smartscale, "Smart Scale System", "System do zarządzania danymi z inteligentnej wagi - zbiera, przechowuje i wyświetla pomiary wagi, tkanki tłuszczowej i zawartości wody")
    
    System_Ext(azure_storage, "Azure Blob Storage", "Usługa chmurowa Microsoft do przechowywania danych pomiarowych w postaci plików JSON")
    
    Rel(user, smartscale, "Przeglądanie historii pomiarów", "Web Browser")
    Rel(smartscale, azure_storage, "Zapisuje i pobiera dane pomiarowe", "HTTPS/Azure SDK")
    
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
