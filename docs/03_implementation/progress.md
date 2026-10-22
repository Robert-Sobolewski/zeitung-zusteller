# Postęp implementacji — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Status modułów (Faza 0)
| Moduł | Status | Dowód weryfikacji |
| :--- | :--- | :--- |
| `docker-compose.yml` (5 serwisów + profile ci/maps) | ✅ zakończone | `docker compose config -q` OK; wszystkie kontenery `Up (healthy)` |
| `backend-spring/` — skeleton Spring Boot 4.1.1, `GET /api/health` z pingiem bazy | ✅ zakończone | `curl :8080/api/health` → `{"status":"UP","database":"connected"}` |
| `frontend-web/` — skeleton React 19 + Vite 6 + TS (strict) | ✅ zakończone | `curl :5173` → HTTP 200; App wyświetla status backendu |
| `ai-pipeline/` — skeleton FastAPI, `GET /health` | ✅ zakończone | `curl :8000/health` → UP |
| `jenkins-ci` + `Jenkinsfile` (build → healthchecki) | ✅ kontener działa; pipeline zdefiniowany | `curl :8082/login` → HTTP 200; uruchomienie w UI = Faza 1 |
| `db/init/01-postgis.sql` — rozszerzenie PostGIS | ✅ zakończone | `psql`: `postgis\|3.4.3` |
| `tools/generate_testdata.py` — generator syntetycznych bezirków | ✅ zakończone | wyjście: `bezirk_8019.json`, `bezirk_8031.json` (po 61 egz.) |
| `.gitignore` / `.gitattributes` / README | ✅ zakończone | `real-data/` poza git; EOL znormalizowane |
| `mobile-app/` — plan + README | ⏳ Faza 4 | tylko dokumentacja |
| `maps/` — serwer kafelków (profil `maps`) | ⏳ Faza 5 | `config.json` = placeholder do weryfikacji |

## Dług techniczny
1. **Brak autoryzacji** na backendzie (zamknięcie: Faza 1, JWT + RBAC).
2. **Brak encji/migracji** — `ddl-auto: update`; przejście na Flyway w Fazie 1 (decyzja otwarta).
3. Frontend bez biblioteki stanu (TanStack Query/Zustand) — Faza 2.
4. `maps/config.json` niezweryfikowany względem schematu tileserver-gl — Faza 5.
5. Pipeline Jenkins zdefiniowany, ale jeszcze nie uruchomiony w UI — Faza 1.
