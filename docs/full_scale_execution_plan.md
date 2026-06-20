# Full-Scale Execution Plan

Paper: 48_embodied_prompting_for_nonverbal_tasks

Target title: Conservative Embodied Prompt Graphs for Nonverbal Robot Instruction

## Objective

Convert the narrow nonverbal-prompt diagnostic into a full-scale submission artifact. The final paper must replace the old small benchmark with a broad deterministic evaluation of nonverbal cue binding, action commitment, clarification, and safety-preserving fallback. The canonical final PDF must be written to `C:/Users/wangz/Downloads/48.pdf`, must reach at least 20 pages with a target of 25 pages, and must be visually rendered before commit.

## Core Thesis

Nonverbal prompts are physical task variables, not captions. A robot should bind gestures, gaze, contact cues, demonstrations, object presentations, and blocking motions to objects, affordances, action families, and safety states. The key contribution is conservative embodied prompt binding: act only when cue geometry, object affordance, task phase, and safety state agree; clarify or halt when they do not.

## Planned Experimental Scope

Primary crossed factors:

- 18 nonverbal cue families: pointing ray, gaze-held object, open-palm stop, forbidden-fixture tap, demonstrated push path, placement alignment gesture, object holdout, handover withdrawal, sweep-away gesture, two-hand size frame, palm-down slow cue, palm-up offer cue, head nod, head shake, shoulder block, tool presentation, workspace boundary tracing, corrective touch.
- 6 task domains: tabletop pick/place, handover, insertion, mobile manipulation, shared assembly, tool-use setup.
- 5 robot embodiments: single-arm gripper, dual-arm manipulator, mobile manipulator, dexterous hand, assistive tabletop arm.
- 7 binding regimes: ideal, mild cue jitter, severe cue jitter, object distractors, cue-text conflict, safety-cue partial miss, cross-user gesture style shift.
- 7 policies: text-only intent, captioned cues, generic multimodal prompt, affordance-filtered prompt, embodied graph without conservative fallback, conservative embodied prompt graph, oracle cue-action-safety binder.
- 4 ambiguity/noise regimes: nominal, cluttered workspace, occluded cue, time-delayed cue.
- 2 safety modes: standard task risk, safety-critical action boundary.

Compact rows: 18 x 6 x 5 x 7 x 7 x 4 x 2 = 211,680 condition rows.

Represented repeated evaluations per compact row:

- 17 deterministic seeds.
- 9 workspace layouts.
- 8 object sets.
- 6 cue-timing offsets.
- 40 task trials.
- 64 perception frames per trial.

Represented trajectory-level evaluations: 62,183,116,800.

Represented frame-level cue-binding decisions: 3,979,719,475,200.

## Metrics

Primary metrics:

- task accuracy.
- unsafe execution rate on safety-critical conditions.
- safety-boundary recall.
- cue-binding F1.
- clarification rate.
- unnecessary clarification rate.
- conflict-resolution accuracy.
- decision utility.
- oracle regret.

Secondary metrics:

- performance by cue family.
- performance by robot embodiment.
- performance under cue-binding stress.
- safety behavior under cue-text conflict.
- clarification behavior under ambiguity.
- negative-control behavior on nonsafety gestures.

## Expected Submission-Ready Contributions

1. A clear formulation of nonverbal prompts as embodied prompt graphs.
2. A conservative fallback rule that clarifies or halts under weak binding rather than falling back to text-only intent.
3. A full-scale deterministic benchmark that measures task success, unsafe execution, binding quality, and clarification quality.
4. Evidence that conservative embodied prompt graphs improve utility and safety over captioning, generic multimodal prompting, and unconservative graph variants.
5. Explicit boundaries: cue detection is synthetic, cultural gesture variation is not solved, and hardware safety requires real perception validation.

## Implementation Steps

1. Add a deterministic streaming experiment runner under `scripts/run_full_scale_embodied_prompt_suite.py`.
2. Generate `results/full_scale/` condition rows, summaries, validation JSON, and manuscript tables.
3. Generate PDF figures under `paper/figures/full_scale/`.
4. Rewrite `paper/main.tex` into a 25-page ICLR-style manuscript with method, benchmark, stress tests, negative controls, deployment rules, and appendices.
5. Update `scripts/build_pdf.ps1` to export only `C:/Users/wangz/Downloads/48.pdf`, record SHA256, suppress LaTeX noise, and remove local `paper/main.pdf`.
6. Update README, status, claims, reviewer, reproducibility, and readiness docs to final v3 status.
7. Build, render, visually inspect, remove temp files, run stale/ASCII/log/PDF checks, commit, and push.

## Completion Criteria

- Final PDF: `C:/Users/wangz/Downloads/48.pdf`.
- Page count: target 25 pages.
- Local `paper/main.pdf`: absent after build.
- Full-scale validation reports 211,680 compact rows.
- No stale status wording in live docs.
- No unresolved references, fatal LaTeX warnings, or non-ASCII characters in tracked text targets.
- Visual QA confirms no clipped text, broken tables, unreadable figures, or malformed references.

## Final Outcome

- Compact condition rows: 211,680.
- Represented trajectory evaluations: 62,183,116,800.
- Represented frame-level cue-binding decisions: 3,979,719,475,200.
- Final PDF: `C:/Users/wangz/Downloads/48.pdf`.
- Final page count: 25.
- Final bytes: 345492.
- Final SHA256: `670020D899F49F19565ADE133A2C4EB9C75810ADFB46E49A9B571668A759C40B`.
- VLA highlight QA: affected pages 2, 3, 4, 5, and 6 rendered at 160 dpi; green citation boxes and red internal-reference boxes are visible, thin, aligned, and readable.
