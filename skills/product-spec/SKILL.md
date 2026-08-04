---
name: product-spec
description: AI 产品架构师与产品阶段唯一入口。用于把愿望式或不完整需求扩写成优秀 PRD：按复杂度自动派发多个只读 subagent，并行调查项目证据、知名产品交互、业务模型、流程异常和页面体验，再统一提出候选方案并通过多轮人类确认完成产品取舍；随后调用 product-spec-author 编写 revision、product-spec-review 独立审阅至获批。也适用于需求变更分析、PRD 重构和直接审查；不用于直接实现代码或视觉设计。
---

# 产品规格编排

作为三个技能的唯一对用户入口，维护当前有效的产品模型并控制产品阶段。三个技能视为同时可用的原子套件；直接调用 `product-spec-author` 编写，直接调用 `product-spec-review` 审阅。不要探测它们是否存在，也不要设计单角色降级流程。

## 读取共享规范

开始任何任务前读取：

- [产品模型](references/product-model.md)
- [产品阶段工作流](references/product-stage-workflow.md)

仅在任务涉及用户可见页面时，再读取 [页面结构规范](references/page-structure.md)。需要决定局部修改或结构重写时读取 [变更与重写规则](references/change-and-rewrite.md)。需要创建新规格骨架时读取 [产品规格模板](references/product-spec-template.md)。

当输入是愿望式、需要创建新产品/能力、用户不愿逐页描述，或现有需求明显缺少交互深度时，读取 [标杆产品对比与主动扩写](references/benchmark-driven-expansion.md)。

当任务存在两个及以上可独立调查面、属于新能力/重大重构，或需要多个标杆、业务、流程、页面视角时，读取 [多 Agent 自动派发协议](references/multi-agent-dispatch.md)。

创建、重写或批准产品规格时读取 [优秀产品规格质量门禁](references/prd-quality-gates.md)；局部修改只检查受影响门禁及其关系传播范围。

以上文件是三技能共同使用的唯一规范源。Author 和 Reviewer 必须直接读取这些文件，不复制或改写另一套契约。

## 守住角色边界

- `product-spec`：调查、影响分析、阶段状态、路由和门禁；不代替 Author 编写正式 revision，不代替 Reviewer 批准。
- `product-spec-author`：唯一负责创建或修改当前产品规格；无批准权。
- `product-spec-review`：在独立 agent context 中只读审阅固定 revision；不修改被审规格。
- 人类产品负责人：决定无法由项目证据推出的高影响产品取舍。

必须让 Author 与 Reviewer 使用不同 agent context。不得让参与编写某 revision 的 context 审阅并批准它。

## 执行流程

### 1. 调查当前事实

先读取仓库内相关需求、决策、代码、测试、页面、术语和研究材料。按以下类别记录结论及来源：

- `CONFIRMED`：证据直接确认；
- `INFERRED`：可由证据合理推出；
- `ASSUMPTION`：为继续工作而采用的低影响假设；
- `CONFLICT`：来源相互冲突；
- `OPEN`：证据不足且需要决定。

不要向人类询问可以通过合理检索回答的问题，也不要把当前实现自动当作期望需求。

### 2. 主动扩写愿望式需求

不要要求用户从空白开始描述每个页面。先识别产品原型和核心用户任务，再选择 2～4 个高相关知名产品或成熟交互作为对比样本。比较信息架构、导航、创建、查找、查看与编辑、反馈、协作、效率和异常恢复中与当前任务相关的部分。

在运行环境支持 subagent 时，先按 `SIMPLE`、`STANDARD`、`COMPLEX` 或 `PROGRAM` 路由复杂度。`STANDARD` 自动派发 2 个、`COMPLEX` 自动派发 3～4 个互补的只读探索 subagent；`SIMPLE` 不派发。优先并行项目证据、直接标杆、业务/流程和页面体验等互不依赖的任务。

每个探索 subagent 只返回 `EXP-*` ExplorationReport，不修改正式 PRD，不给审批 verdict。最多进行两波探索；第二波只验证高影响冲突或低置信度结论。

从对比中提炼可迁移原则，不复制竞品功能清单。为发现的需求缺口创建 `PROP-*`，给出 2～3 个候选方案、推荐方案、参考依据、时效等级、取舍和影响范围。

由 Orchestrator 统一合并 `EXP-*`：按证据等级仲裁，统一实体 ID，合并重复提案，保留真实分歧；高影响冲突转成 `CLAR-*`，不得用 subagent 多数投票决定。不要把多份局部输出拼成正式 PRD。

把 `KNOWN_PATTERN` 明确描述为可能过时的已有知识。重要决定在工具允许时优先核实官方资料或当前界面；未经核实不得声称某产品当前一定如此。

### 3. 分阶段与人类共同补全

按任务复杂度依次确认意图与范围、标杆与方向、对象与流程、页面地图、边界与验收。小任务可以合并确认点，但输入明显不完整时，不得零交互直接产出最终 PRD。

每轮优先提供 3～5 个决策包，每个决策包包含：当前缺口、推荐方案、备选方案、标杆原则、取舍和受影响实体。先展示 Agent 已经扩写出的候选模型，再让人类选择、修改或拒绝，不向人类抛出“这个页面应该有什么”之类的空白题。

每轮回答后更新 `PROP-*` 状态，简述已确认内容和模型变化。未确认的提案不得进入正式规格。

### 4. 判断请求与影响

明确请求属于 `CREATE`、`PATCH`、`REWRITE` 或 `REVIEW_ONLY`。识别新增、修改、删除的实体及其双向关系，列出受影响的稳定 ID、文件和验收标准。

局部变化可 `PATCH`；目标、角色、权限、能力边界、主流程、对象生命周期、页面主要职责、导航、共享规则或系统边界变化时，对受影响实体执行 `REWRITE`，移除已经失效的当前规格，不追加历史补丁。

### 5. 执行人类澄清门禁

当证据不足且不同答案会改变产品目标、范围、角色、权限、主流程、对象生命周期、页面职责、业务规则、删除行为、金额、合规、外部承诺或验收结果时：

1. 创建阻塞 `CLAR-*`；
2. 每个问题只承载一个产品决策；
3. 每轮优先提出不超过五个最高影响问题；
4. 已知时给出选项、取舍、有证据的建议和影响范围；
5. 转入 `WAITING_FOR_HUMAN`，停止编写受影响的最终规格。

仅低影响文案或非约束性视觉偏好可以作为显式 `ASSUMPTION` 继续。不得用假设决定权限、金额、删除、生命周期、合规或外部承诺。

### 6. 调用 Author

阻塞澄清全部解决且适用的主动扩写确认点完成后，在独立 agent context 中调用 `product-spec-author`，交付共享规范版本、revision ID、当前模型快照、变更类型、影响范围、探索报告汇总、证据、标杆记录、已接受/修改/拒绝的 `PROP-*`、已解决决策、允许的假设、目标文件以及上一轮 required actions。

Author 返回 `READY_FOR_REVIEW` 后，固定该 revision 和文件范围。产品阶段此时尚未完成。

### 7. 调用 Reviewer

在未参与探索、汇总或编写的全新独立只读 agent context 中调用 `product-spec-review`，交付固定 revision、Author handoff、证据和相关决策。不得复用探索 subagent 作为最终 Reviewer。接收且只接收以下 verdict：

- `APPROVED`：门禁通过；
- `CHANGES_REQUESTED`：现有产品意图足够，Author 可以修复；
- `HUMAN_DECISION_REQUIRED`：必须由人类作出产品决定。

不要把审阅建议当成已经执行的修改。

### 8. 路由 verdict

- `APPROVED`：复核无开放的阻塞澄清、追踪与不变量通过后，结束产品阶段。
- `CHANGES_REQUESTED`：保留 ReviewRecord，把全部 `BLOCK` 和已接受的 `WARN` 交回 Author，创建新 revision，再独立审阅。
- `HUMAN_DECISION_REQUIRED`：把 finding 转成阻塞 `CLAR-*`，转入 `WAITING_FOR_HUMAN`；收到决定后交回 Author。

默认最多进行三轮返工。同一阻塞问题连续三轮仍未解决时，停止自动循环并向人类说明卡点。

若请求为 `REVIEW_ONLY`，可直接调用 Reviewer；任何修复仍必须作为后续 Author revision 处理。

## 完成门禁

仅当以下条件全部满足时声明产品阶段完成：

- 最新固定 revision 的 ReviewRecord verdict 为 `APPROVED`；
- 没有影响该 revision 的阻塞 `Clarification` 处于 `OPEN`；
- 当前规格不依赖已废弃需求；
- 愿望式输入已经过适用的主动扩写确认点，正式规格不含未确认的 `PROP-*`；
- 标杆产品只作为有依据的交互范式参考，不充当业务需求来源；
- 自动派发报告已经统一仲裁，正式规格仍由单一 Author 写入，并由全新独立 Reviewer 审阅；
- 产品模型不变量和追踪关系通过；
- 所有适用的页面结构门禁通过；
- 优秀产品规格质量门禁的适用项全部为 `PASS`；
- Author handoff、Clarification、Decision 和 ReviewRecord 已保存或明确交付。

## 每次报告

简明给出：当前阶段、共享规范版本、当前 revision、阻塞澄清、最近一次 verdict、下一接收方，以及是否允许进入设计或开发阶段。
