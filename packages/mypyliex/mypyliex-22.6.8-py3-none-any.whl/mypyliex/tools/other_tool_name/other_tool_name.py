from mypyliex.tools.other_tool_name.constants import USER_NAME, USER_HOME_PATH
from mypyliex.classes.system import System


def main():
    print('library => tools => other_tool_name => main.py => main()')
    print(f'Constant USER_NAME: {USER_NAME}')
    print(f'Constant USER_HOME_PATH: {USER_HOME_PATH}')

    system = System()

    username = system.user.get_user_name()
    print(f'Current user name: {username}')

    if username == 'ubuntu':
        system.user.change_user_name('debian')

    print(f'New user name: {system.user.get_user_name()}')

    system.printer.switch_printer('Printer 5th floor')
    system.printer.print(f'Documentation {10_000} pages.')


if __name__ == '__main__':
    main()
