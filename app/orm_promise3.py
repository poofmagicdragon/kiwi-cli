# case: create a new user in the database
#1. create a new user instance of the User class
#2. get a database connection/session
#3. issue command to add the new user to the database

# # testing get_session
# from domain.User import User
# from database import get_session    

# user = User(username = "jdoe", firstname = "Jane", lastname = "Doe", password = "password", balance = 49)

# session = get_session()

# try:
#     session.add(user)
#     session.commit()
# finally:
#     session.close()

# from service.user_service import get_all_users, get_user_by_username, create_user, delete_user

# # testing get_all_users
# users = get_all_users()
# for user in users:
#     print(user)

# # testing get_user_by_username
# user = get_user_by_username("jdoe")
# print(user)

# # testing create_user
# create_user()

# # testing delete_user
# # this needs to add error message if we select a user that doesn't exist in database
# try:
#     delete_user()
# except Exception as e:
#     print(f"Error deleting user: {e}")

# # creating test scenarios
# from service.user_service import create_user_2
# from domain import User
# #1. prepare any objects that are needed for the test
# new_user = User(username = "jdoe", password = "password123", firstname = "John", lastname = "Doe", balance = 1000.0)
# #2. execute the test
# create_user_2(new_user)
# #3. verify the results by querying the database directly
# from database import get_session
# session = get_session()
# create_user = session.query(User).filter_by(username = "jdoe").one_or_none()
# session.close()

from utils import greet_function
greet_function('John', 'Doe', 'ar')