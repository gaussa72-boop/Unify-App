# AURELIS / ULTIMA – Crypto Network & Update Manifest
Version: 1.0
Date: 2026-11-26
Status: Prepared in repository; not automatically installed into all services.

## Project inventory (verified Render inventory)
- AUREALIS OMNIA — https://aurealis-omnia.onrender.com — web service, repo gaussa72-boop/Aurealis-Creative-AI, free plan.
- Aurelis Investment — https://aurelis-investment.onrender.com — static site, repo gaussa72-boop/Unify-App, publish path aurelis-investment.
- ATE REA Exchange — https://ate-rea-exchange.onrender.com — static site, repo gaussa72-boop/Kryptoaurora, publish path ate-rea-exchange.
- Krypto-Aurora is a project/category identity associated with the trading/meme-coin area; no separate Render service verified.
- Aurealis-Trading repository was previously found empty; no deployed service verified.

## Category routes
/categories/, /bitcoin-mining/, /crypto-markets/, /trading/, /meme-coins/, /exchange/, /wallets/, /tokens/, /staking/, /investment/, /block-explorer/.

## Personality preservation rules
1. Each AI service retains its own system prompt, role, voice, memory, safety boundaries, and product-specific configuration.
2. The Update Matrix distributes only versioned, compatible shared updates; it must never overwrite personality prompts or secrets.
3. Each receiving service must explicitly opt in, validate the manifest, stage changes, run tests, and report its own deployment status.
4. No service is considered integrated merely because it appears in this inventory.
5. Never expose API keys, tokens, passwords, wallet private keys, or seed phrases in manifests, logs, source control, or shared update payloads.

## OMNIA mining safety and status
- Mining mode selected by owner: ASIC hosting.
- BTC receive address configured as a proposal only: bc1q4q7lujkr8mcv9e7suet524uxjfwlaxm7aelq5y
- Automatic payouts: disabled; no release authorization.
- Internal simulation is not real mining and creates no BTC.
- A public Bitcoin block feed is network-wide public data, not evidence of owner mining.
- External pool adapter, authenticated payout gateway, persistent DB wiring, and payout verification are required before any payout can be enabled.

## Persistence and operations
- Existing Render Postgres: aurealis-omnia-mining-db, Frankfurt, basic_1gb, status available.
- Database attachment / DATABASE_URL wiring has not yet been verified. DB IP allowlist is empty; direct query attempt may be blocked.
- Public block archive code exists, but durable persistence and automatic scheduled collection are not yet verified.
- Do not create paid cron jobs, upgrade plans, or additional resources without explicit cost approval.

## ASIC hosting due diligence
Compare total monthly cost, kWh tariff, miner power draw, pool fee, downtime SLA, cooling, repair/replacement, contract duration, deposit, shipping/customs, VAT, payout threshold, and provider legal entity. Do not place an order or transfer funds without written contract and owner approval.
