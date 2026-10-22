# Raport testów — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Faza 0 — smoke testy środowiska (2026-10-21)
Metoda: testy ręczne (curl + psql + `docker compose ps`). Testy automatyczne od Fazy 1.

### Wyniki
| # | Test | Oczekiwany wynik | Rzeczywisty wynik | Status |
| :--- | :--- | :--- | :--- | :--- |
| T1 | `docker compose config -q` | walidacja bez błędów | OK (exit 0) | ✅ PASS |
| T2 | Start serwisów (`up -d --build`) | wszystkie kontenery healthy | global-postgis, spring-backend, python-langgraph: `Up (healthy)`; react-vite-frontend, jenkins-ci: `Up` | ✅ PASS |
| T3 | `GET http://localhost:8080/api/health` | status UP + baza połączona | `{"status":"UP","database":"connected","service":"backend-spring"}` | ✅ PASS |
| T4 | `GET http://localhost:8000/health` (ai-pipeline) | status UP | `{"status":"UP","service":"ai-pipeline"}` | ✅ PASS |
| T5 | `GET http://localhost:5173` (frontend) | HTTP 200 | HTTP 200 | ✅ PASS |
| T6 | PostGIS w bazie (`pg_extension`) | rozszerzenie zainstalowane | `postgis\|3.4.3` | ✅ PASS |
| T7 | Jenkins `GET http://localhost:8082/login` | HTTP 200 | HTTP 200 | ✅ PASS |
| T8 | Generator danych testowych | pliki JSON w `test-data/generated/` | `bezirk_8019.json` (61 egz.), `bezirk_8031.json` (61 egz.) | ✅ PASS |

**Wynik: 8/8 PASS.** Środowisko Fazы 0 zweryfikowane end-to-end (frontend → backend → baza).

## Plan testów automatycznych (Faza 1+)
| Warstwa | Framework | Zakres |
| :--- | :--- | :--- |
| Backend | JUnit 5 + Testcontainers (PostGIS) | unit: service; integracja: REST + DB |
| Frontend | Vitest + Testing Library | komponenty, hooki sync |
| AI pipeline | pytest | parser PDF na syntetycznych dokumentach, walidacja sum |
