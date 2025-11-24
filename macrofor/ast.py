"""AST skeleton for macrofor.

Define minimal node classes and a visitor interface. These are intentionally
small and will be expanded to match the API_SPEC extracted from the PDF.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any


class Node:
    pass


@dataclass
class Program(Node):
    name: Optional[str]
    body: List[Node] = field(default_factory=list)


@dataclass
class Module(Node):
    name: str
    body: List[Node] = field(default_factory=list)


@dataclass
class Subroutine(Node):
    name: str
    args: List[str] = field(default_factory=list)
    body: List[Node] = field(default_factory=list)


@dataclass
class Assignment(Node):
    target: str
    expr: str


@dataclass
class DoLoop(Node):
    var: str
    start: Any
    end: Any
    body: List[Node] = field(default_factory=list)


class Visitor:
    def visit(self, node: Node):
        meth = getattr(self, f"visit_{type(node).__name__}", None)
        if meth is None:
            return self.generic_visit(node)
        return meth(node)

    def generic_visit(self, node: Node):
        for attr, val in vars(node).items():
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, Node):
                        self.visit(item)
            elif isinstance(val, Node):
                self.visit(val)


@dataclass
class SingleInstruction(Node):
    """Generic single instruction node for MACROFORT single instructions.

    `name` is a short keyword (e.g. 'call', 'read', 'write', 'parameter', ...)
    `args` is a list of positional arguments (strings or simple expressions).
    """
    name: str
    args: List[Any] = field(default_factory=list)


@dataclass
class MacroInstruction(Node):
    """Macro instruction with a body (list of MACROFORT statements)."""
    name: str
    args: List[Any] = field(default_factory=list)
    body: List[Node] = field(default_factory=list)


@dataclass
class Call(Node):
    name: str
    args: List[str] = field(default_factory=list)


@dataclass
class Read(Node):
    unit: str
    var_list: List[str] = field(default_factory=list)


@dataclass
class Write(Node):
    unit: str
    var_list: List[str] = field(default_factory=list)


@dataclass
class Label(Node):
    label_name: str


@dataclass
class Format(Node):
    name: str
    format_list: List[str] = field(default_factory=list)


@dataclass
class Parameter(Node):
    items: List[str] = field(default_factory=list)


@dataclass
class Goto(Node):
    condition: str
    label: str


@dataclass
class If(Node):
    condition: str
    then_body: List[Node] = field(default_factory=list)
    else_body: List[Node] = field(default_factory=list)


@dataclass
class Comment(Node):
    text: str

