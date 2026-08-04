# 产品阶段工作流

工作流版本：`2.2`

本工作流由三个共同安装的技能共享：`product-spec` 负责编排，`product-spec-author` 负责编写，`product-spec-review` 负责独立审阅。人类产品负责人决定项目证据无法确定的高影响产品问题。

## 状态机

```text
DISCOVERY
  ├─ 输入完整且无阻塞问题 -> AUTHORING
  └─ 愿望式或交互深度不足 -> DISPATCHING -> PARALLEL_DISCOVERY
                               -> SYNTHESIZING -> BENCHMARKING -> PROPOSING
                               -> HUMAN_ALIGNMENT
                                    ├─ 需要调整候选方案 -> PROPOSING
                                    ├─ 需要人类决定 -> WAITING_FOR_HUMAN -> HUMAN_ALIGNMENT
                                    └─ 适用确认点已通过 -> AUTHORING

AUTHORING -> READY_FOR_REVIEW -> IN_REVIEW
  ├─ APPROVED -> 产品阶段完成
  ├─ CHANGES_REQUESTED -> AUTHORING
  └─ HUMAN_DECISION_REQUIRED -> WAITING_FOR_HUMAN -> AUTHORING
```

任一时刻都应明确当前状态、当前 revision、阻塞澄清和下一接收方。

## 角色与写入权限

| 角色 | 职责 | 可写内容 | 禁止事项 |
| --- | --- | --- | --- |
| Orchestrator | 调查、影响分析、门禁、路由、完成判断 | 阶段状态、handoff、治理记录 | 代替 Author 编写或代替 Reviewer 批准 |
| Author | 创建和修改产品规格 revision | 当前规格、Author handoff | 批准自己的 revision |
| Reviewer | 独立审阅固定 revision | ReviewRecord | 修改被审规格 |
| Human | 解决高影响产品取舍 | Clarification resolution、Decision | 无 |

Author 与 Reviewer 必须处于不同 agent context。最终 Reviewer 还必须未参与该 revision 的探索或汇总。

## 调查、对标与主动提案

先调查已有需求、决策、代码、测试、术语和研究资料。不要向人类询问仓库可以回答的问题，也不要把代码现状直接等同于产品意图。

在环境支持 subagent 且任务达到 `STANDARD` 及以上时进入 `DISPATCHING`，按 [多 Agent 自动派发协议](multi-agent-dispatch.md) 自动派发 2～4 个互补的只读探索角色。`SIMPLE` 任务不派发；`PROGRAM` 按能力域分波次，每波最多 4 个并发角色。

`PARALLEL_DISCOVERY` 中每个 subagent 只返回 `EXP-*`，不修改正式 PRD。进入 `SYNTHESIZING` 后由 Orchestrator 按证据等级统一术语、ID、缺口、方案和冲突；高影响分歧进入 Clarification，不用多数投票决定。默认最多两波，第二波只验证具体争议。

输入愿望化、需要创建新能力或缺少交互深度时，进入 `BENCHMARKING`：识别产品原型和用户任务，选择 2～4 个高相关知名产品或成熟范式，按依据等级记录 `BM-*`，提炼可迁移原则和不适用部分。

随后进入 `PROPOSING`：针对需求缺口生成 `PROP-*`，提供候选方案、推荐、取舍和影响范围。标杆只提供方案依据，不自动成为需求。

进入 `HUMAN_ALIGNMENT` 后，按意图与范围、标杆与方向、对象与流程、页面地图、边界与验收分阶段确认。每轮优先给出 3～5 个决策包，先展示 Agent 的候选方案，不要求人类从空白开始描述页面。小任务可以合并确认点，但不得把未经确认的高影响提案直接交给 Author。

当猜测可能改变范围、角色、权限、能力边界、对象生命周期、主流程、页面职责、业务规则、删除行为、金额、合规、外部承诺或验收结果时，创建阻塞 Clarification 并暂停受影响的最终规格。

每个问题只承载一个决定，每轮优先不超过五个最高影响问题。已知时提供选项、取舍、有证据的建议及影响实体。人类答案必须记录后才能继续。

低影响文案或非约束性视觉细节可以作为显式假设；高影响产品决定不可以。

## Orchestrator 到 Author 的 handoff

handoff 至少包含：

1. 模型、工作流、自动派发协议、主动扩写方法、质量门禁和适用的页面结构版本；
2. revision ID 与上一 revision；
3. `CREATE`、`PATCH` 或 `REWRITE`；
4. 当前模型快照或明确位置；
5. 变更实体、关系、文件和验收影响；
6. 派发档位、DispatchRecord、`EXP-*` 汇总和冲突处置；
7. 已确认事实及来源；
8. Benchmark 依据、等级、时效和可迁移原则；
9. `PROP-*` 的 `ACCEPTED`、`MODIFIED`、`REJECTED`、`DEFERRED` 状态；
10. 已解决 Clarification 和 Decision；
11. 允许保留的显式低影响假设；
12. 上一轮 required actions；
13. 目标文件和拆分约束。

存在开放阻塞 Clarification，或影响正式规格的 Proposal 尚未被人类接受或修改时，不得进入 `AUTHORING`。

## Author 到 Reviewer 的 handoff

Author 固定 revision 后输出 `READY_FOR_REVIEW`，并提供变更实体及文件、追踪变化、DispatchRecord、`EXP-*` 使用情况、Benchmark 与 Proposal 处置、证据与决策、假设、required actions 处理结果、页面结构检查、不变量检查、质量门禁自检和已知风险。

进入审阅后不得继续修改同一 revision。任何修复都创建新 revision。

## 审阅门禁

Reviewer 只审阅固定 revision。创建审阅 context 后，将 DispatchRecord 的 `reviewer_context` 从 `RESERVED_NEW_CONTEXT` 回填为实际标识并验证独立性，再输出 findings 与一个 verdict：

- `APPROVED`：无阻塞 finding 或 Clarification，允许结束产品阶段；
- `CHANGES_REQUESTED`：Author 可在现有产品意图下修复；
- `HUMAN_DECISION_REQUIRED`：继续工作前必须获得人类产品决定。

Reviewer 不修改 PRD。Orchestrator 不得把 required action 当作已完成修改。

## 返工与升级

`CHANGES_REQUESTED` 必须保留原 ReviewRecord，把所有 `BLOCK` 与已接受 `WARN` 交回 Author，创建 `rN+1` 并重新独立审阅。

`HUMAN_DECISION_REQUIRED` 必须将问题转成阻塞 Clarification，等待人类决定后再交回 Author。

默认最多三轮返工。同一阻塞问题连续三轮未解决时，停止自动循环并向人类报告证据、已尝试处理和剩余决定。

## 完成条件

产品阶段仅在以下条件全部满足时完成：

- 最新固定 revision 的 ReviewRecord 为 `APPROVED`；
- 没有影响该 revision 的开放阻塞 Clarification；
- 当前规格不依赖已废弃需求；
- 愿望式输入已经过适用的主动扩写和人类确认；
- Benchmark 有依据等级与时效说明，正式规格不含未确认 Proposal；
- DispatchRecord、ExplorationReport 和冲突处置完整，正式规格由单一 Author 写入；
- 模型不变量、追踪关系和适用的页面结构门禁通过；
- 优秀产品规格质量门禁的所有适用项均为 `PASS`；
- Author handoff、Clarification、Decision 和 ReviewRecord 已保存或明确交付。

重大变更应向人类展示批准的 revision 和审阅摘要后，再进入设计或实现。

`CREATE` 和 `REWRITE` 必须执行完整质量门禁。`PATCH` 只复核受影响门禁及其关系传播范围，但不得以局部修改为由绕过新出现的高影响产品决定。
