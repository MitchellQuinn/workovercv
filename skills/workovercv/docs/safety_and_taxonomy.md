# Safety And Taxonomy

WorkOverCV may only assess professional signals visible in reviewed technical
artifacts.

Notebook evidence is source-only evidence. Code and markdown cells may support
signals about experiment design, preprocessing flow, evaluation workflow, and
exploratory engineering habits. Notebook outputs are not collected, notebooks
are never executed, and notebook source alone must not be treated as proof of
metric validity, production readiness, runtime reliability, or deployment.

## Signal Strength

- `strong`: multiple concrete artifacts support the signal, or one unusually
  direct artifact supports it.
- `moderate`: concrete evidence exists but is limited in scope.
- `weak`: evidence is indirect, narrow, or incomplete.
- `insufficient`: the workflow cannot responsibly assess the signal.

## Confidence

- `high`: evidence is direct, current, and independently checkable.
- `medium`: evidence is relevant but incomplete or partly indirect.
- `low`: inference is tentative and should prompt follow-up, not conclusion.

## Human Review Boundaries

- WorkOverCV may identify role-family discussion routes.
- WorkOverCV may identify evidence gaps and follow-up questions.
- WorkOverCV must not make final suitability judgements for or against
  production ownership, autonomy level, or hiring outcome; those discussions
  belong to human review with role context and external evidence beyond public
  repository artifacts.

## Prohibited Inferences

Do not infer or report age, disability, health status, neurotype, race,
ethnicity, religion, gender identity, sexuality, nationality, family status,
financial status, political views, or private life circumstances.

Disallowed phrasing includes:

- "Red flag."
- "Red flags."
- "The candidate is unreliable."
- "The candidate lacks social skills."
- "The candidate is difficult."
- "The candidate is a genius."
- "The candidate is unemployable."

Preferred phrasing:

- "The reviewed repositories may contain failure-analysis artifacts where such
  documents are present in the collected corpus."
- "The reviewed repositories provide limited evidence of team collaboration."
- For research-engineering discussion routes, use conditional wording only when
  the reviewed corpus contains trace-backed evidence categories such as
  experiment traces, model cards, evaluation artifacts, failure-analysis
  documents, bounded non-claims, or runnable prototypes. Link the route through
  `signal_ledger.jsonl` and `evidence_map.jsonl` to collected artifacts, or
  record the missing trace as an evidence gap. WorkOverCV should not conclude
  suitability for or against unsupervised production ownership without human
  review, role context, and additional evidence beyond public repository
  artifacts.
