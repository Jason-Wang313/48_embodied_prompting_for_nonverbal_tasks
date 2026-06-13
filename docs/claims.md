# Claims

Supported claim:

- Nonverbal prompts should be represented as physical task variables, not as captions appended to text.
- Cue-text conflict should trigger clarification unless the physical affordance strongly resolves the action.
- In the clean synthetic diagnostic, the embodied prompt graph reaches 0.978 task accuracy and 0.000 unsafe prompt execution.

V2 narrowed claim:

The safety claim depends on reliable safety-cue binding. With a 5% binding-miss rate on safety-critical cases and fallback to text-only intent, unsafe execution rises to 0.044, worse than the captioned-cue unsafe rate of 0.033. With a 20% miss rate, unsafe execution rises to 0.189.

Unsupported claim:

The paper does not demonstrate deployed nonverbal perception, cross-cultural gesture robustness, hardware safety, or reliable object/region binding.
