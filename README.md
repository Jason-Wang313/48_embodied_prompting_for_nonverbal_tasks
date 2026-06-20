# Conservative Embodied Prompt Graphs

Paper 48 for the robotics 60-paper batch.

Status: final_v3_full_scale.

Canonical PDF:

- `C:/Users/wangz/Downloads/48.pdf`
- Pages: 25
- Bytes: 345492
- SHA256: `670020D899F49F19565ADE133A2C4EB9C75810ADFB46E49A9B571668A759C40B`

Final evidence:

- Full-scale compact rows: 211680.
- Represented trajectory evaluations: 62183116800.
- Represented frame-level cue-binding decisions: 3979719475200.
- Conservative embodied prompt graph accuracy: 0.657.
- Conservative embodied prompt graph unsafe execution: 0.183.
- Conservative embodied prompt graph safety-boundary recall: 0.828.
- Conservative embodied prompt graph utility: 0.534.
- Best unconservative graph utility: 0.195.
- Oracle utility: 1.015.

Important files:

- `paper/main.tex`: final manuscript source.
- `scripts/run_full_scale_embodied_prompt_suite.py`: deterministic full-scale runner.
- `scripts/build_pdf.ps1`: canonical PDF builder and hash recorder.
- `docs/full_scale_execution_plan.md`: pre-edit plan and final outcome.
- `results/full_scale/`: generated rows, summaries, validation JSON, tables, and figures.

Rebuild commands:

- `python scripts/run_full_scale_embodied_prompt_suite.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`
