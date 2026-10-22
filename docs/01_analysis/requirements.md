# Requirements — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Context
Platform supporting a newspaper distribution company. The **subscriber list** (monthly or annual subscriptions) is delivered as a PDF and reflects the current state of active subscriptions. During work it changes with every reader event — Zugang (new subscriber), Abgang (cancellation), Urlaub (temporary pause, e.g. no paper for one month during vacation). These changes must be updated before/at shift start. The project combines real-world utility with portfolio value for job interviews (IHK standards: SDLC documentation, testing, CI/CD).

## Functional Requirements
| ID | Requirement | Priority |
| :--- | :--- | :--- |
| F1 | Import of delivery documents (PDF Tagesliste) into the database with **user approval** before saving (human-in-the-loop) | Must |
| F2 | Desktop web application serving **multiple delivery persons**, RBAC roles (ADMIN / ZUSTELLER) | Must |
| F3 | Mobile app for a **single delivery person**: offline daily route + "current customer" view while driving (surname, house number, left/right side, newspaper type: ME/OE/BILD/…) | Must |
| F4 | Voice input of changes on mobile (de-DE, on-device, offline): e.g. „Müller, Hauptstr. 12, BILD, abgang" → data update; change types: Zugang / Abgang / Urlaub (temporary pause) | Should |
| F5 | Phone ↔ desktop synchronization: **outbox + versioning** pattern (conflict resolution via `updated_at`/`version`) | Must |
| F6 | Map view: OSM/OpenFreeMap **without API key**, offline-capable | Should |
| F7 | Route planning: 1 person = drive the driver's side → return on the opposite side (exception: ≤N houses on the far side = single pass); 2 persons = route split | Should |

## Non-Functional Requirements
| ID | Requirement |
| :--- | :--- |
| NFR1 | **Offline-first** mobile: airplane mode — full daily route works without network; sync after connectivity returns |
| NFR2 | Data protection: real data (`real-data/`) never in the public repository (`.gitignore`); only synthetic test data committed |
| NFR3 | Zero-config local start: `docker compose up -d --build` brings up the entire platform |
| NFR4 | CI/CD: Jenkins pipeline (image build → health checks → tests) as part of the portfolio |
| NFR5 | IHK quality: SDLC documentation (`docs/`), unit + integration tests, clean module architecture |

## Acceptance Criteria
Defined per phase in `05_roadmap/roadmap.md`.
