# Final Audit

Paper: 48_embodied_prompting_for_nonverbal_tasks

Decision: workshop-only

Submission-hardening version: v2

## Original evidence

- Text only: accuracy 0.165, clarification 0.470, unsafe prompt rate 0.678.
- Captioned cues: accuracy 0.819, clarification 0.044, unsafe prompt rate 0.033.
- Embodied prompt graph: accuracy 0.978, clarification 0.007, unsafe prompt rate 0.000.

## V2 safety-cue binding stress

- 2% binding miss: unsafe prompt rate 0.022, 4/180 unsafe safety cases.
- 5% binding miss: unsafe prompt rate 0.044, 8/180 unsafe safety cases.
- 10% binding miss: unsafe prompt rate 0.089, 16/180 unsafe safety cases.
- 20% binding miss: unsafe prompt rate 0.189, 34/180 unsafe safety cases.
- Captioned-cue unsafe prompt rate in the original benchmark: 0.033.

## Main blocker

The paper remains synthetic and assumes reliable cue detection, object binding, and safety-edge extraction. The v2 stress shows the zero-unsafe result does not survive even modest safety-cue binding misses.

## Submission decision

Workshop-only. The paper is coherent as a mechanism and diagnostic benchmark, but it is not ready for a main robotics conference without real perception, hardware validation, and conservative handling of missed safety bindings.

## Artifact audit

- Canonical PDF: `C:/Users/wangz/Downloads/48.pdf`
- Local generated PDF: removed after build
- Desktop copy: absent
- Build script: `scripts/build_pdf.ps1`
- V2 stress script: `scripts/v2_binding_miss_stress.py`
