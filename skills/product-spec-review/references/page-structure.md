# Page Structure Description Standard

Standard version: `1.0`

This standard is shared by `product-spec`, `product-spec-author`, and `product-spec-review`.

## Purpose

Describe the product-level information architecture and functional regions of a page clearly enough for humans, designers, developers, and reviewers to understand the intended structure.

This is not a visual design specification. It does not define colors, typography, pixel dimensions, spacing, shadows, border radius, icon style, or other aesthetic details.

## Primary rule

Every user-visible Page must include an ASCII structure diagram in `layout_structure`.

The ASCII diagram is the primary representation of page structure. Supporting prose should explain only behavior that is difficult to show spatially.

A non-visual capability does not require a page diagram, but it must be explicitly declared non-visual.

## What the ASCII diagram must show

Use Section IDs or stable section names to show:

- the page shell or surrounding navigation context when relevant;
- the major functional regions;
- top-to-bottom ordering;
- side-by-side relationships;
- parent-child nesting;
- tabs, drawers, dialogs, popovers, or other overlays when they materially affect the flow;
- the location of primary and secondary actions;
- which region is replaced or updated by a selection when this is important.

Do not attempt pixel-perfect wireframes. Relative relationships are enough.

## Recommended form

```text
+--------------------------------------------------+
| Page Header                                      |
| [Breadcrumb]  Title                 [Primary]    |
+--------------------------------------------------+
| Filter Section                                   |
+----------------------+---------------------------+
| Navigation Section   | Main Content Section      |
|                      |                           |
|                      |                           |
+----------------------+---------------------------+
| Pagination / Footer                              |
+--------------------------------------------------+
```

A hierarchy-style ASCII description is also acceptable when it communicates the structure more clearly:

```text
PAGE-ORDER-DETAIL
├── SEC-PAGE-HEADER
│   ├── Breadcrumb
│   ├── Order summary
│   └── Primary actions
├── SEC-ORDER-CONTENT
│   ├── SEC-ORDER-INFO
│   └── SEC-PAYMENT-INFO
└── SEC-ACTIVITY-TIMELINE
```

## Special interactions

Describe special interactions with short prose after the ASCII diagram. Use the minimum detail needed to remove ambiguity:

```text
- Selecting a result opens the detail drawer without leaving the list.
- Closing the drawer preserves the current filters and scroll position.
- A failed detail request keeps the drawer open and shows a retry action.
```

Prefer a simple `trigger -> response -> result/feedback` description.

Do not turn ordinary interactions into long sequence specifications. Create a separate Flow document only when the interaction crosses multiple pages, has important branches, or changes business object state.

## Required supporting sections

After the ASCII diagram, provide:

1. a Section table with Section ID, responsibility, content, actions, states, and visibility or permission rules;
2. special interaction notes only where the ASCII structure is insufficient;
3. page-level and section-level state behavior;
4. entry and exit paths;
5. acceptance criteria linked by stable IDs.

## Out of scope

Do not specify these in a product requirement unless they are themselves a functional or regulatory requirement:

- colors or themes;
- font family, font size, or font weight;
- exact width, height, margin, padding, or pixel coordinates;
- border, shadow, radius, animation curve, or visual decoration;
- exact responsive breakpoints;
- component implementation details.

Statements such as “left navigation and main content area” are appropriate. Statements such as “the left panel is 280 px wide and uses #FFFFFF” are not.

## Review rules

A user-visible Page receives a `BLOCK` finding when:

- no ASCII structure diagram is present;
- the diagram does not map to the declared Sections;
- the order, nesting, adjacency, or overlay relationship of major Sections cannot be understood;
- primary actions cannot be located in a functional region;
- a special interaction changes page structure but is neither shown nor described;
- page or section states do not identify which region changes;
- the page description is mostly visual styling rather than product structure and behavior.

A diagram may remain intentionally approximate. Lack of colors, exact dimensions, or pixel-level styling is never a defect in a product specification.
