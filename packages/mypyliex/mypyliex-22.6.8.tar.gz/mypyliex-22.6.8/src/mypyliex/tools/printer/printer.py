from mypyliex.tools.printer.constants import SOME_NUMBER, OTHER_NUMBER  # type: ignore
from mypyliex.classes.printer import Printer  # type: ignore


def main():
    print('library => tools => printer => main.py => main()')
    print(f'Constant SOME_NUMBER: {SOME_NUMBER}')
    print(f'Constant OTHER_NUMBER: {OTHER_NUMBER}')
    printer = Printer()
    printer.print('Some important text')
    printer.switch_printer('Printer 4th floor')
    printer.print('Joke for friends')


if __name__ == '__main__':
    main()
