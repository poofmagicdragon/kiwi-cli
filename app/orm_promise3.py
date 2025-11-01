# case: create a new user in the database
#1. create a new user instance of the User class
#2. get a database connection/session
#3. issue command to add the new user to the database

# from domain.User import User
# from database import get_session    

# user = User(username = "jdoe", firstname = "Jane", lastname = "Doe", password = "password", balance = 49)

# session = get_session()

# try:
#     session.add(user)
#     session.commit()
# finally:
#     session.close()

from service.user_service import get_all_users

users = get_all_users()
for user in users:
    print(user)


