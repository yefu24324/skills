# Product Stage Workflow

Workflow version: `1.0`

This workflow is shared by `product-spec`, `product-spec-author`, and `product-spec-review`.

## Roles

- `product-spec`: orchestrates stages, gates, revisions, and handoffs.
- `product-spec-author`: writes PRD revisions; it cannot approve them.
- `product-spec-review`: reviews a fixed revision in a separate read-only agent context; it cannot rewrite it.
- Human product owner: resolves product decisions that repository evidence cannot determine.

## State machine

```text
DISCOVERY
  -> CLARIFICATION_REQUIRED -> WAITING_FOR_HUMAN -> DISCOVERY
  -> AUTHORING -> IN_REVIEW
       -> APPROVED
       -> CHANGES_REQUESTED -> AUTHORING
       -> HUMAN_DECISION_REQUIRED -> WAITING_FOR_HUMAN -> AUTHORING
```

## Discovery and clarification gate

Explore current requirements, decisions, code, tests, terminology, and research before asking questions. Do not ask humans what the repository can answer.

Create a blocking `Clarification` and pause affected authoring when guessing could change scope, roles, permissions, capability boundaries, object lifecycle, primary flow, page responsibility, business rules, compliance, deletion behavior, money, external commitments, or acceptance outcomes.

Ask one decision per question, preferably in a batch of at most five. Include options, trade-offs, evidence-backed recommendation, and affected entities when known. Record the human answer before continuing.

Low-impact copy or visual details may proceed only as explicit assumptions. High-impact product decisions may not.

## Author handoff

Each revision includes model/workflow versions, revision ID, changed entity IDs and relations, evidence, resolved clarifications, assumptions, affected files, traceability changes, invariant results, and status `READY_FOR_REVIEW`.

Structural changes rewrite complete affected entities and remove superseded text.

## Review gate

The independent Reviewer returns findings as `BLOCK`, `WARN`, or `NOTE`, and one verdict:

- `APPROVED`: no blocking finding or clarification.
- `CHANGES_REQUESTED`: the Author can fix the revision without a new human product decision.
- `HUMAN_DECISION_REQUIRED`: a human product decision is required before revision continues.

The Reviewer never edits the PRD under review.

## Rework

`CHANGES_REQUESTED` preserves the ReviewRecord, routes required actions to the Author, creates revision `rN+1`, and requires another independent review.

Default maximum is three review cycles. Repeated unresolved blocking findings escalate to the human instead of creating an unbounded loop.

## Completion

The product stage completes only when the latest ReviewRecord is `APPROVED`, no blocking clarification is open, model invariants and traceability pass, superseded requirements are removed, and clarification/review evidence is preserved.

For major changes, show the approved revision and review summary to the human before design or implementation.

## Design influence

This workflow adapts useful patterns from `yimwoo/codex-agenteam`: specialist role separation, scoped write authority, structured handoffs, human gates, reviewer verdicts, and rework routing.
