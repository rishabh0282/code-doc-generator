"""
Format generated docstrings or READMEs into desired outputs.
"""
from typing import Dict


def format_docstring(name: str, docstring: str, style: str = "google") -> str:
    if style == "google":
        return f'"""{docstring}\n"""'
    return f'"""{docstring}"""'