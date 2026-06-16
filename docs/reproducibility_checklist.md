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
- Final PDF SHA256: `235B70CC4E379473059444C6266BEC98AF6282DB4210F3155D67E68547CF6DA0`.
- Determinism: stable hash-based condition jitter, fixed factor maps, no global random state.
