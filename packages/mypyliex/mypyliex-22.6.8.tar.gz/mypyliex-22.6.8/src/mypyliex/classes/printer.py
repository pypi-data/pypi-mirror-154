class Printer:
    printer_position: str = 'Printer 2nd floor'

    def print(self, text: str) -> None:
        print(f'{self.printer_position} is printing: {text}')

    def switch_printer(self, new_position: str):
        self.printer_position = new_position
