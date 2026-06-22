---
name: uutils-coreutils
description: 在 Windows 主机上编写或执行 shell、文件操作、文本处理、目录遍历、构建清理、跨平台脚本和一行命令时，优先使用 uutils/coreutils 及相关 POSIX 风格工具替代 PowerShell 专有 cmdlet。适用于需要 ls、cp、mv、rm、cat、pwd、mkdir、touch、tee、sleep、sha256sum、sort、uniq、wc、head、tail 等 GNU/coreutils 兼容命令，或需要在 Linux、macOS、Windows 间保持命令习惯一致的任务。
---

# uutils Coreutils

## Core Rule

On Windows, prefer POSIX-style utilities from `uutils/coreutils` for common file, directory, and text operations instead of writing PowerShell-specific cmdlets.

Use PowerShell only when the task is genuinely Windows-specific, such as registry edits, COM/WMI, services, certificates, ACL management, or other Windows administration.

## Command Mapping

Prefer these command forms when the utility is available on `PATH`:

| Task | Prefer | Avoid |
| --- | --- | --- |
| List files | `ls -la` | `Get-ChildItem`, `dir` |
| Copy files/directories | `cp -r src dst` | `Copy-Item -Recurse` |
| Move/rename | `mv old new` | `Move-Item` |
| Remove a file | `rm file` | `Remove-Item` |
| Remove a directory tree | `rm -rf dir` | `Remove-Item -Recurse -Force` |
| Print working directory | `pwd` | `Get-Location` |
| Make directories | `mkdir -p a/b/c` | `New-Item -ItemType Directory` |
| Read files | `cat file` | `Get-Content` |
| Write pipeline output | `cat a b \| tee out` | Multi-step PowerShell output code |
| Delay | `sleep 2` | `Start-Sleep -Seconds 2` |
| Checksums | `sha256sum file` | `Get-FileHash` |
| Sort lines | `sort file` | `Sort-Object` |
| Unique adjacent lines | `uniq` | `Select-Object -Unique` |
| Count lines/words/bytes | `wc -l file` | `(Get-Content file).Count` |
| Show file prefix/suffix | `head -n 20 f`, `tail -f f` | `Select-Object -First`, `Select-Object -Last` |

For repository-wide code search, prefer `rg` when it is available because it is usually faster and respects ignore files. Use `grep` when POSIX portability or GNU-compatible behavior is the priority.

## Tool Scope

Distinguish the uutils ecosystem from plain `uutils/coreutils`:

- `uutils/coreutils` covers core utilities such as `ls`, `cp`, `mv`, `rm`, `cat`, `mkdir`, `touch`, `tee`, `sleep`, `sort`, `uniq`, `wc`, `head`, and `tail`.
- `find`, `xargs`, and similar commands come from findutils-compatible packages, not plain coreutils.
- `grep` is not part of GNU coreutils. Use a compatible `grep` package, Git for Windows/MSYS tooling, ripgrep for code search, or a Windows bundle that explicitly includes `grep`.

If a command is unavailable or resolves to a Windows built-in with different behavior, check resolution first:

```bash
where.exe ls
where.exe grep
```

Use the full executable path or adjust `PATH` when a PowerShell alias or Windows executable shadows the intended tool.

## Safety

Before running destructive recursive operations such as `rm -rf` or broad `mv`, resolve and inspect the target path. Keep deletion and move commands scoped to the intended workspace or explicitly named target directory.

Do not use POSIX commands for Windows-only management operations where PowerShell provides the correct system API.

## Shell Syntax

Remember that uutils replaces utilities, not the shell language:

- In Bash, zsh, and `.sh` scripts, use POSIX shell syntax such as `$VAR`, command substitution, and shebangs.
- In PowerShell, environment variable expansion is still PowerShell syntax, for example `$env:VAR`.
- A script with `#!/usr/bin/env bash` still requires Bash on Windows; uutils alone does not provide a Bash interpreter.

For cross-platform automation, prefer simple external command pipelines and avoid shell-specific constructs unless the target shell is explicit.

## Installation Assumption

Assume the user has installed uutils/coreutils or a compatible Windows package that exposes the required commands on `PATH`.

Common installation options include:

```bash
scoop install uutils-coreutils
```

Some Windows bundles based on uutils may include additional tools such as `grep`, `find`, and `xargs`; verify the installed package before relying on those commands.

## Examples

PowerShell-specific form to avoid:

```powershell
Get-ChildItem -Recurse -Filter "*.log" | Remove-Item -Force
(Get-Content .\README.md | Select-String "TODO").Count
```

POSIX-style form:

```bash
find . -name "*.log" -delete
grep -c "TODO" README.md
```

Cross-platform cleanup script when Bash and the needed utilities are available:

```bash
#!/usr/bin/env bash
set -euo pipefail

find . \( -name "bin" -o -name "obj" \) -type d -prune -exec rm -rf {} +
find . -name "*.tmp" -type f -delete
echo "cleanup complete"
```

## References

- uutils project: https://uutils.github.io/
- uutils/coreutils: https://github.com/uutils/coreutils
- GNU Coreutils manual: https://www.gnu.org/software/coreutils/manual/
