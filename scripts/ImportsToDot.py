#!/usr/bin/env python3
import argparse
import os
import re
import sys

def module_to_path(module_name: str, root_dir: str) -> str:
    """Converts a Lean module name (e.g., Mathlib.Algebra.Group) to a relative file path."""
    rel_path = module_name.replace('.', os.sep) + '.lean'
    full_path = os.path.join(root_dir, rel_path)
    if os.path.isfile(full_path):
        return rel_path
    return None

def path_to_module(file_path: str, root_dir: str) -> str:
    """Converts a file path into a clean Lean module name for node labeling."""
    rel_path = os.path.relpath(file_path, root_dir)
    if rel_path.endswith('.lean'):
        rel_path = rel_path[:-5]
    return rel_path.replace(os.sep, '.')

def strip_comments(content: str) -> str:
    """Removes nested /- ... -/ block comments and -- single-line comments."""
    result = []
    i = 0
    n = len(content)
    depth = 0
    in_line_comment = False

    while i < n:
        if in_line_comment:
            if content[i] == '\n':
                in_line_comment = False
                result.append('\n')
            i += 1
        elif depth > 0:
            if content[i:i+2] == '/-':
                depth += 1
                i += 2
            elif content[i:i+2] == '-/':
                depth -= 1
                i += 2
            else:
                if content[i] == '\n':
                    result.append('\n')
                i += 1
        else:
            if content[i:i+2] == '--':
                in_line_comment = True
                i += 2
            elif content[i:i+2] == '/-':
                depth += 1
                i += 2
            else:
                result.append(content[i])
                i += 1

    return ''.join(result)

def parse_imports(file_path: str) -> list[str]:
    """Extracts imported module names from a Lean 4 file."""
    imports = []
    # Matches: import [public] [all] Module.Name (supports multiple imports on one line)
    import_line_regex = re.compile(
        r'^\s*(?:public\s+)?import\s+(?:public\s+)?(?:all\s+)?([A-Za-z0-9_.\s«»]+)'
    )

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        clean_content = strip_comments(raw_content)

        for line in clean_content.splitlines():
            line = line.strip()
            if not line:
                continue

            # Skip Lean header keywords that can appear before imports
            if line in ('prelude', 'module') or line.startswith('module '):
                continue

            match = import_line_regex.match(line)
            if match:
                # Lean allows space-separated imports on a single import line
                modules_part = match.group(1).strip()
                for mod in modules_part.split():
                    if mod not in ('public', 'all'):
                        imports.append(mod)
            else:
                # Once we hit actual declarations/code after the header, stop scanning
                break

    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)

    return imports

def build_dependency_graph(start_file: str, root_dir: str, max_depth: int = None):
    """Traverses imports using BFS, avoiding cycles."""
    visited = set()
    edges = set()

    start_abs = os.path.abspath(start_file)
    if not os.path.isfile(start_abs):
        print(f"Error: File '{start_file}' not found.", file=sys.stderr)
        sys.exit(1)

    start_mod = path_to_module(start_abs, root_dir)
    queue = [(start_mod, start_abs, 0)]
    visited.add(start_mod)

    while queue:
        current_mod, current_path, depth = queue.pop(0)

        if max_depth is not None and depth >= max_depth:
            continue

        imported_modules = parse_imports(current_path)
        for imp_mod in imported_modules:
            edges.add((current_mod, imp_mod))

            if imp_mod not in visited:
                visited.add(imp_mod)
                imp_rel_path = module_to_path(imp_mod, root_dir)
                if imp_rel_path:
                    imp_abs_path = os.path.join(root_dir, imp_rel_path)
                    queue.append((imp_mod, imp_abs_path, depth + 1))

    return edges

def generate_dot(edges: set[tuple[str, str]]) -> str:
    """Formats the collected edges as a GraphViz DOT string."""
    lines = [
        "digraph LeanImports {",
        "  rankdir=LR;",
        "  ranksep=1.2;",
        "  nodesep=0.3;",
        "  node [",
        "    shape=box,",
        "    style=\"rounded,filled\",",
        "    fillcolor=\"#f8f9fa\",",
        "    fontname=\"Helvetica,Arial,sans-serif\",",
        "    fontsize=10,",
        "    margin=\"0.25,0.1\",",
        "    height=0.3",
        "  ];",
        "  edge [color=\"#6c757d\", arrowsize=0.7];",
        ""
    ]
    for src, dst in sorted(edges):
        lines.append(f'  "{src}" -> "{dst}";')
    lines.append("}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate a GraphViz .dot diagram of Lean 4 file imports.")
    parser.add_argument("file", help="Path to the starting .lean file (e.g., Mathlib/NumberTheory/SumTwoSquares.lean)")
    parser.add_argument("--root", default=".", help="Root directory of the Lean project (default: current directory)")
    parser.add_argument("--max-depth", type=int, default=None, help="Maximum recursion depth")
    parser.add_argument("--output", "-o", default=None, help="Output .dot file path (prints to stdout if omitted)")

    args = parser.parse_args()
    root_dir = os.path.abspath(args.root)

    edges = build_dependency_graph(args.file, root_dir, args.max_depth)
    dot_code = generate_dot(edges)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(dot_code + "\n")
        print(f"Saved GraphViz DOT to {args.output} ({len(edges)} edges).", file=sys.stderr)
    else:
        print(dot_code)

if __name__ == "__main__":
    main()
