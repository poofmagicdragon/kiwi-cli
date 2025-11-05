import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(project_root))

print(sys.path)

from app.utils import greet_function, divide
def test_greet_function():
    greeting = greet_function('Jane', 'Doe', 'en')
    assert greeting == "Hello, Jane Doe!"

def test_greet_function():
    greeting = greet_function('Juan', 'Doe', 'es')
    assert greeting == "!Hola, Juan Doe!"

def test_greet_function_unsupported_language():
    try:
        greet_function('John', 'Smith', 'fr')
    except Exception as e:
        assert str(e) == "Unsupported language"

def test_divide():
    result = divide(10,2)
    assert result == 5

def test_divide_by_zero():
    try:
        divide(10,0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero."