---
name: git-push-feature
description: 将当前 Git HEAD 推送到以 Git 用户名命名的远程 feature 分支，确认远程同名分支不存在后，让用户选择合并目标并打开 Gitea compare/MR 创建页面。用于用户要求推送个人 feature 分支、按 Git user.name 发布临时合并分支、打开 Gitea 合并请求页面或复用原 git-push-feature 命令时；不覆盖已有远程分支、不 force push、不自动创建或提交 MR。
---

# 推送个人 Feature 分支

把当前已提交的 HEAD 发布为新的个人远程分支，然后打开 Gitea 对比页面。远程分支已存在时必须停止；本流程没有覆盖模式。

## 1. 检查本地状态

1. 使用 `git rev-parse --show-toplevel` 和 `git rev-parse --verify HEAD` 确认仓库及有效提交。
2. 默认使用 `origin`。若不存在，让用户从实际远程列表中明确选择。
3. 读取当前分支、`git status --short --branch`、upstream、`git config --get user.name` 和 `git remote get-url <remote>`。
4. 如果 Git 用户名为空，停止并提示用户设置仓库级或全局 `user.name`；不要替用户写入配置。
5. 目标分支为 `feature/<username>`。使用 `git check-ref-format --branch` 验证完整名称；用户名不能直接形成合法分支时，让用户提供合法后缀，不要静默改写身份。
6. 如果没有 upstream，停止并让用户确认应以哪个远程分支作为当前工作的基线。
7. 确认 HEAD 相对 upstream 至少有一个未推送提交，并展示这些提交的简短列表。若没有，停止而不是创建无实际变更的 feature 分支。
8. 如果存在暂存、未暂存或未跟踪内容，明确说明它们不会被推送，并在推送前请求用户确认是否仍继续。

不要自动提交、暂存或修改本地文件。

## 2. 确认远程分支不存在

使用精确引用查询：

```bash
git ls-remote --heads <remote> refs/heads/feature/<username>
```

返回同名引用时立即停止，告知用户远程分支已存在。不要执行 force push、`--force-with-lease`、删除远程分支或覆盖操作，也不要仅凭本地远程跟踪引用判断远端不存在。

## 3. 推送当前 HEAD

执行：

```bash
git push <remote> HEAD:refs/heads/feature/<username>
```

不添加 `--force`，也不默认使用 `-u` 改写当前本地分支的 upstream。推送失败时概括原始错误并停止，不继续构造“成功”页面。

推送成功后报告远程名、源提交哈希和新分支全名。

## 4. 选择合并目标

重新读取远程 heads，排除刚推送的源分支。若用户尚未指定合并目标，让用户从真实分支中选择，并按以下优先级展示候选项：

1. 当前分支原 upstream；
2. `develop`；
3. `main`；
4. `release/*`；
5. `master`；
6. `hotfix/*`；
7. `feature/*`；
8. 其他分支。

验证目标分支确实存在且不等于源分支。不要自动选择第一个候选项。

## 5. 构造并打开 Gitea 页面

从 `git remote get-url <remote>` 动态解析仓库网页基础地址：

- `https://host/owner/repo.git` 转为 `https://host/owner/repo`；
- `git@host:owner/repo.git` 转为 `https://host/owner/repo`；
- `ssh://git@host/owner/repo.git` 可在主机和网页协议明确时转为 HTTPS。

移除末尾 `.git`，但不要硬编码主机、组织或仓库名。遇到自定义 SSH 端口、非 HTTP(S) 远程、无法确定网页端口或非 Gitea 地址时，不要猜测；报告已推送分支并请用户提供网页基础地址。

按下列格式构造 compare 页面：

```text
<repo-web-url>/compare/<target>...feature/<username>
```

对来自用户或 Git 的路径部分进行 URL 安全编码，且保持 Gitea 所需的分支斜杠语义。优先使用环境提供的浏览器打开能力；否则在 Windows 使用 `Start-Process <url>`，macOS 使用 `open <url>`，Linux 使用 `xdg-open <url>`。打开失败时直接返回完整可复制 URL。

只打开创建页面，不自动填写、提交或发送合并请求。最终报告源分支、目标分支和 compare URL。
