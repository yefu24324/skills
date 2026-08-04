# Product Stage Workflow

Workflow version: `1.0`

This workflow is shared by `product-spec`, `product-spec-author`, and `product-spec-review`. It adapts useful multi-agent pipeline patterns from `yimwoo/codex-agenteam`: role separation, scoped write authority, structured handoffs, explicit gates, reviewer verdicts, and rework loops. It remains focused on product specifications rather than the complete software-delivery pipeline.

## Goal

Produce a decision-complete, modular PRD that has been independently reviewed and can be handed to design or engineering without forcing the next agent to invent product decisions.

## Roles

### Orchestrator: `product-spec`

- Owns stage state, routing, revision numbers, and gates.
- Explores repository evidence before asking humans.
- Does not silently author and approve the same revision.

### Author: `product-spec-author`

- Has write authority for current product specifications.
- Resolves review findings by producing a new revision.
- Cannot mark its own revision approved.

### Reviewer: `product-spec-review`

- Is read-only for the revision under review.
- Uses a separate agent context from the Author.
- Produces findings and a verdict, never a rewritten PRD.

### Human product owner

- Resolves blocking product ambiguities.
- May explicitly defer a decision with named scope and consequence.
- Is the authority for business intent, permissions, commitments, and trade-offs not derivable from repository evidence.

## Stage state machine

```text
DISCOVERY
  -> CLARIFICATION_REQUIRED -> WAITING_FOR_HUMAN -> DISCOVERY
  -> AUTHORING
  -> IN_REVIEW
       -> APPROVED
       -> CHANGES_REQUESTED -> AUTHORING
       -> HUMAN_DECISION_REQUIRED -> WAITING_FOR_HUMAN -> AUTHORING
```

A revision may enter `IN_REVIEW` only when all blocking clarifications affecting that revision are resolved.

## Stage 1: Discovery

Before asking questions:

1. Read current product docs, decisions, relevant code, tests, terminology, and prior research.
2. Build the current product-model snapshot and identify evidence sources.
3. Separate known facts, inferred assumptions, contradictions, and unresolved decisions.
4. Determine whether the request is a `PATCH` or structural `REWRITE`.

Do not ask humans questions that the repository can answer with reasonable inspection.

## Stage 2: Human clarification gate

Create a `Clarification` record for each unresolved decision.

A question is blocking when its answer could change:

- product goal, scope, or non-goals;
- user roles or permissions;
- capability boundaries;
- object ownership or lifecycle;
- primary flow, branch, or failure outcome;
- page responsibility, navigation, or visibility;
- business rules, external commitments, or acceptance outcomes.

For blocking clarifications:

1. Stop authoring the affected requirements.
2. Ask the human before continuing.
3. Ask one decision per question.
4. Prefer a compact batch of at most five high-impact questions.
5. Include concrete options and trade-offs when known.
6. State a recommendation only when evidence supports one.
7. Record the human answer as a resolved clarification and, when durable, a `Decision`.

Low-impact uncertainties may proceed only as explicitly labeled assumptions. Examples include provisional labels, copy, or non-binding visual preferences. Never use an assumption to decide permissions, money, deletion behavior, compliance, lifecycle, or external promises.

## Stage 3: Authoring

The Author creates revision `rN` using the shared product model.

Required author handoff:

- model and workflow versions;
- revision ID;
- changed entity IDs and relationships;
- source evidence used;
- resolved clarifications and explicit assumptions;
- files created, rewritten, or removed;
- traceability changes;
- invariant check results;
- known risks and non-blocking open items.

A structural change rewrites complete affected entities. Do not append a new model after superseded text.

## Stage 4: Independent review

Dispatch `product-spec-review` in a separate context. When the host supports separate models, prefer a different model from the Author to reduce correlated blind spots.

The Reviewer checks:

- problem, goal, scope, and non-goals;
- role, permission, object, flow, page, rule, state, and acceptance completeness;
- contradictions and broken traceability;
- unresolved or hidden product decisions;
- patch accumulation and stale text;
- document modularity;
- whether the PRD is decision-complete for downstream work.

Finding severity:

- `BLOCK`: must be resolved before approval.
- `WARN`: material concern that may proceed only if explicitly accepted.
- `NOTE`: non-blocking improvement.

Verdicts:

- `APPROVED`: no blocking finding and no blocking clarification.
- `CHANGES_REQUESTED`: Author can resolve findings without a new human product decision.
- `HUMAN_DECISION_REQUIRED`: a product decision cannot be safely inferred and must return to the human gate.

## Stage 5: Rework loop

For `CHANGES_REQUESTED`:

1. Preserve the review record.
2. Route every `BLOCK` and accepted `WARN` to the Author as required actions.
3. Produce a new revision; do not edit the old review record.
4. Submit the new revision to a new independent review record.

Default maximum: three review cycles. If the same blocking issue survives three cycles, escalate to the human with the revision history and the exact unresolved conflict instead of continuing an unbounded agent loop.

For `HUMAN_DECISION_REQUIRED`, pause immediately. The Author may continue only after the human resolves or explicitly defers the referenced clarification.

## Completion gate

The product stage is complete only when:

- the latest review verdict is `APPROVED`;
- no blocking clarification remains open;
- the current PRD revision contains no superseded requirements;
- model invariants and traceability pass;
- review and clarification records are preserved as handoff evidence.

For major changes, present the approved revision and review summary to the human product owner before downstream design or implementation begins.

## Durable artifacts

```text
docs/product/
├── clarifications.md
├── reviews/<scope>-r1.md
├── reviews/<scope>-r2.md
├── decisions/<decision>.md
└── ...current product specifications...
```

Keep handoff evidence in repository files rather than relying only on chat history.
