from types import SimpleNamespace
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest
from app.domain import Investment, MenuFunctions, Portfolio, User, Security
from app.cli.menu_printer import handle_user_selection, navigate_to_manage_user_menu, print_error, print_menu, _router, _menus, _console

# this runs before each test function
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestSessionLocal = sessionmaker(bind=engine)
    session = TestSessionLocal()
    yield session
    session.rollback()
    session.close()

def test_navigate_to_manage_user_menu():
    test_admin_user = User(username="admin", firstname="Admin", lastname="User", password="adminpass", balance=0.0)
    result = navigate_to_manage_user_menu(test_admin_user)
    assert result == 2

def test_navigate_to_manage_user_menu_fail():
    test_admin_user = User(username="not_admin", firstname="not", lastname="admin", password="notadminpass", balance=0.0)
    with pytest.raises(Exception) as exc_info:
        navigate_to_manage_user_menu(test_admin_user)
    result = str(exc_info.value)
    assert "Only admin user can manage users" in str(result)

def test_print_error(capsys):
    error = "error message"
    print_error(error)
    captured = capsys.readouterr()
    output = captured.out
    assert error in output

# def test_handle_user_selection(capsys):
#     handle_user_selection(4, 1)

#     captured = capsys.readouterr()
#     output = captured.out

#     assert "Marketplace" in output
#     assert "1. View Securities" in output
#     assert "2. Place Purchase Order" in output
#     assert "3. View Purchase Orders" in output
#     assert "0. Back to main menu" in output


def test_print_menu(capsys, monkeypatch):
    test_menu_id = 99

    monkeypatch.setitem(_menus, test_menu_id, "----\nMarketplace\n----\n1. View securities\n2. Place purchase order\n3. View purchase orders\n0. Back to main menu")

    monkeypatch.setattr(_console, "input", lambda _: "1")

    test_executor = lambda: "Executed"
    test_printer = lambda result: print(f"Result: {result}")
    test_navigator = lambda: None
    test_menu_functions = SimpleNamespace(executor=test_executor, printer=test_printer, navigator=test_navigator)
    
    monkeypatch.setitem(_router, f"{test_menu_id}.1", test_menu_functions)

    print_menu(test_menu_id)
    captured = capsys.readouterr()
    output = captured.out

    assert "Marketplace" in output
    assert "1. View securities" in output
    assert "2. Place purchase order" in output
    assert "3. View purchase orders" in output
    assert "0. Back to main menu" in output    

from app.cli.menu_printer import handle_user_selection, _menus, _console, _router

def test_handle_user_selection_wrong_option(capsys, monkeypatch):
    test_menu_id = 99

    monkeypatch.setitem(_menus, test_menu_id, "Dummy Menu")
    monkeypatch.setattr(_console, "input", lambda _: "1") 
    monkeypatch.setitem(_router, f"{test_menu_id}.9", None)
    
    monkeypatch.setattr("app.cli.menu_printer.print_menu", lambda _: None)

    handle_user_selection(test_menu_id, 9)

    output = capsys.readouterr().out
    assert "Error: 9 is not a valid option" in output

