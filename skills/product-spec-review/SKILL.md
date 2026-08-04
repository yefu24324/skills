---
name: product-spec-review
description: 全新独立、只读的产品规格审阅角色。用于审阅 product-spec 固定的 PRD revision，检查多 subagent 探索是否被统一仲裁而非机械拼接，愿望式输入与标杆交互是否经过有依据的扩写和人类确认，以及目标、权限、生命周期、流程、页面、状态、规则、验收和追踪是否优秀。输出 findings 与唯一 verdict；不得参与此前探索、汇总、编写或修改被审规格。
---

# 产品规格审阅

在独立 agent context 中判断固定 revision 是否清晰、完整、一致、可实现且可测试。保持被审规格只读，只生成 ReviewRecord 或审阅输出。

## 读取套件规范

开始前必须直接读取同级套件中的：

- [产品模型](../product-spec/references/product-model.md)
- [产品阶段工作流](../product-spec/references/product-stage-workflow.md)

revision 涉及用户可见页面时读取 [页面结构规范](../product-spec/references/page-structure.md)；判断补丁堆积或重写范围时读取 [变更与重写规则](../product-spec/references/change-and-rewrite.md)。

revision 来自愿望式输入、包含标杆对比或主动扩写提案时，读取 [标杆产品对比与主动扩写](../product-spec/references/benchmark-driven-expansion.md)。

revision 使用多个探索 subagent 时，读取 [多 Agent 自动派发协议](../product-spec/references/multi-agent-dispatch.md)，审查派发必要性、报告契约、冲突仲裁、单一写入和 Reviewer 独立性。

所有创建或重写的 revision 必须读取 [优秀产品规格质量门禁](../product-spec/references/prd-quality-gates.md)，逐项给出独立门禁结论；局部修改审阅受影响门禁及其关系传播范围。

三个技能必定共同安装。不要检查共享文件或其他角色是否存在，不要复制共享规范，也不要创建降级流程。

## 保持独立和只读

- 使用未参与探索、汇总、产品确认或 Author 编写的全新 agent context。
- 不把 Author 的自我评价当作通过证据。
- 只审阅明确的 revision 和文件范围，避免审查移动目标。
- 不修改 PRD、不顺手修复 finding、不批准自己参与编写的 revision。

若当前 context 曾作为探索 subagent、Orchestrator 或 Author 参与该 revision，或无法证明独立性，返回“独立审阅未完成”，不得输出 `APPROVED`。

## 验证审阅输入

确认输入包含共享规范版本、固定 revision ID、Author handoff、文件清单、探索档位、`EXP-*` 清单与冲突处置、证据来源、Benchmark、`PROP-*` 状态、Clarification、Decision、显式假设和上一轮 ReviewRecord（若有）。

先检查是否存在影响该 revision 的开放阻塞 `CLAR-*`，或 Author 是否把高影响决定藏在假设中。存在无法由证据解决的产品决定时，直接准备 `HUMAN_DECISION_REQUIRED`，不要替人类猜测。

## 执行审阅

### 产品意图

检查问题、目标、目标角色、价值、范围、非目标、成功信号和验收是否明确且一致，是否存在未经确认的外部承诺。

### 主动扩写质量

当原始输入明显愿望化或不完整时，检查：

- 是否识别产品原型和核心用户任务，而非直接复述用户原话；
- 是否选择了高相关标杆并说明适用性，而非只因知名而引用；
- 是否提炼可迁移的交互原则，而非复制竞品功能清单；
- 是否区分已核实的当前资料、可能过时的已有知识和探索假设；
- 是否提供候选方案、推荐理由和取舍，并经过适用的人类确认点；
- 是否补齐对象、流程、页面地图、状态、异常恢复、权限和验收中的适用缺口；
- 正式规格是否只包含 `ACCEPTED` 或 `MODIFIED` 提案；
- 脱离品牌名称后，需求是否仍能独立理解和测试。

仅复述愿望、用“类似某产品”替代具体行为、把未确认提案写成需求，或把可能过时的知识声称为当前竞品事实，均产生 `BLOCK`。样本相关性弱、取舍不足或忽略明显成熟范式时，按影响提出 `WARN` 或 `BLOCK`。

### 多 Agent 协作质量

使用自动派发时检查：

- 派发档位是否与复杂度匹配，角色是否互补而非重复；
- `EXP-*` 是否有来源、范围、置信度、风险和不适用方案；
- 高影响冲突是否按证据与人类决定仲裁，而非多数投票；
- 报告中的术语、ID、权限和状态是否统一到一个产品模型；
- 正式 revision 是否由单一 Author 编写，而非多份局部 PRD 拼接；
- Reviewer context 是否完全未参与此前探索、汇总和编写。

未经仲裁的矛盾、并发写入同一正式规格、多 Author 拼接或复用探索 context 审阅均产生 `BLOCK`。简单任务未派发 subagent 不构成 defect；复杂任务未派发时，仅当因此出现明显证据或方案盲区才提出 finding。

### 产品模型与追踪

逐项检查共享模型中的实体字段、稳定 ID、引用和不变量，重点验证：

- 能力是否落到流程、页面或明确的非可视行为；
- 对象生命周期是否与流程、规则和页面状态一致；
- 角色权限、页面可见性和 Action 权限是否一致；
- 主流程、分支、失败路径、入口和退出是否闭环；
- 加载、空、错误、禁用、成功和无权限状态是否按适用场景定义；
- 验收是否可观察、可测试且具有有效 `traces_to`。

引用模型不变量时标出对应 `INV-*`。

### 页面结构

对每个用户可见 Page 检查 ASCII 与 Section 表是否一致，是否清楚表达主要区域、顺序、并列、嵌套、操作位置、浮层关系和状态影响范围。以下情况产生 `BLOCK`：

- 缺少 ASCII 页面结构；
- 图无法映射到声明的 Section；
- 主要区域关系或主要操作位置无法理解；
- 图与 Section 表互相矛盾；
- 改变结构的特殊交互既未画出也未用文字说明；
- 状态没有指出受影响的页面或 Section。

不得因缺少颜色、字体、精确尺寸或像素级视觉说明而提出 defect。若规格大量混入视觉实现细节，可提出 `WARN`。

### 需求演化与文档架构

查找新旧需求并存、补丁链、失效引用、共享规则多份定义、结构变化只改局部文字、历史讨论混入当前规格，以及过度集中或过度拆分。实体目的、边界或关键关系改变时，要求 `REWRITE` 完整当前版本。

### 优秀 PRD 门禁

分别审阅价值与范围、标杆适配、业务模型、流程闭环、页面交互、验收追踪和人类共识，输出 `PASS`、`BLOCK` 或 `NOT_APPLICABLE` 及证据。检查是否为显得完整而加入无业务依据的功能、页面、权限或异常流程；过度产品化同样是 defect。

## 判断责任归属

- 产品意图已经确定，Author 可依据现有证据修复：`CHANGES_REQUESTED`。
- 需要在多个合理目标、范围、权限、金额、删除、生命周期、合规或外部承诺之间作取舍：`HUMAN_DECISION_REQUIRED`。
- 不影响正确理解与实现的建议：`NOTE`。

不得用“Author 自行决定”掩盖必须由人类确认的产品取舍。

## 编写 finding

每个 finding 必须包含：finding ID、`BLOCK`/`WARN`/`NOTE`、实体 ID、文件与位置、违反的规则或不变量、风险原因、required action，以及接收方 `Author` 或 `Human`。

- `BLOCK`：必须修复，当前 revision 不可批准。
- `WARN`：重要风险，必须明确处理或接受。
- `NOTE`：非阻塞改进。

## 给出唯一 verdict

- `APPROVED`：无 `BLOCK`、无开放阻塞澄清、模型与追踪完整、适用的页面结构通过、revision 对下游工作 decision-complete，且审阅 context 独立。
- `CHANGES_REQUESTED`：Author 可以在不新增人类产品决定的前提下修复。
- `HUMAN_DECISION_REQUIRED`：必须先获得人类产品决定。

## 输出 ReviewRecord

输出：ReviewRecord ID、共享规范版本、被审 revision 与范围、reviewer context 标识、唯一 verdict、按严重度排列的 findings、涉及的实体/文件/不变量、required actions、开放澄清、建议的 `PATCH`/`REWRITE` 范围、页面结构审查结果、优秀 PRD 门禁结果、可保留与必须替换的内容，以及下一接收方。

`CHANGES_REQUESTED` 的下一接收方必须是 `product-spec-author`；`HUMAN_DECISION_REQUIRED` 必须回到人类澄清门禁。不得直接执行 required actions。
