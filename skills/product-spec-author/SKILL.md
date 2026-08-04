---
name: product-spec-author
description: 基于统一产品模型创建和重构模块化产品规格。用于编写 AI 产品架构师维护的产品目标、角色、能力、业务对象、流程、页面、板块、操作、规则、状态和验收标准；特别适用于重大需求变化后的 REWRITE、单体 PRD 拆分和页面级产品设计说明。
---

# Product Spec Author

负责把需求转换为符合共享模型的当前产品规格。

## 必须先读取

开始工作前读取 [references/product-model.md](references/product-model.md)。

使用其中定义的实体、必填字段、稳定 ID、关系和不变量。不要使用另一套临时结构，也不要只写自然语言而不建立实体关系。

## 输入契约

优先接收：

- 当前模型实体和 ID
- 新需求或变更说明
- `PATCH` / `REWRITE` 初步判断
- 受影响实体和文件
- 已确认事实、假设和待确认项

缺少模型时，先从现有文档建立模型清单。

## 工作流程

### 1. 建立当前模型清单

列出已有：

- Product
- Role
- Capability
- Object
- Flow
- Page
- Section
- Action
- Rule
- State
- AcceptanceCriterion
- Decision

标记孤立实体、重复定义、缺失 ID 和相互矛盾的关系。

### 2. 分析变更

明确：

- 哪些实体新增、修改或删除
- 哪些关系发生变化
- 哪些文档受影响
- 变化属于 `PATCH` 还是 `REWRITE`

涉及角色、能力边界、主流程、对象生命周期、页面主要职责、权限、导航或系统边界时，优先 `REWRITE`。

禁止通过增加“补充说明”“特殊情况”“后来调整”等段落维护已经错误的结构。

### 3. 设计文档架构

推荐结构：

```text
docs/product/
├── index.md
├── features/<feature>/
├── objects/<object>.md
├── flows/<flow>.md
├── pages/<page>.md
├── shared/<topic>.md
└── decisions/<decision>.md
```

拆分原则：

- 一个页面一个页面规格。
- 一个跨页面或非可视流程一个流程规格。
- 一个共享规则只有一个权威定义。
- 总览只保留范围、能力地图、页面地图和追踪入口。
- 文档拥有不同目标、生命周期、读者或变化原因时应拆分。
- 不按固定行数机械拆分，也不把整个产品塞进一个文件。

### 4. 编写模型实体

每个实体必须满足共享模型的必填字段。

页面规格必须至少覆盖：

- `purpose`
- `roles`
- `entry_paths` 和 `exit_paths`
- `layout_structure`
- `sections`
- `page_states`
- `permissions`
- `rules`
- `acceptance_criteria`

每个 Section 必须说明位置、职责、内容、操作、局部状态和可见性规则。

每个 Action 必须说明前置条件、结果、反馈、失败行为、权限、规则和验收标准。

### 5. 维护关系和追踪

使用稳定 ID 引用相关实体，避免复制规则正文。

对非简单功能维护：

| Capability | Roles | Objects | Flows | Pages | Rules | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |

所有验收标准必须通过 `traces_to` 指向至少一个模型实体。

### 6. 重写当前版本

选择 `REWRITE` 时：

1. 保留仍然有效的事实和规则。
2. 重新组织受影响实体的完整当前描述。
3. 删除失效、重复和互相矛盾的文本。
4. 将历史原因移入 Decision。
5. 更新所有引用和追踪矩阵。

不要把新模型附加在旧模型后面。

### 7. 验证

逐项检查共享模型的十条不变量，尤其检查：

- 孤立页面和流程
- 重复或冲突规则
- 对象状态转换不一致
- 页面操作缺少反馈或失败行为
- 权限和角色矛盾
- 验收标准不可测试
- 当前文档仍引用已废弃需求

## 输出契约

完成时返回：

1. 模型版本。
2. `PATCH` 或 `REWRITE`。
3. 新增、修改、删除的实体 ID。
4. 关系变化和影响范围。
5. 新的文档目录和更新文件。
6. 追踪矩阵变化。
7. 假设与待确认项。
8. 不变量检查结果。
