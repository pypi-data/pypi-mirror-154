from mypyliex.classes.user import User
from mypyliex.classes.printer import Printer


class System:
    printer_position: str
    printer: Printer
    user: User = User()

    def __init__(self, printer_position: str = 'Printer 3rd floor'):
        self.printer_position = printer_position
        self.printer = Printer()


