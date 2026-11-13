-- ULTIMA central identity schema draft (PostgreSQL)
-- Apply only after security review and backup/restore setup.
CREATE TABLE IF NOT EXISTS ultima_users (
  id UUID PRIMARY KEY,
  email CITEXT NOT NULL UNIQUE,
  email_verified_at TIMESTAMPTZ,
  display_name TEXT NOT NULL DEFAULT '',
  password_hash TEXT NOT NULL,
  mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
  status TEXT NOT NULL DEFAULT 'pending_verification'
    CHECK (status IN ('pending_verification','active','suspended','deleted')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_login_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS ultima_applications (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  issuer TEXT NOT NULL,
  audience TEXT NOT NULL UNIQUE,
  redirect_uris JSONB NOT NULL DEFAULT '[]'::jsonb,
  scopes JSONB NOT NULL DEFAULT '[]'::jsonb,
  commerce_excluded BOOLEAN NOT NULL DEFAULT FALSE,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ultima_entitlements (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES ultima_users(id) ON DELETE CASCADE,
  app_id TEXT NOT NULL REFERENCES ultima_applications(id),
  plan TEXT NOT NULL CHECK (plan IN ('trial','free_override','premium','blocked')),
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ,
  granted_by UUID REFERENCES ultima_users(id),
  reason TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (ends_at IS NULL OR ends_at > starts_at)
);
CREATE INDEX IF NOT EXISTS idx_ultima_entitlements_user_app
  ON ultima_entitlements(user_id, app_id, starts_at DESC);

CREATE TABLE IF NOT EXISTS ultima_audit_events (
  id BIGSERIAL PRIMARY KEY,
  actor_user_id UUID REFERENCES ultima_users(id),
  target_user_id UUID REFERENCES ultima_users(id),
  app_id TEXT,
  action TEXT NOT NULL,
  reason TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ultima_audit_target_time
  ON ultima_audit_events(target_user_id, created_at DESC);

-- A single verified-user activation time anchors the global 72-hour trial.
ALTER TABLE ultima_users
  ADD COLUMN IF NOT EXISTS trial_started_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS trial_ends_at TIMESTAMPTZ;

-- Each app gets a separate database with a minimal identity reference, e.g.:
-- CREATE TABLE app_user_profiles (
--   ultima_user_id UUID PRIMARY KEY,
--   display_name TEXT NOT NULL DEFAULT '',
--   created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );
