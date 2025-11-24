"""Simple heuristic parser to extract code-like snippets and API signatures
from a plain text PDF extraction and produce a starter API_SPEC.md and test file.

Usage:
    python tools\parse_api_from_text.py <input-txt> <out-api-spec-md> <out-test-py>
"""
import re
import sys
from pathlib import Path


def is_code_like(line: str) -> bool:
    line = line.rstrip()
    if not line:
        return False
    # lines starting with at least 2 spaces (indented code) or typical keywords
    if line.startswith('  ') or line.startswith('\t'):
        return True
    keywords = ['subroutine', 'function', 'module', 'end subroutine', 'end function', 'end module', 'macro', '@']
    if any(k in line.lower() for k in keywords):
        return True
    # lines that look like signatures: name(arg, arg2)
    if re.search(r"\w+\s*\([^)]*\)\s*(:=|->|:)?", line):
        return True
    return False


def extract_snippets(text: str):
    lines = text.splitlines()
    snippets = []
    cur = []
    for ln in lines:
        if is_code_like(ln):
            cur.append(ln.rstrip())
        else:
            if cur:
                snippets.append('\n'.join(cur))
                cur = []
    if cur:
        snippets.append('\n'.join(cur))
    # deduplicate
    seen = set()
    out = []
    for s in snippets:
        if s not in seen and len(s.splitlines()) > 0:
            seen.add(s)
            out.append(s)
    return out


def make_api_spec(snippets, src_txt: Path):
    parts = []
    parts.append('# API specification (automatically extracted)')
    parts.append('\n_Source text:_ ' + str(src_txt))
    parts.append('\n## Extracted snippets and candidate signatures')
    if not snippets:
        parts.append('\n_No code-like snippets found. Please review `docs/RT-0119-ocr.txt` manually._')
    for i, s in enumerate(snippets, 1):
        parts.append(f'\n### Snippet {i}')
        parts.append('\n```')
        parts.append(s)
        parts.append('```')
        # try to find first signature line
        first = s.splitlines()[0]
        m = re.search(r"(subroutine|function|module)\s+([\w_]+)", first, re.IGNORECASE)
        if m:
            parts.append(f'\n- Candidate API name: **{m.group(2)}** (type: {m.group(1)})')
    parts.append('\n---\n\n_This file was generated automatically. Review and refine signatures before implementing._')
    return '\n'.join(parts)


def make_test_file(snippets, api_spec_path: Path):
    lines = []
    lines.append('import pathlib')
    lines.append('def test_api_spec_contains_snippets():')
    lines.append(f"    text = pathlib.Path('{api_spec_path.as_posix()}').read_text(encoding='utf-8')")
    if not snippets:
        lines.append("    assert 'code-like snippets' in text")
    else:
        for i, s in enumerate(snippets[:5], 1):
            # use a short fragment to avoid long literals
            frag = s.strip().splitlines()[0][:80].replace("'", "\'")
            lines.append(f"    assert '{frag}' in text")
    return '\n'.join(lines)


def main(argv):
    if len(argv) != 4:
        print('Usage: python tools\\parse_api_from_text.py <input-txt> <out-api-spec-md> <out-test-py>')
        return 2
    inp = Path(argv[1])
    out_md = Path(argv[2])
    out_test = Path(argv[3])
    if not inp.exists():
        print(f'Input file not found: {inp}')
        return 2
    txt = inp.read_text(encoding='utf-8')
    snippets = extract_snippets(txt)
    api_md = make_api_spec(snippets, inp)
    out_md.write_text(api_md, encoding='utf-8')
    test_py = make_test_file(snippets, out_md)
    out_test.parent.mkdir(parents=True, exist_ok=True)
    out_test.write_text(test_py, encoding='utf-8')
    print(f'Wrote API spec to: {out_md}')
    print(f'Wrote test file to: {out_test}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
