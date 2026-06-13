# Embodied Prompting for Nonverbal Tasks

Paper 48 for the robotics 60-paper batch.

Decision: workshop-only.

The v2 safety-cue binding stress narrows the claim. The clean embodied prompt graph reaches 0.978 task accuracy and 0.000 unsafe prompt execution on the synthetic diagnostic. If safety-critical cues are missed and the graph falls back to text-only intent, a 5% binding-miss rate raises unsafe execution to 0.044, worse than the captioned-cue unsafe rate of 0.033. The paper is therefore a mechanism note about conservatively bound nonverbal safety cues, not deployed prompt safety.

Canonical PDF:

- `C:/Users/wangz/Downloads/48.pdf`

Important files:

- `paper/main.tex`: manuscript source.
- `docs/nonverbal_prompt_cases.csv`: original synthetic cases.
- `docs/v2_binding_miss_stress.json`: v2 binding-miss stress summary.
- `docs/v2_binding_miss_stress.csv`: v2 stress table data.
- `paper/v2_binding_miss_table.tex`: manuscript table generated from v2 stress.
- `docs/final_audit.md`: final hardening audit.

Rebuild commands:

- `python scripts/v2_binding_miss_stress.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

The build script copies the generated PDF to `C:/Users/wangz/Downloads/48.pdf` and removes `paper/main.pdf`.
