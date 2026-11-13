# ULTIMA Unify

Central account and website-profile portal for the ULTIMA network.

## Features
- Shared account registration and login
- Password hashing (bcrypt) and CSRF protection
- User-owned, per-website profile records
- Server-side SUPERADMIN role assignment using SUPERADMIN_EMAIL
- PostgreSQL in production; SQLite only for local development
- Health endpoint at /health

## Render environment
Set these values in Render:
- SECRET_KEY: long random secret (never commit it)
- DATABASE_URL: Render PostgreSQL internal connection URL
- SUPERADMIN_EMAIL: verified administrator email

## Important
This is the initial foundation, not yet a complete SSO identity provider. Before connecting production websites, add verified email flows, MFA, rate limiting, audit logs, signed OAuth/OIDC tokens, consent-based site registration, backups, and secure account recovery. Do not store payment credentials or secrets in user profiles.
