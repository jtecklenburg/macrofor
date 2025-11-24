"""Create a structured API_SPEC from the raw extracted API_SPEC.md.

This script looks for '### Snippet' sections and code fences, then
generates `docs/API_SPEC_structured.md` with candidate name/type and
TODO placeholders for manual verification.
"""
import re
import sys
from pathlib import Path


def parse_snippets(md_text: str):
    parts = re.split(r"^###\s+Snippet\s+\d+\s*$", md_text, flags=re.MULTILINE)
    # first part is header; subsequent parts are snippet blocks
    snippets = []
    for p in parts[1:]:
        # find code fence
        m = re.search(r"```\n(.*?)\n```", p, flags=re.DOTALL)
        content = m.group(1).strip() if m else p.strip().splitlines()[0][:200]
        snippets.append(content)
    return snippets


def guess_type_and_name(snippet: str):
    s = snippet
    # common patterns
    m = re.search(r"subroutine\s+([\w_]+)", s, flags=re.IGNORECASE)
    if m:
        return "subroutine", m.group(1)
    m = re.search(r"function\s+([\w_]+)", s, flags=re.IGNORECASE)
    if m:
        return "function", m.group(1)
    m = re.search(r"module\s+([\w_]+)", s, flags=re.IGNORECASE)
    if m:
        return "module", m.group(1)
    # MAPLE/MACROFORT style lists: [subroutinef, name, list]
    m = re.search(r"\[\s*(subroutinef|functionf|functionm|subroutinem)\s*,\s*([\w_]+)", s, flags=re.IGNORECASE)
    if m:
        t = m.group(1).lower()
        if 'subroutine' in t:
            return 'subroutine', m.group(2)
        return 'function', m.group(2)
    # fallback: look for words like 'call name' or 'call name (list)'
    m = re.search(r"call\s+([\w_]+)", s, flags=re.IGNORECASE)
    if m:
        return 'call', m.group(1)
    # default unknown
    return 'unknown', None


def generate_structured(snippets, src_path: Path):
    lines = []
    lines.append("# Structured API_SPEC (generated)")
    lines.append(f"_Source: {src_path}\n")
    for i, snip in enumerate(snippets, 1):
        typ, name = guess_type_and_name(snip)
        header = f"## Entry {i}: {name or '<unknown>'}"
        lines.append(header)
        lines.append(f"- **Detected Type:** {typ}")
        if name:
            lines.append(f"- **Detected Name:** `{name}`")
        lines.append("- **Original Snippet:**")
        lines.append('```text')
        lines.append(snip)
        lines.append('```')
        lines.append("- **TODO:** Verify signature, parameters, behavior; normalize OCR artifacts.")
        lines.append("")
    return "\n".join(lines)


def main(argv):
    if len(argv) != 2:
        print("Usage: python tools\\structure_api_spec.py <path-to-API_SPEC.md>")
        return 2
    mdp = Path(argv[1])
    if not mdp.exists():
        print('File not found:', mdp)
        return 2
    txt = mdp.read_text(encoding='utf-8')
    snippets = parse_snippets(txt)
    out = generate_structured(snippets, mdp)
    outp = mdp.parent / 'API_SPEC_structured.md'
    outp.write_text(out, encoding='utf-8')
    print('Wrote', outp)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
