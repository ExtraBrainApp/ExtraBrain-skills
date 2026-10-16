#!/usr/bin/env python3
"""Validate an interview prep directory before importing it into ExtraBrain.

Usage: python3 -I validate_prep.py <prep-directory>

Checks the interview brief and the topic files against the completion checklist in
references/file-formats.md. Keep the two in sync.
Prints every problem found and exits 1 if any required content is missing.
"""

import re
import sys
from pathlib import Path

BRIEF_SECTIONS = [
    "The interview",
    "What they will assess",
    "Research summary",
    "Preparation files",
    "Preparation plan",
    "Questions to ask them",
    "Sources",
]

# Required `##` heading prefixes per kind, in order. Extra sections may sit between them.
KIND_SECTIONS = {
    "questions": ["Why it matters", "Q1.", "Common mistakes", "Sources"],
    "concepts": ["Why it matters", "Core concepts", "Worked examples", "Common mistakes",
                 "Likely questions", "Sources"],
    "stories": ["Why it matters", "Competency map", "Story 1.", "Likely questions", "Sources"],
    "case": ["Why it matters", "Prompt", "Clarifying questions", "Approach", "Model answer",
             "Trade-offs and alternatives", "Follow-ups", "Timed walkthrough", "Sources"],
    "cheatsheet": ["Why it matters", "Quick reference", "Likely questions", "Sources"],
}

MIN_TOPIC_FILES = 3
MAX_TOPIC_FILES = 12
MIN_SECTION_CHARS = 150
MAX_BLOCK_CHARS = 1500
MAX_FILE_BYTES = 10 * 1024 * 1024


def split_sections(text):
    """Return [(heading, body)] for each `## ` heading."""
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def section_body(sections, prefix):
    return next((body for title, body in sections if title.startswith(prefix)), "")


def numbered_items(body):
    return len(re.findall(r"^\s*\d+\.\s", body, flags=re.M))


def check_ordered_sections(name, sections, required, errors):
    titles = [title for title, _ in sections]
    position = -1
    for section in required:
        matches = [i for i, title in enumerate(titles) if title.startswith(section)]
        if not matches:
            errors.append(f"{name}: missing section '{section}'")
            continue
        if matches[0] < position:
            errors.append(f"{name}: section '{section}' is out of order")
        position = matches[0]
    if titles and not titles[-1].startswith("Sources"):
        errors.append(f"{name}: Sources must be the last section")


def check_citations(name, text, errors):
    sources = section_body(split_sections(text), "Sources")
    defined = set(re.findall(r"^\s*(?:[-*]|\d+\.)?\s*\[S(\d+)\]", sources, flags=re.M))
    if not re.search(r"https?://|User-provided material", sources):
        errors.append(f"{name}: Sources needs URLs or the line 'User-provided material'")
    body_text = text.replace(sources, "")
    for number in sorted(set(re.findall(r"\[S(\d+)\]", body_text)) - defined, key=int):
        errors.append(f"{name}: [S{number}] is cited but not listed in Sources")


def check_blocks(name, text, errors):
    for block in re.split(r"\n\s*\n", text):
        if block.lstrip().startswith("```"):
            continue
        if len(block) > MAX_BLOCK_CHARS:
            errors.append(f"{name}: paragraph over {MAX_BLOCK_CHARS} chars starting "
                          f"'{block.strip()[:60]}...'; split it for retrieval")


def check_kind(name, kind, sections, errors):
    if kind == "questions":
        questions = [(t, b) for t, b in sections if re.match(r"Q\d+\.", t)]
        if len(questions) < 8:
            errors.append(f"{name}: needs at least eight 'Q<n>.' question sections")
        for title, body in questions:
            if "Model answer" not in body:
                errors.append(f"{name}: '{title}' needs a Model answer")
    elif kind == "stories":
        stories = [(t, b) for t, b in sections if re.match(r"Story \d+\.", t)]
        if len(stories) < 3:
            errors.append(f"{name}: needs at least three 'Story <n>.' sections")
        for title, body in stories:
            for part in ("Situation", "Action", "Result"):
                if part not in body:
                    errors.append(f"{name}: '{title}' needs a {part}")
        if not re.search(r"^\|.*\|\s*$", section_body(sections, "Competency map"), flags=re.M):
            errors.append(f"{name}: Competency map needs a table")
    elif kind == "case":
        if numbered_items(section_body(sections, "Follow-ups")) < 5:
            errors.append(f"{name}: Follow-ups needs at least five numbered items")
        walkthrough = section_body(sections, "Timed walkthrough")
        if len(re.findall(r"\d+\s*[–-]\s*\d+", walkthrough)) < 3:
            errors.append(f"{name}: Timed walkthrough needs at least three timed phases")
    elif kind == "cheatsheet":
        reference = section_body(sections, "Quick reference")
        if not re.search(r"^\s*(\|.*\||[-*]\s|\d+\.\s)", reference, flags=re.M):
            errors.append(f"{name}: Quick reference needs a table or list")
    if kind in ("concepts", "stories", "cheatsheet"):
        if numbered_items(section_body(sections, "Likely questions")) < 6:
            errors.append(f"{name}: Likely questions needs at least six numbered items")


def check_topic(path, title, errors):
    name = path.name
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    if not first.startswith(f"# {title}:"):
        errors.append(f"{name}: first line must be '# {title}: <Topic title>'")
    header = text.split("\n## ", 1)[0]
    match = re.search(r"^\*\*Kind:\*\*\s*`?(\w+)", header, flags=re.M)
    kind = match.group(1) if match else ""
    if kind not in KIND_SECTIONS:
        errors.append(f"{name}: needs a '**Kind:**' line naming one of "
                      f"{', '.join(KIND_SECTIONS)}")
    sections = split_sections(text)
    if kind in KIND_SECTIONS:
        check_ordered_sections(name, sections, KIND_SECTIONS[kind], errors)
        check_kind(name, kind, sections, errors)
    for heading, body in sections:
        if not re.search(r"\s-\s\S", heading):
            errors.append(f"{name}: heading '{heading}' must end with ' - <short topic name>'")
        if len(body.strip()) < MIN_SECTION_CHARS and not heading.startswith("Sources"):
            errors.append(f"{name}: section '{heading}' is too thin ({len(body.strip())} chars)")
    check_citations(name, text, errors)
    check_blocks(name, text, errors)


def check_brief(path, topic_count, errors):
    name = path.name
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    match = re.match(r"# (.+?): Interview brief\s*$", first)
    if not match:
        errors.append(f"{name}: first line must be '# <Interview title>: Interview brief'")
    sections = split_sections(text)
    check_ordered_sections(name, sections, BRIEF_SECTIONS, errors)
    listed = numbered_items(section_body(sections, "Preparation files"))
    if listed != topic_count:
        errors.append(f"{name}: Preparation files lists {listed} files, "
                      f"but there are {topic_count} topic files")
    if numbered_items(section_body(sections, "Questions to ask them")) < 3:
        errors.append(f"{name}: Questions to ask them needs at least three numbered items")
    check_citations(name, text, errors)
    check_blocks(name, text, errors)
    return match.group(1).strip() if match else ""


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"FAIL: {directory} is not a directory")
        return 1
    errors = []
    files = sorted(p for p in directory.iterdir() if p.is_file())
    briefs = [p for p in files if re.fullmatch(r"00-[a-z0-9-]+-brief\.md", p.name)]
    slug = briefs[0].name[3:-len("-brief.md")] if len(briefs) == 1 else ""
    topics = [p for p in files if re.fullmatch(r"(?!00)\d\d-[a-z0-9-]+\.md", p.name)]
    extra = [p.name for p in files if p not in briefs and p not in topics]

    if len(briefs) != 1:
        errors.append("expected exactly one 00-<interview-slug>-brief.md")
    if not MIN_TOPIC_FILES <= len(topics) <= MAX_TOPIC_FILES:
        errors.append(f"expected {MIN_TOPIC_FILES} to {MAX_TOPIC_FILES} topic files, "
                      f"found {len(topics)}")
    numbers = [int(p.name[:2]) for p in topics]
    if numbers != list(range(1, len(topics) + 1)):
        errors.append("topic files must be numbered 01, 02, ... without gaps or duplicates")
    if extra:
        errors.append(f"unexpected files: {', '.join(extra)}")
    for path in files:
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{path.name}: larger than 10 MiB")

    title = check_brief(briefs[0], len(topics), errors) if len(briefs) == 1 else ""
    for topic in topics:
        if slug and not topic.name[3:].startswith(f"{slug}-"):
            errors.append(f"{topic.name}: file name must start with NN-{slug}-")
        check_topic(topic, title, errors)

    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {title} brief and {len(topics)} topic files are complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
