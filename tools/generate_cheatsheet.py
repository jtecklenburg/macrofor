#!/usr/bin/env python
"""Generate MACROFOR_CHEATSHEET.md from api.py docstrings."""

import sys
import pathlib
import inspect

# Ensure project root is on sys.path so `import macrofor` works when running the
# script from the repository root or tools directory. This avoids requiring
# users to install the package in their environment just to generate docs.
project_root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from macrofor import api


def extract_docstring_parts(docstring: str) -> dict:
    """Parse docstring into sections: description, args, returns, example."""
    if not docstring:
        return {"description": "", "args": "", "returns": "", "example": ""}
    
    lines = docstring.strip().split('\n')
    parts = {
        "description": "",
        "args": "",
        "returns": "",
        "example": ""
    }
    
    current_section = "description"
    description_lines = []
    args_lines = []
    returns_lines = []
    example_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Args:"):
            current_section = "args"
            continue
        elif stripped.startswith("Returns:"):
            current_section = "returns"
            continue
        elif stripped.startswith("Example:"):
            current_section = "example"
            continue
        
        if current_section == "description":
            description_lines.append(stripped)
        elif current_section == "args":
            args_lines.append(stripped)
        elif current_section == "returns":
            returns_lines.append(stripped)
        elif current_section == "example":
            example_lines.append(stripped)
    
    # preserve line breaks in description so docstring-specified examples
    # or spec-like blocks remain intact for detailed rendering
    parts["description"] = '\n'.join(description_lines).strip()
    parts["args"] = ' '.join(args_lines).strip()
    parts["returns"] = ' '.join(returns_lines).strip()
    parts["example"] = '\n'.join(example_lines).strip()
    
    return parts


    


def generate_cheatsheet():
    """Generate cheatsheet markdown from api.py."""
    output = []
    output.append("# MACROFOR Quick Reference")
    output.append("")
    output.append("Auto-generated from `macrofor/api.py` docstrings.")
    output.append("")
    
    # The generator now relies entirely on docstrings in `api.py`.

    # Collect all public functions
    single_instr_funcs = []
    macro_funcs = []
    
    for name, obj in inspect.getmembers(api, inspect.isfunction):
        if name.startswith('_'):
            continue
        
        if name.endswith('f'):
            single_instr_funcs.append((name, obj))
        elif name.endswith('m'):
            macro_funcs.append((name, obj))
    
    # Single-instruction functions table
    output.append("## Single-Instruction Functions (*f)")
    output.append("")
    output.append("| Function | Signature | Description |")
    output.append("|----------|-----------|-------------|")
    
    for name, func in sorted(single_instr_funcs):
        sig = str(inspect.signature(func))
        docstring = func.__doc__ or ""
        parts = extract_docstring_parts(docstring)
        # collapse description lines into a single short line for the table
        description = ' '.join(l.strip() for l in parts["description"].splitlines() if l.strip())
        if len(description) > 120:
            description = description[:117] + "..."
        output.append(f"| `{name}` | `{name}{sig}` | {description} |")
    
    output.append("")
    output.append("## Macro Functions (*m)")
    output.append("")
    output.append("| Function | Signature | Description |")
    output.append("|----------|-----------|-------------|")
    
    for name, func in sorted(macro_funcs):
        sig = str(inspect.signature(func))
        docstring = func.__doc__ or ""
        parts = extract_docstring_parts(docstring)
        # collapse description lines into a single short line for the table
        description = ' '.join(l.strip() for l in parts["description"].splitlines() if l.strip())
        if len(description) > 120:
            description = description[:117] + "..."
        output.append(f"| `{name}` | `{name}{sig}` | {description} |")
    
    output.append("")
    output.append("---")
    output.append("")
    output.append("## Detailed Function Reference")
    output.append("")
    
    # Single-instruction functions detail
    output.append("### Single-Instruction Functions (*f)")
    output.append("")
    
    for name, func in sorted(single_instr_funcs):
        sig = str(inspect.signature(func))
        docstring = func.__doc__ or "No documentation"
        parts = extract_docstring_parts(docstring)
        
        output.append(f"#### `{name}{sig}`")
        output.append("")
        if parts["description"]:
            output.append(f"{parts['description']}")
            output.append("")
        if parts["args"]:
            output.append("**Args:**")
            output.append(f"{parts['args']}")
            output.append("")
        if parts["returns"]:
            output.append("**Returns:**")
            output.append(f"{parts['returns']}")
            output.append("")
        # Render example block from docstring. If no explicit Example: is
        # present but the description itself contains multiple lines, show
        # the description as a Fortran example block.
        if parts["example"]:
            example_text = parts["example"].replace('\\n', '\n').replace('\\nend', '\nend')
            output.append("**Example:**")
            output.append("```fortran")
            output.append(example_text)
            output.append("```")
            output.append("")
        elif '\n' in parts["description"]:
            output.append("**Example:**")
            output.append("```fortran")
            output.append(parts["description"])
            output.append("```")
            output.append("")
    
    # Macro functions detail
    output.append("### Macro Functions (*m)")
    output.append("")
    
    for name, func in sorted(macro_funcs):
        sig = str(inspect.signature(func))
        docstring = func.__doc__ or "No documentation"
        parts = extract_docstring_parts(docstring)
        
        output.append(f"#### `{name}{sig}`")
        output.append("")
        if parts["description"]:
            output.append(f"{parts['description']}")
            output.append("")
        if parts["args"]:
            output.append("**Args:**")
            output.append(f"{parts['args']}")
            output.append("")
        if parts["returns"]:
            output.append("**Returns:**")
            output.append(f"{parts['returns']}")
            output.append("")
        if parts["example"]:
            example_text = parts["example"].replace('\\n', '\n').replace('\\nend', '\nend')
            output.append("**Example:**")
            output.append("```fortran")
            output.append(example_text)
            output.append("```")
            output.append("")
        elif '\n' in parts["description"]:
            output.append("**Example:**")
            output.append("```fortran")
            output.append(parts["description"])
            output.append("```")
            output.append("")
    
    return "\n".join(output)


def main():
    cheatsheet = generate_cheatsheet()
    
    # Write to docs/MACROFOR_CHEATSHEET.md
    docs_dir = pathlib.Path(__file__).parent.parent / "docs"
    output_file = docs_dir / "MACROFOR_CHEATSHEET.md"
    
    output_file.write_text(cheatsheet)
    print(f"✓ Generated {output_file.resolve()}")


if __name__ == "__main__":
    main()
