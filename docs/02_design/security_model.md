# Model bezpieczeństwa — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Stan obecny (Faza 0)
**Brak autoryzacji** — świadoma luka zamknięta w Fazie 1. Endpoint `GET /api/health` jest publiczny
(healthchecki compose + podgląd statusu). Baza dostępna tylko w sieci Docker (`app-network`) + port hosta 5432 (tylko dev).

## Model docelowy (Faza 1+)
### Backend — Spring Security + JWT
- Logowanie: `POST /api/auth/login` → JWT (access token, krótki TTL) + refresh token.
- **RBAC**:
  | Rola | Uprawnienia |
  | :--- | :--- |
  | ADMIN | wszystkie bezirki, import PDF, zarządzanie dostawcami i typami gazet |
  | ZUSTELLER | tylko własny bezirk: podgląd trasy dnia, zgłaszanie zmian (Zugang/Abgang) |
- Autorytatywny punkt egzekwowania = backend (`@PreAuthorize` / filtry). Klienckie guardy są wyłącznie wygodą UX.

### Warstwa SPA (desktop web + mobile)
- **Decyzja otwarta** (roadmapa): przechowywanie tokena — plan domyślny: access token w pamięci (React state/context), refresh w **httpOnly cookie** (odporność na XSS). Alternatywa odrzucona na start: `localStorage` — czytelny z JS, ryzyko przy XSS; jeśli zostanie wybrany, jest to świadomie zaakceptowane ryzyko z nazwanym krokiem hardeningu (CSP + sanitizacja).
- Interceptor/fetch wrapper dodaje `Authorization: Bearer <token>` do każdego żądania API.
- Route guardy w UI ukrywają niedostępne widoki — nie zastępują RBAC backendu.

### Mobile (Faza 4)
- Token po stronie telefonu: bezpieczny storage (expo-secure-store), outbox sync wysyłany z autoryzacją.
- Dane offline (trasa dnia) = wycinek uprawnień ZUSTELLERA — telefon nie widzi innych bezirków.

## Zagrożenia i mitigacje
| Zagrożenie | Mitigacja |
| :--- | :--- |
| XSS → kradzież tokena | refresh w httpOnly cookie, CSP (Faza 2) |
| Konflikty sync przy równoległych zmianach | wersjonowanie `version` + rozstrzyganie po `updated_at` na backendzie |
| Dane realne w repo | `.gitignore`: `real-data/`, `test-data/generated/`; generator syntetycznych danych |
