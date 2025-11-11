# ...
from app.domain.User import User # from domain package and user module, import user class
from app.cli.menu_printer import print_menu
from app.cli import constants

print_menu(constants.LOGIN_MENU)



# from database import get_session
# from app.domain.User import User

# # session = get_session()
# # # Now that I have a session how do I query all users
# # users = session.query(User).all()

# # for user in users:
# #     print(user)

# # session.close()

# user = User(username = "mt1", firstname = "Michael", lastname = "Tsang", password = "password", balance = 1000.0)

# try:
#     session.add(user)
#     session.commit()
# except Exception as e:
#     print(f"Error occurred: {e}")
#     session.rollback()
# else:
#     session.close()

