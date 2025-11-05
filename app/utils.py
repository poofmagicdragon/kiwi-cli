
from app.domain import User

def greet_user(user: User):
    return f"Hello user: {user.firstname} {user.lastname}"

def greet_function(firstname, lastname, language = 'en'):
    if language == 'en':
        return f"Hello, {firstname} {lastname}!"
    if language == 'es':
        return f"!Hola, {firstname} {lastname}!"   
    else:
        raise Exception("Unsupported language")   

def sum(a,b):
    return a+b  

def divide(a,b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a/b