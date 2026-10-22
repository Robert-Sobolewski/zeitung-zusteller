# Wymagania — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Kontekst
Platforma wspierająca firmę dystrybucji prasy. Codzienna lista dostaw (Tagesliste) przychodzi
jako PDF; w terenie dochodzi do zmian (Zugang/Abgang — klienci dochodzą/odchodzą), które trzeba
aktualizować przed rozpoczęciem zmiany. Projekt łączy realne zastosowanie z portfolio pod
rozmowy o pracę (standardy IHK: dokumentacja SDLC, testy, CI/CD).

## Wymagania funkcjonalne
| ID | Wymaganie | Priorytet |
| :--- | :--- | :--- |
| F1 | Import dokumentu dostawy (PDF Tagesliste) do bazy danych z **aprobata użytkownika** przed zapisem (human-in-the-loop) | Must |
| F2 | Aplikacja desktopowa (web) obsługująca **wielu dostawców**, role RBAC (ADMIN / ZUSTELLER) | Must |
| F3 | Aplikacja mobilna dla **jednego dostawcy**: trasa dnia offline + widok "bieżący klient" podczas jazdy (nazwisko, nr domu, lewa/prawa strona, rodzaj gazety: ME/OE/BILD/…) | Must |
| F4 | Voice input zmian na telefonie (de-DE, on-device, offline): np. „Müller, Hauptstr. 12, BILD, abgang" → aktualizacja danych | Should |
| F5 | Synchronizacja phone ↔ desktop: wzorzec **outbox + wersjonowanie** (rozstrzyganie konfliktów po `updated_at`/`version`) | Must |
| F6 | Podgląd na mapie: OSM/OpenFreeMap **bez API key**, zdolność do pracy offline | Should |
| F7 | Planowanie trasy: 1 osoba = przejazd stroną kierowcy → powrót drugą stroną (wyjątek: ≤N domów po drugiej stronie = jeden przejazd); 2 osoby = podział tras | Should |

## Wymagania niefunkcjonalne
| ID | Wymaganie |
| :--- | :--- |
| NFR1 | **Offline-first** mobile: tryb samolotowy — pełna trasa dnia działa bez sieci; sync po powrocie do zasięgu |
| NFR2 | Ochrona danych: dane realne (`real-data/`) nigdy w repo publicznym (`.gitignore`); do repo tylko syntetyczne dane testowe |
| NFR3 | Zero-config start lokalny: `docker compose up -d --build` podnosi całą platformę |
| NFR4 | CI/CD: pipeline Jenkins (build obrazów → healthchecki → testy) jako część portfolio |
| NFR5 | Jakość IHK: dokumentacja SDLC (`docs/`), testy jednostkowe + integracyjne, czysta architektura modułów |

## Kryteria akceptacji
Zdefiniowane per faza w `05_roadmap/roadmap.md`.
