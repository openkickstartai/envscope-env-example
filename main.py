#!/usr/bin/env python3
"""EnvScope CLI — environment variable topology analyzer."""
import argparse
import json
import sys
from envscope import scan_directory, find_dead, find_orphans, find_inconsistent, generate_example


def cmd_scan(args):
    reads, defs = scan_directory(args.path)
    dead = find_dead(reads, defs)
    orphans = find_orphans(reads, defs)
    inconsistent = find_inconsistent(reads)
    has_issues = bool(dead or orphans or inconsistent)
    if args.format == "json":
        print(json.dumps({
            "summary": {"reads": len(reads), "defs": len(defs)},
            "dead": [{"name": d.name, "file": d.file, "line": d.line} for d in dead],
            "orphans": [{"name": o.name, "file": o.file, "line": o.line} for o in orphans],
            "inconsistent": {
                k: [{"default": r.default, "file": r.file, "line": r.line} for r in v]
                for k, v in inconsistent.items()
            },
        }, indent=2))
        return 1 if has_issues else 0
    print(f"\n\U0001f4ca EnvScope Scan: {args.path}")
    print(f"   {len(reads)} env reads in source \u00b7 {len(defs)} definitions in config\n")
    if dead:
        print(f"\U0001f480 Dead Configs ({len(dead)}):")
        for d in dead:
            print(f"   {d.name:<30} defined {d.file}:{d.line}")
    if orphans:
        print(f"\n\U0001f47b Orphan Reads ({len(orphans)}):")
        for o in orphans:
            print(f"   {o.name:<30} read at {o.file}:{o.line}")
    if inconsistent:
        print(f"\n\u26a0\ufe0f  Inconsistent Defaults ({len(inconsistent)}):")
        for name, refs in inconsistent.items():
            vals = " vs ".join(f'"{r.default}" @{r.file}:{r.line}' for r in refs)
            print(f"   {name}: {vals}")
    if not has_issues:
        print("\u2705 All clear \u2014 no config issues found!")
    return 1 if has_issues else 0


def cmd_generate(args):
    reads, _ = scan_directory(args.path)
    output = generate_example(reads)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"\u2705 Written to {args.output} ({len({r.name for r in reads})} vars)")
    else:
        print(output)
    return 0


def main():
    parser = argparse.ArgumentParser(prog="envscope", description="Env var topology analyzer")
    sub = parser.add_subparsers(dest="cmd")
    scan_p = sub.add_parser("scan", help="Scan project for env var issues")
    scan_p.add_argument("path", nargs="?", default=".")
    scan_p.add_argument("-f", "--format", choices=["text", "json"], default="text")
    gen_p = sub.add_parser("generate", help="Generate .env.example from code")
    gen_p.add_argument("path", nargs="?", default=".")
    gen_p.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(0)
    handler = cmd_scan if args.cmd == "scan" else cmd_generate
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
