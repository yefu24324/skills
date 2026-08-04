# Shared Product Model

Model version: `1.1`

This file is the common conceptual schema used by `product-spec`, `product-spec-author`, and `product-spec-review`. Each skill carries an identical copy so it remains usable when installed alone. When the model changes, update all copies together and run `python scripts/validate_product_model_sync.py`.

## Purpose

Represent the current product as connected product entities instead of an unstructured PRD. Documents may use Markdown tables, YAML, diagrams, or prose, but they must preserve the entities, identifiers, relations, governance records, and invariants below.

## Current truth and history

- Current product documents describe only the currently valid product model.
- Historical reasoning, rejected alternatives, and superseded structures belong in `decisions/` or version control.
- Assumptions and unresolved questions must be explicitly labeled; they are not confirmed requirements.
- A blocking clarification must be resolved by a human before affected requirements are authored as final.
- A product-stage draft is not approved until an independent review record has verdict `APPROVED`.

## Entity schema

### Product

Required fields: `id`, `goal`, `scope`, `non_goals`, `roles`, `capabilities`, `success_signals`.

### Role

Required fields: `id`, `name`, `goals`, `permissions`, `capabilities_used`.

A role describes a meaningful difference in goals, access, or behavior. Do not create roles only for demographic descriptions.

### Capability

Required fields: `id`, `name`, `goal`, `roles`, `objects`, `flows`, `pages`, `rules`, `acceptance_criteria`.

A capability is a coherent product ability, not a page name or implementation component.

### Object

Required fields: `id`, `name`, `meaning`, `owner_or_scope`, `lifecycle_states`, `related_objects`, `governing_rules`.

Describe business meaning and lifecycle. Include technical fields only when they are observable product requirements.

### Flow

Required fields: `id`, `name`, `actor`, `trigger`, `preconditions`, `steps`, `branches`, `failure_paths`, `completion_result`, `pages`, `objects_changed`, `rules`, `acceptance_criteria`.

Every branch must state its condition and result. A flow may be non-visual, but this must be explicit.

### Page

Required fields: `id`, `name`, `purpose`, `roles`, `entry_paths`, `exit_paths`, `layout_structure`, `sections`, `page_states`, `permissions`, `rules`, `acceptance_criteria`.

A page must have one primary responsibility. Split pages whose primary goals conflict or whose independent lifecycles make one specification difficult to understand.

### Section

Required fields: `id`, `name`, `responsibility`, `location`, `content`, `actions`, `local_states`, `visibility_rules`.

A section is a functional page region, not a pixel-level visual component.

### Action

Required fields: `id`, `label_or_intent`, `actor`, `preconditions`, `effect`, `feedback`, `failure_behavior`, `permissions`, `rules`, `acceptance_criteria`.

### Rule

Required fields: `id`, `statement`, `applies_to`, `condition`, `result`, `exceptions`, `source_or_status`.

Rules must be stated once and referenced by ID. Avoid copying slightly different versions into several pages.

### State

Required fields: `id`, `subject`, `name`, `meaning`, `entry_condition`, `allowed_transitions`, `visible_behavior`.

Distinguish business object states from interface states such as loading, empty, error, disabled, success, and no permission.

### AcceptanceCriterion

Required fields: `id`, `traces_to`, `given`, `when`, `then`.

Each criterion must be observable and testable. `traces_to` references at least one capability, flow, page, section, action, rule, or state ID.

### Decision

Required fields: `id`, `context`, `decision`, `consequences`, `status`, `supersedes`, `affected_entities`.

Decisions explain why the current model exists without polluting current specifications with historical narration.

## Governance record schema

Governance records control how the product model is clarified and approved. They are not substitutes for product entities.

### Clarification

Required fields:

- `id`: `CLAR-*`.
- `question`: one concrete product decision.
- `reason`: why repository evidence cannot resolve it.
- `impact`: affected goal, scope, role, capability, object, flow, page, rule, state, or acceptance.
- `affected_entities`: stable IDs when available.
- `options`: concrete alternatives with trade-offs when useful.
- `recommended_option`: optional recommendation with rationale.
- `status`: `OPEN`, `RESOLVED`, or `DEFERRED`.
- `blocking`: boolean.
- `resolution`: human answer or explicit deferral.
- `resolved_by`: human source or decision ID.

A clarification is blocking when guessing could change product scope, permissions, lifecycle, main flow, page responsibility, business rule, external commitment, or acceptance outcome.

### ReviewRecord

Required fields:

- `id`: `REVIEW-*`.
- `model_version`.
- `draft_revision`.
- `review_scope`.
- `reviewer_context`: must differ from the authoring context.
- `verdict`: `APPROVED`, `CHANGES_REQUESTED`, or `HUMAN_DECISION_REQUIRED`.
- `findings`: `BLOCK`, `WARN`, and `NOTE` items.
- `affected_entities`.
- `required_actions`.
- `open_clarifications`.
- `supersedes`.

The reviewer is read-only. It reports defects and required changes but does not rewrite the PRD it is judging.

## Required relations

```text
Product -> Role
Product -> Capability
Capability -> Object
Capability -> Flow
Capability -> Page or explicit non-visual behavior
Flow -> Page
Flow -> Object state transition
Page -> Section
Section -> Action
Action -> Rule
Rule -> Object, Flow, Page, Section, Action, or State
AcceptanceCriterion -> one or more model entities
Decision -> affected model entities
Clarification -> affected model entities
Decision -> resolves Clarification
ReviewRecord -> reviewed model entities and draft revision
```

## Model invariants

1. Every ID is unique and stable across files.
2. Every capability traces to at least one flow, page, or explicitly declared non-visual behavior.
3. Every page belongs to a capability and participates in at least one entry path or flow.
4. Every section belongs to exactly one page specification unless explicitly declared shared.
5. Every user action defines effect, feedback, failure behavior, permission, and testable acceptance.
6. Every business state transition appears consistently in object, flow, page, and rule specifications.
7. Shared rules have one authoritative definition and are referenced rather than duplicated.
8. No current document depends on a superseded requirement.
9. Orphan entities, broken references, circular navigation without an exit, and contradictory permissions are defects.
10. Assumptions and open questions never silently become confirmed rules.
11. No blocking `Clarification` remains `OPEN` when the affected PRD revision is submitted for review.
12. A product-stage revision is not approved without a `ReviewRecord` whose verdict is `APPROVED`.
13. Authoring and review use separate agent contexts; the reviewer cannot approve its own authored revision.
14. `CHANGES_REQUESTED` returns to the author with required actions and a new revision; findings are not silently ignored.
15. `HUMAN_DECISION_REQUIRED` pauses revision until the named human decision is resolved or explicitly deferred.

## Traceability matrix

| Requirement or capability | Roles | Objects | Flows | Pages | Rules | Acceptance | Clarifications | Review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CAP-*` | `ROLE-*` | `OBJ-*` | `FLOW-*` | `PAGE-*` | `RULE-*` | `AC-*` | `CLAR-*` | `REVIEW-*` |

The matrix is a navigation and completeness tool, not a replacement for detailed specifications.

## Document mapping

```text
docs/product/
├── index.md                    # Product, scope, capability map, traceability index
├── features/<feature>/         # Capability-level goals and boundaries
├── objects/<object>.md         # Business meaning and lifecycle
├── flows/<flow>.md             # Cross-page and non-visual flows
├── pages/<page>.md             # Page, section, action, UI state specifications
├── shared/<topic>.md           # Authoritative shared rules and patterns
├── clarifications.md           # Open and resolved clarification register
├── reviews/<scope>-rN.md       # Read-only review records by revision
└── decisions/<decision>.md     # Historical rationale and supersession
```

Split by responsibility, not by arbitrary line count. Split when a document has multiple independent owners, primary goals, lifecycles, or change reasons, or when readers repeatedly skip unrelated sections.

## Change impact protocol

Before editing:

1. Identify changed entities and relations.
2. Classify the change as `PATCH` or `REWRITE`.
3. Traverse incoming and outgoing relations to identify impacted documents.
4. Identify unresolved high-impact decisions as `Clarification` records.
5. Resolve blocking clarifications with a human before final authoring.
6. Rewrite complete affected entities when their purpose or relationships changed.
7. Remove superseded text from current specifications.
8. Revalidate invariants and traceability after writing.
9. Submit the revision to an independent reviewer.
10. Repeat author-review until `APPROVED`, or escalate `HUMAN_DECISION_REQUIRED`.

Typical `REWRITE` triggers include changes to roles, capability boundaries, main flows, page responsibilities, object lifecycles, permissions, navigation, or system boundaries.
