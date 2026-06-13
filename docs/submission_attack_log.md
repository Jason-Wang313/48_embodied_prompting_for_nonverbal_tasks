# Submission Attack Log

## Attack 1: Captioned cues may be enough.

Result: Partially rejected in the clean diagnostic. Captioned cues reach 0.819 accuracy and 0.033 unsafe rate; clean graph reaches 0.978 accuracy and 0.000 unsafe rate.

Decision impact: The graph representation has a useful mechanism in synthetic cases.

## Attack 2: Safety cue binding misses can destroy the zero-unsafe claim.

Result: Sustained. At 5% safety-cue binding misses, graph unsafe rate rises to 0.044, worse than captioned cues at 0.033.

Decision impact: The paper must claim conservative safety-cue binding, not robust safe prompting.

## Attack 3: Nonverbal cues are culturally or physically ambiguous.

Result: Sustained. The paper has no real human-subject or hardware evidence.

Decision impact: workshop-only.
