# Roadmapa — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Faza 0 — Szkielet repo + Docker + CI ✅ (zakończona 2026-10-21)
- [x] Struktura modułów: `backend-spring/`, `frontend-web/`, `mobile-app/`, `ai-pipeline/`, `tools/`
- [x] `.gitignore` z `real-data/`; generator syntetycznych danych testowych (zweryfikowany)
- [x] `docker-compose.yml`: PostGIS + Spring Boot + FastAPI + Vite (+ profile ci/maps), healthchecki
- [x] `Jenkinsfile` (build → healthchecki); kontener Jenkins działa
- [x] Dokumentacja IHK (`docs/`) — analiza, projekt, postęp, raport testów, roadmapa
- ✅ Akceptacja: `docker compose up -d --build` podnosi platformę; smoke testy 8/8 PASS (patrz `04_quality_assurance/testing_report.md`)

## Faza 1 — AI parser + API importu
- [ ] LangGraph pipeline: PDF → JSON (regex + LLM fallback) → walidacja sum egz. → węzeł aprobaty (human-in-the-loop)
- [ ] Spring Boot: encje JPA wg `02_design/database_model.md`, repozytoria, REST CRUD, JWT login, role ADMIN/ZUSTELLER
- [ ] Migracje bazy (Flyway — decyzja otwarta)
- [ ] Uruchomienie pipeline'a Jenkins w UI + etap testów
- ✅ Akceptacja: import realnego PDF-u przez UI z podglądem i aprobatą; testy jednostkowe + integracyjne (Testcontainers)

## Faza 2 — Desktop app (React)
- [ ] TanStack Query + Zustand; widoki: lista bezirków, trasa dnia, zarządzanie dostawcami, log zmian
- [ ] Warstwa bezpieczeństwa SPA wg `02_design/security_model.md` (token storage, interceptor, guardy)
- ✅ Akceptacja: pełny workflow ADMIN od PDF do DB w przeglądarce

## Faza 3 — Planowanie trasy
- [ ] Heurystyka Python: 1 osoba = strona kierowcy → powrót drugą stroną (wyjątek ≤N domów); 2 osoby = podział tras
- ✅ Akceptacja: endpoint zwraca uporządkowaną listę przystanków per przejazd; testy na danych testowych

## Faza 4 — Mobile app (Expo)
- [ ] Trasa dnia offline (expo-sqlite); widok „bieżący klient" podczas jazdy
- [ ] Voice on-device de-DE → NLU → zmiana do outboxa; sync z API (outbox + wersjonowanie)
- ✅ Akceptacja: tryb samolotowy — pełna trasa działa; po powrocie online zmiany synchronizują się bez konfliktów

## Faza 5 — Mapa offline + polerowanie
- [ ] MapLibre GL + OpenFreeMap, cache kafelek w IndexedDB (Workbox) lub lokalny tileserver-gl (decyzja otwarta)
- [ ] Podświetlenie bieżącej ulicy/stopu; deploy całości przez Jenkins na serwer
- ✅ Akceptacja: mapa trasy działa offline; pipeline CI/CD end-to-end

## Open Decisions
| # | Decyzja | Opcje | Kiedy rozstrzygnąć |
| :--- | :--- | :--- | :--- |
| OD1 | Migracje bazy | Flyway vs `ddl-auto: update` | Faza 1 (przed encjami) |
| OD2 | Voice engine | Vosk (lekki, w pełni offline) vs Whisper (dokładniejszy, cięższy model) | Faza 4 |
| OD3 | Cache map offline | Workbox/IndexedDB po stronie klienta vs lokalny tileserver-gl (`maps/`) | Faza 5 |
| OD4 | Token storage SPA | pamięć + httpOnly cookie (plan domyślny) vs localStorage (ryzyko XSS, prostsze) | Faza 2 |
