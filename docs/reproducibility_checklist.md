# Reproducibility Checklist

- Full-scale generator: `scripts/run_full_scale_embodied_prompt_suite.py`.
- Build script: `scripts/build_pdf.ps1`.
- Canonical PDF path: `C:/Users/wangz/Downloads/48.pdf`.
- Local generated PDF policy: `paper/main.pdf` is removed after build.
- Compact rows: `results/full_scale/condition_metrics.csv`.
- Summaries: `results/full_scale/*_summary.csv`.
- Validation: `results/full_scale/experiment_validation.json`.
- Figures: `paper/figures/full_scale/*.pdf`.
- Tables: `results/full_scale/table_*.tex`.
- Final PDF SHA256: `670020D899F49F19565ADE133A2C4EB9C75810ADFB46E49A9B571668A759C40B`.
- Determinism: stable hash-based condition jitter, fixed factor maps, no global random state.
- Visual QA: render pages 2, 3, 4, 5, and 6 at 160 dpi and confirm VLA-style green citation boxes and red internal-reference boxes are thin, aligned, readable, and collision-free.
