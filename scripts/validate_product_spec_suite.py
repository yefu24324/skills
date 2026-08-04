#!/usr/bin/env python3
"""校验 product-spec 三技能套件的结构、引用与中文参考资料。"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SUITE = ("product-spec", "product-spec-author", "product-spec-review")
REFERENCE_ROOT = SKILLS_ROOT / "product-spec" / "references"
REQUIRED_REFERENCES = {
    "product-model.md": r"^模型版本：`([^`]+)`$",
    "product-stage-workflow.md": r"^工作流版本：`([^`]+)`$",
    "page-structure.md": r"^规范版本：`([^`]+)`$",
    "flow-structure.md": r"^规范版本：`([^`]+)`$",
    "change-and-rewrite.md": r"^规则版本：`([^`]+)`$",
    "wish-driven-expansion.md": r"^方法版本：`([^`]+)`$",
}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)")
HAN_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
ENGLISH_ONLY_HEADING = re.compile(r"^#{1,6}\s+[A-Za-z][A-Za-z0-9 /&_-]*\s*$")
LEGACY_ENGLISH_MARKERS = (
    "Model version:",
    "Workflow version:",
    "Standard version:",
    "## Purpose",
    "## Roles",
    "## Review rules",
)

# 这些片段共同构成人类可读页面规格的最低契约，防止规范退回内部代号驱动的旧格式。
HUMAN_READABLE_CONTRACT = {
    "page-structure.md": (
        "[PascalCaseComponent] <中文用途>",
        "[Input] <按名称搜索工作项>",
        "页面用途",
        "主要任务",
        "操作结果",
        "状态与恢复",
        "不在正式需求正文、组件树或功能说明中生成",
    ),
    "flow-structure.md": (
        "节点显示文本全部使用清楚、自然的中文",
        "流程目的",
        "异常恢复",
        "不添加 `FLOW-*`、`PAGE-*`、`ACT-*`、`RULE-*`、`STATE-*`",
    ),
}

# Author 和 Reviewer 都必须执行可读性门禁，不能只由共享参考资料单方面声明。
ROLE_READABILITY_CONTRACT = {
    "product-spec-author": (
        "[大驼峰英文组件] <中文用途>",
        "不得生成 `CAP-*`、`PAGE-*`、`SEC-*`、`ACT-*`、`RULE-*`",
    ),
    "product-spec-review": (
        "[大驼峰英文组件] <中文用途>",
        "需要读者自行解码的内部代号",
    ),
}


def report_error(message: str) -> None:
    print(f"错误：{message}", file=sys.stderr)


def validate_skill_structure() -> bool:
    valid = True
    for name in SUITE:
        skill_root = SKILLS_ROOT / name
        for relative in ("SKILL.md", "agents/openai.yaml"):
            path = skill_root / relative
            if not path.is_file():
                report_error(f"缺少 {path.relative_to(ROOT)}")
                valid = False

    for name in ("product-spec-author", "product-spec-review"):
        duplicate_dir = SKILLS_ROOT / name / "references"
        duplicates = sorted(duplicate_dir.glob("*.md")) if duplicate_dir.exists() else []
        for path in duplicates:
            report_error(f"共享 reference 不应复制到 {path.relative_to(ROOT)}")
            valid = False

    return valid


def validate_references() -> bool:
    valid = True
    actual = {path.name for path in REFERENCE_ROOT.glob("*.md")}
    expected = set(REQUIRED_REFERENCES)

    for name in sorted(expected - actual):
        report_error(f"缺少 references/{name}")
        valid = False
    for name in sorted(actual - expected):
        report_error(f"发现未登记的 references/{name}")
        valid = False

    for name, version_pattern in REQUIRED_REFERENCES.items():
        path = REFERENCE_ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")

        if not HAN_PATTERN.search(text):
            report_error(f"{path.relative_to(ROOT)} 不包含中文内容")
            valid = False
        for line_number, line in enumerate(text.splitlines(), start=1):
            if ENGLISH_ONLY_HEADING.fullmatch(line):
                report_error(
                    f"{path.relative_to(ROOT)}:{line_number} 存在纯英文标题：{line}"
                )
                valid = False
        for marker in LEGACY_ENGLISH_MARKERS:
            if marker in text:
                report_error(f"{path.relative_to(ROOT)} 残留英文规范标记：{marker}")
                valid = False

        if version_pattern:
            match = re.search(version_pattern, text, re.MULTILINE)
            if not match:
                report_error(f"{path.relative_to(ROOT)} 缺少中文版本声明")
                valid = False
            else:
                print(f"通过：{path.relative_to(ROOT)} 版本 {match.group(1)}")
        else:
            print(f"通过：{path.relative_to(ROOT)}")

    return valid


def validate_markdown_links() -> bool:
    valid = True
    files = [SKILLS_ROOT / name / "SKILL.md" for name in SUITE]
    files.extend(sorted(REFERENCE_ROOT.glob("*.md")))

    for source in files:
        text = source.read_text(encoding="utf-8")
        for target_text in LINK_PATTERN.findall(text):
            target = (source.parent / target_text).resolve()
            if not target.is_file():
                report_error(
                    f"{source.relative_to(ROOT)} 引用了不存在的 {target_text}"
                )
                valid = False
    if valid:
        print("通过：所有 Markdown reference 链接均有效")
    return valid


def validate_human_readable_contract() -> bool:
    """校验组件树格式、自然中文正文和角色门禁没有在后续修改中丢失。"""

    valid = True

    for name, required_fragments in HUMAN_READABLE_CONTRACT.items():
        path = REFERENCE_ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                report_error(
                    f"{path.relative_to(ROOT)} 缺少人类可读契约：{fragment}"
                )
                valid = False

    for skill_name, required_fragments in ROLE_READABILITY_CONTRACT.items():
        path = SKILLS_ROOT / skill_name / "SKILL.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                report_error(
                    f"{path.relative_to(ROOT)} 缺少人类可读门禁：{fragment}"
                )
                valid = False

    if valid:
        print("通过：页面与流程的人类可读契约完整")
    return valid


def main() -> int:
    checks = (
        validate_skill_structure(),
        validate_references(),
        validate_markdown_links(),
        validate_human_readable_contract(),
    )
    if all(checks):
        print("product-spec 三技能套件校验通过")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
