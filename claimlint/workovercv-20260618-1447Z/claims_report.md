# ClaimLint Claims Report

## Executive Summary

- Repository: .
- Manifest: claimlint/input_manifest.yml
- Workflow version: 0.1.0
- Run timestamp: 2026-06-18T14:47:04+00:00
- Claim count: 59
- Auditable claim count: 30
- Repository claim surface status: high_claim_surface
- High-importance claims: 4
- Claims requiring action: 1
- Boundary/non-goal statements: 25
- Suppressed reference or low-quality records: 4

Static repository review only unless otherwise stated. Smoke tests are not metric reproduction, and external hardware/environment claims may require human review.

Rights, licensing, dataset redistribution, and artifact distribution claims are separated from technical, scientific, and model-performance claims by `claim_domain`.

## Verdict Summary

| Verdict | Count |
| --- | ---: |
| unsupported | 1 |
| ambiguous | 29 |
| supported | 29 |

## Domain Summary

| Domain | Count | Auditable | High Importance | Requiring Action | Suppressed/Reference |
| --- | ---: | ---: | ---: | ---: | ---: |
| Model Performance | 3 | 3 | 3 | 0 | 0 |
| Generalisation and Scope | 6 | 1 | 1 | 1 | 1 |
| Technical Capability | 4 | 4 | 0 | 0 | 0 |
| Runtime Behavior | 3 | 3 | 0 | 0 | 0 |
| Architecture | 4 | 4 | 0 | 0 | 0 |
| Documentation Policy | 2 | 0 | 0 | 0 | 2 |
| Process and Traceability | 2 | 2 | 0 | 0 | 0 |
| Adoption and Usability | 1 | 1 | 0 | 0 | 0 |
| Other | 34 | 12 | 0 | 0 | 1 |

## Priority Findings

- claim_030_1674d248 | Generalisation and Scope | high | unsupported | add_evidence_or_remove_claim | "The reviewed repositories provide limited evidence of team collaboration."
  Risk: No meaningful supporting evidence was found in the selected corpus.

## High-Importance Claims Requiring Action

| Claim | Domain | Verdict | Action | Source |
| --- | --- | --- | --- | --- |
| claim_030_1674d248: "The reviewed repositories provide limited evidence of team collaboration." | Generalisation and Scope | unsupported | add_evidence_or_remove_claim | docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Prohibited Inferences; line 55) |

## Claims Grouped by Domain

### Model Performance

- claim_019_7c06b9d6 | Model Performance | high | supported | keep_evidence_linked | | Final validation | `src/workovercv/validation.py` | Checks required artifacts, record references, v0.6 report shape, gap follow-ups, ro...
- claim_037_9e53727b | Model Performance | high | supported | keep_evidence_linked | | Role-family references | `src/workovercv/validation.py::_validate_role_family_fit` and `_validate_report_role_family_fit` require non-e...
- claim_038_e91a205a | Model Performance | high | supported | keep_evidence_linked | | | Gap follow-up structure | `src/workovercv/validation.py::_validate_mitigations` checks mitigation references and requires every evide...

### Generalisation and Scope

- claim_030_1674d248 | Generalisation and Scope | high | unsupported | add_evidence_or_remove_claim | "The reviewed repositories provide limited evidence of team collaboration."
- 1 suppressed reference or low-quality record(s) in this domain are listed separately or in the Full Claim Listing.
- 4 boundary or non-goal statement(s) in this domain are listed separately.

### Technical Capability

- claim_024_d01f7c52 | Technical Capability | medium | supported | no_action | Code and markdown cells may support signals about experiment design, preprocessing flow, evaluation workflow, and exploratory engineering...
- claim_026_dc093b0b | Technical Capability | medium | supported | no_action | `strong`: multiple concrete artifacts support the signal, or one unusually direct artifact supports it.
- claim_021_a72214cc | Technical Capability | low | supported | no_action | | | Schema references | `schemas/*.schema.json`, `src/workovercv/validation.py` | Provide machine-readable output shapes and the implemen...
- claim_023_a41b6335 | Technical Capability | low | supported | no_action | The deterministic `analyze` command provides a local rubric path for smoke tests without API calls.

### Runtime Behavior

- claim_009_6746abcf | Runtime Behavior | medium | supported | no_action | The shared runtime contract remains `docs/runtime_contract.md`.
- claim_012_b4ce718c | Runtime Behavior | medium | supported | no_action | This is packaging only; the canonical workflow and runtime contract remain in the WorkOverCV repository.
- claim_017_aea193d7 | Runtime Behavior | medium | supported | no_action | | Runtime behavior or workflow stage | Implementation modules | Evidence notes |

### Architecture

- claim_015_d98cdebb | Architecture | medium | supported | no_action | Use the module paths below as code pointers.
- claim_020_9d68e0a0 | Architecture | medium | supported | no_action | | | Workflow output contract | `workflows/workovercv.yml`, `src/workovercv/constants.py` | Lists canonical output paths and the current `...
- claim_032_63df0cdb | Architecture | medium | supported | no_action | The final `validate` gate checks the required artifacts defined by the current validation implementation and workflow output contract.
- claim_035_75ded822 | Architecture | medium | supported | no_action | Workflow output contract: `workflows/workovercv.yml` lists the canonical output paths and schemas for final run artifacts.

### Documentation Policy

No audit-ready claims in this domain.
- 2 suppressed reference or low-quality record(s) in this domain are listed separately or in the Full Claim Listing.

### Process and Traceability

- claim_018_6e6458f9 | Process and Traceability | medium | supported | no_action | | Repository materialization and corpus | `src/workovercv/collect.py` | Clones or reads selected repositories, inventories artifacts with...
- claim_033_057230dc | Process and Traceability | medium | supported | no_action | `review_scope.yml` is the review boundary and is validated by manifest logic in `src/workovercv/manifest.py`; JSON Schema validation cove...

### Adoption and Usability

- claim_002_a7781a09 | Adoption and Usability | low | supported | no_action | It turns public repository artifacts into reviewable evidence, behaviour signals, evidence gaps, role-family discussion routes, and follo...

### Other

- claim_003_e5645ca0 | Other | low | supported | no_action | Agent adapters under `adapters/` must point to those contracts rather than redefining the workflow.
- claim_013_bfc91353 | Other | low | supported | no_action | Status: v0.6 retest required for the GitHub-profile Codex adapter smoke.
- claim_034_858f8c1d | Other | low | supported | no_action | Required artifact list: `src/workovercv/constants.py::REQUIRED_FINAL_ARTIFACTS` defines the current final file set checked by `_check_req...
- claim_036_038c6490 | Other | low | supported | no_action | Complete-run tests: `tests/test_render_validate.py::test_validate_run_accepts_complete_run` proves a complete rendered run is accepted; t...
- claim_041_1105624d | Other | low | supported | no_action | Use schemas under `schemas/` for the required record shapes.
- claim_052_e6694079 | Other | low | supported | no_action | The final `summary-report.md` must render as a shorter human-facing conversation guide titled `Work Behaviour Profile Summary`.
- claim_054_66c64e30 | Other | low | supported | no_action | It must use concise repository/path evidence references, avoid full evidence tables, avoid an Evidence Appendix, and avoid old SWOT-style...
- claim_055_1d9200d1 | Other | low | supported | no_action | `repo_id` must exist in `repo_inventory.json`.
- claim_056_f693cd0f | Other | low | supported | no_action | `artifact_id` and `path` must exist in `artifact_inventory.json` or the collected `review_corpus.jsonl`.
- claim_057_50105854 | Other | low | supported | no_action | `evidence_ids` must exist in `evidence_map.jsonl`.
- claim_058_e9713652 | Other | low | supported | no_action | `related_signal_ids` must exist in `signal_ledger.jsonl`.
- claim_059_2fd6faa4 | Other | low | supported | no_action | `related_gap_id` and `limiting_gap_ids` must exist in `gap_register.jsonl`.
- 1 suppressed reference or low-quality record(s) in this domain are listed separately or in the Full Claim Listing.
- 21 boundary or non-goal statement(s) in this domain are listed separately.

## Boundary / Non-Goal Statements

- claim_008_8cea47f5 | README.md | Private repositories, authenticated GitHub access, hosted services, web UI, live GitHub fetching during local scans, and API-backed LLM execution are out of...
- claim_025_2af4bcfc | docs/safety_and_taxonomy.md | Notebook outputs are not collected, notebooks are never executed, and notebook source alone must not be treated as proof of metric validity, production readi...
- claim_028_f6d9611a | docs/safety_and_taxonomy.md | WorkOverCV must not make final suitability judgements for or against production ownership, autonomy level, or hiring outcome; those discussions belong to hum...
- claim_031_7c975a67 | docs/safety_and_taxonomy.md | WorkOverCV should not conclude suitability for or against unsupervised production ownership without human review, role context, and additional evidence beyon...
- claim_001_d2aa7005 | README.md | WorkOverCV does not make hiring decisions, certify competence, infer protected or private traits, or treat popularity metrics as competence metrics.
- claim_004_a48ae21f | README.md | It does not fetch GitHub data and does not call an LLM.
- claim_006_9b0f1ac4 | README.md | It may contain bounded git commit metadata, but raw commit hashes, raw commit messages, and raw timelines must not be emitted in `report.json`, `report.md`,...
- claim_007_3927a1bc | README.md | signal, claim, gap, mitigation, or role-family references that do not resolve
- claim_010_90fef500 | adapters/claude-code/README.md | Do not claim Claude Code compatibility until an end-to-end adapter run has been verified.
- claim_011_e03d19ba | adapters/codex/README.md | They do not install Python dependencies or alter the WorkOverCV runtime.
- claim_014_e42776e0 | adapters/codex/README.md | Do not claim a separate Codex plugin-install smoke unless one is separately recorded.
- claim_016_984679d8 | docs/implementation_map.md | This page is not a conformance matrix and does not define every runtime, schema, or configuration boundary.
- claim_022_64350d65 | docs/implementation_map.md | The repository documents the contract an adapter must follow in `skills/workovercv/SKILL.md`, `docs/adapter_contract.md`, and adapter-specific README files;...
- claim_027_520670aa | docs/safety_and_taxonomy.md | `low`: inference is tentative and should prompt follow-up, not conclusion.
- claim_029_4b518f6f | docs/safety_and_taxonomy.md | Do not infer or report age, disability, health status, neurotype, race, ethnicity, religion, gender identity, sexuality, nationality, family status, financia...
- claim_040_9b4d66f0 | skills/workovercv/SKILL.md | It does not make hiring decisions, certify competence, infer protected or private traits, or equate popularity metrics with capability.
- claim_042_fdeae135 | skills/workovercv/SKILL.md | Do not treat this skill file as the canonical workflow source.
- claim_043_30edc1b1 | skills/workovercv/SKILL.md | Read their markdown/code cells for engineering signal, but do not execute them and do not treat omitted outputs as evidence.
- claim_044_f0b796ba | skills/workovercv/SKILL.md | It may contain bounded commit hashes, subjects, and timestamps, but raw commit hashes, raw commit messages, and raw timelines must not appear in `report.json...
- claim_045_a97b9799 | skills/workovercv/SKILL.md | Do not emit them as ordinary observed work behaviour signals in `report.json`.
- claim_046_a28e7eed | skills/workovercv/SKILL.md | Describe observable work behaviour, not candidate grades.
- claim_047_8c567b54 | skills/workovercv/SKILL.md | Treat missing public evidence as uncertainty, not proof of inability.
- claim_048_097882f0 | skills/workovercv/SKILL.md | Record the active agent/model in `report.json` under `analysis_model_information`; use the model identity exposed by the host environment, or state that the...
- claim_049_a14f7146 | skills/workovercv/SKILL.md | Do not infer or invent model/provider details.
- claim_051_c406bafc | skills/workovercv/SKILL.md | Do not emit `Strengths`, `Weaknesses`, `Opportunities`, or `Mitigations of Weaknesses`.

## Suppressed Reference Records

- claim_053_33caf85a | claim_source | policy_statement | It should include scope, executive synthesis, top observed work behaviour signals, problem-solving style, environment fit, role-family di...
- claim_005_3229684f | claim_source | policy_statement | Agent-authored `report.json` must include `analysis_model_information` with the active model identity exposed by the host environment, or...
- claim_050_28e69cdf | claim_source | policy_statement | It must include the rendered `analysis_model_information` value.
- claim_039_c1f24b8c | claim_source | frontmatter_metadata | --- name: workovercv description: Produce evidence-bounded work behaviour profile reports from public GitHub repository evidence using th...

## Full Claim Listing

### claim_001_d2aa7005

- Claim: WorkOverCV does not make hiring decisions, certify competence, infer protected or private traits, or treat popularity metrics as competence metrics.
- Source: README.md (section: WorkOverCV; lines 11-14)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV; lines 6-14): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 6-14, matched terms: certify, competence, decisions, does, hiring, infer, make, metrics. Strength: contradictory. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV; lines 6-14): Candidate evidence from skills/workovercv/SKILL.md, lines 6-14, matched terms: certify, competence, decisions, does, hiring, infer, make, metrics. Strength: contradictory. Source role: claim_source.
- adapters/codex/README.md (section: Codex Adapter > Boundaries; lines 107-118): Candidate evidence from adapters/codex/README.md, lines 107-118, matched terms: competence, hiring, infer, make, metrics, not, private, protected. Strength: strong. Source role: claim_source.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: competence, infer, make, metrics, not, private, protected, traits. Strength: strong. Source role: adapter_contract.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: competence, hiring, infer, metrics, not, private, protected, treat. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_002_a7781a09

- Claim: It turns public repository artifacts into reviewable evidence, behaviour signals, evidence gaps, role-family discussion routes, and follow-up questions.
- Source: README.md (section: WorkOverCV; lines 11-14)
- Source role: claim_source
- Auditable claim: True
- Type: adoption_usability_claim
- Domain: Adoption and Usability
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: human_review_required
- Verdict: supported
- Confidence: high

Found evidence:
- src/workovercv/render.py (section: line range; lines 321-400): Candidate evidence from src/workovercv/render.py, lines 321-400, matched terms: behaviour, discussion, evidence, family, follow, gaps, guide, into. Strength: contradictory. Source role: source_code.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: artifacts, behaviour, documented, evidence, follow, gaps, into, public. Strength: contradictory. Source role: example_output.
- src/workovercv/rubric.py (section: line range; lines 1281-1360): Candidate evidence from src/workovercv/rubric.py, lines 1281-1360, matched terms: artifacts, discussion, evidence, family, follow, gaps, into, public. Strength: strong. Source role: source_code.
- tests/test_render_validate.py (section: line range; lines 1-80): Candidate evidence from tests/test_render_validate.py, lines 1-80, matched terms: behaviour, discussion, evidence, family, follow, gaps, guide, questions. Strength: strong. Source role: test_fixture.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 121-153, matched terms: behaviour, discussion, evidence, family, follow, gaps, guide, questions. Strength: strong. Source role: adapter_contract.

Missing evidence:
- examples: No selected corpus artifact clearly covers required evidence item 'examples' for this adoption_usability_claim. Suggested fix: Add evidence covering: examples.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- Add evidence covering: examples.

### claim_003_e5645ca0

- Claim: Agent adapters under `adapters/` must point to those contracts rather than redefining the workflow.
- Source: README.md (section: WorkOverCV > V0.6 Shape; lines 18-20)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: adapters, agent, must, point, under, workflow. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: artifact, contracts, direct, documentation, rather, than, those, workflow. Strength: contradictory. Source role: example_output.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: adapters, agent, artifact, must, redefining, workflow. Strength: strong. Source role: adapter_contract.
- src/workovercv/rubric.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/rubric.py, lines 1-80, matched terms: artifact, contracts, documentation, rather, than, workflow. Strength: contradictory. Source role: source_code.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: agent, artifact, must, under, workflow. Strength: contradictory. Source role: runtime_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_004_a48ae21f

- Claim: It does not fetch GitHub data and does not call an LLM.
- Source: README.md (section: WorkOverCV > V0.6 Shape; lines 55-59)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- docs/runtime_contract.md (section: Runtime Contract; lines 1-10): Candidate evidence from docs/runtime_contract.md, lines 1-10, matched terms: call, data, does, llm, not. Strength: contradictory. Source role: runtime_contract.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 1-80): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 1-80, matched terms: does, github, llm, not. Strength: contradictory. Source role: example_output.
- src/workovercv/github.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/github.py, lines 1-80, matched terms: data, fetch, github, not. Strength: contradictory. Source role: source_code.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: does, github, not. Strength: contradictory. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: data, does, not. Strength: contradictory. Source role: example_output.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_005_3229684f

- Claim: Agent-authored `report.json` must include `analysis_model_information` with the active model identity exposed by the host environment, or a statement that the runtime did not disclose one.
- Source: README.md (section: WorkOverCV > V0.6 Shape; lines 70-79)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Documentation Policy
- Importance: low
- Review action: ignore_low_quality_extraction
- Extraction quality: policy_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: active, agent, analysis, authored, did, disclose, environment, exposed. Strength: contradictory. Source role: runtime_contract.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: active, agent, analysis, environment, exposed, host, identity, information. Strength: strong. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from skills/workovercv/SKILL.md, lines 71-120, matched terms: active, agent, analysis, environment, exposed, host, identity, information. Strength: strong. Source role: claim_source.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: agent, authored, environment, include, json, must, not, report. Strength: strong. Source role: adapter_contract.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: agent, analysis, authored, json, model, must, not, report. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This extraction is too fragmentary or artifact-like for priority review and is demoted to the full listing.

Recommended remediation:
- Do not treat this reference or low-quality record as an auditable project claim.

### claim_006_9b0f1ac4

- Claim: It may contain bounded git commit metadata, but raw commit hashes, raw commit messages, and raw timelines must not be emitted in `report.json`, `report.md`, or `summary-report.md`.
- Source: README.md (section: WorkOverCV > Required Final Artifacts; lines 103-105)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: bounded, commit, git, hashes, json, may, md, messages. Strength: contradictory. Source role: runtime_contract.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: bounded, commit, contain, hashes, json, may, md, messages. Strength: strong. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from skills/workovercv/SKILL.md, lines 27-70, matched terms: bounded, commit, contain, hashes, json, may, md, messages. Strength: strong. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Work Rhythm and Development Cadence; lines 247-276): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 247-276, matched terms: bounded, commit, hashes, json, may, md, not, raw. Strength: contradictory. Source role: example_output.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: bounded, git, json, may, md, metadata, must, not. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_007_3927a1bc

- Claim: signal, claim, gap, mitigation, or role-family references that do not resolve
- Source: README.md (section: WorkOverCV > Strict Validation; line 119)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- src/workovercv/validation.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/validation.py, lines 1-80, matched terms: claim, family, gap, mitigation, not, resolve, role, signal. Strength: strong. Source role: source_code.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: family, gap, mitigation, not, resolve, role, signal. Strength: contradictory. Source role: adapter_contract.
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: claim, family, gap, mitigation, references, role, signal. Strength: strong. Source role: claim_source.
- skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from skills/workovercv/SKILL.md, lines 154-198, matched terms: family, gap, mitigation, not, resolve, role, signal. Strength: contradictory. Source role: claim_source.
- src/workovercv/validation.py (section: line range; lines 481-560): Candidate evidence from src/workovercv/validation.py, lines 481-560, matched terms: family, gap, mitigation, not, references, role, signal. Strength: strong. Source role: source_code.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_008_8cea47f5

- Claim: Private repositories, authenticated GitHub access, hosted services, web UI, live GitHub fetching during local scans, and API-backed LLM execution are out of scope for v0.6.
- Source: README.md (section: WorkOverCV > Status; lines 144-147)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Generalisation and Scope
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: execution, github, llm, local, out, repositories, scope, v0.6. Strength: contradictory. Source role: runtime_contract.
- adapters/status.yml (section: line range; lines 1-9): Candidate evidence from adapters/status.yml, lines 1-9, matched terms: api, backed, execution, github, local, out, scope, v0.6. Strength: moderate. Source role: adapter_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: execution, github, llm, local, scans, scope, v0.6. Strength: contradictory. Source role: claim_source.
- workflows/workovercv.yml (section: line range; lines 81-109): Candidate evidence from workflows/workovercv.yml, lines 81-109, matched terms: api, backed, execution, llm, private, repositories, v0.6. Strength: contradictory. Source role: workflow_contract.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: api, github, local, repositories, scope, v0.6. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_009_6746abcf

- Claim: The shared runtime contract remains `docs/runtime_contract.md`.
- Source: adapters/claude-code/README.md (section: Claude Code Adapter; lines 5-7)
- Source role: claim_source
- Auditable claim: True
- Type: runtime_claim
- Domain: Runtime Behavior
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: high_claim_surface
- Verification mode: artifact_presence_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: configuration, contract, docs, implementation, md, notes, output, runtime. Strength: contradictory. Source role: claim_source.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: contract, docs, environment, example, implementation, md, output, runtime. Strength: contradictory. Source role: claim_source.
- adapters/codex/README.md (section: Codex Adapter; lines 1-9): Candidate evidence from adapters/codex/README.md, lines 1-9, matched terms: contract, docs, md, remains, runtime, shared. Strength: strong. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: contract, environment, md, output, remains, runtime. Strength: contradictory. Source role: runtime_contract.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: contract, docs, md, output, runtime, shared, smoke. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_010_90fef500

- Claim: Do not claim Claude Code compatibility until an end-to-end adapter run has been verified.
- Source: adapters/claude-code/README.md (section: Claude Code Adapter; lines 28-29)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/status.yml (section: line range; lines 1-9): Candidate evidence from adapters/status.yml, lines 1-9, matched terms: adapter, been, claude, code, end, has, not, verified. Strength: strong. Source role: adapter_contract.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: adapter, compatibility, end, not, run, verified. Strength: strong. Source role: adapter_contract.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: adapter, compatibility, do, end, not, run. Strength: strong. Source role: adapter_contract.
- adapters/codex/README.md (section: Codex Adapter > Verification; lines 125-138): Candidate evidence from adapters/codex/README.md, lines 125-138, matched terms: adapter, claim, compatibility, do, not, run. Strength: strong. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 1-80): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 1-80, matched terms: code, do, not, run, verified. Strength: contradictory. Source role: example_output.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_011_e03d19ba

- Claim: They do not install Python dependencies or alter the WorkOverCV runtime.
- Source: adapters/codex/README.md (section: Codex Adapter > Repo Skill Install; lines 55-57)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: alter, do, not, runtime, they, workovercv. Strength: strong. Source role: adapter_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: install, not, python, runtime, workovercv. Strength: contradictory. Source role: claim_source.
- adapters/claude-code/README.md (section: Claude Code Adapter; lines 1-29): Candidate evidence from adapters/claude-code/README.md, lines 1-29, matched terms: do, not, python, runtime, workovercv. Strength: strong. Source role: claim_source.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: do, not, python, runtime, workovercv. Strength: strong. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from skills/workovercv/SKILL.md, lines 27-70, matched terms: do, not, python, runtime, workovercv. Strength: strong. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_012_b4ce718c

- Claim: This is packaging only; the canonical workflow and runtime contract remain in the WorkOverCV repository.
- Source: adapters/codex/README.md (section: Codex Adapter > Optional Plugin Package; lines 121-123)
- Source role: claim_source
- Auditable claim: True
- Type: runtime_claim
- Domain: Runtime Behavior
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: high_claim_surface
- Verification mode: artifact_presence_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: canonical, configuration, contract, implementation, notes, only, output, remain. Strength: contradictory. Source role: claim_source.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: canonical, contract, environment, example, implementation, only, output, repository. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: contract, environment, only, output, repository, runtime, workflow, workovercv. Strength: contradictory. Source role: runtime_contract.
- docs/runtime_contract.md (section: Runtime Contract; lines 1-10): Candidate evidence from docs/runtime_contract.md, lines 1-10, matched terms: canonical, contract, repository, runtime, workflow, workovercv. Strength: contradictory. Source role: runtime_contract.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: contract, environment, only, output, repository, runtime, smoke, test. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_013_bfc91353

- Claim: Status: v0.6 retest required for the GitHub-profile Codex adapter smoke.
- Source: adapters/codex/README.md (section: Codex Adapter > Verification; lines 137-138)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: adapter, artifact, codex, github, profile, required, smoke, status. Strength: strong. Source role: adapter_contract.
- adapters/status.yml (section: line range; lines 1-9): Candidate evidence from adapters/status.yml, lines 1-9, matched terms: adapter, codex, direct, github, profile, retest, smoke, status. Strength: strong. Source role: adapter_contract.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: adapter, artifact, github, profile, required, smoke, status, v0.6. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifact, github, profile, required, status, v0.6. Strength: contradictory. Source role: runtime_contract.
- adapters/claude-code/README.md (section: Claude Code Adapter; lines 1-29): Candidate evidence from adapters/claude-code/README.md, lines 1-29, matched terms: adapter, github, profile, required, status. Strength: strong. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_014_e42776e0

- Claim: Do not claim a separate Codex plugin-install smoke unless one is separately recorded.
- Source: adapters/codex/README.md (section: Codex Adapter > Verification; lines 137-138)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/README.md (section: Codex Adapter > Repo Skill Install; lines 27-58): Candidate evidence from adapters/codex/README.md, lines 27-58, matched terms: codex, do, install, not, one. Strength: moderate. Source role: claim_source.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: codex, do, not, recorded, smoke. Strength: moderate. Source role: adapter_contract.
- src/workovercv/rubric.py (section: line range; lines 1521-1600): Candidate evidence from src/workovercv/rubric.py, lines 1521-1600, matched terms: claim, do, not, recorded, separately. Strength: contradictory. Source role: source_code.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: not, one, separate, unless. Strength: contradictory. Source role: runtime_contract.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 401-480): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 401-480, matched terms: install, not, one, recorded. Strength: contradictory. Source role: example_output.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_015_d98cdebb

- Claim: Use the module paths below as code pointers.
- Source: docs/implementation_map.md (section: Implementation Map; lines 3-7)
- Source role: claim_source
- Auditable claim: True
- Type: architecture_claim
- Domain: Architecture
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: below, code, evidence, files, source, use. Strength: strong. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from skills/workovercv/SKILL.md, lines 27-70, matched terms: below, code, evidence, files, source, use. Strength: strong. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/summary-report.md (section: Work Behaviour Profile Summary > Executive Work Profile; lines 11-16): Candidate evidence from examples/mitchellquinn-20260618-1431Z/summary-report.md, lines 11-16, matched terms: below, code, documentation, evidence, paths, use. Strength: contradictory. Source role: example_output.
- src/workovercv/render.py (section: line range; lines 161-240): Candidate evidence from src/workovercv/render.py, lines 161-240, matched terms: below, evidence, paths, use. Strength: contradictory. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 161-240): Candidate evidence from src/workovercv/rubric.py, lines 161-240, matched terms: code, contracts, documentation, evidence, interfaces, paths, source. Strength: strong. Source role: source_code.

Missing evidence:
- architecture documentation: No selected corpus artifact clearly covers required evidence item 'architecture documentation' for this architecture_claim. Suggested fix: Add architecture documentation or link the claim to source modules/interfaces.
- interfaces/contracts: No selected corpus artifact clearly covers required evidence item 'interfaces/contracts' for this architecture_claim. Suggested fix: Add architecture documentation or link the claim to source modules/interfaces.

Artifact gaps:
- architecture_doc: Architecture documentation was not found. Impact: Architecture claims are harder to verify from source evidence alone.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- Add architecture documentation or link the claim to source modules/interfaces.
- Address artifact gap: Architecture documentation was not found.

### claim_016_984679d8

- Claim: This page is not a conformance matrix and does not define every runtime, schema, or configuration boundary.
- Source: docs/implementation_map.md (section: Implementation Map; lines 3-7)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: conformance, does, not, runtime, schema. Strength: contradictory. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 1-80): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 1-80, matched terms: boundary, configuration, does, not, runtime. Strength: contradictory. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: boundary, configuration, does, not, runtime. Strength: contradictory. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Problem-Solving Style; lines 232-246): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 232-246, matched terms: configuration, does, not, runtime, schema. Strength: contradictory. Source role: example_output.
- src/workovercv/rubric.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/rubric.py, lines 1-80, matched terms: boundary, configuration, does, not, runtime. Strength: contradictory. Source role: source_code.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_017_aea193d7

- Claim: | Runtime behavior or workflow stage | Implementation modules | Evidence notes |
- Source: docs/implementation_map.md (section: Implementation Map; line 9)
- Source role: claim_source
- Auditable claim: True
- Type: runtime_claim
- Domain: Runtime Behavior
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: high_claim_surface
- Verification mode: artifact_presence_review
- Verdict: supported
- Confidence: high

Found evidence:
- src/workovercv/render.py (section: line range; lines 961-1040): Candidate evidence from src/workovercv/render.py, lines 961-1040, matched terms: behavior, configuration, evidence, implementation, notes, runtime, test, trace. Strength: strong. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/rubric.py, lines 1-80, matched terms: behavior, configuration, evidence, implementation, runtime, stage, workflow. Strength: contradictory. Source role: source_code.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: behavior, configuration, evidence, implementation, runtime, test, workflow. Strength: contradictory. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 1-80): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 1-80, matched terms: behavior, configuration, evidence, implementation, notes, runtime. Strength: contradictory. Source role: example_output.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: environment, evidence, example, implementation, output, runtime, test, workflow. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_018_6e6458f9

- Claim: | Repository materialization and corpus | `src/workovercv/collect.py` | Clones or reads selected repositories, inventories artifacts with canonical `artifact_type`, chunks text, writes schema-validated `review_corpus.jsonl`, collects bounded `work_chronology.json`, and cleans worktrees by default.
- Source: docs/implementation_map.md (section: Implementation Map; line 15)
- Source role: claim_source
- Auditable claim: True
- Type: process_claim
- Domain: Process and Traceability
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: analysis, artifact, artifacts, bounded, chronology, collect, commit, corpus. Strength: contradictory. Source role: runtime_contract.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Problem-Solving Style; lines 232-246): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 232-246, matched terms: analysis, artifact, artifacts, bounded, json, py, report, repositories. Strength: contradictory. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Evidence Appendix; lines 396-442): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 396-442, matched terms: analysis, artifact, artifacts, bounded, chronology, commit, history, json. Strength: strong. Source role: example_output.
- workflows/workovercv.yml (section: line range; lines 1-80): Candidate evidence from workflows/workovercv.yml, lines 1-80, matched terms: analysis, artifact, artifacts, bounded, chronology, collect, corpus, inventories. Strength: strong. Source role: workflow_contract.
- tests/test_collect.py (section: line range; lines 81-160): Candidate evidence from tests/test_collect.py, lines 81-160, matched terms: artifact, artifacts, chronology, collect, corpus, json, jsonl, materialization. Strength: strong. Source role: test_fixture.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_019_7c06b9d6

- Claim: | Final validation | `src/workovercv/validation.py` | Checks required artifacts, record references, v0.6 report shape, gap follow-ups, role-family references and caveats, raw chronology leakage, red-team status, prohibited wording, hiring-decision language, and legacy heading regressions.
- Source: docs/implementation_map.md (section: Implementation Map; lines 18-20)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Model Performance
- Importance: high
- Review action: keep_evidence_linked
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifact, artifacts, checks, chronology, decision, family, final, follow. Strength: contradictory. Source role: runtime_contract.
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: artifact, artifacts, caveats, checks, chronology, decision, family, final. Strength: strong. Source role: claim_source.
- workflows/workovercv.yml (section: line range; lines 81-109): Candidate evidence from workflows/workovercv.yml, lines 81-109, matched terms: artifact, artifacts, caveats, checks, chronology, decision, family, follow. Strength: contradictory. Source role: workflow_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: artifacts, checks, chronology, family, final, follow, gap, heading. Strength: contradictory. Source role: claim_source.
- README.md (section: WorkOverCV > Strict Validation; lines 107-141): Candidate evidence from README.md, lines 107-141, matched terms: artifacts, chronology, decision, family, final, follow, gap, hiring. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_020_9d68e0a0

- Claim: | | Workflow output contract | `workflows/workovercv.yml`, `src/workovercv/constants.py` | Lists canonical output paths and the current `REQUIRED_FINAL_ARTIFACTS` used by the final validation gate.
- Source: docs/implementation_map.md (section: Implementation Map; lines 18-20)
- Source role: claim_source
- Auditable claim: True
- Type: architecture_claim
- Domain: Architecture
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/validation_contract.md (section: Validation Contract; lines 1-25): Candidate evidence from docs/validation_contract.md, lines 1-25, matched terms: artifacts, canonical, constants, contract, current, evidence, files, final. Strength: strong. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifacts, contract, evidence, files, final, output, required, source. Strength: contradictory. Source role: runtime_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: artifacts, canonical, contract, contracts, evidence, files, final, output. Strength: contradictory. Source role: claim_source.
- adapters/claude-code/README.md (section: Claude Code Adapter; lines 1-29): Candidate evidence from adapters/claude-code/README.md, lines 1-29, matched terms: artifacts, canonical, contract, output, required, source, src, workflow. Strength: strong. Source role: claim_source.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: contract, current, evidence, final, output, required, src, workflow. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_021_a72214cc

- Claim: | | Schema references | `schemas/*.schema.json`, `src/workovercv/validation.py` | Provide machine-readable output shapes and the implementation mapping from final artifacts to schema validators.
- Source: docs/implementation_map.md (section: Implementation Map; lines 18-20)
- Source role: claim_source
- Auditable claim: True
- Type: capability_claim
- Domain: Technical Capability
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: artifacts, boundaries, final, implementation, json, mapping, py, references. Strength: strong. Source role: claim_source.
- docs/validation_contract.md (section: Validation Contract; lines 1-25): Candidate evidence from docs/validation_contract.md, lines 1-25, matched terms: artifacts, final, implementation, json, output, py, schema, schemas. Strength: strong. Source role: claim_source.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: artifacts, boundaries, example, final, implementation, json, mapping, output. Strength: contradictory. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Evidence Appendix; lines 396-442): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 396-442, matched terms: artifacts, boundaries, documentation, implementation, json, py, references, schema. Strength: strong. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/screening_brief.md (section: Repository Review Guide > Behaviour Signals To Discuss; lines 6-16): Candidate evidence from examples/mitchellquinn-20260618-1431Z/screening_brief.md, lines 6-16, matched terms: artifacts, boundaries, implementation, json, py, schema, schemas, src. Strength: strong. Source role: example_output.

Missing evidence:
- documentation describing boundaries: No selected corpus artifact clearly covers required evidence item 'documentation describing boundaries' for this capability_claim. Suggested fix: Add evidence covering: documentation describing boundaries.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- Add evidence covering: documentation describing boundaries.

### claim_022_64350d65

- Claim: The repository documents the contract an adapter must follow in `skills/workovercv/SKILL.md`, `docs/adapter_contract.md`, and adapter-specific README files; the shared Python runtime does not execute those judgement stages directly.
- Source: docs/implementation_map.md (section: Implementation Map; lines 23-28)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: contract, docs, does, files, follow, md, must, not. Strength: contradictory. Source role: claim_source.
- adapters/claude-code/README.md (section: Claude Code Adapter; lines 1-29): Candidate evidence from adapters/claude-code/README.md, lines 1-29, matched terms: adapter, contract, docs, md, must, not, python, runtime. Strength: strong. Source role: claim_source.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: adapter, contract, md, must, not, python, repository, runtime. Strength: strong. Source role: adapter_contract.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: adapter, contract, docs, md, must, not, runtime, shared. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Problem-Solving Style; lines 232-246): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 232-246, matched terms: adapter, contract, docs, documents, does, execute, md, not. Strength: contradictory. Source role: example_output.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_023_a41b6335

- Claim: The deterministic `analyze` command provides a local rubric path for smoke tests without API calls.
- Source: docs/implementation_map.md (section: Implementation Map; lines 23-28)
- Source role: claim_source
- Auditable claim: True
- Type: capability_claim
- Domain: Technical Capability
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: artifact_presence_review
- Verdict: supported
- Confidence: high

Found evidence:
- tests/test_analyze.py (section: line range; lines 1-80): Candidate evidence from tests/test_analyze.py, lines 1-80, matched terms: analyze, command, deterministic, example, local, path, rubric, test. Strength: strong. Source role: test_fixture.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Evidence Appendix; lines 396-442): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 396-442, matched terms: analyze, boundaries, documentation, implementation, path, provides, test, tests. Strength: strong. Source role: example_output.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: analyze, deterministic, local, path, rubric, without. Strength: contradictory. Source role: runtime_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: analyze, boundaries, deterministic, example, implementation, local, path, test. Strength: contradictory. Source role: claim_source.
- tests/test_rubric.py (section: line range; lines 1-80): Candidate evidence from tests/test_rubric.py, lines 1-80, matched terms: api, deterministic, documentation, example, implementation, path, rubric, test. Strength: strong. Source role: test_fixture.

Missing evidence:
- documentation describing boundaries: No selected corpus artifact clearly covers required evidence item 'documentation describing boundaries' for this capability_claim. Suggested fix: Add evidence covering: documentation describing boundaries.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- Add evidence covering: documentation describing boundaries.

### claim_024_d01f7c52

- Claim: Code and markdown cells may support signals about experiment design, preprocessing flow, evaluation workflow, and exploratory engineering habits.
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy; lines 6-10)
- Source role: claim_source
- Auditable claim: True
- Type: capability_claim
- Domain: Technical Capability
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: high_claim_surface
- Verification mode: artifact_presence_review
- Verdict: supported
- Confidence: high

Found evidence:
- src/workovercv/rubric.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/rubric.py, lines 81-160, matched terms: about, boundaries, code, design, documentation, evaluation, experiment, exploratory. Strength: contradictory. Source role: source_code.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: about, boundaries, code, design, documentation, evaluation, experiment, habits. Strength: contradictory. Source role: example_output.
- src/workovercv/rubric.py (section: line range; lines 161-240): Candidate evidence from src/workovercv/rubric.py, lines 161-240, matched terms: boundaries, code, design, documentation, engineering, evaluation, experiment, exploratory. Strength: strong. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 1521-1600): Candidate evidence from src/workovercv/rubric.py, lines 1521-1600, matched terms: about, boundaries, documentation, engineering, evaluation, experiment, exploratory, implementation. Strength: contradictory. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 1441-1520): Candidate evidence from src/workovercv/rubric.py, lines 1441-1520, matched terms: boundaries, code, design, documentation, engineering, evaluation, habits, implementation. Strength: strong. Source role: source_code.

Missing evidence:
- usage example: No selected corpus artifact clearly covers required evidence item 'usage example' for this capability_claim. Suggested fix: Add evidence covering: usage example.
- documentation describing boundaries: No selected corpus artifact clearly covers required evidence item 'documentation describing boundaries' for this capability_claim. Suggested fix: Add evidence covering: documentation describing boundaries.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- Add evidence covering: usage example.
- Add evidence covering: documentation describing boundaries.

### claim_025_2af4bcfc

- Claim: Notebook outputs are not collected, notebooks are never executed, and notebook source alone must not be treated as proof of metric validity, production readiness, runtime reliability, or deployment.
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy; lines 6-10)
- Source role: claim_source
- Auditable claim: False
- Type: generalisation_claim
- Domain: Generalisation and Scope
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: collected, deployment, metric, must, not, notebook, outputs, reliability. Strength: strong. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from skills/workovercv/SKILL.md, lines 27-70, matched terms: collected, deployment, metric, must, not, notebook, outputs, reliability. Strength: strong. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: collected, metric, not, notebook, production, proof, reliability, runtime. Strength: contradictory. Source role: example_output.
- src/workovercv/rubric.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/rubric.py, lines 81-160, matched terms: metric, not, notebook, outputs, production, proof, reliability, source. Strength: contradictory. Source role: source_code.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: collected, must, never, not, notebook, notebooks, outputs, runtime. Strength: contradictory. Source role: runtime_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_026_dc093b0b

- Claim: `strong`: multiple concrete artifacts support the signal, or one unusually direct artifact supports it.
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Signal Strength; lines 14-15)
- Source role: claim_source
- Auditable claim: True
- Type: capability_claim
- Domain: Technical Capability
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: high_claim_surface
- Verification mode: artifact_presence_review
- Verdict: supported
- Confidence: high

Found evidence:
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: artifact, artifacts, boundaries, concrete, direct, documentation, implementation, signal. Strength: contradictory. Source role: example_output.
- src/workovercv/rubric.py (section: line range; lines 1521-1600): Candidate evidence from src/workovercv/rubric.py, lines 1521-1600, matched terms: artifact, artifacts, boundaries, concrete, documentation, implementation, signal, strong. Strength: contradictory. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 801-880): Candidate evidence from src/workovercv/rubric.py, lines 801-880, matched terms: artifact, artifacts, direct, multiple, signal, strong. Strength: strong. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 881-960): Candidate evidence from src/workovercv/rubric.py, lines 881-960, matched terms: artifact, artifacts, direct, documentation, implementation, signal, strong, test. Strength: strong. Source role: source_code.
- tests/test_render_validate.py (section: line range; lines 561-640): Candidate evidence from tests/test_render_validate.py, lines 561-640, matched terms: artifact, direct, documentation, example, one, signal, supports. Strength: contradictory. Source role: test_fixture.

Missing evidence:
- documentation describing boundaries: No selected corpus artifact clearly covers required evidence item 'documentation describing boundaries' for this capability_claim. Suggested fix: Add evidence covering: documentation describing boundaries.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- Add evidence covering: documentation describing boundaries.

### claim_027_520670aa

- Claim: `low`: inference is tentative and should prompt follow-up, not conclusion.
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Confidence; line 24)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 81-160): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 81-160, matched terms: follow, low, not, should, up. Strength: contradictory. Source role: example_output.
- src/workovercv/render.py (section: line range; lines 321-400): Candidate evidence from src/workovercv/render.py, lines 321-400, matched terms: follow, low, not, prompt, up. Strength: contradictory. Source role: source_code.
- src/workovercv/render.py (section: line range; lines 401-480): Candidate evidence from src/workovercv/render.py, lines 401-480, matched terms: follow, not, prompt, should, up. Strength: strong. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 241-320): Candidate evidence from src/workovercv/rubric.py, lines 241-320, matched terms: conclusion, follow, not, should, up. Strength: contradictory. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 801-880): Candidate evidence from src/workovercv/rubric.py, lines 801-880, matched terms: follow, not, prompt, should, up. Strength: strong. Source role: source_code.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_028_f6d9611a

- Claim: WorkOverCV must not make final suitability judgements for or against production ownership, autonomy level, or hiring outcome; those discussions belong to human review with role context and external evidence beyond public repository artifacts.
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Human Review Boundaries; lines 30-33)
- Source role: claim_source
- Auditable claim: False
- Type: generalisation_claim
- Domain: Generalisation and Scope
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Prohibited Inferences; lines 35-64): Candidate evidence from docs/safety_and_taxonomy.md, lines 35-64, matched terms: against, artifacts, beyond, context, evidence, human, not, ownership. Strength: strong. Source role: claim_source.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifacts, evidence, final, hiring, human, level, must, not. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifacts, evidence, final, hiring, human, must, not, public. Strength: contradictory. Source role: runtime_contract.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: artifacts, context, evidence, external, make, not, ownership, production. Strength: contradictory. Source role: example_output.
- src/workovercv/rubric.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/rubric.py, lines 81-160, matched terms: artifacts, context, evidence, make, not, ownership, production, public. Strength: contradictory. Source role: source_code.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_029_4b518f6f

- Claim: Do not infer or report age, disability, health status, neurotype, race, ethnicity, religion, gender identity, sexuality, nationality, family status, financial status, political views, or private life circumstances.
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Prohibited Inferences; lines 37-39)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- src/workovercv/constants.py (section: line range; lines 81-137): Candidate evidence from src/workovercv/constants.py, lines 81-137, matched terms: age, circumstances, disability, ethnicity, family, financial, gender, health. Strength: strong. Source role: source_code.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: do, family, identity, infer, not, private, report. Strength: moderate. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from skills/workovercv/SKILL.md, lines 71-120, matched terms: do, family, identity, infer, not, private, report. Strength: moderate. Source role: claim_source.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: do, infer, not, private, report, status. Strength: moderate. Source role: adapter_contract.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: family, identity, not, report, status. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_030_1674d248

- Claim: "The reviewed repositories provide limited evidence of team collaboration."
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Prohibited Inferences; line 55)
- Source role: claim_source
- Auditable claim: True
- Type: bounded_non_claim
- Domain: Generalisation and Scope
- Importance: high
- Review action: add_evidence_or_remove_claim
- Extraction quality: caveat_or_scope_note
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: unsupported
- Confidence: medium

Found evidence:
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: boundary, collaboration, evidence, provide, repositories, reviewed, team. Strength: contradictory. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 401-480): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 401-480, matched terms: boundary, collaboration, evidence, limitations, repositories, reviewed, scope, team. Strength: contradictory. Source role: example_output.
- tests/test_render_validate.py (section: line range; lines 721-800): Candidate evidence from tests/test_render_validate.py, lines 721-800, matched terms: collaboration, evidence, limitations, repositories, reviewed, scope, team. Strength: contradictory. Source role: test_fixture.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 81-160): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 81-160, matched terms: collaboration, evidence, repositories, reviewed, scope, team. Strength: contradictory. Source role: example_output.
- tests/test_render_validate.py (section: line range; lines 641-720): Candidate evidence from tests/test_render_validate.py, lines 641-720, matched terms: collaboration, evidence, repositories, reviewed, scope, team. Strength: contradictory. Source role: test_fixture.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: No meaningful supporting evidence was found in the selected corpus.

Recommended remediation:
- Either add supporting evidence or remove the claim from audited documentation.

### claim_031_7c975a67

- Claim: WorkOverCV should not conclude suitability for or against unsupervised production ownership without human review, role context, and additional evidence beyond public repository artifacts.
- Source: docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Prohibited Inferences; lines 56-64)
- Source role: claim_source
- Auditable claim: False
- Type: generalisation_claim
- Domain: Generalisation and Scope
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Human Review Boundaries; lines 26-34): Candidate evidence from docs/safety_and_taxonomy.md, lines 26-34, matched terms: against, artifacts, beyond, context, evidence, human, not, ownership. Strength: strong. Source role: claim_source.
- src/workovercv/rubric.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/rubric.py, lines 81-160, matched terms: artifacts, context, evidence, not, ownership, production, public, repository. Strength: contradictory. Source role: source_code.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 1-80): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 1-80, matched terms: artifacts, context, evidence, not, ownership, production, public, repository. Strength: contradictory. Source role: example_output.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifacts, evidence, human, not, public, repository, review, role. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifacts, evidence, human, not, public, repository, review, role. Strength: contradictory. Source role: runtime_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_032_63df0cdb

- Claim: The final `validate` gate checks the required artifacts defined by the current validation implementation and workflow output contract.
- Source: docs/validation_contract.md (section: Validation Contract; lines 3-8)
- Source role: claim_source
- Auditable claim: True
- Type: architecture_claim
- Domain: Architecture
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifacts, checks, contract, current, defined, evidence, files, final. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifacts, checks, contract, evidence, files, final, output, required. Strength: contradictory. Source role: runtime_contract.
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: artifacts, checks, contract, evidence, files, final, gate, implementation. Strength: strong. Source role: claim_source.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: artifacts, checks, contract, contracts, evidence, files, final, implementation. Strength: contradictory. Source role: claim_source.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: contract, current, evidence, final, output, required, validate, workflow. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_033_057230dc

- Claim: `review_scope.yml` is the review boundary and is validated by manifest logic in `src/workovercv/manifest.py`; JSON Schema validation covers the final JSON and JSONL artifacts.
- Source: docs/validation_contract.md (section: Validation Contract; lines 3-8)
- Source role: claim_source
- Auditable claim: True
- Type: process_claim
- Domain: Process and Traceability
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: analysis, artifact, artifacts, boundary, final, history, json, jsonl. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: analysis, artifact, artifacts, boundary, commit, final, history, json. Strength: contradictory. Source role: runtime_contract.
- tests/test_rubric.py (section: line range; lines 1-80): Candidate evidence from tests/test_rubric.py, lines 1-80, matched terms: analysis, artifact, artifacts, boundary, commit, history, incident, json. Strength: strong. Source role: test_fixture.
- src/workovercv/constants.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/constants.py, lines 1-80, matched terms: analysis, artifact, artifacts, boundary, final, json, jsonl, manifest. Strength: strong. Source role: source_code.
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: artifact, artifacts, boundary, final, json, jsonl, py, report. Strength: strong. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_034_858f8c1d

- Claim: Required artifact list: `src/workovercv/constants.py::REQUIRED_FINAL_ARTIFACTS` defines the current final file set checked by `_check_required_files`.
- Source: docs/validation_contract.md (section: Validation Contract; lines 14-15)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifact, artifacts, constants, current, defines, files, final, py. Strength: contradictory. Source role: claim_source.
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: artifact, artifacts, check, checked, constants, file, files, final. Strength: strong. Source role: claim_source.
- src/workovercv/validation.py (section: line range; lines 161-240): Candidate evidence from src/workovercv/validation.py, lines 161-240, matched terms: artifact, artifacts, check, file, files, final, list, required. Strength: contradictory. Source role: source_code.
- src/workovercv/validation.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/validation.py, lines 1-80, matched terms: artifact, artifacts, check, constants, files, final, list, required. Strength: strong. Source role: source_code.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifact, artifacts, file, files, final, required, set, workovercv. Strength: contradictory. Source role: runtime_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_035_75ded822

- Claim: Workflow output contract: `workflows/workovercv.yml` lists the canonical output paths and schemas for final run artifacts.
- Source: docs/validation_contract.md (section: Validation Contract; lines 16-17)
- Source role: claim_source
- Auditable claim: True
- Type: architecture_claim
- Domain: Architecture
- Importance: medium
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: medium_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifacts, canonical, contract, evidence, files, final, lists, module. Strength: contradictory. Source role: claim_source.
- adapters/claude-code/README.md (section: Claude Code Adapter; lines 1-29): Candidate evidence from adapters/claude-code/README.md, lines 1-29, matched terms: artifacts, canonical, contract, output, run, source, workflow, workflows. Strength: strong. Source role: claim_source.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: artifacts, canonical, contract, contracts, evidence, files, final, output. Strength: contradictory. Source role: claim_source.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: contract, output, paths, run, schemas, workflow, workflows, workovercv. Strength: strong. Source role: adapter_contract.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifacts, contract, evidence, files, final, output, run, source. Strength: contradictory. Source role: runtime_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_036_038c6490

- Claim: Complete-run tests: `tests/test_render_validate.py::test_validate_run_accepts_complete_run` proves a complete rendered run is accepted; the missing-artifact tests in the same file prove required final outputs are enforced; and `tests/test_scan.py::test_scan_local_path_writes_valid_run` validates the offline end-to-end scan output.
- Source: docs/validation_contract.md (section: Validation Contract; lines 20-24)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: accepts, artifact, complete, file, final, local, missing, outputs. Strength: strong. Source role: claim_source.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifact, complete, final, local, output, outputs, path, py. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifact, file, final, local, output, outputs, path, render. Strength: contradictory. Source role: runtime_contract.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: artifact, complete, end, final, output, outputs, path, render. Strength: strong. Source role: adapter_contract.
- tests/test_render_validate.py (section: line range; lines 401-480): Candidate evidence from tests/test_render_validate.py, lines 401-480, matched terms: artifact, complete, file, missing, path, py, render, required. Strength: strong. Source role: test_fixture.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_037_9e53727b

- Claim: | Role-family references | `src/workovercv/validation.py::_validate_role_family_fit` and `_validate_report_role_family_fit` require non-empty role-family entries, caveats, supporting signal references, limiting gap references, and interview probes.
- Source: docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 33-34)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Model Performance
- Importance: high
- Review action: keep_evidence_linked
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- src/workovercv/validation.py (section: line range; lines 481-560): Candidate evidence from src/workovercv/validation.py, lines 481-560, matched terms: caveats, entries, family, fit, gap, interview, limiting, probes. Strength: strong. Source role: source_code.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, caveats, direct, documentation, family, fit, gap, interview. Strength: contradictory. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, caveats, direct, documentation, family, fit, gap, interview. Strength: contradictory. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 401-480): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 401-480, matched terms: artifact, caveats, documentation, family, fit, gap, interview, limiting. Strength: contradictory. Source role: example_output.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifact, caveats, entries, family, fit, gap, py, references. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_038_e91a205a

- Claim: | | Gap follow-up structure | `src/workovercv/validation.py::_validate_mitigations` checks mitigation references and requires every evidence gap to have a follow-up record in `mitigations.jsonl`.
- Source: docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 33-34)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Model Performance
- Importance: high
- Review action: keep_evidence_linked
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifact, checks, every, evidence, follow, gap, jsonl, py. Strength: contradictory. Source role: claim_source.
- src/workovercv/validation.py (section: line range; lines 481-560): Candidate evidence from src/workovercv/validation.py, lines 481-560, matched terms: evidence, follow, gap, jsonl, mitigation, mitigations, record, references. Strength: strong. Source role: source_code.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, direct, documentation, every, evidence, follow, gap, jsonl. Strength: contradictory. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, direct, documentation, every, evidence, follow, gap, jsonl. Strength: contradictory. Source role: claim_source.
- README.md (section: WorkOverCV > Strict Validation; lines 107-141): Candidate evidence from README.md, lines 107-141, matched terms: evidence, follow, gap, jsonl, mitigation, mitigations, record, references. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_039_c1f24b8c

- Claim: --- name: workovercv description: Produce evidence-bounded work behaviour profile reports from public GitHub repository evidence using the WorkOverCV workflow, shared CLI, and required structured ledgers.
- Source: skills/workovercv/SKILL.md (section: unheaded; lines 1-4)
- Source role: claim_source
- Auditable claim: False
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: ignore_low_quality_extraction
- Extraction quality: frontmatter_metadata
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: line range; lines 1-5): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 1-5, matched terms: behaviour, bounded, cli, description, evidence, github, ledgers, name. Strength: strong. Source role: adapter_contract.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: behaviour, bounded, cli, evidence, github, ledgers, profile, public. Strength: contradictory. Source role: claim_source.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: behaviour, cli, evidence, github, ledgers, name, profile, repository. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/repo_inventory.json (section: line range; lines 81-136): Candidate evidence from examples/mitchellquinn-20260618-1431Z/repo_inventory.json, lines 81-136, matched terms: behaviour, bounded, description, evidence, github, name, profile, public. Strength: strong. Source role: example_output.
- workflows/workovercv.yml (section: line range; lines 1-80): Candidate evidence from workflows/workovercv.yml, lines 1-80, matched terms: behaviour, bounded, description, evidence, github, produce, profile, public. Strength: strong. Source role: workflow_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is frontmatter metadata and is not an auditable project claim.

Recommended remediation:
- Keep this as source metadata; do not audit it as a project claim.

### claim_040_9b4d66f0

- Claim: It does not make hiring decisions, certify competence, infer protected or private traits, or equate popularity metrics with capability.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV; lines 11-13)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV; lines 6-14): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 6-14, matched terms: capability, certify, competence, decisions, does, equate, hiring, infer. Strength: contradictory. Source role: adapter_contract.
- README.md (section: WorkOverCV; lines 1-15): Candidate evidence from README.md, lines 1-15, matched terms: certify, competence, decisions, does, hiring, infer, make, metrics. Strength: contradictory. Source role: claim_source.
- adapters/codex/README.md (section: Codex Adapter > Boundaries; lines 107-118): Candidate evidence from adapters/codex/README.md, lines 107-118, matched terms: competence, hiring, infer, make, metrics, not, private, protected. Strength: strong. Source role: claim_source.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: competence, infer, make, metrics, not, private, protected, traits. Strength: strong. Source role: adapter_contract.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: competence, hiring, infer, metrics, not, private, protected. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_041_1105624d

- Claim: Use schemas under `schemas/` for the required record shapes.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Source Of Truth; lines 24-25)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Source Of Truth; lines 15-26): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 15-26, matched terms: record, required, schemas, shapes, under, use. Strength: strong. Source role: adapter_contract.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifact, record, required, schemas, shapes, use. Strength: contradictory. Source role: claim_source.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: documentation, record, required, supporting, under, use. Strength: strong. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from skills/workovercv/SKILL.md, lines 71-120, matched terms: documentation, record, required, supporting, under, use. Strength: strong. Source role: claim_source.
- docs/validation_contract.md (section: Validation Contract > Gate Mapping; lines 26-37): Candidate evidence from docs/validation_contract.md, lines 26-37, matched terms: artifact, record, schemas, shapes, supporting. Strength: strong. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_042_fdeae135

- Claim: Do not treat this skill file as the canonical workflow source.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Source Of Truth; lines 24-25)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Source Of Truth; lines 15-26): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 15-26, matched terms: canonical, do, file, not, skill, source, treat, workflow. Strength: strong. Source role: adapter_contract.
- adapters/claude-code/README.md (section: Claude Code Adapter; lines 1-29): Candidate evidence from adapters/claude-code/README.md, lines 1-29, matched terms: canonical, do, not, skill, source, workflow. Strength: strong. Source role: claim_source.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 161-240): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 161-240, matched terms: do, file, not, source, workflow. Strength: contradictory. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 241-320): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 241-320, matched terms: do, file, not, source, workflow. Strength: contradictory. Source role: example_output.
- src/workovercv/rubric.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/rubric.py, lines 1-80, matched terms: do, file, not, source, workflow. Strength: contradictory. Source role: source_code.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_043_30edc1b1

- Claim: Read their markdown/code cells for engineering signal, but do not execute them and do not treat omitted outputs as evidence.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 60-64)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: cells, code, do, engineering, evidence, execute, markdown, not. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 241-320): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 241-320, matched terms: code, do, engineering, evidence, execute, not, omitted, outputs. Strength: contradictory. Source role: example_output.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: code, evidence, execute, markdown, not, outputs, signal, their. Strength: contradictory. Source role: runtime_contract.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: do, evidence, markdown, not, outputs, signal, them, treat. Strength: strong. Source role: adapter_contract.
- skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from skills/workovercv/SKILL.md, lines 71-120, matched terms: do, evidence, markdown, not, outputs, signal, them, treat. Strength: strong. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_044_f0b796ba

- Claim: It may contain bounded commit hashes, subjects, and timestamps, but raw commit hashes, raw commit messages, and raw timelines must not appear in `report.json`, `report.md`, or `summary-report.md`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 66-69)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: appear, bounded, commit, contain, hashes, json, may, md. Strength: strong. Source role: adapter_contract.
- README.md (section: WorkOverCV > Required Final Artifacts; lines 81-106): Candidate evidence from README.md, lines 81-106, matched terms: bounded, commit, contain, hashes, json, may, md, messages. Strength: strong. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: bounded, commit, hashes, json, may, md, messages, must. Strength: contradictory. Source role: runtime_contract.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Work Rhythm and Development Cadence; lines 247-276): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 247-276, matched terms: bounded, commit, hashes, json, may, md, not, raw. Strength: contradictory. Source role: example_output.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 481-504): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 481-504, matched terms: bounded, commit, hashes, may, md, not, raw, subjects. Strength: contradictory. Source role: example_output.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_045_a97b9799

- Claim: Do not emit them as ordinary observed work behaviour signals in `report.json`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 103-105)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: behaviour, do, emit, json, not, observed, ordinary, report. Strength: strong. Source role: adapter_contract.
- README.md (section: WorkOverCV > Strict Validation; lines 107-141): Candidate evidence from README.md, lines 107-141, matched terms: behaviour, do, json, not, observed, report, signals, work. Strength: contradictory. Source role: claim_source.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 121-153, matched terms: behaviour, do, emit, not, observed, report, signals, work. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Observed Work Behaviour Signals > 2. Externalises system boundaries and contracts; lines 41-56): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 41-56, matched terms: behaviour, do, json, not, observed, report, signals, work. Strength: strong. Source role: example_output.
- skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from skills/workovercv/SKILL.md, lines 121-153, matched terms: behaviour, do, emit, not, observed, report, signals, work. Strength: strong. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_046_a28e7eed

- Claim: Describe observable work behaviour, not candidate grades.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; line 109)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: behaviour, candidate, describe, grades, not, observable, work. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/report.json (section: line range; lines 401-480): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.json, lines 401-480, matched terms: behaviour, candidate, not, observable, work. Strength: contradictory. Source role: example_output.
- README.md (section: WorkOverCV; lines 1-15): Candidate evidence from README.md, lines 1-15, matched terms: behaviour, not, observable, work. Strength: contradictory. Source role: claim_source.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: behaviour, candidate, not, work. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/report.md (section: Work Behaviour Profile Report > Scope and Evidence Base; lines 3-13): Candidate evidence from examples/mitchellquinn-20260618-1431Z/report.md, lines 3-13, matched terms: behaviour, candidate, not, work. Strength: strong. Source role: example_output.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_047_8c567b54

- Claim: Treat missing public evidence as uncertainty, not proof of inability.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; line 112)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: evidence, inability, missing, not, proof, public, treat, uncertainty. Strength: strong. Source role: adapter_contract.
- examples/mitchellquinn-20260618-1431Z/screening_brief.md (section: Repository Review Guide; lines 1-5): Candidate evidence from examples/mitchellquinn-20260618-1431Z/screening_brief.md, lines 1-5, matched terms: evidence, inability, missing, not, proof, public. Strength: strong. Source role: example_output.
- src/workovercv/render.py (section: line range; lines 321-400): Candidate evidence from src/workovercv/render.py, lines 321-400, matched terms: evidence, inability, missing, not, proof, public. Strength: contradictory. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 241-320): Candidate evidence from src/workovercv/rubric.py, lines 241-320, matched terms: evidence, missing, not, proof, public, uncertainty. Strength: contradictory. Source role: source_code.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: evidence, inability, missing, not, public. Strength: contradictory. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_048_097882f0

- Claim: Record the active agent/model in `report.json` under `analysis_model_information`; use the model identity exposed by the host environment, or state that the model was not disclosed by the runtime.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; line 119)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: active, agent, analysis, disclosed, environment, exposed, host, identity. Strength: strong. Source role: adapter_contract.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: active, agent, analysis, environment, exposed, host, identity, information. Strength: contradictory. Source role: runtime_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: active, agent, analysis, environment, exposed, host, identity, information. Strength: contradictory. Source role: claim_source.
- tests/test_render_validate.py (section: line range; lines 1-80): Candidate evidence from tests/test_render_validate.py, lines 1-80, matched terms: analysis, environment, information, json, model, not, record, report. Strength: strong. Source role: test_fixture.
- README.md (section: WorkOverCV > Strict Validation; lines 107-141): Candidate evidence from README.md, lines 107-141, matched terms: analysis, environment, information, json, model, not, record, report. Strength: contradictory. Source role: claim_source.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_049_a14f7146

- Claim: Do not infer or invent model/provider details.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; line 119)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: details, do, infer, invent, model, not, provider. Strength: strong. Source role: adapter_contract.
- docs/adapter_contract.md (section: Adapter Contract; lines 1-22): Candidate evidence from docs/adapter_contract.md, lines 1-22, matched terms: do, infer, invent, not. Strength: strong. Source role: adapter_contract.
- docs/safety_and_taxonomy.md (section: Safety And Taxonomy > Prohibited Inferences; lines 35-64): Candidate evidence from docs/safety_and_taxonomy.md, lines 35-64, matched terms: do, infer, model, not. Strength: strong. Source role: claim_source.
- README.md (section: WorkOverCV > Strict Validation; lines 107-141): Candidate evidence from README.md, lines 107-141, matched terms: do, model, not. Strength: contradictory. Source role: claim_source.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Runtime Flow; lines 27-70): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 27-70, matched terms: do, model, not. Strength: moderate. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_050_28e69cdf

- Claim: It must include the rendered `analysis_model_information` value.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; line 139)
- Source role: claim_source
- Auditable claim: False
- Type: other_claim
- Domain: Documentation Policy
- Importance: low
- Review action: ignore_low_quality_extraction
- Extraction quality: policy_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 121-153, matched terms: analysis, include, information, model, must, rendered, value. Strength: strong. Source role: adapter_contract.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: analysis, include, information, model, must, rendered. Strength: contradictory. Source role: runtime_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: analysis, include, information, model, must. Strength: contradictory. Source role: claim_source.
- src/workovercv/rubric.py (section: line range; lines 561-640): Candidate evidence from src/workovercv/rubric.py, lines 561-640, matched terms: analysis, model, must, rendered, value. Strength: contradictory. Source role: source_code.
- src/workovercv/render.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/render.py, lines 81-160, matched terms: analysis, information, model, must. Strength: strong. Source role: source_code.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This extraction is too fragmentary or artifact-like for priority review and is demoted to the full listing.

Recommended remediation:
- Do not treat this reference or low-quality record as an auditable project claim.

### claim_051_c406bafc

- Claim: Do not emit `Strengths`, `Weaknesses`, `Opportunities`, or `Mitigations of Weaknesses`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 141-142)
- Source role: claim_source
- Auditable claim: False
- Type: bounded_non_claim
- Domain: Other
- Importance: low
- Review action: keep_as_boundary_note
- Extraction quality: boundary_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 121-153, matched terms: do, emit, mitigations, not, opportunities, strengths, weaknesses. Strength: strong. Source role: adapter_contract.
- README.md (section: WorkOverCV > Strict Validation; lines 107-141): Candidate evidence from README.md, lines 107-141, matched terms: do, mitigations, not, opportunities, strengths, weaknesses. Strength: contradictory. Source role: claim_source.
- tests/test_render_validate.py (section: line range; lines 1-80): Candidate evidence from tests/test_render_validate.py, lines 1-80, matched terms: mitigations, not, opportunities, strengths, weaknesses. Strength: strong. Source role: test_fixture.
- src/workovercv/constants.py (section: line range; lines 81-137): Candidate evidence from src/workovercv/constants.py, lines 81-137, matched terms: mitigations, opportunities, strengths, weaknesses. Strength: strong. Source role: source_code.
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Agentic Analysis Duties; lines 71-120): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 71-120, matched terms: do, emit, mitigations, not. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This is a boundary, safety, or non-goal statement and is retained as context rather than audited as an implementation claim.

Recommended remediation:
- Keep this as a boundary or non-goal note; do not audit it as an implementation claim.

### claim_052_e6694079

- Claim: The final `summary-report.md` must render as a shorter human-facing conversation guide titled `Work Behaviour Profile Summary`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 144-150)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 121-153, matched terms: behaviour, conversation, facing, final, guide, human, md, must. Strength: strong. Source role: adapter_contract.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: behaviour, conversation, facing, final, guide, human, md, must. Strength: contradictory. Source role: claim_source.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifact, facing, final, guide, human, md, must, profile. Strength: contradictory. Source role: runtime_contract.
- docs/implementation_map.md (section: Implementation Map; lines 1-28): Candidate evidence from docs/implementation_map.md, lines 1-28, matched terms: artifact, behaviour, facing, final, human, md, must, profile. Strength: contradictory. Source role: claim_source.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: artifact, behaviour, final, md, must, profile, render, report. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_053_33caf85a

- Claim: It should include scope, executive synthesis, top observed work behaviour signals, problem-solving style, environment fit, role-family discussion routes, evidence gaps to clarify, and confidence notes.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 144-150)
- Source role: claim_source
- Auditable claim: False
- Type: other_claim
- Domain: Generalisation and Scope
- Importance: low
- Review action: ignore_low_quality_extraction
- Extraction quality: policy_statement
- Claim surface status: low_claim_surface
- Verification mode: not_verifiable_from_available_material
- Verdict: ambiguous
- Confidence: low

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 121-153, matched terms: behaviour, clarify, confidence, discussion, environment, evidence, executive, family. Strength: strong. Source role: adapter_contract.
- tests/test_render_validate.py (section: line range; lines 1-80): Candidate evidence from tests/test_render_validate.py, lines 1-80, matched terms: behaviour, clarify, confidence, discussion, environment, evidence, executive, family. Strength: strong. Source role: test_fixture.
- src/workovercv/render.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/render.py, lines 81-160, matched terms: behaviour, confidence, environment, evidence, executive, family, fit, gaps. Strength: strong. Source role: source_code.
- src/workovercv/constants.py (section: line range; lines 1-80): Candidate evidence from src/workovercv/constants.py, lines 1-80, matched terms: behaviour, confidence, environment, evidence, executive, family, fit, gaps. Strength: strong. Source role: source_code.
- tests/test_render_validate.py (section: line range; lines 721-800): Candidate evidence from tests/test_render_validate.py, lines 721-800, matched terms: behaviour, confidence, environment, evidence, executive, family, fit, gaps. Strength: contradictory. Source role: test_fixture.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: This extraction is too fragmentary or artifact-like for priority review and is demoted to the full listing.

Recommended remediation:
- Do not treat this reference or low-quality record as an auditable project claim.

### claim_054_66c64e30

- Claim: It must use concise repository/path evidence references, avoid full evidence tables, avoid an Evidence Appendix, and avoid old SWOT-style headings.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 144-150)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Required Report Sections; lines 121-153): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 121-153, matched terms: appendix, avoid, concise, evidence, full, headings, must, old. Strength: strong. Source role: adapter_contract.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: appendix, artifact, concise, evidence, headings, must, old, path. Strength: contradictory. Source role: runtime_contract.
- tests/test_render_validate.py (section: line range; lines 1-80): Candidate evidence from tests/test_render_validate.py, lines 1-80, matched terms: appendix, artifact, evidence, full, headings, path, references, repository. Strength: strong. Source role: test_fixture.
- README.md (section: WorkOverCV > V0.6 Shape; lines 16-80): Candidate evidence from README.md, lines 16-80, matched terms: appendix, concise, evidence, must, old, path, references, repository. Strength: contradictory. Source role: claim_source.
- tests/test_render_validate.py (section: line range; lines 81-160): Candidate evidence from tests/test_render_validate.py, lines 81-160, matched terms: appendix, artifact, evidence, full, path, references, repository, tables. Strength: strong. Source role: test_fixture.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_055_1d9200d1

- Claim: `repo_id` must exist in `repo_inventory.json`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; line 158)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, direct, documentation, exist, id, inventory, json, must. Strength: contradictory. Source role: adapter_contract.
- src/workovercv/manifest.py (section: line range; lines 1-70): Candidate evidence from src/workovercv/manifest.py, lines 1-70, matched terms: exist, id, inventory, json, must, repo. Strength: strong. Source role: source_code.
- src/workovercv/collect.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/collect.py, lines 81-160, matched terms: artifact, exist, id, inventory, json, repo. Strength: strong. Source role: source_code.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: artifact, id, inventory, json, must, repo. Strength: strong. Source role: adapter_contract.
- adapters/codex/VERIFY.md (section: Codex Adapter Verification > Required Evidence; lines 39-65): Candidate evidence from adapters/codex/VERIFY.md, lines 39-65, matched terms: artifact, exist, id, inventory, json, repo. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_056_f693cd0f

- Claim: `artifact_id` and `path` must exist in `artifact_inventory.json` or the collected `review_corpus.jsonl`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; line 159)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, collected, corpus, direct, documentation, exist, id, inventory. Strength: contradictory. Source role: adapter_contract.
- src/workovercv/rubric.py (section: line range; lines 241-320): Candidate evidence from src/workovercv/rubric.py, lines 241-320, matched terms: artifact, collected, corpus, direct, id, inventory, json, jsonl. Strength: contradictory. Source role: source_code.
- docs/runtime_contract.md (section: Runtime Contract > Commands; lines 11-90): Candidate evidence from docs/runtime_contract.md, lines 11-90, matched terms: artifact, collected, corpus, inventory, json, jsonl, must, path. Strength: contradictory. Source role: runtime_contract.
- tests/test_analyze.py (section: line range; lines 1-80): Candidate evidence from tests/test_analyze.py, lines 1-80, matched terms: artifact, collected, corpus, id, inventory, json, jsonl, path. Strength: strong. Source role: test_fixture.
- adapters/codex/SMOKE.md (section: Codex Adapter Smoke Verification > Historical 2026-06-17 GitHub Profile Smoke; lines 3-73): Candidate evidence from adapters/codex/SMOKE.md, lines 3-73, matched terms: artifact, corpus, id, inventory, json, jsonl, must, path. Strength: strong. Source role: adapter_contract.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_057_50105854

- Claim: `evidence_ids` must exist in `evidence_map.jsonl`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; line 160)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, direct, documentation, evidence, exist, ids, jsonl, map. Strength: contradictory. Source role: adapter_contract.
- docs/runtime_contract.md (section: Runtime Contract > Required Final Outputs; lines 91-121): Candidate evidence from docs/runtime_contract.md, lines 91-121, matched terms: artifact, evidence, exist, jsonl, map, must. Strength: strong. Source role: runtime_contract.
- tests/test_render_validate.py (section: line range; lines 561-640): Candidate evidence from tests/test_render_validate.py, lines 561-640, matched terms: artifact, direct, documentation, evidence, ids, jsonl, map. Strength: contradictory. Source role: test_fixture.
- src/workovercv/rubric.py (section: line range; lines 241-320): Candidate evidence from src/workovercv/rubric.py, lines 241-320, matched terms: artifact, direct, evidence, ids, jsonl, map. Strength: contradictory. Source role: source_code.
- tests/test_rubric.py (section: line range; lines 1-80): Candidate evidence from tests/test_rubric.py, lines 1-80, matched terms: artifact, documentation, evidence, ids, jsonl, map. Strength: strong. Source role: test_fixture.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_058_e9713652

- Claim: `related_signal_ids` must exist in `signal_ledger.jsonl`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; line 161)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, direct, documentation, exist, ids, jsonl, ledger, must. Strength: contradictory. Source role: adapter_contract.
- src/workovercv/validation.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/validation.py, lines 81-160, matched terms: artifact, ids, jsonl, ledger, related, signal. Strength: strong. Source role: source_code.
- docs/runtime_contract.md (section: Runtime Contract > Required Final Outputs; lines 91-121): Candidate evidence from docs/runtime_contract.md, lines 91-121, matched terms: artifact, exist, jsonl, ledger, must, signal. Strength: strong. Source role: runtime_contract.
- tests/test_render_validate.py (section: line range; lines 561-640): Candidate evidence from tests/test_render_validate.py, lines 561-640, matched terms: artifact, direct, documentation, ids, jsonl, ledger, signal. Strength: contradictory. Source role: test_fixture.
- tests/test_render_validate.py (section: line range; lines 641-720): Candidate evidence from tests/test_render_validate.py, lines 641-720, matched terms: artifact, documentation, ids, jsonl, related, signal, supporting. Strength: contradictory. Source role: test_fixture.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.

### claim_059_2fd6faa4

- Claim: `related_gap_id` and `limiting_gap_ids` must exist in `gap_register.jsonl`.
- Source: skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; line 162)
- Source role: claim_source
- Auditable claim: True
- Type: other_claim
- Domain: Other
- Importance: low
- Review action: no_action
- Extraction quality: auditable_claim
- Claim surface status: low_claim_surface
- Verification mode: documentation_review
- Verdict: supported
- Confidence: high

Found evidence:
- adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md (section: WorkOverCV > Structured Artifact Templates; lines 154-198): Candidate evidence from adapters/codex/plugin/workovercv/skills/workovercv/SKILL.md, lines 154-198, matched terms: artifact, direct, documentation, exist, gap, id, ids, jsonl. Strength: contradictory. Source role: adapter_contract.
- tests/test_render_validate.py (section: line range; lines 641-720): Candidate evidence from tests/test_render_validate.py, lines 641-720, matched terms: artifact, documentation, gap, id, ids, jsonl, limiting, register. Strength: contradictory. Source role: test_fixture.
- src/workovercv/validation.py (section: line range; lines 481-560): Candidate evidence from src/workovercv/validation.py, lines 481-560, matched terms: gap, id, ids, jsonl, limiting, related, supporting. Strength: strong. Source role: source_code.
- src/workovercv/validation.py (section: line range; lines 81-160): Candidate evidence from src/workovercv/validation.py, lines 81-160, matched terms: artifact, gap, id, ids, jsonl, register, related. Strength: strong. Source role: source_code.
- src/workovercv/rubric.py (section: line range; lines 1201-1280): Candidate evidence from src/workovercv/rubric.py, lines 1201-1280, matched terms: artifact, gap, id, ids, limiting, related, supporting. Strength: strong. Source role: source_code.

Missing evidence:
- None identified.

Artifact gaps:
- None identified.

Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

Recommended remediation:
- None.
