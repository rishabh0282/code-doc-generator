"""
Simple CLI to run the parser + generator (dry-run supported).
"""
import argparse
import os
from src.code_parser import CodeParser
from src.llm_generator import DocGenerator
from src.doc_formatter import format_docstring

def main():
    parser = argparse.ArgumentParser(description="Code documentation generator (MVP)")
    parser.add_argument("path", help="File or directory")
    parser.add_argument("--lang", default="python", choices=["python"], help="Language")
    parser.add_argument("--format", default="docstring", choices=["docstring","markdown"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--api-key", default=None)
    args = parser.parse_args()

    cp = CodeParser()
    dg = DocGenerator(api_key=args.api_key)
    files = []
    if os.path.isdir(args.path):
        for root, _, filenames in os.walk(args.path):
            for f in filenames:
                if f.endswith(".py"):
                    files.append(os.path.join(root, f))
    else:
        files = [args.path]

    for f in files:
        items = cp.parse_python(f)
        for it in items:
            if it["type"] == "function":
                sig = f'{it["name"]}({", ".join(it["args"])})'
                gen = dg.generate_for_function(sig, it.get("doc") or "")
                formatted = format_docstring(it["name"], gen)
                if args.dry_run:
                    print(f"--- {f}::{it['name']} ---\n{formatted}\n")
                else:
                    # Insert logic to write docstring into file (user review recommended)
                    print(f"Would write docstring for {f}::{it['name']}")

if __name__ == "__main__":
    main()