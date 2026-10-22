# Implementation Progress — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Module Status (Phase 0)
| Module | Status | Verification evidence |
| :--- | :--- | :--- |
| `docker-compose.yml` (5 services + ci/maps profiles) | ✅ done | `docker compose config -q` OK; all containers `Up (healthy)` |
| `backend-spring/` — Spring Boot 4.1.1 skeleton, `GET /api/health` with DB ping | ✅ done | `curl :8080/api/health` → `{"status":"UP","database":"connected"}` |
| `frontend-web/` — React 19 + Vite 6 + TS (strict) skeleton | ✅ done | `curl :5173` → HTTP 200; App displays backend status |
| `ai-pipeline/` — FastAPI + LangGraph Tagesliste parser (PDF→JSON, copy-total validation) | ✅ done | pytest 7/7 PASS on real PDFs; totals match document (84/37/54/35) |
| `jenkins-ci` + `Jenkinsfile` (build → health checks) | ✅ container running; pipeline defined | `curl :8082/login` → HTTP 200; UI run = Phase 1 |
| `db/init/01-postgis.sql` — PostGIS extension | ✅ done | `psql`: `postgis\|3.4.3` |
| `tools/generate_testdata.py` — synthetic Bezirk generator | ✅ done | output: `bezirk_8019.json`, `bezirk_8031.json` (61 copies each) |
| `.gitignore` / `.gitattributes` / README | ✅ done | `real-data/` outside git; EOL normalized |
| `mobile-app/` — plan + README | ⏳ Phase 4 | documentation only |
| `maps/` — tile server (profile `maps`) | ⏳ Phase 5 | `config.json` = placeholder to verify |

## Technical Debt
1. **No authentication** on the backend (closure: Phase 1, JWT + RBAC).
2. **No entities/migrations** — `ddl-auto: update`; move to Flyway in Phase 1 (open decision).
3. Frontend without a state library (TanStack Query/Zustand) — Phase 2.
4. `maps/config.json` unverified against the tileserver-gl schema — Phase 5.
5. Jenkins pipeline defined but not yet executed in the UI — Phase 1.
