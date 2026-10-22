# Technology Selection & Rationale — Zeitungszusteller Platform
Last Updated: 2026-10-21

## 1. Selection Criteria
Every decision is evaluated against:
1. **Industry standard** — what enterprise teams actually run in production (IHK relevance)
2. **Requirements fit** — does it satisfy a requirement from `01_analysis/requirements.md`?
3. **Ecosystem & longevity** — active maintenance, LTS, community size
4. **Maintainability** — readable, testable, hand-over friendly

## 2. Backend API
### 2.1 Spring Boot 4.1.1 (Java 21)
- **Why**: industry standard for enterprise Java; ready-made JPA/PostGIS integration and the Spring Security + JWT ecosystem for RBAC (F2, NFR5). Version 4.1.1 is the current stable line (`spring-boot-starter-webmvc`).
- **Alternative considered**: Quarkus — lost: smaller integration ecosystem and weaker coverage in the job market this portfolio targets.

### 2.2 PostgreSQL 16 + PostGIS 3.4
- **Why**: single source of truth for application data AND spatial data (F6, F7) — native geo queries and GIST indexes; industry standard for GIS.
- **Alternative considered**: MongoDB (geo queries) — lost: weaker relational modeling for business entities (subscriptions, versioning), no schema-level transactions.

## 3. Desktop Frontend
### 3.1 React 19 + Vite 6 + TypeScript
- **Why**: fits F2/F3 — one language (TS) shared between web and mobile (Expo/RN), reducing maintenance cost; Vite = fast dev server (hot reload in compose); TS strict mode for type safety (NFR5).
- **Alternative considered**: Angular 20 — lost: heavier build, less code portability to the mobile layer; the user is learning Angular separately (sisie project) and deliberately shows stack breadth here.

### 3.2 State Management: TanStack Query + Zustand
- **Why**: separation of server state (cache, refetch — F5 sync) from UI state; de-facto standard in the React ecosystem for 2026.
- **Alternative considered**: Redux Toolkit — alive and well, but overkill at this project's scale (query layer + a lightweight UI store suffice).

## 4. Mobile
### 4.1 Expo (React Native) + EAS
- **Why**: the standard RN workflow in 2026 (bare workflow is out of mainstream); EAS Build = native APK/IPA without local Android Studio/Xcode; expo-sqlite for offline-first (NFR1, F3).
- **Alternative considered**: Flutter — lost: different language (Dart), zero code sharing with the web layer.

### 4.2 On-device Voice (de-DE)
- **Why**: F4 requires working without internet in the field; on-device recognition = no API costs and full customer-data privacy.
- **Alternative considered**: cloud ASR (e.g. Web Speech API) — lost: network dependency, violates NFR1.

## 5. AI Pipeline
### 5.1 Python 3.12 + FastAPI + LangGraph
- **Why**: the PDF/AI ecosystem is in Python; LangGraph provides multi-step orchestration with human-in-the-loop (F1: parse → copies-sum validation → approval) — exactly the pattern the import process requires.
- **Alternative considered**: Node.js parser / Spring AI — lost: weaker document-extraction ecosystem; graph orchestration with an approval node is natural only in LangGraph.

## 6. Offline Maps
### 6.1 OpenFreeMap (OSM) + MapLibre GL JS
- **Why**: F6 requires a map **without API key** and offline capability — OSM/OpenFreeMap = open data, zero cost; tiles cached in IndexedDB (Workbox).
- **Alternative considered**: Google Maps / Mapbox — lost: API key + per-request costs + customer-data privacy policies.

## 7. Infrastructure
### 7.1 Docker Compose
- **Why**: NFR3 — zero-config start (`docker compose up -d --build`); identical dev/CI environment; health checks enforce startup ordering.
- **Alternative considered**: startup scripts / systemd — lost: scattered configuration, no network isolation.

### 7.2 Jenkins (CI/CD)
- **Why**: NFR4 + portfolio — self-hosted CI is a frequent job requirement; `Jenkinsfile` as pipeline-as-code (build → health checks → tests).
- **Alternative considered**: GitHub Actions — solid choice, but platform-dependent; Jenkins exercises full control over the agent and Docker-in-Docker.

## 8. Summary Table
| Layer | Choice | Primary criterion | Rejected alternative |
| :--- | :--- | :--- | :--- |
| Backend API | Spring Boot 4.1.1 / Java 21 | industry standard + RBAC/JWT | Quarkus |
| Database | PostgreSQL 16 + PostGIS 3.4 | relational + spatial data in one | MongoDB |
| Desktop FE | React 19 + Vite 6 + TS | shared language with mobile, type safety | Angular 20 |
| FE state | TanStack Query + Zustand | server/UI state separation | Redux Toolkit |
| Mobile | Expo + EAS + expo-sqlite | RN standard 2026, offline-first | Flutter |
| Voice | on-device de-DE (Vosk/Whisper — open decision) | works without internet (F4/NFR1) | cloud ASR |
| AI pipeline | Python 3.12 + FastAPI + LangGraph | human-in-the-loop, PDF/AI ecosystem | Node.js parser / Spring AI |
| Maps | OpenFreeMap/OSM + MapLibre GL | no API key, offline (F6) | Google Maps / Mapbox |
| Orchestration | Docker Compose | zero-config start (NFR3) | scripts/systemd |
| CI/CD | Jenkins | self-hosted, portfolio (NFR4) | GitHub Actions |

> **Note on honesty**: "I know this technology" is a legitimate *secondary* factor (team skill reduces risk), never the primary justification. In an interview: lead with the criterion, add experience as reinforcement — not as the reason.
