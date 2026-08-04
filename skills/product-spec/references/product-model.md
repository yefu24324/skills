# Shared Product Model

Model version: `1.0`

This file is the common conceptual schema used by `product-spec`, `product-spec-author`, and `product-spec-review`. Each skill carries an identical copy so it remains usable when installed alone. When the model changes, update all copies together and run `python scripts/validate_product_model_sync.py`.

## Purpose

Represent the current product as connected product entities instead of an unstructured PRD. The model is conceptual: documents may use Markdown tables, YAML, diagrams, or prose, but they must preserve the entities, identifiers, relations, and invariants below.

## Current truth and history

- Current product documents describe only the currently valid product model.
- Historical reasoning, rejected alternatives, and superseded structures belong in `decisions/` or version control.
- Assumptions and unresolved questions must be explicitly labeled; they are not confirmed requirements.

## Entity schema

### Product

Required fields:

- `id`: stable identifier.
- `goal`: user or business outcome.
- `scope`: included product boundary.
- `non_goals`: explicitly excluded boundary.
- `roles`: role IDs.
- `capabilities`: capability IDs.
- `success_signals`: observable measures when known.

### Role

Required fields:

- `id`
- `name`
- `goals`
- `permissions`
- `capabilities_used`

A role describes a meaningful difference in goals, access, or behavior. Do not create separate roles only for demographic descriptions.

### Capability

Required fields:

- `id`
- `name`
- `goal`
- `roles`
- `objects`
- `flows`
- `pages`
- `rules`
- `acceptance_criteria`

A capability is a coherent product ability, not a page name or implementation component.

### Object

Required fields:

- `id`
- `name`
- `meaning`
- `owner_or_scope`
- `lifecycle_states`
- `related_objects`
- `governing_rules`

Describe business meaning and lifecycle. Include technical fields only when they are observable product requirements.

### Flow

Required fields:

- `id`
- `name`
- `actor`
- `trigger`
- `preconditions`
- `steps`
- `branches`
- `failure_paths`
- `completion_result`
- `pages`
- `objects_changed`
- `rules`
- `acceptance_criteria`

Every branch must state its condition and result. A flow may be non-visual, but this must be explicit.

### Page

Required fields:

- `id`
- `name`
- `purpose`
- `roles`
- `entry_paths`
- `exit_paths`
- `layout_structure`
- `sections`
- `page_states`
- `permissions`
- `rules`
- `acceptance_criteria`

A page must have one primary responsibility. Split pages whose primary goals conflict or whose independent lifecycles make one specification difficult to understand.

### Section

Required fields:

- `id`
- `name`
- `responsibility`
- `location`
- `content`
- `actions`
- `local_states`
- `visibility_rules`

A section is a functional page region. It is not a pixel-level visual component.

### Action

Required fields:

- `id`
- `label_or_intent`
- `actor`
- `preconditions`
- `effect`
- `feedback`
- `failure_behavior`
- `permissions`
- `rules`
- `acceptance_criteria`

### Rule

Required fields:

- `id`
- `statement`
- `applies_to`
- `condition`
- `result`
- `exceptions`
- `source_or_status`

Rules must be stated once and referenced by ID. Avoid copying slightly different versions into several pages.

### State

Required fields:

- `id`
- `subject`
- `name`
- `meaning`
- `entry_condition`
- `allowed_transitions`
- `visible_behavior`

Distinguish business object states from interface states such as loading, empty, error, disabled, success, and no permission.

### AcceptanceCriterion

Required fields:

- `id`
- `traces_to`
- `given`
- `when`
- `then`

Each criterion must be observable and testable. `traces_to` references at least one capability, flow, page, section, action, rule, or state ID.

### Decision

Required fields:

- `id`
- `context`
- `decision`
- `consequences`
- `status`
- `supersedes`

Decisions explain why the current model exists without polluting current specifications with historical narration.

## Required relations

Use stable IDs to maintain these relations:

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

## Traceability matrix

For non-trivial features, maintain a compact matrix:

| Requirement or capability | Roles | Objects | Flows | Pages | Rules | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |
| `CAP-*` | `ROLE-*` | `OBJ-*` | `FLOW-*` | `PAGE-*` | `RULE-*` | `AC-*` |

The matrix is a navigation and completeness tool, not a replacement for detailed specifications.

## Document mapping

Recommended placement:

```text
docs/product/
├── index.md                 # Product, scope, capability map, traceability index
├── features/<feature>/      # Capability-level goals and boundaries
├── objects/<object>.md      # Business meaning and lifecycle
├── flows/<flow>.md          # Cross-page and non-visual flows
├── pages/<page>.md          # Page, section, action, UI state specifications
├── shared/<topic>.md        # Authoritative shared rules and patterns
└── decisions/<decision>.md  # Historical rationale and supersession
```

Split by responsibility, not by arbitrary line count. A document should be split when it has multiple independent owners, primary goals, lifecycles, or change reasons, or when readers must repeatedly skip unrelated sections.

## Change impact protocol

Before editing:

1. Identify changed entities and relations.
2. Classify the change as `PATCH` or `REWRITE`.
3. Traverse incoming and outgoing relations to identify impacted documents.
4. Rewrite complete affected entities when their purpose or relationships changed.
5. Remove superseded text from current specifications.
6. Revalidate invariants and traceability after writing.

Typical `REWRITE` triggers include changes to roles, capability boundaries, main flows, page responsibilities, object lifecycles, permissions, navigation, or system boundaries.
