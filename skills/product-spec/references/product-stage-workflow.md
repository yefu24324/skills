# 产品阶段工作流

工作流版本：`3.1`

## 角色权限

| 角色 | 职责 | 可写内容 | 禁止事项 |
| --- | --- | --- | --- |
| Orchestrator | 调查、产品协调、路由和完成判断 | 阶段记录、决定和 handoff | 编写正式 revision 或代替 Reviewer 批准 |
| Author | 创建或修改固定范围的产品规格 | 正式 revision 和 Author handoff | 批准自己的产物 |
| Reviewer | 独立审阅固定 revision | ReviewRecord | 修改被审规格 |
| Human | 决定证据无法推出的高影响产品取舍 | 决策结论 | 无 |

Author 与 Reviewer 必须使用不同 context。Reviewer 还必须未参与被审 revision 的调查和协调。

## 流程

```text
调查与产品协调
  -> 许愿式输入：标杆对比 -> 主动扩写 -> 人类确认
  -> 需要人类决定：等待决定
  -> Author 创建 revision
  -> Reviewer 独立审阅固定 revision
       -> APPROVED：产品阶段完成
       -> CHANGES_REQUESTED：Author 创建新 revision
       -> HUMAN_DECISION_REQUIRED：等待人类决定后由 Author 创建新 revision
```

Agent 根据任务自主决定调查、方案探索、人类确认和文档组织方式。任何探索产物都只是证据或候选方案，不能绕过人类决定、Author 单一写入和 Reviewer 独立审阅。

## 交接契约

Orchestrator 交给 Author 的信息应足以确定 revision、范围、当前规格、关键证据、人类决定、允许的低影响假设、目标文件和待处理 required actions。

Author 固定 revision 后，交给 Reviewer 的信息应足以确定审阅范围、实际变更、依据、决定、假设、自检结果和已知风险。审阅开始后不得继续修改同一 revision。

## Verdict 路由

- `APPROVED`：无阻塞问题，可结束产品阶段。
- `CHANGES_REQUESTED`：产品意图已足够，Author 可依据现有信息修复。
- `HUMAN_DECISION_REQUIRED`：存在必须由人类决定的产品取舍。

Reviewer 的 required action 不是已经完成的修改。任何修复都由 Author 产生新 revision 后重新独立审阅。

## 完成条件

只有最新固定 revision 获得独立 Reviewer 的 `APPROVED`，不存在开放阻塞决定，共享模型的质量条件成立，且必要的 handoff、产品决定与审阅记录可追溯时，产品阶段才完成。
