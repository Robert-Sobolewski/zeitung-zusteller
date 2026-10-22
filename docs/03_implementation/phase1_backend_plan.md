# Phase 1 — Backend Implementation Plan

> **Working agreement.** Implementation happens on branch `dev` (cut from `main`).
> Each step has an owner and verifiable acceptance criteria. After each push to `dev`,
> the diff is reviewed before merging back to `main`.

## Architecture overview (Phase 1 target)

```
com.zeitungszusteller.app
├── ZustellerApplication.java        [done] bootstrap
├── HealthController.java            [done] GET /api/health
├── domain/                          entities + repositories (JPA, Spring Data)
│   ├── entity/                      Zusteller, Bezirk, Street, DeliveryPoint, NewspaperType, Subscription
│   └── repository/                  Spring Data interfaces
├── api/                             REST controllers (import, daily list, sync)
└── security/                        JWT filter + RBAC (ADMIN / MANAGER / ZUSTELLER)
```

**Single source of truth for the schema: `db/init/02-schema.sql`.** Entities must map to it 1:1 —
the file is loaded into every test container, so a mismatch fails tests immediately.

## Steps

| # | Step | Owner | Status | Acceptance criteria |
| :--- | :--- | :--- | :--- | :--- |
| S1 | Test harness: Testcontainers + schema load (`SchemaSmokeTest`) | AIAlex | ✅ done | smoke test green — 7 tables present in disposable PostGIS container |
| S2 | `Zusteller` entity + repository + repository test | **YOU** | ⬜ open | see task below; `mvn test` green locally AND Jenkins pipeline green on `dev` |
| S3 | Remaining entities (Bezirk, Street, DeliveryPoint, NewspaperType, Subscription) + repositories | AIAlex | ⬜ queued | all map to 02-schema.sql; repository tests green |
| S4 | JWT auth + RBAC (three roles per requirements F2) | AIAlex | ⬜ queued | login endpoint; role-filtered access covered by tests |
| S5 | Import endpoint — F1: parser JSON → DB with human-in-the-loop approve/reject | AIAlex | ⬜ queued | end-to-end test using a real parsed Bezirk payload |
| S6 | Daily list endpoint (derived query per domain rule, no stored daily lists) | AIAlex | ⬜ queued | returns only subscriptions valid on the requested date |

## YOUR TASK — S2: `Zusteller` entity + repository

Create exactly **3 files** (do not touch anything else):

### 1. `src/main/java/com/zeitungszusteller/app/domain/entity/Zusteller.java`

Maps table `zustellers` from `db/init/02-schema.sql`:

| Java field | Column | Notes |
| :--- | :--- | :--- |
| `Long id` | `id` | `@Id @GeneratedValue(strategy = GenerationType.IDENTITY)` |
| `String firstName` | `first_name` | NOT NULL — use `@Column(name = "first_name", nullable = false)` |
| `String lastName` | `last_name` | NOT NULL |
| `UserRole role` | `role` | Java enum `UserRole { ADMIN, MANAGER, ZUSTELLER }`; map to the real Postgres ENUM type with `@JdbcTypeCode(SqlTypes.NAMED_ENUM)` (Hibernate 6+) — this makes JPA write native enum values instead of varchar |

### 2. `src/main/java/com/zeitungszusteller/app/domain/repository/ZustellerRepository.java`

```java
public interface ZustellerRepository extends JpaRepository<Zusteller, Long> {
    List<Zusteller> findByRole(UserRole role);   // derived query — no @Query needed
}
```

### 3. `src/test/java/com/zeitungszusteller/app/domain/ZustellerRepositoryTest.java`

Copy the container pattern from `SchemaSmokeTest` (the static `@Bean` with `@ServiceConnection`), then:

1. save one ZUSTELLER and one ADMIN through the repository,
2. assert `findByRole(UserRole.ZUSTELLER)` returns exactly 1 row with the expected name,
3. assert an invalid role is impossible by construction (it's an enum — no test needed, just don't fight it).

### Acceptance criteria (ALL must hold)

1. **Local** — from the repo root:
   ```bash
   docker run --rm \
     -v "F:\2026_code\zeitung-zusteller":/work -w /work/backend-spring \
     -v maven-cache:/root/.m2 \
     -v /var/run/docker.sock:/var/run/docker.sock \
     -e DOCKER_HOST=unix:///var/run/docker.sock -e RYUK_DISABLED=true \
     maven:3.9-eclipse-temurin-21 mvn test
   ```
   → `BUILD SUCCESS`, both tests green (smoke + yours).
2. **CI** — push to `dev` → Jenkins pipeline **green**; the Unit tests stage log shows your test running.
3. No changes to `db/init/*.sql`, `pom.xml`, or main `application.yml`.

## CI/CD — how the automation works (Jenkinsfile)

```
git push dev
   ↓
Unit tests            ← cheapest first; fails fast, no image build yet
   ├─ ai-pipeline:    docker compose run --rm … pytest      (7 parser tests, real-data mounted)
   └─ backend-spring: mvn test in a Maven container         (Testcontainers PostGIS inside)
   ↓ green?
Build images          ← docker compose build
   ↓
Healthcheck           ← compose up + curl :8080 /api/health and :8000/health
```

Notes:
- The Docker socket is mounted into the Maven container so Testcontainers can start PostGIS.
- `maven-cache` (named volume) caches `~/.m2` between runs — first run downloads, later ones are fast.
- `real-data/` is **mounted**, never baked into any image (data must not be published).
- The frontend `vitest` stage joins the pipeline when the first frontend test exists.
