# Database Model — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Current State (Phase 0)
Schema is empty. The backend is connected to the database (`ddl-auto: update`); JPA entities do not exist yet and will be created in Phase 1 together with migrations. The **PostGIS 3.4.3** extension is installed and verified (`db/init/01-postgis.sql`, mounted into `/docker-entrypoint-initdb.d`).

## Target Model (Phase 1+)
The structure mirrors the real Tagesliste document: street → house number → surname → newspaper code → copy count.

```mermaid
erDiagram
    ZUSTELLER ||--o{ BEZIRK : "delivers"
    BEZIRK ||--o{ STREET : "contains"
    STREET ||--o{ DELIVERY_POINT : "contains"
    NEWSPAPER_TYPE ||--o{ SUBSCRIPTION : ""
    DELIVERY_POINT ||--o{ SUBSCRIPTION : "subscribes to"
    DELIVERY_POINT {
        int id PK
        int street_id FK
        string house_number
        enum side "LEFT/RIGHT"
        string last_name "surname (primary in route view)"
        string first_name "given name(s), may carry suffixes"
        string annotation "free-text delivery note (e.g. 'BK next to garage')"
        bool active "address still a delivery point"
        int version "sync versioning"
        timestamptz updated_at
        geometry point "PostGIS: WGS84"
    }
    BEZIRK {
        int id PK
        string code "e.g. 8019"
        string name
        int zusteller_id FK
    }
    STREET {
        int id PK
        int bezirk_id FK
        string name
        int route_order "order within the route"
    }
    ZUSTELLER {
        int id PK
        string first_name
        string last_name
        enum role "ADMIN/MANAGER/ZUSTELLER"
    }
    NEWSPAPER_TYPE {
        string code PK "e.g. ME-OBB/AUSGABE"
        string name
    }
    SUBSCRIPTION {
        int id PK
        int delivery_point_id FK
        string newspaper_code FK
        int quantity "copy count"
        enum sub_type "ANNUAL/MONTHLY/PAUSE (Urlaub)"
        date valid_from
        date valid_until
    }
```

## Principles
- **Time-bounded subscriptions**: the daily list is *derived*, not stored — `WHERE today BETWEEN valid_from AND valid_until`. Zugang = new row with `valid_from` = today; Abgang = `valid_until` = yesterday; Urlaub (vacation pause) = a gap in validity, after which the subscription resumes automatically.
- **Versioning**: `DeliveryPoint.version` + `updated_at` — the basis for sync conflict resolution (F5).
- **Geometry**: each delivery point stored as `geometry(Point, 4326)` — GIST index for spatial queries (map, route planning).
- **Change tracking**: outbox / change log table (`sync_outbox`) — phone→desktop events with acknowledgement.
- Migrations: Flyway from Phase 1 (open decision in the roadmap — see `05_roadmap/roadmap.md`).
