"""
CodeParser MVP: parses Python files using AST and returns structured objects.
"""
import ast
from typing import List, Dict, Any
import os
from pathlib import Path


class CodeParser:
    def parse_python(self, path: str) -> List[Dict[str, Any]]:
        """Parse a Python file and extract functions, classes, and methods."""
        with open(path, "r", encoding="utf-8") as fh:
            src = fh.read()
        tree = ast.parse(src)
        items = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [a.arg for a in node.args.args]
                doc = ast.get_docstring(node)
                items.append(
                    {
                        "type": "function",
                        "name": node.name,
                        "args": args,
                        "doc": doc,
                        "lineno": node.lineno,
                    }
                )
            elif isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node)
                methods = []
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        methods.append(
                            {
                                "name": n.name,
                                "args": [a.arg for a in n.args.args],
                                "doc": ast.get_docstring(n),
                                "lineno": n.lineno,
                            }
                        )
                items.append(
                    {
                        "type": "class",
                        "name": node.name,
                        "doc": doc,
                        "methods": methods,
                        "lineno": node.lineno,
                    }
                )
        return items

    def parse_directory(self, directory: str) -> Dict[str, List[Dict[str, Any]]]:
        """Parse all Python files in a directory recursively."""
        results = {}
        for root, _, filenames in os.walk(directory):
            for f in filenames:
                if f.endswith(".py"):
                    file_path = os.path.join(root, f)
                    try:
                        results[file_path] = self.parse_python(file_path)
                    except Exception as e:
                        results[file_path] = {"error": str(e)}
        return results