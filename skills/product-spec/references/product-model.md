# 共享产品模型

模型版本：`2.2`

本文件是 `product-spec`、`product-spec-author` 和 `product-spec-review` 的共同概念模型，也是唯一权威定义。三个技能共同安装，并直接读取本文件。

## 目标

用相互关联的产品实体表达当前产品，而不是维护一篇缺少结构的长篇 PRD。文档可使用 Markdown 表格、YAML、ASCII 图或文字，但必须保留下述实体、稳定 ID、关系、治理记录和不变量。

## 当前事实与历史

- 当前产品规格只描述当前有效的产品模型。
- 历史原因、被否决方案和被替代结构进入 `decisions/` 或版本历史。
- 假设与未决问题必须显式标记，不能冒充已确认需求。
- 影响范围、权限、生命周期、主流程、规则或验收的阻塞澄清，必须由人类解决后才能写成最终规格。
- 只有独立 ReviewRecord 的 verdict 为 `APPROVED`，revision 才能通过产品阶段。

## 产品实体

字段名是跨技能契约，保留英文标识；字段含义和内容使用中文。

### Product（产品）

必填字段：`id`、`goal`、`scope`、`non_goals`、`roles`、`capabilities`、`success_signals`。

### Role（角色）

必填字段：`id`、`name`、`goals`、`permissions`、`capabilities_used`。

角色必须体现目标、访问范围或行为差异；不要仅因人口属性不同创建角色。

### Capability（能力）

必填字段：`id`、`name`、`goal`、`roles`、`objects`、`flows`、`pages`、`rules`、`acceptance_criteria`。

能力表示一项完整的产品能力，不等同于页面名称或技术组件。

### Object（业务对象）

必填字段：`id`、`name`、`meaning`、`owner_or_scope`、`lifecycle_states`、`related_objects`、`governing_rules`。

描述业务含义、归属与生命周期。只有技术字段能够被用户观察，或直接构成功能要求时，才进入产品规格。

### Flow（流程）

必填字段：`id`、`name`、`actor`、`trigger`、`preconditions`、`steps`、`branches`、`failure_paths`、`completion_result`、`pages`、`objects_changed`、`rules`、`acceptance_criteria`。

每个分支都说明条件和结果。非可视流程必须明确标记为非可视。

### Page（页面）

必填字段：`id`、`name`、`purpose`、`roles`、`entry_paths`、`exit_paths`、`layout_structure`、`sections`、`page_states`、`permissions`、`rules`、`acceptance_criteria`。

一个页面只承担一个主要职责。若主要目标冲突，或独立生命周期使规格难以理解，应拆成多个页面。

### Section（功能板块）

必填字段：`id`、`name`、`responsibility`、`location`、`content`、`actions`、`local_states`、`visibility_rules`。

Section 是具有产品职责的页面区域，不是像素级视觉组件。

### Action（操作）

必填字段：`id`、`label_or_intent`、`actor`、`preconditions`、`effect`、`feedback`、`failure_behavior`、`permissions`、`rules`、`acceptance_criteria`。

### Rule（规则）

必填字段：`id`、`statement`、`applies_to`、`condition`、`result`、`exceptions`、`source_or_status`。

共享规则只在一个权威位置定义，其他文档通过 ID 引用，不复制出略有差异的版本。

### State（状态）

必填字段：`id`、`subject`、`name`、`meaning`、`entry_condition`、`allowed_transitions`、`visible_behavior`。

区分业务对象状态与加载、空、错误、禁用、成功、无权限等界面状态。

### AcceptanceCriterion（验收标准）

必填字段：`id`、`traces_to`、`given`、`when`、`then`。

验收必须可观察、可测试；`traces_to` 至少引用一个能力、流程、页面、Section、Action、规则或状态 ID。

### Decision（产品决策）

必填字段：`id`、`context`、`decision`、`consequences`、`status`、`supersedes`、`affected_entities`。

Decision 保存当前模型形成的理由和替代关系，避免把历史叙述混入当前规格。

### Benchmark（标杆记录）

必填字段：`id`、`product_or_pattern`、`relevance`、`evidence_level`、`source`、`observed_or_known_at`、`transferable_principles`、`non_applicable_parts`、`affected_entities`。

`evidence_level` 使用 `CURRENT_VERIFIED`、`PROJECT_EVIDENCE`、`KNOWN_PATTERN` 或 `HYPOTHESIS`。Benchmark 用于记录方案依据，不自动构成产品需求。

### Proposal（主动扩写提案）

必填字段：`id`、`gap`、`user_job`、`benchmarks`、`options`、`recommended_option`、`transferable_principle`、`tradeoffs`、`affected_entities`、`decision_owner`、`status`。

`id` 使用 `PROP-*`；`status` 使用 `PROPOSED`、`ACCEPTED`、`MODIFIED`、`REJECTED` 或 `DEFERRED`。只有人类接受或修改后的提案才能进入正式规格。

### ExplorationReport（探索报告）

必填字段：`id`、`role`、`scope`、`agent_context`、`sources`、`confirmed_findings`、`interaction_patterns`、`gaps`、`options`、`affected_entities`、`suggested_records`、`risks_and_unknowns`、`non_applicable_ideas`、`confidence`。

`id` 使用 `EXP-*`。ExplorationReport 是只读探索产物，只提供证据和候选方案，不是正式产品规格，也没有批准权。

### DispatchRecord（派发记录）

必填字段：`id`、`complexity_tier`、`reason`、`planned_roles`、`agent_contexts`、`reports`、`waves`、`failures`、`conflicts`、`resolution`、`author_context`、`reviewer_context`。

`complexity_tier` 使用 `SIMPLE`、`STANDARD`、`COMPLEX` 或 `PROGRAM`。记录为什么派发或不派发、报告如何汇总，以及 Author/Reviewer 是否满足独立性。创建 Reviewer 前将 `reviewer_context` 标为 `RESERVED_NEW_CONTEXT`，实际审阅启动后必须回填真实 context 标识。

## 治理记录

治理记录控制澄清和批准过程，不替代产品实体。

### Clarification（澄清）

必填字段：

- `id`：格式为 `CLAR-*`；
- `question`：一个具体产品决定；
- `reason`：项目证据无法解决的原因；
- `impact`：对目标、范围、角色、能力、对象、流程、页面、规则、状态或验收的影响；
- `affected_entities`：已有稳定 ID 时必须列出；
- `options`：适用时列出具体选项和取舍；
- `recommended_option`：可选，必须附有依据；
- `status`：`OPEN`、`RESOLVED` 或 `DEFERRED`；
- `blocking`：布尔值；
- `resolution`：人类答案或明确延期；
- `resolved_by`：人类来源或 Decision ID。

如果猜测可能改变范围、权限、生命周期、主流程、页面职责、业务规则、删除行为、金额、合规、外部承诺或验收结果，该澄清必须阻塞。

### ReviewRecord（审阅记录）

必填字段：

- `id`：格式为 `REVIEW-*`；
- `model_version`、`workflow_version`、`page_structure_version`、`expansion_method_version`、`quality_gate_version`；
- `draft_revision`、`review_scope`；
- `reviewer_context`：必须与 Author context 及所有探索/汇总 context 不同；
- `verdict`：`APPROVED`、`CHANGES_REQUESTED` 或 `HUMAN_DECISION_REQUIRED`；
- `findings`：由 `BLOCK`、`WARN`、`NOTE` 项组成；
- `affected_entities`、`required_actions`、`open_clarifications`、`supersedes`。

Reviewer 只报告问题、证据和 required actions，不修改正在审阅的规格。

## 必须维护的关系

```text
Product -> Role
Product -> Capability
Capability -> Object
Capability -> Flow
Capability -> Page 或明确的非可视行为
Flow -> Page
Flow -> Object 状态迁移
Page -> Section
Section -> Action
Action -> Rule
Rule -> Object、Flow、Page、Section、Action 或 State
AcceptanceCriterion -> 一个或多个产品实体
Decision -> 受影响产品实体
Benchmark -> Proposal 及受影响产品实体
DispatchRecord -> ExplorationReport
ExplorationReport -> Benchmark、Proposal、Clarification 及受影响产品实体
Proposal -> 候选产品实体或 Decision
Clarification -> 受影响产品实体
Decision -> 解决 Clarification
ReviewRecord -> 固定 revision 及被审产品实体
```

## 模型不变量

使用以下编号报告校验或 finding：

1. `INV-01`：每个 ID 在产品范围内唯一，并在跨文件引用时保持稳定。
2. `INV-02`：每项 Capability 至少追踪到一个 Flow、Page 或明确的非可视行为。
3. `INV-03`：每个 Page 属于一项 Capability，并至少参与一个入口路径或 Flow。
4. `INV-04`：每个 Section 只属于一个 Page，除非显式声明为共享结构。
5. `INV-05`：每个用户 Action 定义效果、反馈、失败行为、权限和可测试验收。
6. `INV-06`：业务状态迁移在 Object、Flow、Page 和 Rule 中保持一致。
7. `INV-07`：共享 Rule 只有一个权威定义，其他位置只引用。
8. `INV-08`：当前规格不依赖已被替代的需求。
9. `INV-09`：不得存在孤立实体、断裂引用、无出口循环导航或矛盾权限。
10. `INV-10`：假设和开放问题不得静默变成已确认规则。
11. `INV-11`：提交审阅时，不得存在影响该 revision 的开放阻塞 Clarification。
12. `INV-12`：没有 verdict 为 `APPROVED` 的独立 ReviewRecord，revision 不得通过产品阶段。
13. `INV-13`：Author 与 Reviewer 使用不同 agent context，Reviewer 不得批准自己参与编写的 revision。
14. `INV-14`：`CHANGES_REQUESTED` 必须带 required actions 返回 Author，并产生新 revision。
15. `INV-15`：`HUMAN_DECISION_REQUIRED` 必须暂停受影响 revision，直至人类决定已解决或明确延期。
16. `INV-16`：标杆对比必须记录相关性、依据等级、时效和可迁移原则；`KNOWN_PATTERN` 不得表示为已核实的当前事实。
17. `INV-17`：正式规格只能吸收状态为 `ACCEPTED` 或 `MODIFIED` 的 Proposal，不得静默采纳 `PROPOSED`、`REJECTED` 或 `DEFERRED` 内容。
18. `INV-18`：来自标杆产品的方案必须转写为当前用户任务、行为、规则和验收；品牌名称不得替代产品规格。
19. `INV-19`：质量门禁的适用项必须全部 `PASS`；`NOT_APPLICABLE` 必须说明原因，不能用来规避缺失需求。
20. `INV-20`：探索 subagent 只读且不写正式 PRD；并发 Agent 不得修改同一正式规格文件。
21. `INV-21`：多个 ExplorationReport 必须统一术语、稳定 ID 和冲突处置后才能交给 Author；一致意见也不能替代证据或人类决定。
22. `INV-22`：每个 revision 只有一个 Author context；最终 Reviewer 必须是未参与探索、汇总或编写的全新 context。

## 追踪矩阵

| 需求或能力 | 角色 | 对象 | 流程 | 页面 | 规则 | 验收 | 探索、标杆与提案 | 澄清 | 审阅 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CAP-*` | `ROLE-*` | `OBJ-*` | `FLOW-*` | `PAGE-*` | `RULE-*` | `AC-*` | `EXP-*` / `BM-*` / `PROP-*` | `CLAR-*` | `REVIEW-*` |

追踪矩阵用于导航和完整性检查，不能替代实体的详细规格。

## 推荐文档映射

```text
docs/product/
├── index.md                    # 产品范围、能力地图、页面地图和追踪入口
├── features/<feature>/         # 能力目标与边界
├── objects/<object>.md         # 业务含义与生命周期
├── flows/<flow>.md             # 跨页面或非可视流程
├── pages/<page>.md             # 页面、板块、操作和界面状态
├── shared/<topic>.md           # 共享规则的权威定义
├── research/explorations/      # 只读探索报告和派发记录
├── research/benchmarks.md      # 标杆依据、时效和可迁移原则
├── proposals.md                # 主动扩写提案及人类确认状态
├── clarifications.md           # 开放与已解决澄清
├── reviews/<scope>-rN.md       # 固定 revision 的只读审阅记录
└── decisions/<decision>.md     # 决策原因与替代关系
```

按职责、生命周期、读者和变化原因拆分，不按任意行数机械切割。
