# Test Report — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Phase 0 — Environment Smoke Tests (2026-10-21)
Method: manual tests (curl + psql + `docker compose ps`). Automated testing starts in Phase 1.

### Results
| # | Test | Expected result | Actual result | Status |
| :--- | :--- | :--- | :--- | :--- |
| T1 | `docker compose config -q` | validation without errors | OK (exit 0) | ✅ PASS |
| T2 | Service start (`up -d --build`) | all containers healthy | global-postgis, spring-backend, python-langgraph: `Up (healthy)`; react-vite-frontend, jenkins-ci: `Up` | ✅ PASS |
| T3 | `GET http://localhost:8080/api/health` | status UP + DB connected | `{"status":"UP","database":"connected","service":"backend-spring"}` | ✅ PASS |
| T4 | `GET http://localhost:8000/health` (ai-pipeline) | status UP | `{"status":"UP","service":"ai-pipeline"}` | ✅ PASS |
| T5 | `GET http://localhost:5173` (frontend) | HTTP 200 | HTTP 200 | ✅ PASS |
| T6 | PostGIS in database (`pg_extension`) | extension installed | `postgis\|3.4.3` | ✅ PASS |
| T7 | Jenkins `GET http://localhost:8082/login` | HTTP 200 | HTTP 200 | ✅ PASS |
| T8 | Test data generator | JSON files in `test-data/generated/` | `bezirk_8019.json` (61 copies), `bezirk_8031.json` (61 copies) | ✅ PASS |

**Result: 8/8 PASS.** Phase 0 environment verified end-to-end (frontend → backend → database).

## Automated Test Plan (Phase 1+)
| Layer | Framework | Scope |
| :--- | :--- | :--- |
| Backend | JUnit 5 + Testcontainers (PostGIS) | unit: services; integration: REST + DB |
| Frontend | Vitest + Testing Library | components, sync hooks |
| AI pipeline | pytest | PDF parser on synthetic documents, copies-sum validation |
