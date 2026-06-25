# Work Behaviour Profile Report

## Scope and Evidence Base

Candidate URL: https://github.com/MitchellQuinn
Repositories reviewed: 5
Artifacts reviewed: 894
Repository names: skilldoctor, workovercv, claimlint, bounded-monocular-perception, industrial-sound-anomaly-detection
The report is based on 894 collected artifact(s), 45 evidence record(s), and bounded chronology inputs from public or local repositories.
This is not a hiring decision record, ranking, background check, or pass/fail assessment.
Private, company, and uncollected work may not be visible in the reviewed repository evidence.
Analysis model information: Deterministic WorkOverCV rubric analysis; no LLM model used.

## How to Use This Report

Use this report as a conversation guide, not a hiring decision record. The strongest use is to identify what to ask about: which artifacts to inspect, which working behaviours appear repeatedly, and which evidence gaps should be clarified through discussion.

## Executive Work Profile

Across 894 collected artifact(s) from 5 repository record(s), the reviewed work suggests an engineer who tends to make technical work inspectable: project purpose, boundaries, reviewer context, and packaging are repeatedly externalised into durable artifacts. The strongest pattern is systems-oriented work made reviewable through runnable code surfaces, tests, metrics, manifests, or evaluation records, project structure that supports later modification, and experiment, model, notebook, or failure-analysis traces. Confidence is strongest for documentation and handoff habits, system-boundary habits, implementation habits, and validation habits. Public evidence remains weaker for live collaboration, operational pressure, and private or company work unless those traces are present in the collected corpus. Evidence gaps are explicit: 3 follow-up area(s) bound interpretation rather than serving as adverse conclusions.

## Observed Work Behaviour Signals

### 1. Makes technical work inspectable for reviewers

Category: documentation_and_handoff
Evidence: Reviewer-facing documentation explains purpose, usage, boundaries, or operating assumptions. The evidence bundle contains 5 artifacts across 3 repositories, including readme, technical writeup, and architecture document; reviewers can quickly understand purpose, setup, and stated limits.
Implication: This suggests a working style that values external legibility, explicit context, and reviewer handoff.
Confidence: high
Caveats: Public documentation does not directly prove workplace team handoff behavior.
Evidence references: ev-001-documentation-reviewer-context-01, ev-001-documentation-reviewer-context-02, ev-001-documentation-reviewer-context-03, ev-001-documentation-reviewer-context-04, ev-001-documentation-reviewer-context-05

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-001-documentation-reviewer-context-01 | mitchellquinn-skilldoctor | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-03 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-04 | mitchellquinn-workovercv | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-05 | mitchellquinn-claimlint | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |

### 2. Externalises system boundaries and contracts

Category: system_design
Evidence: Architecture, contract, and configuration artifacts expose design intent, workflow boundaries, or runtime interfaces. The evidence bundle contains 5 artifacts across 4 repositories, including architecture document, technical writeup, and configuration file; technical reviewers can probe design tradeoffs and ownership boundaries.
Implication: This suggests a tendency to make system shape and operating constraints explicit before or during implementation.
Confidence: high
Caveats: Repository artifacts show documented boundaries but do not prove how these decisions were negotiated in a team.
Evidence references: ev-002-architecture-explicit-boundaries-01, ev-002-architecture-explicit-boundaries-02, ev-002-architecture-explicit-boundaries-03, ev-002-architecture-explicit-boundaries-04, ev-002-architecture-explicit-boundaries-05

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-002-architecture-explicit-boundaries-01 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-03 | mitchellquinn-skilldoctor | schemas/run_manifest.schema.json | configuration_file | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-04 | mitchellquinn-claimlint | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-05 | mitchellquinn-bounded-monocular-perception | documents/specifications/Live Inference Pipeline - Architecture Sketch v0.3.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |

### 3. Translates ideas into runnable, inspectable systems

Category: implementation_execution
Evidence: Implementation artifacts expose concrete runtime behavior rather than only project descriptions. The evidence bundle contains 5 artifacts across 4 repositories, including source code, inference script, training script, and evaluation script; technical reviewers can inspect how ideas are translated into runnable code.
Implication: This suggests a working style oriented toward executable artifacts that reviewers can inspect and run.
Confidence: high
Caveats: Static source inspection does not prove production runtime reliability or operational ownership.
Evidence references: ev-003-implementation-inspectable-runtime-01, ev-003-implementation-inspectable-runtime-02, ev-003-implementation-inspectable-runtime-03, ev-003-implementation-inspectable-runtime-04, ev-003-implementation-inspectable-runtime-05

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-003-implementation-inspectable-runtime-01 | mitchellquinn-bounded-monocular-perception | scripts/analyze_brightness_run.py | source_code | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-02 | mitchellquinn-skilldoctor | src/skill_doctor/infer_contract.py | inference_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-03 | mitchellquinn-industrial-sound-anomaly-detection | preprocessing/export_2d_training.py | training_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-04 | mitchellquinn-bounded-monocular-perception | 03_rb-training-v2.0/src/evaluate.py | evaluation_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-05 | mitchellquinn-claimlint | src/claimlint/classify_claims.py | source_code | Selected because it provides runnable or inspectable implementation evidence. |

### 4. Adds validation gates around technical claims and runtime behaviour

Category: validation_and_reliability
Evidence: Test and CI artifacts provide direct evidence of reliability checks and validation gates. The evidence bundle contains 5 artifacts across 3 repositories, including test file; reviewers can route the conversation toward validation habits instead of relying on repository size.
Implication: This suggests a habit of surrounding implementation work with repeatable checks.
Confidence: medium
Caveats: Repository tests show public validation behavior, not the full reliability practices used in private or deployed systems.
Evidence references: ev-004-testing-validation-gates-01, ev-004-testing-validation-gates-02, ev-004-testing-validation-gates-03, ev-004-testing-validation-gates-04, ev-004-testing-validation-gates-05

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-004-testing-validation-gates-01 | mitchellquinn-workovercv | tests/test_analyze.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-02 | mitchellquinn-claimlint | tests/test_claim_extraction.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-03 | mitchellquinn-skilldoctor | tests/test_cli_audit.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-04 | mitchellquinn-claimlint | tests/test_cli_audit.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-05 | mitchellquinn-workovercv | tests/test_collect.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |

### 5. Prefers measured evidence over assertion

Category: measurement_and_evaluation
Evidence: Evaluation, model, run, or data manifest artifacts make measurement workflow and benchmark context inspectable. The evidence bundle contains 5 artifacts across 3 repositories, including evaluation script, model card, run manifest, and data manifest; applied-ML reviewers can ask targeted questions about metric validity and evaluation design.
Implication: This suggests a tendency to support technical claims with measurement artifacts and reproducibility context.
Confidence: high
Caveats: Metric artifacts need domain review before being treated as proof of model or system quality.
Evidence references: ev-005-evaluation-measurement-artifacts-01, ev-005-evaluation-measurement-artifacts-02, ev-005-evaluation-measurement-artifacts-03, ev-005-evaluation-measurement-artifacts-04, ev-005-evaluation-measurement-artifacts-05

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-005-evaluation-measurement-artifacts-01 | mitchellquinn-bounded-monocular-perception | 03_rb-training-v2.0/src/evaluate.py | evaluation_script | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-02 | mitchellquinn-industrial-sound-anomaly-detection | models/20260319-1829-2d_sound_v0.2/model_card.md | model_card | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-03 | mitchellquinn-workovercv | claimlint/workovercv-20260618-1447Z/run_manifest.json | run_manifest | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-04 | mitchellquinn-industrial-sound-anomaly-detection | models/20260320-1607-2d_sound_v0.4/metrics.json | data_manifest | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-05 | mitchellquinn-bounded-monocular-perception | 04_ROI-FCN/02_training/src/roi_fcn_training_v0_1/evaluate.py | evaluation_script | Selected because it exposes measurement, benchmark, model, data, or run context. |

### 6. Structures projects for modification and handoff

Category: maintainability
Evidence: Configuration, source organization, and supporting documentation expose maintainability-relevant project structure. The evidence bundle contains 5 artifacts across 3 repositories, including configuration file, source code, technical writeup, and architecture document; founders can inspect whether the work is organized for handoff and repeated modification.
Implication: This suggests attention to project shape, repeatable setup, and future modification.
Confidence: high
Caveats: Public structure does not prove long-term maintenance in a production organization.
Evidence references: ev-006-maintainability-project-structure-01, ev-006-maintainability-project-structure-02, ev-006-maintainability-project-structure-03, ev-006-maintainability-project-structure-04, ev-006-maintainability-project-structure-05

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-006-maintainability-project-structure-01 | mitchellquinn-skilldoctor | pyproject.toml | configuration_file | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-02 | mitchellquinn-bounded-monocular-perception | 02_synthetic-data-processing-v4.0/rb_pipeline_v4/config.py | source_code | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-03 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-04 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-05 | mitchellquinn-workovercv | pyproject.toml | configuration_file | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |

### 7. Explores uncertain technical spaces while preserving traceability

Category: experimentation_and_learning
Evidence: Research, experiment, model-card, notebook-source, or failure-analysis artifacts expose exploratory workflow and tradeoff records. The evidence bundle contains 4 artifacts across 2 repositories, including failure analysis, model card, training script, and notebook source; research-oriented reviewers can discuss experiment design, iteration, and failure analysis.
Implication: This suggests comfort with uncertain technical spaces when there is a visible trail of experiments and tradeoffs.
Confidence: medium
Caveats: Notebook source and experiment traces are static evidence; WorkOverCV does not execute them or validate omitted outputs.
Evidence references: ev-007-research-experimentation-trace-01, ev-007-research-experimentation-trace-02, ev-007-research-experimentation-trace-03, ev-007-research-experimentation-trace-04

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-007-research-experimentation-trace-01 | mitchellquinn-bounded-monocular-perception | failure-analysis/failure-analysis-index.md | failure_analysis | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |
| ev-007-research-experimentation-trace-02 | mitchellquinn-industrial-sound-anomaly-detection | models/20260319-1829-2d_sound_v0.2/model_card.md | model_card | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |
| ev-007-research-experimentation-trace-03 | mitchellquinn-industrial-sound-anomaly-detection | preprocessing/export_2d_training.py | training_script | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |
| ev-007-research-experimentation-trace-04 | mitchellquinn-bounded-monocular-perception | 03_rb-training-v2.0/notebooks/01_dataset_audit_v0.1.ipynb | notebook_source | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |

### 8. Packages technical work so other people can understand and interrogate it

Category: product_packaging
Evidence: Product or reviewer-positioning artifacts show how the work is packaged, explained, or made usable by others. The evidence bundle contains 5 artifacts across 4 repositories, including readme, technical writeup, and configuration file; reviewers can identify whether the work is framed for users, reviewers, or adapter consumers.
Implication: This suggests attention to audience, usage context, and public inspectability.
Confidence: high
Caveats: Public packaging does not by itself prove user adoption or product-market fit.
Evidence references: ev-008-product-reviewer-positioning-01, ev-008-product-reviewer-positioning-02, ev-008-product-reviewer-positioning-03, ev-008-product-reviewer-positioning-04, ev-008-product-reviewer-positioning-05

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-008-product-reviewer-positioning-01 | mitchellquinn-skilldoctor | README.md | README | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-03 | mitchellquinn-workovercv | adapters/status.yml | configuration_file | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-04 | mitchellquinn-claimlint | README.md | README | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-05 | mitchellquinn-bounded-monocular-perception | README.md | README | Selected because it packages the work for technical readers, users, or adapter reviewers. |

## Engineering Habits

### 1. Externalising context and boundaries

Documentation and design-boundary evidence point to a habit of moving context out of private assumptions and into artifacts that reviewers can inspect.
Supporting signals: sig-001-documentation-reviewer-context, sig-002-architecture-explicit-boundaries
Confidence: high
Caveats: Public documentation does not directly prove workplace team handoff behavior. Repository artifacts show documented boundaries but do not prove how these decisions were negotiated in a team.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-001-documentation-reviewer-context-01 | mitchellquinn-skilldoctor | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-03 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-04 | mitchellquinn-workovercv | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-05 | mitchellquinn-claimlint | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |

### 2. Building inspectable runnable artifacts

Implementation evidence shows ideas being converted into code surfaces that can be inspected, run, or traced by another technical reader.
Supporting signals: sig-003-implementation-inspectable-runtime
Confidence: high
Caveats: Static source inspection does not prove production runtime reliability or operational ownership.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-003-implementation-inspectable-runtime-01 | mitchellquinn-bounded-monocular-perception | scripts/analyze_brightness_run.py | source_code | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-02 | mitchellquinn-skilldoctor | src/skill_doctor/infer_contract.py | inference_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-03 | mitchellquinn-industrial-sound-anomaly-detection | preprocessing/export_2d_training.py | training_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-04 | mitchellquinn-bounded-monocular-perception | 03_rb-training-v2.0/src/evaluate.py | evaluation_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-05 | mitchellquinn-claimlint | src/claimlint/classify_claims.py | source_code | Selected because it provides runnable or inspectable implementation evidence. |

### 3. Validating claims through tests, manifests, metrics, or run records

Validation and measurement evidence shows technical claims being surrounded by checks, benchmark context, manifests, or reproducibility records.
Supporting signals: sig-004-testing-validation-gates, sig-005-evaluation-measurement-artifacts
Confidence: medium
Caveats: Repository tests show public validation behavior, not the full reliability practices used in private or deployed systems. Metric artifacts need domain review before being treated as proof of model or system quality.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-004-testing-validation-gates-01 | mitchellquinn-workovercv | tests/test_analyze.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-02 | mitchellquinn-claimlint | tests/test_claim_extraction.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-03 | mitchellquinn-skilldoctor | tests/test_cli_audit.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-04 | mitchellquinn-claimlint | tests/test_cli_audit.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-05 | mitchellquinn-workovercv | tests/test_collect.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |

### 4. Structuring work for modification and review

Project structure, configuration, boundaries, and checks create surfaces for later modification and focused technical review.
Supporting signals: sig-002-architecture-explicit-boundaries, sig-004-testing-validation-gates, sig-006-maintainability-project-structure
Confidence: medium
Caveats: Repository artifacts show documented boundaries but do not prove how these decisions were negotiated in a team. Repository tests show public validation behavior, not the full reliability practices used in private or deployed systems.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-002-architecture-explicit-boundaries-01 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-03 | mitchellquinn-skilldoctor | schemas/run_manifest.schema.json | configuration_file | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-04 | mitchellquinn-claimlint | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-05 | mitchellquinn-bounded-monocular-perception | documents/specifications/Live Inference Pipeline - Architecture Sketch v0.3.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |

### 5. Packaging work for technical readers

Packaging and documentation evidence frames the work for readers who need setup context, usage paths, and points to interrogate.
Supporting signals: sig-001-documentation-reviewer-context, sig-008-product-reviewer-positioning
Confidence: high
Caveats: Public documentation does not directly prove workplace team handoff behavior. Public packaging does not by itself prove user adoption or product-market fit.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-001-documentation-reviewer-context-01 | mitchellquinn-skilldoctor | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-03 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-04 | mitchellquinn-workovercv | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-05 | mitchellquinn-claimlint | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |

## Problem-Solving Style

The reviewed work suggests a problem-solving style that turns uncertain technical spaces into bounded, inspectable systems. Ambiguity is narrowed through explicit boundaries, runnable implementations, checks, metrics, or reproducibility records, and experiment or failure-analysis traces. Where exploratory artifacts are present, the work leaves assumptions, failure modes, or measurement context available for review rather than relying on broad unsupported claims. This supports a research-adjacent engineering profile: exploratory, but biased toward traceability and falsifiable evidence.
Supporting signals: sig-002-architecture-explicit-boundaries, sig-003-implementation-inspectable-runtime, sig-004-testing-validation-gates, sig-005-evaluation-measurement-artifacts, sig-006-maintainability-project-structure, sig-007-research-experimentation-trace
Confidence: medium
Caveats: Static repositories do not show live decision-making, WorkOverCV does not execute notebook artifacts, and public evidence cannot fully show collaboration or operational pressure.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-002-architecture-explicit-boundaries-01 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-03 | mitchellquinn-skilldoctor | schemas/run_manifest.schema.json | configuration_file | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-04 | mitchellquinn-claimlint | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-05 | mitchellquinn-bounded-monocular-perception | documents/specifications/Live Inference Pipeline - Architecture Sketch v0.3.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |

## Work Rhythm and Development Cadence

Commit-history evidence and artifact-chronology evidence are interpreted separately. Bounded chronology contains 5 readable public commit record(s) across 5 repository record(s). Dated or staged artifact paths such as 06_live-inference_v0.1/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md, 06_live-inference_v0.2/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md, and 06_live-inference_v0.2/models/distance-orientation/260515-1301_ts-2d-cnn/model_card.md provide artifact-chronology evidence independent of commit count. The visible staged-output modes are staged iteration, release or run curation, failure-analysis progression, and benchmark progression.

Commit-history evidence:
Bounded chronology contains 5 readable public commit record(s) across 5 repository record(s). The public history may represent a curated snapshot rather than the whole work process, so commit cadence should be treated as low-confidence evidence.
Confidence: low
Caveats: Do not equate shallow public history, commit count, or velocity with competence or productivity.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-009-commit-history-signal | mitchellquinn-bounded-monocular-perception | work_chronology.json | work_chronology | Anchors bounded commit-history interpretation without exposing raw commit subjects or hashes. |

Artifact-chronology evidence:
Dated or staged artifact paths such as 06_live-inference_v0.1/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md, 06_live-inference_v0.2/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md, and 06_live-inference_v0.2/models/distance-orientation/260515-1301_ts-2d-cnn/model_card.md provide artifact-chronology evidence independent of commit count. The visible staged-output modes are staged iteration, release or run curation, failure-analysis progression, and benchmark progression.
Confidence: medium
Caveats: Artifact chronology is inferred from inventory paths and artifact types; it does not show the full private work process.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-010-artifact-chronology-signal-01 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.1/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-011-artifact-chronology-signal-02 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.2/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-012-artifact-chronology-signal-03 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.2/models/distance-orientation/260515-1301_ts-2d-cnn/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-013-artifact-chronology-signal-04 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.3/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-014-artifact-chronology-signal-05 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.3/models/distance-orientation/260515-1301_ts-2d-cnn/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |

Public history limitations: Public repositories may be curated snapshots of a larger work process. Commit counts, commit velocity, and shallow history are not treated as competence or productivity measures.
Confidence: medium
Caveats: Raw commit hashes, commit subjects, and raw timelines remain analysis input only. Dated artifact paths can suggest staged refinement but cannot prove the full work rhythm.

## Environment Fit

May fit well:
- Applied ML, evaluation-heavy, or measurement-oriented teams.
- Research-adjacent engineering or ambiguous technical problem spaces.
- Tool-building contexts that value documentation, boundaries, and inspectability.
- Engineering contexts where runnable artifacts and concrete implementation are important.

May require care:
- Roles where private/company work, live collaboration, or production operation history is essential should probe beyond public repositories.
- Recorded evidence gaps should be handled as interview prompts, not adverse conclusions.

## Role-Family Fit

### 1. Software Engineer

Why discuss: Software-engineering fit is worth discussing when runnable code, explicit interfaces, validation checks, and project structure appear together in the public artifacts. Supporting evidence covers runnable implementation artifacts, system-boundary artifacts, tests or validation gates, maintainability-oriented project structure, and reviewer-facing documentation.
Behaviour fit: The observable match is implementation that is packaged with setup context, bounded interfaces, and checks another engineer can inspect or extend. Evidence basis: runnable implementation artifacts, system-boundary artifacts, tests or validation gates, maintainability-oriented project structure, and reviewer-facing documentation.
Likely contribution: The person would likely contribute inspectable implementation work with clear setup context, bounded interfaces, and reviewable maintenance paths, subject to the recorded evidence gaps.
Confidence: medium
Caveats: Interpret role-family fit with the recorded evidence gaps in view: gap-001-collaboration_visibility_gap, gap-002-private_and_company_work_visibility_gap, gap-003-development_cadence_visibility_gap.
Interview probes:
- Ask for a code walkthrough that covers interfaces, error handling, validation, and maintenance tradeoffs.
- Ask for a walkthrough of one artifact that demonstrates implementation execution.
- Ask for a walkthrough of one artifact that demonstrates system design.
- Ask for an example of reviewed team work, handoff notes, or pull request discussion.
- Ask which private or workplace projects best represent the same working behaviours.

### 2. Applied ML Engineer

Why discuss: Applied-ML fit is worth discussing when model, data, run, or evaluation artifacts make representation choices and measurement context visible. Supporting evidence covers measurement and evaluation records, experiment or failure-analysis traces, runnable implementation artifacts, and reviewer-facing documentation.
Behaviour fit: The observable match is ML-adjacent work that connects implementation to metrics, manifests, model cards, and stated limitations. Evidence basis: measurement and evaluation records, experiment or failure-analysis traces, runnable implementation artifacts, and reviewer-facing documentation.
Likely contribution: The person would likely turn model or data work into reproducible engineering artifacts with measurable claims and reviewer-visible assumptions, subject to the recorded evidence gaps.
Confidence: medium
Caveats: Interpret role-family fit with the recorded evidence gaps in view: gap-001-collaboration_visibility_gap, gap-002-private_and_company_work_visibility_gap, gap-003-development_cadence_visibility_gap.
Interview probes:
- Ask how one metric, dataset, or model-card claim was chosen, validated, and revised.
- Ask for a walkthrough of one artifact that demonstrates measurement and evaluation.
- Ask for a walkthrough of one artifact that demonstrates experimentation and learning.
- Ask for an example of reviewed team work, handoff notes, or pull request discussion.
- Ask which private or workplace projects best represent the same working behaviours.

### 3. Research Engineer

Why discuss: Research-engineering fit is worth discussing when exploratory artifacts preserve assumptions, rejected paths, experiment traces, or bounded technical claims. Supporting evidence covers experiment or failure-analysis traces, measurement and evaluation records, system-boundary artifacts, and reviewer-facing documentation.
Behaviour fit: The observable match is exploratory engineering that turns ambiguity into documented hypotheses, runnable prototypes, and evidence that can be challenged. Evidence basis: experiment or failure-analysis traces, measurement and evaluation records, system-boundary artifacts, and reviewer-facing documentation.
Likely contribution: The person would likely move exploratory technical ideas toward runnable, traceable prototypes without losing evidence boundaries, subject to the recorded evidence gaps.
Confidence: medium
Caveats: Interpret role-family fit with the recorded evidence gaps in view: gap-001-collaboration_visibility_gap, gap-002-private_and_company_work_visibility_gap, gap-003-development_cadence_visibility_gap.
Interview probes:
- Ask for an experiment walkthrough that covers the uncertainty, rejected paths, and evidence that changed direction.
- Ask for a walkthrough of one artifact that demonstrates experimentation and learning.
- Ask for a walkthrough of one artifact that demonstrates measurement and evaluation.
- Ask for an example of reviewed team work, handoff notes, or pull request discussion.
- Ask which private or workplace projects best represent the same working behaviours.

### 4. AI Evaluation Engineer

Why discuss: AI-evaluation fit is worth discussing when claims are paired with metrics, checks, reproducibility context, or explicit evidence limits. Supporting evidence covers measurement and evaluation records, tests or validation gates, reviewer-facing documentation, and experiment or failure-analysis traces.
Behaviour fit: The observable match is a claims-auditing style: evidence records, validation gates, and metric context are available for review instead of being left as assertion. Evidence basis: measurement and evaluation records, tests or validation gates, reviewer-facing documentation, and experiment or failure-analysis traces.
Likely contribution: The person would likely make evaluation work auditable by connecting claims to metrics, manifests, checks, and explicit limitations, subject to the recorded evidence gaps.
Confidence: medium
Caveats: Interpret role-family fit with the recorded evidence gaps in view: gap-001-collaboration_visibility_gap, gap-002-private_and_company_work_visibility_gap, gap-003-development_cadence_visibility_gap.
Interview probes:
- Ask for a claims-audit walkthrough that traces an evaluation result back to source evidence and limitations.
- Ask for a walkthrough of one artifact that demonstrates measurement and evaluation.
- Ask for a walkthrough of one artifact that demonstrates validation and reliability.
- Ask for an example of reviewed team work, handoff notes, or pull request discussion.
- Ask which private or workplace projects best represent the same working behaviours.

### 5. Developer Tools Engineer

Why discuss: Developer-tools fit is worth discussing when workflows are packaged with command surfaces, adapter contracts, setup documentation, or reviewer context. Supporting evidence covers packaging and usage context, reviewer-facing documentation, runnable implementation artifacts, tests or validation gates, and maintainability-oriented project structure.
Behaviour fit: The observable match is tool-shaped work that exposes installation, invocation, extension points, and failure surfaces for other engineers. Evidence basis: packaging and usage context, reviewer-facing documentation, runnable implementation artifacts, tests or validation gates, and maintainability-oriented project structure.
Likely contribution: The person would likely package technical workflows so other engineers can install, inspect, run, and extend them with less hidden context, subject to the recorded evidence gaps.
Confidence: medium
Caveats: Interpret role-family fit with the recorded evidence gaps in view: gap-001-collaboration_visibility_gap, gap-002-private_and_company_work_visibility_gap, gap-003-development_cadence_visibility_gap.
Interview probes:
- Ask for a tool-user walkthrough that covers setup friction, extension points, and failure modes.
- Ask for a walkthrough of one artifact that demonstrates product packaging.
- Ask for a walkthrough of one artifact that demonstrates documentation and handoff.
- Ask for an example of reviewed team work, handoff notes, or pull request discussion.
- Ask which private or workplace projects best represent the same working behaviours.

## Evidence Gaps and Follow-Up Questions

### 1. Collaboration Visibility Gap

Observed: Public repository evidence can show documentation and packaging, but it does not directly show team review, pull-request discussion, or workplace collaboration.
Why uncertain: The repository corpus is a public evidence sample and does not expose every work context.
Follow-up: Ask for an example of reviewed team work, handoff notes, or pull request discussion.
Confidence: medium
Scope: collected public repository evidence

### 2. Private And Company Work Visibility Gap

Observed: The reviewed corpus is public repository evidence and may omit private, company, or collaborative work that would materially change interpretation.
Why uncertain: The repository corpus is a public evidence sample and does not expose every work context.
Follow-up: Ask which private or workplace projects best represent the same working behaviours.
Confidence: medium
Scope: collected public repository evidence

### 3. Development Cadence Visibility Gap

Observed: Readable git chronology was unavailable or shallow, so public commit cadence cannot support a confident work-rhythm interpretation.
Why uncertain: The repository corpus is a public evidence sample and does not expose every work context.
Follow-up: Ask the person to walk through a representative project timeline and explain major iteration points.
Confidence: low
Scope: collected public repository evidence

## Confidence and Uncertainty Notes

- Authorship Bounds: Authorship interpretation is bounded to collected public repository evidence and should be verified through discussion when it materially affects interpretation.
- Confidence Summary: Signal confidence distribution: high=6, medium=2, low=0; evidence gaps recorded: 3.
- Cross Repository Consistency: Signals are drawn from 5 repository record(s); cross-repository confidence depends on how many repositories contain matching artifact types.
- Evidence Density: 894 artifact(s) and 8 behaviour signal(s) were selected for analysis.
- Private Work Limitations: Private and company work may be absent from the corpus and should be treated as unknown.
- Public Repository Limitations: GitHub evidence is a sample of public work, not a complete employment history.

## Evidence Appendix

Evidence IDs are included here for audit traceability; human-facing sections use repository/path references.

| Evidence ID | Repository | Path | Artifact type | Why it matters |
| ----------- | ---------- | ---- | ------------- | -------------- |
| ev-001-documentation-reviewer-context-01 | mitchellquinn-skilldoctor | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-03 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-04 | mitchellquinn-workovercv | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-001-documentation-reviewer-context-05 | mitchellquinn-claimlint | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |
| ev-002-architecture-explicit-boundaries-01 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-03 | mitchellquinn-skilldoctor | schemas/run_manifest.schema.json | configuration_file | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-04 | mitchellquinn-claimlint | docs/architecture.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-002-architecture-explicit-boundaries-05 | mitchellquinn-bounded-monocular-perception | documents/specifications/Live Inference Pipeline - Architecture Sketch v0.3.md | architecture_document | Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions. |
| ev-003-implementation-inspectable-runtime-01 | mitchellquinn-bounded-monocular-perception | scripts/analyze_brightness_run.py | source_code | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-02 | mitchellquinn-skilldoctor | src/skill_doctor/infer_contract.py | inference_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-03 | mitchellquinn-industrial-sound-anomaly-detection | preprocessing/export_2d_training.py | training_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-04 | mitchellquinn-bounded-monocular-perception | 03_rb-training-v2.0/src/evaluate.py | evaluation_script | Selected because it provides runnable or inspectable implementation evidence. |
| ev-003-implementation-inspectable-runtime-05 | mitchellquinn-claimlint | src/claimlint/classify_claims.py | source_code | Selected because it provides runnable or inspectable implementation evidence. |
| ev-004-testing-validation-gates-01 | mitchellquinn-workovercv | tests/test_analyze.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-02 | mitchellquinn-claimlint | tests/test_claim_extraction.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-03 | mitchellquinn-skilldoctor | tests/test_cli_audit.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-04 | mitchellquinn-claimlint | tests/test_cli_audit.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-004-testing-validation-gates-05 | mitchellquinn-workovercv | tests/test_collect.py | test_file | Selected because it shows repeatable checks around runtime behavior or technical claims. |
| ev-005-evaluation-measurement-artifacts-01 | mitchellquinn-bounded-monocular-perception | 03_rb-training-v2.0/src/evaluate.py | evaluation_script | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-02 | mitchellquinn-industrial-sound-anomaly-detection | models/20260319-1829-2d_sound_v0.2/model_card.md | model_card | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-03 | mitchellquinn-workovercv | claimlint/workovercv-20260618-1447Z/run_manifest.json | run_manifest | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-04 | mitchellquinn-industrial-sound-anomaly-detection | models/20260320-1607-2d_sound_v0.4/metrics.json | data_manifest | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-005-evaluation-measurement-artifacts-05 | mitchellquinn-bounded-monocular-perception | 04_ROI-FCN/02_training/src/roi_fcn_training_v0_1/evaluate.py | evaluation_script | Selected because it exposes measurement, benchmark, model, data, or run context. |
| ev-006-maintainability-project-structure-01 | mitchellquinn-skilldoctor | pyproject.toml | configuration_file | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-02 | mitchellquinn-bounded-monocular-perception | 02_synthetic-data-processing-v4.0/rb_pipeline_v4/config.py | source_code | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-03 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-04 | mitchellquinn-skilldoctor | docs/architecture.md | architecture_document | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-006-maintainability-project-structure-05 | mitchellquinn-workovercv | pyproject.toml | configuration_file | Selected because it helps reviewers inspect project structure, setup, or modification boundaries. |
| ev-008-product-reviewer-positioning-01 | mitchellquinn-skilldoctor | README.md | README | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-02 | mitchellquinn-workovercv | docs/adapter_contract.md | technical_writeup | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-03 | mitchellquinn-workovercv | adapters/status.yml | configuration_file | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-04 | mitchellquinn-claimlint | README.md | README | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-008-product-reviewer-positioning-05 | mitchellquinn-bounded-monocular-perception | README.md | README | Selected because it packages the work for technical readers, users, or adapter reviewers. |
| ev-007-research-experimentation-trace-01 | mitchellquinn-bounded-monocular-perception | failure-analysis/failure-analysis-index.md | failure_analysis | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |
| ev-007-research-experimentation-trace-02 | mitchellquinn-industrial-sound-anomaly-detection | models/20260319-1829-2d_sound_v0.2/model_card.md | model_card | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |
| ev-007-research-experimentation-trace-03 | mitchellquinn-industrial-sound-anomaly-detection | preprocessing/export_2d_training.py | training_script | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |
| ev-007-research-experimentation-trace-04 | mitchellquinn-bounded-monocular-perception | 03_rb-training-v2.0/notebooks/01_dataset_audit_v0.1.ipynb | notebook_source | Selected because it preserves experiment, notebook, model-card, or failure-analysis context. |
| ev-010-artifact-chronology-signal-01 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.1/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-011-artifact-chronology-signal-02 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.2/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-012-artifact-chronology-signal-03 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.2/models/distance-orientation/260515-1301_ts-2d-cnn/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-013-artifact-chronology-signal-04 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.3/models/distance-orientation/260504-1100_ts-2d-cnn__run_0001/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-014-artifact-chronology-signal-05 | mitchellquinn-bounded-monocular-perception | 06_live-inference_v0.3/models/distance-orientation/260515-1301_ts-2d-cnn/model_card.md | model_card | Shows dated or staged artifact chronology that can be read separately from commit count. |
| ev-009-commit-history-signal | mitchellquinn-bounded-monocular-perception | work_chronology.json | work_chronology | Anchors bounded commit-history interpretation without exposing raw commit subjects or hashes. |
