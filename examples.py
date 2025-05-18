from turmac import *

class Adder(Operator):
    """No snake!

    Uses fresh tape to add 2 numbers every time.
    """
    def __init__(self) -> None:
        self.machine: Machine = Machine(
            Tape(),
            Program.from_patterns(['oR0,oR2', 'xL3,xR2', 'oR4,xL3', 'oR0,oR0'])
        )

    def calculate(self, tape_pattern: str) -> None:
        self.machine.rewind()
        self.machine.tape = Tape.from_pattern(tape_pattern)
        def add_x(symbols: list[bool], is_above: bool) -> str:
            marks = ''.join( 'x' if p else 'o' for p in symbols)
            numbers = ' '.join(
                str(len(mark) - 1)
                for mark in marks.split('o')
                if len(mark) > 0
            )
            return numbers
        print(Operator.admire(self, add_x))

adder = Adder()
adder.calculate('xxoxx')
adder.calculate('xxxxxox')
adder.calculate('xxxxxxxxxoxxxx')
