---
name: workovercv
description: Produce evidence-bounded work behaviour profile reports from public GitHub repository evidence using the WorkOverCV workflow, shared CLI, and required structured ledgers.
---

# WorkOverCV

Use this skill when asked to assess employment-relevant work behaviour signals
from public GitHub repositories with WorkOverCV.

WorkOverCV turns public repository evidence into an auditable Work Behaviour
Profile Report. It does not make hiring decisions, certify competence, infer
protected or private traits, or equate popularity metrics with capability.

## Source Of Truth

Before running or completing an assessment, read:

- `workflows/workovercv.yml`
- `docs/runtime_contract.md`
- `docs/manifest_contract.md`
- `docs/safety_and_taxonomy.md`

Use schemas under `schemas/` for the required record shapes. Do not treat this
skill file as the canonical workflow source.

## Runtime Flow

Examples below use the installed console command. In a development checkout,
use the same arguments with `PYTHONPATH=src python -m workovercv ...`; on
PowerShell, first run `$env:PYTHONPATH = "src"`.

For a public GitHub user:

```bash
workovercv discover --candidate https://github.com/<user>
```

Inspect the generated `review_scope.yml`. The scope manifest is the hard
boundary. Only repositories with `selected_for_review: true` may be collected or
analyzed unless the user edits the scope and asks you to continue.

Then run:

```bash
workovercv collect --scope output/<run>/review_scope.yml
```

For deterministic rubric analysis, run:

```bash
workovercv analyze --run output/<run>
```

For agent-authored analysis, write the structured ledgers and `report.json`
manually after collection. In both modes, use `review_corpus.jsonl`,
`repo_inventory.json`, `artifact_inventory.json`, `work_chronology.json`, and
`review_scope.yml` as the evidence boundary.

Notebook artifacts with `artifact_type` `notebook_source` are static source-only
projections. Read their markdown/code cells for engineering signal, but do not
execute them and do not treat omitted outputs as evidence. Prefer committed
metrics, model cards, run manifests, tests, source files, or technical reports
for metric validity, runtime reliability, and deployment claims.

`work_chronology.json` is analysis input. It may contain bounded commit hashes,
subjects, and timestamps, but raw commit hashes, raw commit messages, and raw
timelines must not appear in `report.json`, `report.md`, or
`summary-report.md`.

## Agentic Analysis Duties

Write the required structured artifacts:

- `explicit_claims.jsonl`
- `signal_ledger.jsonl`
- `evidence_map.jsonl`
- `gap_register.jsonl`
- `role_family_fit.json`
- `mitigations.jsonl`
- `red_team_review.json`
- `report.json`

Then run `workovercv render` to produce the required Markdown outputs:

- `report.md`
- `summary-report.md`
- `screening_brief.md`

Use only the closed signal categories:

- `documentation_and_handoff`
- `system_design`
- `implementation_execution`
- `validation_and_reliability`
- `measurement_and_evaluation`
- `maintainability`
- `experimentation_and_learning`
- `product_packaging`
- `development_cadence`
- `authorship_bounds`

For deterministic v0.6 output, treat `development_cadence` and
`authorship_bounds` as meta-level interpretation limits. Do not emit them as
ordinary observed work behaviour signals in `report.json`.

For each final report:

1. Describe observable work behaviour, not candidate grades.
2. Use Evidence -> Implication -> Confidence for major statements.
3. Bind every signal, role-family entry, and gap to in-bound evidence or known evidence gaps.
4. Treat missing public evidence as uncertainty, not proof of inability.
5. Ensure every evidence gap has a follow-up record in `mitigations.jsonl`.
6. Ensure every role-family entry has supporting signals and caveats.
7. Avoid protected/private trait inference.
8. Avoid hiring recommendations.
9. Avoid loaded labels such as "red flag"; frame limits as evidence gaps or follow-up areas.
10. Treat stars, forks, watchers, followers, and commit velocity only as weak public context, never competence metrics.
11. Record the active agent/model in `report.json` under `analysis_model_information`; use the model identity exposed by the host environment, or state that the model was not disclosed by the runtime. Do not infer or invent model/provider details.

## Required Report Sections

The final `report.md` is the full audit-oriented report and must render only
the Work Behaviour Profile sections:

- `Scope and Evidence Base`
- `How to Use This Report`
- `Executive Work Profile`
- `Observed Work Behaviour Signals`
- `Engineering Habits`
- `Problem-Solving Style`
- `Work Rhythm and Development Cadence`
- `Environment Fit`
- `Role-Family Fit`
- `Evidence Gaps and Follow-Up Questions`
- `Confidence and Uncertainty Notes`
- `Evidence Appendix`

It must include the rendered `analysis_model_information` value.

Do not emit `Strengths`, `Weaknesses`, `Opportunities`, or `Mitigations of
Weaknesses`.

The final `summary-report.md` must render as a shorter human-facing conversation
guide titled `Work Behaviour Profile Summary`. It should include scope,
executive synthesis, top observed work behaviour signals, problem-solving
style, environment fit, role-family discussion routes, evidence gaps to
clarify, and confidence notes. It must use concise repository/path evidence
references, avoid full evidence tables, avoid an Evidence Appendix, and avoid
old SWOT-style headings.

It must include the rendered `analysis_model_information` value.

## Structured Artifact Templates

Every ID reference must resolve inside the run boundary:

- `repo_id` must exist in `repo_inventory.json`.
- `artifact_id` and `path` must exist in `artifact_inventory.json` or the collected `review_corpus.jsonl`.
- `evidence_ids` must exist in `evidence_map.jsonl`.
- `related_signal_ids` must exist in `signal_ledger.jsonl`.
- `related_gap_id` and `limiting_gap_ids` must exist in `gap_register.jsonl`.

Valid compact example:

`signal_ledger.jsonl`

```json
{"signal_id":"sig-docs","category":"documentation_and_handoff","label":"Makes technical work inspectable for reviewers","evidence_ids":["ev1"],"evidence_summary":"README explains purpose, setup, and review context.","implication":"This suggests a working style that values external legibility and reviewer handoff.","confidence":"medium","confidence_reason":"Evidence is direct but narrow.","caveats":"Public documentation does not directly prove workplace team handoff behaviour."}
```

`gap_register.jsonl`

```json
{"gap_id":"gap1","repo_id":"example-small","category":"collaboration_visibility_gap","description":"Public repository evidence does not directly show team review, PR discussion, or workplace collaboration.","impact_on_report":"bounds_interpretation","related_signal_ids":["sig-docs"],"suggested_follow_up":"Ask for an example of reviewed team work, handoff notes, or pull request discussion."}
```

`mitigations.jsonl`

```json
{"mitigation_id":"mit1","related_gap_id":"gap1","related_signal_ids":["sig-docs"],"mitigation_type":"interview_probe","recommendation":"Ask for a code review walkthrough.","rationale":"This probes a collaboration evidence gap without treating missing public evidence as inability."}
```

`role_family_fit.json`

```json
{"role_family_fit":[{"role_family":"Software Engineer","why_discuss":"Evidence supports a bounded software-engineering discussion.","behaviour_fit":"Reviewer-facing documentation supports a technical walkthrough.","likely_contribution":"The person would likely contribute inspectable implementation work with clear review context.","interview_probes":["Ask for a code review walkthrough."],"confidence":"medium","caveats":"Interpret with the recorded collaboration evidence gap.","supporting_signal_ids":["sig-docs"],"limiting_gap_ids":["gap1"]}]}
```

When `report.json` is complete, run:

```bash
workovercv render --run output/<run>
workovercv validate --run output/<run>
```

Report the run directory and validation result.

## Red-Team Gate

The final report cannot pass if:

- a signal lacks supporting evidence IDs
- a role-family entry lacks supporting signals or caveats
- an evidence gap lacks a follow-up record
- high-severity red-team issues remain
- protected/private traits are inferred
- missing evidence is treated as proof of inability
- the report makes a hiring decision
- the report or review guide uses loaded risk-label framing
- old SWOT-style report headings appear
- raw chronology data leaks into final report outputs
