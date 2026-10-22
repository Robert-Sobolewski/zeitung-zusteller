# Security Model — Zeitungszusteller Platform
Last Updated: 2026-10-21

## Current State (Phase 0)
**No authentication** — a known gap, closed in Phase 1. Endpoint `GET /api/health` is public (compose health checks + status display). The database is reachable only inside the Docker network (`app-network`) plus host port 5432 (dev only).

## Target Model (Phase 1+)
### Backend — Spring Security + JWT
- Login: `POST /api/auth/login` → JWT (short-lived access token) + refresh token.
- **RBAC**:
  | Role | Permissions |
  | :--- | :--- |
  | ADMIN | all Bezirke, PDF import, management of delivery persons and newspaper types |
  | ZUSTELLER | own Bezirk only: daily route view, change reports (Zugang/Abgang) |
- The authoritative enforcement point is the backend (`@PreAuthorize` / filters). Client-side guards are UX convenience only.

### SPA Layer (desktop web + mobile)
- **Open decision** (roadmap): token storage — default plan: access token in memory (React state/context), refresh token in an **httpOnly cookie** (XSS resilience). Rejected alternative for the start: `localStorage` — readable from JS, risky under XSS; if chosen later it is a consciously accepted risk with a named hardening step (CSP + sanitization).
- An interceptor/fetch wrapper attaches `Authorization: Bearer <token>` to every API request.
- UI route guards hide inaccessible views — they do not replace backend RBAC.

### Mobile (Phase 4)
- Token on the phone: secure storage (expo-secure-store); outbox sync sent with authentication.
- Offline data (daily route) = a slice of ZUSTELLER permissions — the phone never sees other Bezirke.

## Threats and Mitigations
| Threat | Mitigation |
| :--- | :--- |
| XSS → token theft | refresh in httpOnly cookie, CSP (Phase 2) |
| Sync conflicts from concurrent changes | `version` field + resolution by `updated_at` on the backend |
| Real data leaking into the repo | `.gitignore`: `real-data/`, `test-data/generated/`; synthetic test data generator |
