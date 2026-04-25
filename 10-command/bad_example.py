# bad_example.py - button handler with inline logic and no undo support
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TextDocument:
    content: str = ""
    font_size: int = 12
    clipboard: str = ""
    history: list[str] = field(default_factory=list)


def button_bold(doc: TextDocument, selection: str) -> None:
    replacement = f"**{selection}**"
    doc.content = doc.content.replace(selection, replacement, 1)
    print(f"Applied bold to '{selection}'")


def button_change_font(doc: TextDocument, new_size: int) -> None:
    doc.font_size = new_size
    print(f"Font size changed to {new_size}")


def button_insert(doc: TextDocument, position: int, text: str) -> None:
    doc.content = doc.content[:position] + text + doc.content[position:]
    print(f"Inserted '{text}' at position {position}")


def button_delete(doc: TextDocument, start: int, end: int) -> None:
    deleted = doc.content[start:end]
    doc.content = doc.content[:start] + doc.content[end:]
    print(f"Deleted '{deleted}'")


def button_undo(doc: TextDocument) -> None:
    print("Undo not supported")


if __name__ == "__main__":
    doc = TextDocument(content="Hello World")
    button_bold(doc, "World")
    button_change_font(doc, 16)
    button_insert(doc, 5, " Beautiful")
    button_delete(doc, 0, 5)
    button_undo(doc)
    print(f"Final: '{doc.content}' font={doc.font_size}")
