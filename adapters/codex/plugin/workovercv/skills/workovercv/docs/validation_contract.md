# Validation Contract

This document maps the validation gates claimed in the README to concrete
implementation and test evidence. The final `validate` gate checks the required
artifacts defined by the current validation implementation and workflow output
contract. `review_scope.yml` is the review boundary and is validated by
manifest logic in `src/workovercv/manifest.py`; JSON Schema validation covers
the final JSON and JSONL artifacts.

Evidence anchors for the required-artifact gate:

- Validation implementation: `src/workovercv/validation.py::validate_run` calls
  `_check_required_files` before loading structured records.
- Required artifact list: `src/workovercv/constants.py::REQUIRED_FINAL_ARTIFACTS`
  defines the current final file set checked by `_check_required_files`.
- Workflow output contract: `workflows/workovercv.yml` lists the canonical
  output paths and schemas for final run artifacts.
- Schema evidence: `schemas/*.schema.json` defines the JSON and JSONL shapes
  loaded by `src/workovercv/validation.py`.
- Complete-run tests: `tests/test_render_validate.py::test_validate_run_accepts_complete_run`
  proves a complete rendered run is accepted; the missing-artifact tests in
  the same file prove required final outputs are enforced; and
  `tests/test_scan.py::test_scan_local_path_writes_valid_run` validates the
  offline end-to-end scan output.

## Gate Mapping

| Gate | Implementation evidence | Schema evidence | Test evidence |
| --- | --- | --- | --- |
| JSON Schema validation | `src/workovercv/validation.py` maps JSON and JSONL artifacts to schema files and validates them with `Draft202012Validator`. | `schemas/*.schema.json`, including strict `additionalProperties: false` where generated records are closed. | `tests/test_render_validate.py::test_validate_run_accepts_complete_run`, `test_validate_run_rejects_legacy_signal_field`, `test_validate_run_rejects_invalid_confidence`; `tests/test_scan.py::test_scan_local_path_writes_valid_run`. |
| Closed enum values | `src/workovercv/validation.py::_validate_closed_signal_enums` checks signal categories and confidence values against `src/workovercv/constants.py`. | Enum definitions in `schemas/signal.schema.json`, `schemas/report.schema.json`, `schemas/evidence.schema.json`, `schemas/mitigation.schema.json`, and related final-artifact schemas. | `tests/test_render_validate.py::test_validate_run_rejects_invalid_signal_category`, `test_validate_run_rejects_invalid_confidence`, `test_validate_run_rejects_meta_category_as_observed_signal`. |
| Evidence boundaries | `src/workovercv/validation.py` builds a boundary index from `repo_inventory.json`, `artifact_inventory.json`, and `review_corpus.jsonl`, then checks repository, artifact, path, evidence, signal, claim, gap, mitigation, and chronology references. | Boundary-bearing shapes in `schemas/repo_inventory.schema.json`, `schemas/artifact_inventory.schema.json`, `schemas/review_corpus.schema.json`, `schemas/evidence.schema.json`, `schemas/explicit_claim.schema.json`, `schemas/signal.schema.json`, `schemas/gap.schema.json`, and `schemas/work_chronology.schema.json`. | `tests/test_render_validate.py::test_validate_run_rejects_missing_repo_reference`, `test_validate_run_rejects_missing_artifact_reference`, `test_validate_run_rejects_missing_file_path`, `test_validate_run_rejects_missing_evidence_reference`, `test_validate_run_rejects_missing_boundary_artifact`, `test_validate_run_rejects_raw_chronology_leak`. |
| Role-family references | `src/workovercv/validation.py::_validate_role_family_fit` and `_validate_report_role_family_fit` require non-empty role-family entries, caveats, supporting signal references, limiting gap references, and interview probes. | `schemas/role_family_fit.schema.json` and the `role_family_fit` section of `schemas/report.schema.json`. | `tests/test_render_validate.py::test_validate_run_rejects_role_family_without_caveats`, `test_validate_run_rejects_empty_role_family_fit`, `test_validate_run_rejects_role_family_unknown_signal_reference`, `test_validate_run_rejects_role_family_unknown_gap_reference`. |
| Gap follow-up structure | `src/workovercv/validation.py::_validate_mitigations` checks mitigation references and requires every evidence gap to have a follow-up record in `mitigations.jsonl`. | `schemas/gap.schema.json` and `schemas/mitigation.schema.json`. | `tests/test_render_validate.py::test_validate_run_rejects_gap_without_follow_up_record`. |
| Old-heading regressions | `src/workovercv/constants.py::OLD_REPORT_HEADINGS` and `src/workovercv/validation.py` heading checks reject legacy report headings and unknown generated Markdown headings. | `schemas/report.schema.json` rejects old report JSON shapes such as legacy `summary` and `findings` fields. | `tests/test_render_validate.py::test_render_report_outputs_full_and_summary_reports_without_legacy_sections`, `test_validate_run_rejects_legacy_report_findings`, `test_validate_run_rejects_legacy_markdown_heading`, `test_validate_run_rejects_legacy_summary_report_heading`, `test_validate_run_rejects_unknown_report_heading`. |
| Safety wording checks | `src/workovercv/constants.py::DISALLOWED_REPORT_PHRASES`, `PROTECTED_TRAIT_TERMS`, and `src/workovercv/validation.py::_validate_prohibited_wording` and `_validate_no_hiring_decisions` check report JSON, generated Markdown, structured ledgers, role-family entries, mitigations, and red-team text. | Safety wording checks are text validators layered on top of schema validation; the schemas define the text-bearing fields being checked. | `tests/test_render_validate.py::test_validate_run_rejects_disallowed_wording`, `test_validate_run_rejects_hiring_decision_language`, `test_validate_run_rejects_disallowed_screening_brief_wording`, `test_validate_run_rejects_disallowed_summary_report_wording`, `test_validate_run_rejects_screening_brief_hiring_language`, `test_validate_run_rejects_summary_report_hiring_language`, `test_validate_run_rejects_disallowed_signal_wording`, `test_validate_run_rejects_protected_evidence_summary`. |

## Acceptance Boundary

A final run is accepted only when `workovercv validate --run <run_dir>` returns
success. `discover` and `collect` produce partial runs, and the scope manifest
is the hard review boundary for later collection and analysis.
