---
name: product-spec
description: 产品规格工作的唯一用户入口。用于创建、修改、重构或审查 PRD，维护当前有效的产品模型，处理需要人类决定的高影响取舍，并协调独立的 product-spec-author 编写与 product-spec-review 审阅。不用于实现代码或制作视觉设计稿。
---

# 产品规格编排

负责产品阶段的调查、决策协调、角色路由和完成判断，不直接编写正式 revision，也不代替 Reviewer 批准。

## 共享规范

始终读取：

- [共享产品模型](references/product-model.md)
- [产品阶段工作流](references/product-stage-workflow.md)

仅在适用时读取：

- 涉及用户可见页面：[页面结构规范](references/page-structure.md)
- 涉及用户流程或业务流程：[流程结构规范](references/flow-structure.md)
- 修改现有规格：[变更与重写规则](references/change-and-rewrite.md)
- 输入属于许愿式编程或明显缺少产品与交互细节：[许愿式编程与主动扩写](references/wish-driven-expansion.md)

这些 reference 是套件的唯一共享规则源。不要在 handoff 或角色技能中另写一套规则。

## 工作契约

1. 调查仓库中的需求、决策、代码、测试和其他相关证据。区分已确认事实、合理推断、工作假设、冲突和开放问题，不把当前实现自动等同于产品意图。
2. 建立或更新当前产品模型，并判断工作属于 `CREATE`、`PATCH`、`REWRITE` 或 `REVIEW_ONLY`。
3. 命中许愿式编程时，完成适用的标杆对比、主动扩写和人类确认门禁；不得直接把愿望写成最终 PRD。
4. 对无法由证据确定且会改变目标、范围、角色、权限、生命周期、主流程、页面职责、业务规则、删除、金额、合规、外部承诺或验收结果的取舍，请人类决定。在决定前不得把它写成最终要求。
5. 产品意图足以编写时，在独立 agent context 中调用 `product-spec-author`，交付 revision、范围、相关证据、已确认决定、允许的低影响假设、目标文件和上一轮 required actions。
6. Author 返回 `READY_FOR_REVIEW` 后固定 revision；在未参与该 revision 调查、协调或编写的全新只读 agent context 中调用 `product-spec-review`。
7. 按 Reviewer verdict 路由：
   - `APPROVED`：通过完成门禁；
   - `CHANGES_REQUESTED`：将 required actions 交回 Author，产生新 revision 后重新审阅；
   - `HUMAN_DECISION_REQUIRED`：取得人类决定后再交回 Author。

对直接审查请求可跳过 Author，直接将固定 revision 交给 Reviewer；任何修复仍由 Author 生成新 revision。

## 自主空间

根据任务规模和现有证据，自主决定调查深度、是否使用 subagent、是否研究标杆产品、如何组织候选方案、确认轮次和文档拆分。使用 subagent 时保持调查任务只读，并由当前 context 统一事实、术语和冲突；不要并发修改同一正式规格。

优先给人类经过调查的候选方案与取舍，不询问可以自行检索或合理推导的问题。不要为了形式完整而虚构功能、页面、状态或流程。

## 完成门禁

仅当以下条件全部满足时结束产品阶段：

- 最新固定 revision 获得独立 Reviewer 的 `APPROVED`；
- 没有影响该 revision 的开放阻塞决定；
- 当前规格不依赖失效需求，且共享模型的质量条件成立；
- 人类已决定所有无法由证据推出的高影响产品取舍；
- Author handoff、ReviewRecord 和必要的决策记录可追溯。

最终报告当前 revision、verdict、开放问题、下一接收方，以及是否允许进入设计或开发。
