# ...
from domain.User import User # from domain package and user module, import user class
from cli.menu_printer import print_menu
from cli import constants

print_menu(constants.LOGIN_MENU)
