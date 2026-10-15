#!/usr/bin/env python3
"""Validate a system design interview prep directory before importing it into ExtraBrain.

Usage: python3 -I validate_prep.py <prep-directory>

Checks the company brief and the five problem files against references/problem-template.md.
Prints every problem found and exits 1 if any required content is missing.
"""

import re
import sys
from pathlib import Path

PROBLEM_SECTIONS = [
    "Why this fits",
    "Interview prompt",
    "Clarifying questions",
    "Requirements",
    "Scale estimation",
    "API design",
    "Data model and schema",
    "Storage choice",
    "High-level architecture",
    "Read/write path and consistency",
    "Caching",
    "Sharding, partitioning and replication",
    "Async processing, queues and fan-out",
    "Search and indexing",
    "Security, auth, rate limiting and abuse",
    "Reliability, monitoring and SLOs",
    "Deep dives",
    "Bottlenecks, trade-offs and evolution",
    "Company-specific twists",
    "Follow-up questions",
    "45-minute walkthrough",
    "Sources",
]

BRIEF_SECTIONS = [
    "What",
    "Scale",
    "Engineering signals",
    "Interview format",
    "The five practice problems",
    "Preparation plan",
    "Sources",
]

D2_RESERVED = {
    "index", "shape", "label", "style", "icon", "link", "tooltip", "near", "width", "height",
    "direction", "constraint", "class", "classes", "vars", "source", "target", "src", "dst",
}

MAX_BLOCK_CHARS = 1500
MAX_FILE_BYTES = 10 * 1024 * 1024


def split_sections(text):
    """Return [(heading, body)] for each `## ` heading."""
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def fenced_blocks(body, language=None):
    pattern = r"^```(\w*)[^\n]*\n(.*?)^```"
    return [code for lang, code in re.findall(pattern, body, flags=re.M | re.S)
            if language is None or lang == language]


def check_citations(name, text, errors):
    sections = dict(split_sections(text))
    sources = next((body for heading, body in sections.items()
                    if re.sub(r"^\d+\.\s*", "", heading).startswith("Sources")), "")
    defined = set(re.findall(r"^\s*-?\s*\[S(\d+)\]", sources, flags=re.M))
    if not re.search(r"https?://", sources):
        errors.append(f"{name}: Sources section has no URLs")
    body_text = text.replace(sources, "")
    for number in sorted(set(re.findall(r"\bS(\d+)\b", body_text)) - defined, key=int):
        errors.append(f"{name}: S{number} is cited but not listed in Sources")


def check_ordered_sections(name, text, required, errors, numbered):
    headings = [h for h, _ in split_sections(text)]
    titles = [re.sub(r"^\d+\.\s*", "", h) for h in headings]
    position = -1
    for index, section in enumerate(required, start=1):
        matches = [i for i, title in enumerate(titles) if title.startswith(section)]
        if not matches:
            errors.append(f"{name}: missing section '{section}'")
            continue
        found = matches[0]
        if found < position:
            errors.append(f"{name}: section '{section}' is out of order")
        position = found
        if numbered and not headings[found].startswith(f"{index}. "):
            errors.append(f"{name}: section '{section}' should be numbered '{index}.'")
    return dict(zip(titles, (b for _, b in split_sections(text))))


def section_body(sections, prefix):
    return next((body for title, body in sections.items() if title.startswith(prefix)), "")


def check_problem(path, company, errors):
    name = path.name
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    if not first.startswith(f"# {company}:"):
        errors.append(f"{name}: first line must be '# {company}: <Problem title>'")
    if "**Likelihood:**" not in text:
        errors.append(f"{name}: missing **Likelihood:** line")
    sections = check_ordered_sections(name, text, PROBLEM_SECTIONS, errors, numbered=True)
    for heading, _ in split_sections(text):
        if not re.search(r"\s-\s\S", heading):
            errors.append(f"{name}: heading '{heading}' must end with ' - <short problem name>'")

    for title, body in sections.items():
        if len(body.strip()) < 200 and not title.startswith("Sources"):
            errors.append(f"{name}: section '{title}' is too thin ({len(body.strip())} chars)")

    scale = section_body(sections, "Scale estimation")
    if not re.search(r"QPS|/s\b|per second", scale, flags=re.I) or not re.search(r"\d", scale):
        errors.append(f"{name}: Scale estimation needs QPS math with numbers")
    if not re.search(r"replicat", scale, flags=re.I):
        errors.append(f"{name}: Scale estimation needs raw and replicated storage")

    api = section_body(sections, "API design")
    if not re.search(r"^\|.*\|\s*$", api, flags=re.M):
        errors.append(f"{name}: API design needs an endpoint table")
    if not re.search(r"\b(GET|POST|PUT|PATCH|DELETE)\b", api):
        errors.append(f"{name}: API design needs HTTP methods or equivalent RPCs")
    if not fenced_blocks(api):
        errors.append(f"{name}: API design needs a fenced example request/response")
    if not re.search(r"idempoten", api, flags=re.I):
        errors.append(f"{name}: API design must state idempotency for writes")

    model = section_body(sections, "Data model and schema")
    if not fenced_blocks(model):
        errors.append(f"{name}: Data model needs a fenced DDL or key schema")
    if not re.search(r"primary key|partition key|\bPK\b", model, flags=re.I):
        errors.append(f"{name}: Data model must name primary/partition keys")
    if not re.search(r"index", model, flags=re.I):
        errors.append(f"{name}: Data model must describe indexes")

    architecture = section_body(sections, "High-level architecture")
    diagrams = fenced_blocks(architecture, "d2")
    if len(diagrams) != 1:
        errors.append(f"{name}: High-level architecture needs exactly one ```d2 diagram")
    for diagram in diagrams:
        if not re.search(r"^direction:\s*down\s*$", diagram, flags=re.M):
            errors.append(f"{name}: D2 diagram should set 'direction: down'")
        for line in diagram.splitlines():
            nodes = []
            if re.search(r"->|<-", line):
                edge, _, label = line.partition(":")
                if not label.strip():
                    errors.append(f"{name}: D2 edge without a label: '{line.strip()}'")
                nodes = re.split(r"<?->|<-", edge)
            else:
                # Top-level declarations only; nested `shape:`/`label:` attributes are valid.
                nodes = re.findall(r"^([A-Za-z_][\w]*)\s*:\s*\{", line)
            for node in nodes:
                node_id = node.strip().split(".")[0]
                if node_id in D2_RESERVED:
                    errors.append(f"{name}: D2 node ID '{node_id}' is a reserved word")
    if not re.search(r"^\s*1\.", architecture, flags=re.M):
        errors.append(f"{name}: High-level architecture needs numbered request flow steps")

    walkthrough = section_body(sections, "45-minute walkthrough")
    if len(re.findall(r"\d+\s*[–-]\s*\d+", walkthrough)) < 4:
        errors.append(f"{name}: 45-minute walkthrough needs timed phases")

    follow_ups = section_body(sections, "Follow-up questions")
    if len(re.findall(r"^\s*\d+\.", follow_ups, flags=re.M)) < 6:
        errors.append(f"{name}: Follow-up questions needs at least six numbered items")

    check_citations(name, text, errors)
    check_blocks(name, text, errors)


def check_blocks(name, text, errors):
    for block in re.split(r"\n\s*\n", text):
        if block.lstrip().startswith("```"):
            continue
        if len(block) > MAX_BLOCK_CHARS:
            errors.append(f"{name}: paragraph over {MAX_BLOCK_CHARS} chars starting "
                          f"'{block.strip()[:60]}...'; split it for retrieval")


def check_brief(path, company, errors):
    name = path.name
    text = path.read_text(encoding="utf-8")
    if not text.startswith(f"# {company}:"):
        errors.append(f"{name}: first line must be '# {company}: ...'")
    sections = check_ordered_sections(name, text, BRIEF_SECTIONS, errors, numbered=False)
    problems = section_body(sections, "The five practice problems")
    if len(re.findall(r"^\s*\d+\.", problems, flags=re.M)) != 5:
        errors.append(f"{name}: list exactly five numbered practice problems")
    check_citations(name, text, errors)


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    directory = Path(sys.argv[1])
    errors = []
    files = sorted(p for p in directory.iterdir() if p.is_file())
    briefs = [p for p in files if re.match(r"00-[a-z0-9-]+-company-brief\.md$", p.name)]
    problems = [p for p in files if re.match(r"0[1-5]-[a-z0-9-]+\.md$", p.name)]
    extra = [p.name for p in files if p not in briefs and p not in problems]
    if len(briefs) != 1:
        errors.append("expected one 00-<company-slug>-company-brief.md")
    if len(problems) != 5:
        errors.append(f"expected five problem files 01-05, found {len(problems)}")
    if extra:
        errors.append(f"unexpected files: {', '.join(extra)}")
    company = ""
    if briefs:
        first = briefs[0].read_text(encoding="utf-8").splitlines()[0]
        company = first[2:].split(":")[0].strip() if first.startswith("# ") else ""
        slug = briefs[0].name[3:-len("-company-brief.md")]
        for problem in problems:
            if not problem.name[3:].startswith(f"{slug}-"):
                errors.append(f"{problem.name}: file name must start with 0N-{slug}-")
        check_brief(briefs[0], company, errors)
    for path in files:
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{path.name}: larger than 10 MiB")
    for problem in problems:
        check_problem(problem, company, errors)

    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {company} brief and {len(problems)} problems are complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
