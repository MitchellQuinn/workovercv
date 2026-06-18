from __future__ import annotations

WORKFLOW_ID = "workovercv.repository-employment-signal"
WORKFLOW_VERSION = "0.6.0"
TOOL_NAME = "workovercv"
SUMMARY_REPORT_ARTIFACT = "summary-report.md"
SCREENING_BRIEF_ARTIFACT = "screening_brief.md"

REQUIRED_FINAL_ARTIFACTS = [
    "report.md",
    SUMMARY_REPORT_ARTIFACT,
    SCREENING_BRIEF_ARTIFACT,
    "report.json",
    "repo_inventory.json",
    "review_scope.yml",
    "artifact_inventory.json",
    "review_corpus.jsonl",
    "work_chronology.json",
    "explicit_claims.jsonl",
    "signal_ledger.jsonl",
    "evidence_map.jsonl",
    "gap_register.jsonl",
    "role_family_fit.json",
    "mitigations.jsonl",
    "red_team_review.json",
    "run_manifest.json",
]

DISCOVERY_ARTIFACTS = [
    "repo_inventory.json",
    "review_scope.yml",
    "run_manifest.json",
]

COLLECTION_ARTIFACTS = [
    "artifact_inventory.json",
    "review_corpus.jsonl",
    "work_chronology.json",
    "run_manifest.json",
]

ANALYSIS_ARTIFACTS = [
    "explicit_claims.jsonl",
    "signal_ledger.jsonl",
    "evidence_map.jsonl",
    "gap_register.jsonl",
    "role_family_fit.json",
    "mitigations.jsonl",
    "red_team_review.json",
    "report.json",
]

EVIDENCE_BOUNDARY_ARTIFACTS = [
    "review_scope.yml",
    "repo_inventory.json",
    "artifact_inventory.json",
    "review_corpus.jsonl",
    "work_chronology.json",
]

REPORT_HEADINGS = [
    "Scope and Evidence Base",
    "How to Use This Report",
    "Executive Work Profile",
    "Observed Work Behaviour Signals",
    "Engineering Habits",
    "Problem-Solving Style",
    "Work Rhythm and Development Cadence",
    "Environment Fit",
    "Role-Family Fit",
    "Evidence Gaps and Follow-Up Questions",
    "Confidence and Uncertainty Notes",
    "Evidence Appendix",
]

SUMMARY_REPORT_HEADINGS = [
    "Scope",
    "Executive Work Profile",
    "Top Observed Work Behaviour Signals",
    "Problem-Solving Style",
    "Environment Fit",
    "Role-Family Discussion Routes",
    "Evidence Gaps to Clarify",
    "Confidence Notes",
]

OLD_REPORT_HEADINGS = [
    "## Strengths",
    "## Weaknesses",
    "## Opportunities",
    "## Mitigations of Weaknesses",
]

SIGNAL_CATEGORIES = [
    "documentation_and_handoff",
    "system_design",
    "implementation_execution",
    "validation_and_reliability",
    "measurement_and_evaluation",
    "maintainability",
    "experimentation_and_learning",
    "product_packaging",
    "development_cadence",
    "authorship_bounds",
]

SIGNAL_CATEGORY_IDS = set(SIGNAL_CATEGORIES)

STRENGTHS = {"weak", "moderate", "strong"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}

DISALLOWED_REPORT_PHRASES = [
    "red flag",
    "red flags",
    "the candidate is unreliable",
    "the candidate lacks social skills",
    "the candidate is difficult",
    "the candidate is a genius",
    "the candidate is unemployable",
]

PROTECTED_TRAIT_TERMS = [
    "age",
    "disability",
    "health status",
    "neurotype",
    "race",
    "ethnicity",
    "religion",
    "gender identity",
    "sexuality",
    "nationality",
    "family status",
    "financial status",
    "political views",
    "private life circumstances",
]
