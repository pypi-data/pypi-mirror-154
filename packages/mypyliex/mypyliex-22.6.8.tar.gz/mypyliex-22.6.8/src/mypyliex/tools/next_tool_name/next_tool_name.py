from mypyliex.tools.next_tool_name.constants import SOME_CONSTANT, DOMAIN
from mypyliex.classes.system import System


def main():
    print('library => tools => next_tool_name => main.py => main()')
    print(f'Constant SOME_CONSTANT: {SOME_CONSTANT}')
    print(f'Constant DOMAIN: {DOMAIN}')

    system = System()
    username = system.user.get_user_name()
    print(f'Current user name: {username}')

    if username == 'ubuntu':
        system.user.change_user_name('debian')

    print(f'New user name: {system.user.get_user_name()}')


if __name__ == '__main__':
    main()
