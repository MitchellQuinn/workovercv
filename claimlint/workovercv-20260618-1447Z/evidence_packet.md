# ClaimLint Evidence Packet

## Safely supported claims

- claim_002_a7781a09: It turns public repository artifacts into reviewable evidence, behaviour signals, evidence gaps, role-family discussion routes, and follow-up questions.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_003_e5645ca0: Agent adapters under `adapters/` must point to those contracts rather than redefining the workflow.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_009_6746abcf: The shared runtime contract remains `docs/runtime_contract.md`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_012_b4ce718c: This is packaging only; the canonical workflow and runtime contract remain in the WorkOverCV repository.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_013_bfc91353: Status: v0.6 retest required for the GitHub-profile Codex adapter smoke.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_015_d98cdebb: Use the module paths below as code pointers.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_017_aea193d7: | Runtime behavior or workflow stage | Implementation modules | Evidence notes |
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_018_6e6458f9: | Repository materialization and corpus | `src/workovercv/collect.py` | Clones or reads selected repositories, inventories artifacts with canonical `artifact_type`, chunks text, writes schema-validated `review_corpus.jsonl`, collects bounded `work_chronology.json`, and cleans worktrees by default.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_019_7c06b9d6: | Final validation | `src/workovercv/validation.py` | Checks required artifacts, record references, v0.6 report shape, gap follow-ups, role-family references and caveats, raw chronology leakage, red-team status, prohibited wording, hiring-decision language, and legacy heading regressions.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_020_9d68e0a0: | | Workflow output contract | `workflows/workovercv.yml`, `src/workovercv/constants.py` | Lists canonical output paths and the current `REQUIRED_FINAL_ARTIFACTS` used by the final validation gate.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_021_a72214cc: | | Schema references | `schemas/*.schema.json`, `src/workovercv/validation.py` | Provide machine-readable output shapes and the implementation mapping from final artifacts to schema validators.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_023_a41b6335: The deterministic `analyze` command provides a local rubric path for smoke tests without API calls.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_024_d01f7c52: Code and markdown cells may support signals about experiment design, preprocessing flow, evaluation workflow, and exploratory engineering habits.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_026_dc093b0b: `strong`: multiple concrete artifacts support the signal, or one unusually direct artifact supports it.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_032_63df0cdb: The final `validate` gate checks the required artifacts defined by the current validation implementation and workflow output contract.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_033_057230dc: `review_scope.yml` is the review boundary and is validated by manifest logic in `src/workovercv/manifest.py`; JSON Schema validation covers the final JSON and JSONL artifacts.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_034_858f8c1d: Required artifact list: `src/workovercv/constants.py::REQUIRED_FINAL_ARTIFACTS` defines the current final file set checked by `_check_required_files`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_035_75ded822: Workflow output contract: `workflows/workovercv.yml` lists the canonical output paths and schemas for final run artifacts.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_036_038c6490: Complete-run tests: `tests/test_render_validate.py::test_validate_run_accepts_complete_run` proves a complete rendered run is accepted; the missing-artifact tests in the same file prove required final outputs are enforced; and `tests/test_scan.py::test_scan_local_path_writes_valid_run` validates the offline end-to-end scan output.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_037_9e53727b: | Role-family references | `src/workovercv/validation.py::_validate_role_family_fit` and `_validate_report_role_family_fit` require non-empty role-family entries, caveats, supporting signal references, limiting gap references, and interview probes.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_038_e91a205a: | | Gap follow-up structure | `src/workovercv/validation.py::_validate_mitigations` checks mitigation references and requires every evidence gap to have a follow-up record in `mitigations.jsonl`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_041_1105624d: Use schemas under `schemas/` for the required record shapes.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_052_e6694079: The final `summary-report.md` must render as a shorter human-facing conversation guide titled `Work Behaviour Profile Summary`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_054_66c64e30: It must use concise repository/path evidence references, avoid full evidence tables, avoid an Evidence Appendix, and avoid old SWOT-style headings.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_055_1d9200d1: `repo_id` must exist in `repo_inventory.json`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_056_f693cd0f: `artifact_id` and `path` must exist in `artifact_inventory.json` or the collected `review_corpus.jsonl`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_057_50105854: `evidence_ids` must exist in `evidence_map.jsonl`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_058_e9713652: `related_signal_ids` must exist in `signal_ledger.jsonl`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.
- claim_059_2fd6faa4: `related_gap_id` and `limiting_gap_ids` must exist in `gap_register.jsonl`.
  Verdict: supported. Risk: The selected corpus contains strong matching evidence and no major missing evidence was identified.

## Partially supported claims with caveats

None.

## Claims requiring human/external review

None.

## Claims not supported by selected corpus

- claim_030_1674d248: "The reviewed repositories provide limited evidence of team collaboration."
  Verdict: unsupported. Risk: No meaningful supporting evidence was found in the selected corpus.

## Overclaimed wording

None.

## Suggested README wording improvements

- Link claims directly to selected evidence artifacts where possible.
- Add caveats when metrics depend on missing checkpoints, protocols, or external environments.
- Remove or narrow claims that go beyond selected repository evidence.
