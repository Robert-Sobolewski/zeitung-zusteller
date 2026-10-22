-- 02-schema.sql — application schema (PostgreSQL 16 + PostGIS)
-- Runs automatically on first volume creation (after 01-postgis.sql).
-- Mirrors docs/02_design/database_model.md.

-- ---------------------------------------------------------------------------
-- Enum types (stronger than TEXT: the DB rejects invalid values at INSERT)
-- ---------------------------------------------------------------------------
CREATE TYPE user_role AS ENUM ('ADMIN', 'MANAGER', 'ZUSTELLER');
CREATE TYPE delivery_side AS ENUM ('LEFT', 'RIGHT');
CREATE TYPE subscription_type AS ENUM ('ANNUAL', 'MONTHLY', 'PAUSE');

-- ---------------------------------------------------------------------------
-- Delivery persons (company staff)
-- ---------------------------------------------------------------------------
CREATE TABLE zustellers (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    role       user_role NOT NULL DEFAULT 'ZUSTELLER'
);

-- ---------------------------------------------------------------------------
-- Districts. One delivery person can deliver many districts (1:M).
-- NOTE: F7 (2-person route split) will require a junction table
-- bezirk_zusteller — kept 1:M for now to match the documented model.
-- ---------------------------------------------------------------------------
CREATE TABLE bezirke (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code         TEXT NOT NULL UNIQUE,          -- e.g. '8019'
    name         TEXT,                          -- area/city label from the PDF header
    zusteller_id INTEGER NOT NULL REFERENCES zustellers(id)
);

-- ---------------------------------------------------------------------------
-- Streets within a district; route_order = chronological order from the PDF
-- (the document order IS the delivery route order).
-- ---------------------------------------------------------------------------
CREATE TABLE streets (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bezirk_id   INTEGER NOT NULL REFERENCES bezirke(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,                  -- e.g. 'Am Holzberg'
    route_order INTEGER,                        -- 1..N within the district route
    UNIQUE (bezirk_id, name)                    -- a street appears once per district
);

-- ---------------------------------------------------------------------------
-- Physical delivery points (address on the route).
-- house_number is TEXT: real data contains letters ('2B').
-- ---------------------------------------------------------------------------
CREATE TABLE delivery_points (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    street_id    INTEGER NOT NULL REFERENCES streets(id) ON DELETE CASCADE,
    house_number TEXT NOT NULL,                 -- '1', '2B', ...
    side         delivery_side,                 -- driver's side / opposite side
    last_name    TEXT NOT NULL,                 -- surname (primary in the route view)
    first_name   TEXT,                          -- given name(s), may carry suffixes ('Walter Sen')
    active       BOOLEAN NOT NULL DEFAULT TRUE, -- address still a delivery point
    version      INTEGER NOT NULL DEFAULT 0,    -- sync versioning (F5 conflict resolution)
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    geom         geometry(Point, 4326),         -- WGS84 coordinates (geocoding: Phase 5)
    CHECK (version >= 0)
);

CREATE INDEX idx_delivery_points_street ON delivery_points (street_id);
CREATE INDEX idx_delivery_points_geom   ON delivery_points USING GIST (geom);

-- ---------------------------------------------------------------------------
-- Newspaper types. Code is the canonical identifier from the PDF, e.g.
-- 'ME-OBB/AUSGABE', 'FR-FAZ-MSA/AUSGABE' (multi-segment codes exist).
-- ---------------------------------------------------------------------------
CREATE TABLE newspaper_types (
    code TEXT PRIMARY KEY,                      -- e.g. 'ME-OBB/AUSGABE'
    name TEXT                                   -- human-readable label
);

-- ---------------------------------------------------------------------------
-- Subscriptions — time-bounded (domain rule: the daily list is DERIVED).
--   Zugang = new row with valid_from = today
--   Abgang = valid_until = yesterday
--   Urlaub = PAUSE gap in validity; the subscription resumes automatically.
-- Daily list query: WHERE current_date BETWEEN valid_from AND COALESCE(valid_until, '9999-12-31')
-- ---------------------------------------------------------------------------
CREATE TABLE subscriptions (
    id                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    delivery_point_id INTEGER NOT NULL REFERENCES delivery_points(id) ON DELETE CASCADE,
    newspaper_code    TEXT NOT NULL REFERENCES newspaper_types(code),
    quantity          INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),  -- 'Ex.' from the PDF
    sub_type          subscription_type NOT NULL DEFAULT 'ANNUAL',
    valid_from        DATE NOT NULL,
    valid_until       DATE,                     -- NULL = open-ended (annual)
    version           INTEGER NOT NULL DEFAULT 0,
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (valid_until IS NULL OR valid_until >= valid_from),
    CHECK (version >= 0)
);

CREATE INDEX idx_subscriptions_point ON subscriptions (delivery_point_id);
CREATE INDEX idx_subscriptions_validity ON subscriptions (valid_from, valid_until);

-- ---------------------------------------------------------------------------
-- Sync outbox — phone -> desktop change events with acknowledgement (F5).
-- synced_at IS NULL = pending; the sync endpoint drains and acknowledges.
-- ---------------------------------------------------------------------------
CREATE TABLE sync_outbox (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    zusteller_id INTEGER NOT NULL REFERENCES zustellers(id),
    payload      JSONB NOT NULL,                -- change event (Zugang/Abgang/Urlaub)
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    synced_at    TIMESTAMPTZ                    -- set when acknowledged by the backend
);

CREATE INDEX idx_sync_outbox_pending ON sync_outbox (zusteller_id, synced_at) WHERE synced_at IS NULL;
