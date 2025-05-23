from collections.abc import Iterator, Callable

"""Turing Machine emulation in object-oriented Python

We use a Machine that will have Tape and a Program.
The Tape consists of Squares that contains a symbol
that has to be either True or False.
The Program consists of States,
that in turn consist of Behaviors.
A Behavior determines what needs to happen
when either a True Square or False Square is scanned.
When iterating through a Machine,
we will get Moves that can be used to record all
the steps a Machine went through.
Finally, an Operator is used to record
and present(!) the Moves a Machine went through,
i.e. the Operator admires the Machine.
"""

class Square:
    """Squares are the segments of a Turing Machine Tape.

    They can contain 2 types of symbols: True or False.
    """
    def __init__(self, symbol: bool = False):
        self.symbol: bool = symbol

    @classmethod
    def from_pattern(cls, pattern: str) -> 'Square':
        """This enables creating instances from a pattern.

        We use a from_pattern(s) class methods throughout this script.
        The @classmethod decorater provides an alternative
        way to create instancest.
        Here, 'o' and 'x' translate to False and True.
        In other from_pattern(s),
        'L' and 'R' will be about the direction: Left or Right,
        and a number will be about what state to go to.
        """
        if pattern not in ['o', 'x']:
            raise ValueError("Pattern should be either 'o' or 'x'")
        return cls(pattern[0] == 'x')

    def __str__(self) -> str:
        return f'Square({str(self.symbol)})'

    def __bool__(self) -> bool:
        return self.symbol

class Tape:
    """This special Tape is used for our Turing Machines.

    It can be infinitely extended (with `feed_left` and `feed_right`).
    However, we try to look only at the meaningful part,
    which might be very short.
    """
    def __init__(self, squares: list[Square] = [Square()]):
        self.squares: list[Square] = squares

    @classmethod
    def from_pattern(cls, pattern: str) -> 'Tape':
        return cls([Square.from_pattern(c) for c in pattern])

    def __str__(self) -> str:
        return f"Tape([{', '.join([str(x) for x in self.squares])}])"

    def __iter__(self) -> Iterator[Square]:
        return (x for x in self.squares)

    def __getitem__(self, i: int) -> Square:
        return self.squares[i]

    def __len__(self) -> int:
        return len(self.squares)

    def feed_left(self) -> None:
        """Adds new squares on the left side of the tape."""
        self.squares.insert(0, Square())

    def feed_right(self) -> None:
        """Adds new squares on the right side of the tape."""
        self.squares.append(Square())

class Behavior:
    """A Behavior describes the actions of a Turing Machine Program.

    We define what symbol needs to be stamped,
    whether we need to move to the Square to the right
    or the left of the current Square (of the Tape),
    and what State we should go to next.
    """
    def __init__(self, symbol: bool, goes_right: bool, state_i: int):
        self.symbol: bool = symbol
        self.goes_right: bool = goes_right
        self.state_i: int = state_i

    @classmethod
    def from_pattern(cls, pattern: str) -> 'Behavior':
        c1, c2, rest = pattern[0], pattern[1], pattern[2:]
        if c1 not in ['o', 'x']:
            raise ValueError("First character should be either 'o' or 'x'")
        if c2 not in ['L', 'R']:
            raise ValueError("Second character should be either 'L' or 'R'")
        return cls(c1 == 'x', c2 == 'R', int(rest))

    def __str__(self) -> str:
        return f"Behavior({self.symbol}, {self.goes_right}, {self.state_i})"

class State:
    """A State is basically a combination of 2 Behaviors.

    We define what needs to happen
    when a Machine scans a Square that has the symbol False,
    and what needs to happen
    when the Machine scans a Square that has the symbol True.
    """
    def __init__(self, when_false: Behavior, when_true: Behavior):
        self.when_false: Behavior = when_false
        self.when_true: Behavior = when_true

    @classmethod
    def from_pattern(cls, pattern: str) -> 'State':
        return cls(*[Behavior.from_pattern(x) for x in pattern.split(',')])

    def __str__(self) -> str:
        return f"State({self.when_false}, {self.when_true})"

    def __getitem__(self, p: bool) -> Behavior:
        if p == False:
            return self.when_false
        else:
            return self.when_true

class Program:
    """A Turing Machine Program consists of States.

    The first state has the index 1: it is State 1.
    The index 0 is out of range because we use an 1-based sequence.
    However, 0 is used in the Machine to stop the iteration.
    """
    def __init__(self, states: list[State] = []):
        self.states: list[State] = states

    @classmethod
    def from_patterns(cls, patterns: list[str]) -> 'Program':
        return cls([State.from_pattern(x) for x in patterns])

    def __str__(self) -> str:
        return f"Program([{', '.join([str(state) for state in self.states])}])"

    def __getitem__(self, i: int) -> State:
        if i < 1:
            raise IndexError("0 is out of range: Program is 1-based")
        return self.states[i - 1]

class Move:
    """A move can be used to record the steps a Machine goes through.

    It shows what the symbols are after completing a step,
    but also what square we came from and what square we are going to,
    as well as what state we came from and what state we are going to.
    """
    def __init__(
        self,
        symbols: list[bool],
        from_square_i: int,
        to_square_i: int,
        from_state_i: int,
        to_state_i: int
    ):
        self.symbols: list[bool] = symbols
        self.from_square_i: int = from_square_i
        self.to_square_i: int = to_square_i
        self.from_state_i: int = from_square_i
        self.to_state_i: int = to_state_i

    def __str__(self) -> str:
        move_args = [
            str(self.from_square_i),
            str(self.to_square_i),
            str(self.from_state_i),
            str(self.to_state_i)
        ]
        return f"Move({', '.join(move_args)})"

    def to_table_row(
        self,
        show_pointer: bool = True,
        is_fancy: bool = True
    ) -> str:
        """This pretty prints the symbols that result from a move."""
        sep = '\u2502' if is_fancy else '|'
        pointer_left = '\u251c' if is_fancy else '>'
        pointer_right = '\u2524' if is_fancy else sep
        row = [sep]
        pointer_start: int = self.from_square_i * 2
        pointer_end: int = self.from_square_i * 2 + 2
        for symbol in self.symbols:
            row.append('x' if symbol == True else 'o')
            row.append(sep)
        if show_pointer:
            row[pointer_start] = pointer_left
            row[pointer_end] = pointer_right
        return ''.join(row)

class Machine:
    """Our actual Turing Machine!

    In essence, it consist of a Tape and a Program.
    We can iterate through it,
    executing all the relevant steps
    and returning the Moves in the process.
    These moves can be used to show what motions the machine went through,
    but for that we need something that records the moves!
    """
    def __init__(self, tape: Tape = Tape(), program: Program = Program()):
        self.tape: Tape = tape
        self.program: Program = program
        self.square_i: int = 0
        self.state_i: int = 1 # 0 means halt!
        self.configuration: Behavior

    @classmethod
    def from_patterns(
        cls,
        tape_pattern: str,
        program_patterns: list[str]
    ) -> 'Machine':
        return cls(
            Tape.from_pattern(tape_pattern),
            Program.from_patterns(program_patterns)
        )

    def __str__(self) -> str:
        return f"Machine({self.tape}, {self.program})"

    def scan(self) -> None:
        """Scans the symbol of the current square on the tape.

        When we scan the tape,
        we retrieve the value of the symbol that is in the current square,
        i.e. we take a look at it.
        We also set the configuration attribute
        that will be used for some of the other methods
        (i.e. stamp, change_square, and change_state).
        """
        scanned_symbol = self.tape[self.square_i].symbol
        self.configuration = self.program[self.state_i][scanned_symbol]

    def stamp(self) -> None:
        """Changes the symbol of the current square."""
        self.tape[self.square_i].symbol = self.configuration.symbol

    def change_square(self) -> None:
        """Move to an adjacent Square on the Tape.

        We can only go to the square immediately left or right
        of the current square.
        If the adjacent square is not visible yet,
        we need to feed some more tape to the machine!
        """
        goes_right: bool = self.configuration.goes_right
        goes_left: bool = not goes_right
        last_i: int = len(self.tape) - 1
        if goes_left and self.square_i == 0:
            self.tape.feed_left()
        elif goes_left:
            self.square_i -= 1
        elif goes_right and self.square_i == last_i:
            self.tape.feed_right()
            self.square_i += 1
        else:
            self.square_i += 1

    def change_state(self) -> None:
        self.state_i = self.configuration.state_i

    def __iter__(self) -> Iterator[Move]:
        return self

    def __next__(self):
        if self.state_i == 0:
            raise StopIteration
        self.scan()
        self.stamp()
        from_square_i = self.square_i
        from_state_i = self.state_i
        self.change_square()
        self.change_state()
        to_square_i = self.square_i
        to_state_i = self.state_i
        move = Move(
            [bool(s) for s in self.tape],
            from_square_i,
            to_square_i,
            from_state_i,
            to_state_i
        )
        return move

    def run(self) -> None:
        for move in self:
            pass

    def rewind(self) -> None:
        self.square_i = 0
        self.state_i = 1 # 0 means halt!
        if hasattr(self, 'configuration'):
            delattr(self, 'configuration')

class Operator:
    """We need an Operator if we want to look at the Moves of our Machine!

    Our Machine is automatic: it can run by itself!
    However, if we want to take a look at what it does,
    we need an operator that will record the moves.
    Imagine someone running the machine,
    taking a look at the tape at every stage,
    and recording what square and state we went to.
    """
    def __init__(self, machine: Machine = Machine()):
        self.machine: Machine = machine
        self.moves: list[Move] = []

    @classmethod
    def from_patterns(
        cls,
        tape_pattern: str,
        program_patterns: list[str]
    ) -> 'Operator':
        return cls(Machine.from_patterns(tape_pattern, program_patterns))

    def __str__(self) -> str:
        return f"Operator({self.machine})"

    def operate(self) -> None:
        self.moves = list(self.machine)

    def admire(
        self,
        header_fun: Callable[[list[bool], bool], str] =
             lambda x, y: 'Input' if y else 'Output',
        is_fancy: bool = True
    ) -> str:
        """Pretty print the tape!

        Once we feel it's time,
        we can take the tape out of the machine and admire it.
        """
        input_symbols: list[bool] = [bool(x) for x in self.machine.tape]
        header_above = header_fun(input_symbols, True)
        self.operate()
        output_symbols: list[bool] = [bool(x) for x in self.machine.tape]
        header_below = header_fun(output_symbols, False)
        headers = [f'State {move.from_state_i}' for move in self.moves]
        headers.insert(0, header_above)
        headers.append(header_below)
        rows = [move.to_table_row() for move in self.moves]
        rows.insert(0, Move(input_symbols, 0, 0, 1, 1).to_table_row(False))
        rows.append(Move(output_symbols, 0, 0, 1, 1).to_table_row(False))
        header_size = max(len(x) for x in headers) + 1
        empty_space = ' ' * header_size
        zipped = zip(headers, rows)
        lines = [f'{x.ljust(header_size)}{y}' for x, y in zipped]
        if is_fancy:
            r1 = list(rows[0].replace('x', 'o').replace('o', '\u2500'))
            r2 = list(rows[0].replace('x', 'o').replace('o', '\u2500'))
            r3 = list(rows[-1].replace('x', 'o').replace('o', '\u2500'))
            r4 = list(rows[-1].replace('x', 'o').replace('o', '\u2500'))
            r1[0], r1[-1] = '\u250c', '\u2510'
            r2[0], r2[-1] = '\u251c', '\u2524'
            r3[0], r3[-1] = '\u251c', '\u2524'
            r4[0], r4[-1] = '\u2514', '\u2518'
            s1 = empty_space + ''.join(r1).replace('\u2502', '\u252c')
            s2 = empty_space + ''.join(r2).replace('\u2502', '\u253c')
            s3 = empty_space + ''.join(r3).replace('\u2502', '\u253c')
            s4 = empty_space + ''.join(r4).replace('\u2502', '\u2534')
            lines.insert(0, s1)
            lines.insert(2, s2)
            lines.insert(-1, s3)
            lines.append(s4)
        return '\n'.join(lines)
