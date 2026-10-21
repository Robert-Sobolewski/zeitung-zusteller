# Zeitungszusteller Platform

Platforma dla firmy dystrybucji prasy: import dokumentów dostawy (PDF Tagesliste),
planowanie tras, offline mobile app dla dostawcy.

## Struktura
```
├── backend-spring/      # Java 21 + Spring Boot 4.x + Maven
├── frontend-web/        # Node 26 + Vite + TypeScript (+ MapLibre GL — Faza 5)
├── mobile-app/          # Expo + EAS + Android Voice (Faza 4)
├── ai-pipeline/         # Python 3.12 + LangGraph + FastAPI
├── db/init/             # Skrypty init PostGIS
├── maps/                # Dane dla lokalnego serwera kafelków (opcjonalne)
├── tools/               # Generator danych testowych
├── real-data/           # DANE REALNE — NIGDY do git (.gitignore)
├── docker-compose.yml
└── Jenkinsfile
```

## Start (1 komenda)
```bash
docker compose up -d --build
```
- Backend: http://localhost:8080/api/health
- Frontend dev: http://localhost:5173
- AI pipeline: http://localhost:8000/health
- PostGIS: localhost:5432 (dev_user/dev_password/app_database)

## Dane testowe
```bash
python tools/generate_testdata.py   # generuje test-data/generated/*.json
```
Dane realne (`real-data/`) nigdy nie wchodzą do git — generator tworzy syntetyczne bezirki.

## Fazy
- [x] Faza 0: szkielet repo + Docker + CI (ten commit)
- [ ] Faza 1: AI parser PDF → JSON + API importu + RBAC/JWT
- [ ] Faza 2: Desktop app (React) — workflow ADMIN od PDF do DB
- [ ] Faza 3: Planowanie trasy (1/2 osoby, strony ulicy)
- [ ] Faza 4: Mobile Expo — trasa dnia offline + voice Zugang/Abgang
- [ ] Faza 5: Mapa offline (MapLibre + OpenFreeMap cache)

Szczegóły: `PLAN.md`
