# ULTIMA Character AI Studio and Update-KI-Matrix

## Character AI Studio

Open the studio at `/ultima-ai/characters/`.

A user-defined character contains:
- name and role / archetype
- personality
- speaking style
- areas of expertise
- background story
- goals and tasks
- behavioral rules

The current first release stores profiles in the browser's localStorage. It supports create, edit, delete, JSON export and JSON import. Chat requests pass the selected profile to the ULTIMA AI chat endpoint, which builds a bounded persona context and applies the platform's safety and approval rules after the user-defined content.

Important limitations:
- Profiles are local to the browser and are not synced between devices or accounts.
- Chat requires the configured model provider and can incur provider usage charges.
- The feature is implemented in ULTIMA AI; each external AI service still needs its own adapter and integration test before it can be called integrated.

## Update-KI-Matrix

Canonical source: `data/ai-feature-matrix.json`
Changelog: `data/ai-feature-changelog.json`
Human-readable lookup: `/updates/`
Machine-readable endpoint: `/ultima-ai/api/feature-matrix`
Machine-readable changelog: `/ultima-ai/api/update-log`

Every feature has a stable ID, description, category, implementation stage, release version and rollout note. The matrix is the shared implementation contract for the owned AI network.

## Rollout standard for each owned AI

1. Read the central matrix and select the feature IDs supported by the target service.
2. Inspect that repository and its current provider API before changing anything.
3. Add the feature without replacing existing system prompts, persona identities, routes or project-specific behavior.
4. Add the feature ID and version to the service's local capability response.
5. Add an integration test and a health check.
6. Open a pull request or isolated branch; do not silently deploy to production.
7. Verify the deployed service and record the exact repository, commit, deploy and test result in the central changelog.

Protected exclusions remain excluded: Rothshild, Lyca, BullRun Apparel, Lyca Parfum and Sneaker. Autokrypt remains unchanged.

## Next stages

- Account-backed encrypted character synchronization with consent, export and deletion.
- Multi-character roundtables and agent orchestration.
- Automated GitHub repository discovery and staged pull requests.
- Per-service API health checks and adapter verification.
