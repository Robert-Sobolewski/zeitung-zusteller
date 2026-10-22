# Roadmap — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Phase 0 — Repo Skeleton + Docker + CI ✅ (completed 2026-10-21)
- [x] Module structure: `backend-spring/`, `frontend-web/`, `mobile-app/`, `ai-pipeline/`, `tools/`
- [x] `.gitignore` with `real-data/`; synthetic test data generator (verified)
- [x] `docker-compose.yml`: PostGIS + Spring Boot + FastAPI + Vite (+ ci/maps profiles), health checks
- [x] `Jenkinsfile` (build → health checks); Jenkins container running
- [x] IHK documentation (`docs/`) — analysis, design, progress, test report, roadmap
- ✅ Acceptance: `docker compose up -d --build` brings up the platform; smoke tests 8/8 PASS (see `04_quality_assurance/testing_report.md`)

## Phase 1 — AI Parser + Import API
- [ ] LangGraph pipeline: PDF → JSON (regex + LLM fallback) → copies-sum validation → approval node (human-in-the-loop); import = current subscription state, field changes applied as validity-period updates (Zugang/Abgang/Urlaub)
- [ ] Spring Boot: JPA entities per `02_design/database_model.md`, repositories, REST CRUD, JWT login, ADMIN/ZUSTELLER roles
- [ ] Database migrations (Flyway — open decision)
- [ ] Jenkins pipeline run in UI + test stage
- ✅ Acceptance: real PDF imported through the UI with preview and approval; unit + integration tests (Testcontainers)

## Phase 2 — Desktop App (React)
- [ ] TanStack Query + Zustand; views: Bezirk list, daily route, delivery-person management, change log
- [ ] SPA security layer per `02_design/security_model.md` (token storage, interceptor, guards)
- ✅ Acceptance: full ADMIN workflow from PDF to DB in the browser

## Phase 3 — Route Planning
- [ ] Python heuristics: 1 person = driver's side → return on the opposite side (exception ≤N houses); 2 persons = route split
- ✅ Acceptance: endpoint returns an ordered stop list per pass; tests on synthetic data

## Phase 4 — Mobile App (Expo)
- [ ] Offline daily route (expo-sqlite); "current customer" view while driving
- [ ] On-device de-DE voice → NLU → change into outbox; API sync (outbox + versioning)
- ✅ Acceptance: airplane mode — full route works; after returning online, changes sync without conflicts

## Phase 5 — Offline Maps + Polish
- [ ] MapLibre GL + OpenFreeMap, tile cache in IndexedDB (Workbox) or local tileserver-gl (open decision)
- [ ] Highlight current street/stop; deploy the whole stack via Jenkins to a server
- ✅ Acceptance: route map works offline; CI/CD pipeline end-to-end

## Open Decisions
| # | Decision | Options | Resolve in |
| :--- | :--- | :--- | :--- |
| OD1 | Database migrations | Flyway vs `ddl-auto: update` | Phase 1 (before entities) |
| OD2 | Voice engine | Vosk (light, fully offline) vs Whisper (more accurate, heavier model) | Phase 4 |
| OD3 | Offline map cache | client-side Workbox/IndexedDB vs local tileserver-gl (`maps/`) | Phase 5 |
| OD4 | SPA token storage | memory + httpOnly cookie (default plan) vs localStorage (XSS risk, simpler) | Phase 2 |
