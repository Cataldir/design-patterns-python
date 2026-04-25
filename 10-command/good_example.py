# good_example.py - Command pattern with undo/redo and Invoker history stack
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...


@dataclass
class TextDocument:
    content: str = ""
    font_size: int = 12


class InsertTextCommand:
    def __init__(self, doc: TextDocument, position: int, text: str) -> None:
        self._doc = doc
        self._position = position
        self._text = text

    def execute(self) -> None:
        self._doc.content = (
            self._doc.content[: self._position]
            + self._text
            + self._doc.content[self._position :]
        )

    def undo(self) -> None:
        start = self._position
        end = self._position + len(self._text)
        self._doc.content = (
            self._doc.content[:start] + self._doc.content[end:]
        )


class DeleteTextCommand:
    def __init__(self, doc: TextDocument, start: int, end: int) -> None:
        self._doc = doc
        self._start = start
        self._end = end
        self._deleted: str = ""

    def execute(self) -> None:
        self._deleted = self._doc.content[self._start : self._end]
        self._doc.content = (
            self._doc.content[: self._start]
            + self._doc.content[self._end :]
        )

    def undo(self) -> None:
        self._doc.content = (
            self._doc.content[: self._start]
            + self._deleted
            + self._doc.content[self._start :]
        )


class ChangeFontCommand:
    def __init__(self, doc: TextDocument, new_size: int) -> None:
        self._doc = doc
        self._new_size = new_size
        self._previous_size: int = 0

    def execute(self) -> None:
        self._previous_size = self._doc.font_size
        self._doc.font_size = self._new_size

    def undo(self) -> None:
        self._doc.font_size = self._previous_size


class Invoker:
    def __init__(self) -> None:
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self) -> None:
        if not self._history:
            return
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            return
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)

    @property
    def history_size(self) -> int:
        return len(self._history)

    @property
    def redo_size(self) -> int:
        return len(self._redo_stack)


if __name__ == "__main__":
    doc = TextDocument()
    invoker = Invoker()

    invoker.execute(InsertTextCommand(doc, 0, "Hello World"))
    invoker.execute(InsertTextCommand(doc, 5, " Beautiful"))
    invoker.execute(ChangeFontCommand(doc, 18))
    invoker.execute(DeleteTextCommand(doc, 0, 6))

    print(f"After edits:  '{doc.content}' font={doc.font_size}")
    invoker.undo()
    invoker.undo()
    print(f"After 2 undo: '{doc.content}' font={doc.font_size}")
    invoker.redo()
    print(f"After redo:   '{doc.content}' font={doc.font_size}")
