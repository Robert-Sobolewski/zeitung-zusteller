# Technology Selection & Rationale — Zeitungszusteller Platform
Last Updated: 2026-10-21

## 1. Kryteria wyboru
Każda decyzja oceniana względem:
1. **Standard branżowy** — co zespoły enterprise realnie produkcyjnie wdrażają (relewność IHK)
2. **Zgodność z wymaganiami** — czy spełnia wymaganie z `01_analysis/requirements.md`?
3. **Ekosystem i długowieczność** — aktywna pielęgnacja, LTS, rozmiar społeczności
4. **Maintainability** — czytelność, testowalność, możliwość przekazania komuś innemu

## 2. Backend API
### 2.1 Spring Boot 4.1.1 (Java 21)
- **Why**: standard branżowy enterprise Java; gotowa integracja JPA/PostGIS i ekosystem Spring Security + JWT pod RBAC (F2, NFR5). Wersja 4.1.1 = aktualna stabilna linia (starter `spring-boot-starter-webmvc`).
- **Alternative considered**: Quarkus — przegrał: mniejszy ekosystem integracji i słabsze pokrycie w ofertach pracy, które użytkownik celuje w portfolio.

### 2.2 PostgreSQL 16 + PostGIS 3.4
- **Why**: jedno źródło prawdy dla danych aplikacji I danych przestrzennych (F6, F7) — natywne zapytania geo i indeks GIST; standard branżowy dla GIS.
- **Alternative considered**: MongoDB (geo queries) — przegrał: słabszy model relacyjny dla encji biznesowych (prenumeraty, wersjonowanie), brak transakcji na poziomie schematu.

## 3. Frontend desktop
### 3.1 React 19 + Vite 6 + TypeScript
- **Why**: zgodność z wymaganiami F2/F3 — jeden język (TS) na web i mobile (Expo/RN), co zmniejsza koszt utrzymania; Vite = szybki dev server (hot reload w compose); TS = strict type safety (NFR5).
- **Alternative considered**: Angular 20 — przegrał: cięższy build, mniejsza przenośność kodu do warstwy mobilnej; użytkownik uczy się Angulara osobno (projekt sisie), tu celowo pokazuje szerokość stacku.

### 3.2 Zarządzanie stanem: TanStack Query + Zustand
- **Why**: separacja stanu serwera (cache, refetch — F5 sync) od stanu UI; standard de facto w ekosystemie React 2026.
- **Alternative considered**: Redux Toolkit — żywy i dobry, ale nadmiarowy przy skali tego projektu (query + lekki store UI wystarcza).

## 4. Mobile
### 4.1 Expo (React Native) + EAS
- **Why**: standard workflow RN w 2026 (bare workflow wycofany z mainstreamu); EAS Build = natywne APK/IPA bez lokalnego Android Studio/Xcode; expo-sqlite pod offline-first (NFR1, F3).
- **Alternative considered**: Flutter — przegrał: inny język (Dart), zerowa współdzieloność kodu z warstwą web.

### 4.2 Voice on-device de-DE
- **Why**: F4 wymaga pracy bez internetu w terenie; rozpoznawanie na urządzeniu = zero opłat API i pełna prywatność danych klienta.
- **Alternative considered**: chmurowe ASR (np. Web Speech API) — przegrał: zależność od sieci, naruszenie NFR1.

## 5. AI pipeline
### 5.1 Python 3.12 + FastAPI + LangGraph
- **Why**: ekosystem PDF/AI jest w Pythonie; LangGraph daje orkiestrację wielokrokową z human-in-the-loop (F1: parse → walidacja sum egz. → aprobata) — dokładnie ten wzorzec, którego wymaga proces importu.
- **Alternative considered**: parser w Node.js + Spring AI — przegrały: słabszy ekosystem ekstrakcji dokumentów; orkiestracja grafowa z węzłem aprobaty naturalna dopiero w LangGraph.

## 6. Mapa offline
### 6.1 OpenFreeMap (OSM) + MapLibre GL JS
- **Why**: F6 wymaga mapy **bez API key** i zdolności offline — OSM/OpenFreeMap = otwarte dane, zero kosztów; kafelki cache'owane w IndexedDB (Workbox).
- **Alternative considered**: Google Maps / Mapbox — przegrały: klucz API + koszty per request + polityka prywatności danych klientów.

## 7. Infrastruktura
### 7.1 Docker Compose
- **Why**: NFR3 — zero-config start (`docker compose up -d --build`); środowisko identyczne dev/CI; healthchecki wymuszają kolejność startu.
- **Alternative considered**: skrypty startowe / systemd — przegrały: konfiguracja rozproszona, brak izolacji sieciowej.

### 7.2 Jenkins (CI/CD)
- **Why**: NFR4 + portfolio — self-hosted CI to częste wymaganie w ofertach; `Jenkinsfile` jako pipeline-as-code (build → healthchecki → testy).
- **Alternative considered**: GitHub Actions — dobry wybór, ale zależny od platformy; Jenkins ćwiczy pełną kontrolę nad agentem i Docker-in-Docker.

## 8. Tabela podsumowująca
| Warstwa | Wybór | Kryterium główne | Odrzucona alternatywa |
| :--- | :--- | :--- | :--- |
| Backend API | Spring Boot 4.1.1 / Java 21 | standard branżowy + RBAC/JWT | Quarkus |
| Baza danych | PostgreSQL 16 + PostGIS 3.4 | dane relacyjne + przestrzenne w jednym | MongoDB |
| Desktop FE | React 19 + Vite 6 + TS | współdzielony język z mobile, type safety | Angular 20 |
| Stan (FE) | TanStack Query + Zustand | separacja stanu serwera/UI | Redux Toolkit |
| Mobile | Expo + EAS + expo-sqlite | standard RN 2026, offline-first | Flutter |
| Voice | on-device de-DE (Vosk/Whisper — decyzja otwarta) | praca bez internetu (F4/NFR1) | chmurowe ASR |
| AI pipeline | Python 3.12 + FastAPI + LangGraph | human-in-the-loop, ekosystem PDF/AI | Node.js parser / Spring AI |
| Mapa | OpenFreeMap/OSM + MapLibre GL | bez API key, offline (F6) | Google Maps / Mapbox |
| Orkiestracja | Docker Compose | zero-config start (NFR3) | skrypty/systemd |
| CI/CD | Jenkins | self-hosted, portfolio (NFR4) | GitHub Actions |

> **Uwaga o uczciwości**: „znam tę technologię" jest uzasadnieniem wtórnym (zmniejsza ryzyko), nigdy głównym. W rozmowie: kryterium najpierw, doświadczenie jako wzmocnienie.
