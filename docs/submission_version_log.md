# Submission Version Log

## v1

- Recovered manuscript, synthetic diagnostic cases, figure, and PDF.
- Claimed embodied prompt graph reaches 0.978 accuracy and 0.000 unsafe prompt execution.

## v2

- Added safety-cue binding-miss stress via `scripts/v2_binding_miss_stress.py`.
- Found 5% binding misses raise graph unsafe prompt rate to 0.044, worse than captioned cues at 0.033.
- Found 20% binding misses raise graph unsafe prompt rate to 0.189.
- Updated paper and docs to mark the repo workshop-only.
- Enforced canonical PDF location at `C:/Users/wangz/Downloads/48.pdf`.
