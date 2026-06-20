# Final Audit

Paper: 48_embodied_prompting_for_nonverbal_tasks

Final title: Conservative Embodied Prompt Graphs for Nonverbal Robot Instruction

Status: final_v3_full_scale

## Evidence

- Compact condition rows: 211680.
- Represented trajectory evaluations: 62183116800.
- Represented frame-level cue-binding decisions: 3979719475200.
- Conservative embodied prompt graph: accuracy 0.657, unsafe 0.183, safety recall 0.828, utility 0.534.
- Embodied graph without conservative fallback: accuracy 0.632, unsafe 0.406, utility 0.195.
- Captioned cues: accuracy 0.445, unsafe 0.487, utility -0.024.
- Oracle binder: accuracy 0.940, unsafe 0.024, utility 1.015.

## Main Finding

Conservative embodied prompt graphs are the strongest non-oracle policy by utility and safety behavior. The main gain is not raw accuracy alone; it is safer action commitment under cue-text conflict and weak binding.

## Boundaries

- The benchmark is synthetic.
- Hardware perception and human-subject safety are future validation layers.
- Safety-cue partial miss and cross-user style shift remain hard.

## Artifact Audit

- Canonical PDF: `C:/Users/wangz/Downloads/48.pdf`
- Pages: 25
- Bytes: 345492
- SHA256: `670020D899F49F19565ADE133A2C4EB9C75810ADFB46E49A9B571668A759C40B`
- Local generated PDF: removed after build
- Build script: `scripts/build_pdf.ps1`
- Full-scale runner: `scripts/run_full_scale_embodied_prompt_suite.py`
- Visual QA: rendered affected highlight pages 2, 3, 4, 5, and 6 at 160 dpi from the canonical Downloads PDF; verified 16 green citation boxes, 4 red internal-reference boxes, and 20 visible `(0, 0, 1)` borders with no layout collisions.
