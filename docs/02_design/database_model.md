# Model bazy danych — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Stan obecny (Faza 0)
Schemat pusty. Backend połączony z bazą (`ddl-auto: update`), encje JPA nie istnieją jeszcze —
tworzone w Fazie 1 wraz z migracjami. Rozszerzenie **PostGIS 3.4.3** zainstalowane i zweryfikowane
(`db/init/01-postgis.sql`, mount do `/docker-entrypoint-initdb.d`).

## Model docelowy (Faza 1+)
Struktura odwzorowuje realny dokument Tagesliste: ulica → nr domu → nazwisko → kod gazety → liczba egz.

```mermaid
erDiagram
    ZUSTELLER ||--o{ BEZIRK : "dostarcza"
    BEZIRK ||--o{ STREET : "zawiera"
    STREET ||--o{ DELIVERY_POINT : "zawiera"
    NEWSPAPER_TYPE ||--o{ SUBSCRIPTION : ""
    DELIVERY_POINT ||--o{ SUBSCRIPTION : "prenumeruje"
    DELIVERY_POINT {
        int id PK
        int street_id FK
        string house_number
        enum side "LEFT/RIGHT"
        string customer_name
        bool active "AKTYWNY/ABGANG"
        int version "wersjonowanie sync"
        timestamptz updated_at
        geometry point "PostGIS: WGS84"
    }
    BEZIRK {
        int id PK
        string code "np. 8019"
        string name
        int zusteller_id FK
    }
    STREET {
        int id PK
        int bezirk_id FK
        string name
        int route_order "kolejność w trasie"
    }
    ZUSTELLER {
        int id PK
        string first_name
        string last_name
        enum role "ADMIN/ZUSTELLER"
    }
    NEWSPAPER_TYPE {
        string code PK "np. ME-OBB/AUSGABE"
        string name
    }
    SUBSCRIPTION {
        int id PK
        int delivery_point_id FK
        string newspaper_code FK
        int quantity "liczba egz."
    }
```

## Zasady
- **Wersjonowanie**: `DeliveryPoint.version` + `updated_at` — podstawa rozstrzygania konfliktów sync (F5).
- **Geometria**: punkt dostawy jako `geometry(Point, 4326)` — indeks GIST dla zapytań przestrzennych (mapa, planowanie trasy).
- **Zmiany**: kolejka outbox / change log (tabela `sync_outbox`) — zdarzenia phone→desktop z potwierdzeniem odbioru.
- Migracje: Flyway od Fazy 1 (decyzja otwarta w roadmapie — patrz `05_roadmap/roadmap.md`).
