---
name: git-rebase-pull
description: 获取 Git 远程更新，选择一个远程目标分支，并把当前分支 rebase 到该分支最新提交之上以保持线性历史。用于用户要求 pull --rebase、rebase 拉取 develop/main/release、同步远程后重放本地提交或复用原 git-rebase-pull 命令时；遇到未提交改动、detached HEAD、缺少远程或 rebase 冲突时安全暂停，不自动 stash、abort、skip 或解决冲突。
---

# 使用 Rebase 拉取远程更新

此流程的准确语义是：先获取远程引用，再执行 `git rebase <remote>/<target>`，把当前分支的本地提交重放到用户选择的远程目标分支之上。不要在选择目标后执行含义不明确的无参数 `git pull --rebase`。

## 1. 执行前检查

1. 使用 `git rev-parse --show-toplevel` 确认仓库。
2. 读取当前分支、`git status --short --branch`、远程列表和当前 upstream。
3. 如果处于 detached HEAD、已有 merge/rebase/cherry-pick 操作，或工作区/暂存区存在未提交改动，停止并解释状态。
4. 不要自动 stash、提交、清理或丢弃改动。
5. 默认使用 `origin`；如果不存在 `origin`，根据仓库远程列表让用户明确选择，不能猜测。

## 2. 获取并选择目标分支

1. 执行 `git fetch <remote>`。获取失败时报告错误并停止。
2. 从远程跟踪引用或 `git ls-remote --heads <remote>` 获取真实分支列表，排除远程 HEAD 符号引用。
3. 如果用户已经明确指定目标分支，验证 `<remote>/<target>` 存在后使用它。
4. 如果用户没有指定，让用户选择目标分支。建议候选项时按以下优先级排列：当前 upstream、`develop`、`main`、`release/*`、`master`、`hotfix/*`、`feature/*`，然后是其他分支。
5. 不要把“最可能的分支”当作用户已经作出的选择。

目标分支名称必须来自远程实际结果或用户明确输入，不得把远程输出拼接成未经校验的额外 shell 命令。

## 3. 执行 Rebase

在执行前简要报告：当前分支、目标 `<remote>/<target>`、当前分支相对目标的本地提交数量，以及将被重放的提交摘要。随后执行：

```bash
git rebase <remote>/<target>
```

用户明确选择目标分支或原始请求中已指定目标分支，即视为授权本次 rebase。不要附加 `--autostash`、`--onto`、`--interactive` 或其他会改变约定语义的参数，除非用户明确要求。

## 4. 处理冲突或失败

发生冲突时：

1. 读取 `git status --short`、冲突文件列表和 Git 当前提示。
2. 报告 rebase 已暂停、已完成到哪一步以及哪些文件冲突。
3. 不要自动编辑冲突、执行 `git add`、`git rebase --continue`、`--skip` 或 `--abort`。
4. 等待用户决定是手动解决后继续，还是中止 rebase 后改用 merge。用户选择改用 merge 时，也必须先获得其对 `git rebase --abort` 的明确授权。

非冲突失败同样保留现场并报告，不用 reset 或 checkout 恢复。

## 5. 验证结果

成功后显示简短的 `git status --short --branch` 和最近几条带拓扑的日志，例如：

```bash
git log --oneline --decorate --graph -10
```

确认当前分支已经基于所选远程提交，并报告是否仍领先或落后。不要自动 push；若后续推送需要 force，单独解释原因并取得明确授权，本 skill 内绝不执行 force push。
