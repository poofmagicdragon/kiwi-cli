from app.cli.menu_printer import print_menu, _console
from app.cli import constants


def test_initialization(capsys, monkeypatch):
    monkeypatch.setattr(_console, "input", lambda _: "1")
    monkeypatch.setattr("app.cli.menu_printer.handle_user_selection", lambda *_: None)
    print_menu(constants.LOGIN_MENU)
    output = capsys.readouterr().out
    assert "1. Login" in output
    assert "0. Exit" in output