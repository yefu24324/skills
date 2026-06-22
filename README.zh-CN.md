# Personal Codex Skills

语言：[English](README.md) | **中文**

这个仓库用于维护个人 Codex skills。每个 skill 是一个独立目录，包含必需的 `SKILL.md`，以及可选的 `agents/`、`scripts/`、`references/`、`assets/` 等资源。

## 目录结构

```text
skills/
  uutils-coreutils/
    SKILL.md
    agents/
      openai.yaml
```

新增个人技能时，建议放在 `skills/<skill-name>/` 下，并保持 skill 名称为小写字母、数字和连字符。

## 已包含技能

- `uutils-coreutils`：在 Windows 上编写或执行常见 shell/file/text 命令时，优先使用 uutils/coreutils 及相关 POSIX 风格工具，减少 PowerShell 专有写法。

## 使用 `npx skills` 安装

交互式安装仓库中的可用技能：

```bash
npx skills add https://github.com/yefu24324/skills
```

安装指定技能：

```bash
npx skills add https://github.com/yefu24324/skills --skill uutils-coreutils
```

安装完成后，重启你的 agent 以加载新技能。

## 维护约定

- 每个 skill 目录只放 agent 使用该技能所需的内容；仓库说明、安装说明和发布说明放在仓库根目录。
- `SKILL.md` frontmatter 只保留 `name` 和 `description`，以提高兼容性。
- 修改 skill 后，尽量在新会话中用真实任务验证触发条件和执行效果。
