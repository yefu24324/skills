# Product Document Architecture

## Goal

Keep product specifications readable for humans and useful for AI agents.

Avoid one giant PRD file containing hundreds of sections. Split documents by stable product concepts.

## Recommended Structure

```text
docs/product/
├── index.md                 # Product map and navigation
├── features/
│   └── feature-name/
│       ├── overview.md      # Feature goal and scope
│       └── rules.md         # Feature business rules
├── flows/
│   └── user-flow.md         # End-to-end scenarios
├── pages/
│   └── page-name.md         # One page specification
├── shared/
│   └── common-rule.md       # Cross-feature concepts
└── decisions/
    └── ADR.md               # Why decisions were made
```

## Split Rules

Create a separate document when:

- A page exceeds comfortable human reading length.
- A feature has independent ownership or lifecycle.
- A workflow is reused by multiple features.
- A rule affects multiple pages.
- A decision needs historical context.

## Avoid

Do not create:

- A single PRD containing every page.
- Pages mixed with unrelated business rules.
- Historical change logs inside current requirements.
- Repeated copies of the same rule in multiple documents.

## AI Maintenance Rule

When updating documentation:

1. Locate the smallest valid document boundary.
2. Update the owner document.
3. Update indexes and references.
4. Do not append another exception section if the model has changed.
