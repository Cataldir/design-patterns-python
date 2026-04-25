# test_command.py - pytest suite for Command pattern with undo/redo
from __future__ import annotations

from good_example import (
    ChangeFontCommand,
    DeleteTextCommand,
    InsertTextCommand,
    Invoker,
    TextDocument,
)


class TestInsertTextCommand:
    def test_execute_inserts_at_position(self) -> None:
        doc = TextDocument(content="Hello")
        cmd = InsertTextCommand(doc, 5, " World")
        cmd.execute()
        assert doc.content == "Hello World"

    def test_undo_removes_inserted_text(self) -> None:
        doc = TextDocument(content="Hello")
        cmd = InsertTextCommand(doc, 5, " World")
        cmd.execute()
        cmd.undo()
        assert doc.content == "Hello"


class TestDeleteTextCommand:
    def test_execute_removes_range(self) -> None:
        doc = TextDocument(content="Hello World")
        cmd = DeleteTextCommand(doc, 5, 11)
        cmd.execute()
        assert doc.content == "Hello"

    def test_undo_restores_deleted_text(self) -> None:
        doc = TextDocument(content="Hello World")
        cmd = DeleteTextCommand(doc, 0, 6)
        cmd.execute()
        assert doc.content == "World"
        cmd.undo()
        assert doc.content == "Hello World"


class TestChangeFontCommand:
    def test_execute_changes_font_size(self) -> None:
        doc = TextDocument(font_size=12)
        cmd = ChangeFontCommand(doc, 24)
        cmd.execute()
        assert doc.font_size == 24

    def test_undo_restores_previous_size(self) -> None:
        doc = TextDocument(font_size=12)
        cmd = ChangeFontCommand(doc, 24)
        cmd.execute()
        cmd.undo()
        assert doc.font_size == 12


class TestInvokerUndoRedo:
    def test_execute_tracks_history(self) -> None:
        doc = TextDocument()
        invoker = Invoker()
        invoker.execute(InsertTextCommand(doc, 0, "Hello"))
        assert invoker.history_size == 1

    def test_undo_reverses_last_command(self) -> None:
        doc = TextDocument()
        invoker = Invoker()
        invoker.execute(InsertTextCommand(doc, 0, "Hello"))
        invoker.undo()
        assert doc.content == ""
        assert invoker.history_size == 0
        assert invoker.redo_size == 1

    def test_redo_replays_undone_command(self) -> None:
        doc = TextDocument()
        invoker = Invoker()
        invoker.execute(InsertTextCommand(doc, 0, "Hello"))
        invoker.undo()
        invoker.redo()
        assert doc.content == "Hello"
        assert invoker.history_size == 1
        assert invoker.redo_size == 0

    def test_new_execute_clears_redo_stack(self) -> None:
        doc = TextDocument()
        invoker = Invoker()
        invoker.execute(InsertTextCommand(doc, 0, "Hello"))
        invoker.undo()
        invoker.execute(InsertTextCommand(doc, 0, "World"))
        assert invoker.redo_size == 0
