# Adapter Contract

Adapters make WorkOverCV discoverable to specific agent environments. They do
not redefine the workflow, create a second CLI, or alter output paths.

Each adapter must point to:

- `workflows/workovercv.yml`
- `docs/runtime_contract.md`
- `docs/manifest_contract.md`
- schemas under `schemas/`
- the shared `workovercv` CLI

Adapters must not:

- analyze repositories outside `review_scope.yml`
- invent another report format
- mark compatibility as tested without an end-to-end smoke run
- infer protected/private traits
- treat stars, forks, or followers as competence metrics

The Codex adapter status is recorded in `adapters/status.yml`.
