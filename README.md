# TurMac: a Turing Machine emulation in object-oriented Python

## Introduction

Turing Machines are very interesting.
They don't seem to do much:
look at a bit of tape,
stamp something on it,
move to an adjacent section of that tape,
go into a state and then do some more of that,
perhaps in a slightly different way.
However, if we give it a tape
that has a pattern on it that has some meaning to us,
it can compute stuff by changing the pattern.
Once it is done (or has done enough),
we can look at the tape and interpret it.
If we know how to read the tape
(and how to program the machine!),
we can get answers,
that is, it can compute things for us.
What can it compute?
Perhaps everything as long as it is computable!

This project is not about any of the mathematical
or philosophical implications of Turing's ideas.
I just wanted to make some Turing-inspired Python objects,
that enabled me to do some emulated tape programming.
Object-oriented programming is especially well-suited for this.
It can be risky and sometimes tedious to keep track of state,
but it resembles what we would have had to do with a physical machine.

## How to use the Machine

The `examples.py` file contains a few examples of how to use
the objects that make up our Turing Machine emulation.
We can do some computation directly with the `Machine` object,
by calling the `.run()` method on one of its instances.
Let's take a look at this simple example:

```python
from turmac import *

machine = Machine(
    Tape(),
    Program([State(Behavior(True, True, 0), Behavior(False, True, 0))])
)
print(machine.tape) # will give us: `Tape([Square(False)])`
machine.run()
print(machine.tape) # now gives: `Tape([Square(True), Square(False)])`
```

We have created a simple program that takes the tape
and inverts the symbol (`True` will become `False` and vice versa).
Then, it extends the tape on the right side.
Finally, it goes into state `0` which will halt the machine.
We can simplify the creation of this machine
by using the shorthand notation defined in the `from_pattern`(`s`)
class methods:

```python
machine = Machine.from_patterns('o', ['xR0,oR0'])
```

This will do the same.
Now, if we want to have some prettier output
and also keep track of what moves the machine went through,
we can use the `Operator` class.
Imagine someone looking at the tape,
setting the machine in motion
and recording all to moves the machine makes
to finally show us all this information in a nice way.
Such an operator can be instantiation in a similar shorthand way:

```
from turmac import *

andrea = Operator.from_patterns('oo', ['xR0,oR0'])
print(andrea.admire()) # will run the machine and show it!
```

This will print out the following:

```txt
        ┌─┬─┐
Input   │o│o│
        ├─┼─┤
State 0 │x├o┤
        ├─┼─┤
Output  │x│o│
        └─┴─┘
```

This might not be very interesting,
but in `examples.py` we can see how we would create
a program that adds 2 numbers together.
We also exploit the fact that the `.admire()` method
takes as an extra argument a function
that can be used to display an interpretation of the tape.
Take a look at that code if you want to know more.
But here is an example of the output:

```txt
        ┌─┬─┬─┬─┬─┬─┬─┬─┐
4 1     │x│x│x│x│x│o│x│x│
        ├─┼─┼─┼─┼─┼─┼─┼─┤
State 0 │o├x┤x│x│x│o│x│x│
State 1 │o│x├x┤x│x│o│x│x│
State 2 │o│x│x├x┤x│o│x│x│
State 3 │o│x│x│x├x┤o│x│x│
State 4 │o│x│x│x│x├o┤x│x│
State 5 │o│x│x│x├x┤x│x│x│
State 4 │o│x│x├x┤x│x│x│x│
State 3 │o│x├x┤x│x│x│x│x│
State 2 │o├x┤x│x│x│x│x│x│
State 1 ├o┤x│x│x│x│x│x│x│
State 0 │o├x┤x│x│x│x│x│x│
State 1 │o│o├x┤x│x│x│x│x│
        ├─┼─┼─┼─┼─┼─┼─┼─┤
5       │o│o│x│x│x│x│x│x│
        └─┴─┴─┴─┴─┴─┴─┴─┘
```

Here we see how the machine moves through the tape
modifying the squares and going into different states.
A quick note on the numbers:
we have to interpret the tape that contains only `x`'s and `o`'s
in this representation.
We can say that 1 `x` stands for zero (or 0)
and 2 `x`'x stand for one (or 1).
From that point we can count on:

- `xxx` is 2
- `xxxx` is 3
- `xxxxx` is 4
- and so on...

If we then use `o` to separate the numbers,
we can interpret `xxxxxoxx` as `4 1`.
Adding them together would give us `5`.
Which is exactly what we see in the output example above.
We can create something similar with the code below:

```python
from turmac import *

def add_x(symbols: list[bool], is_above: bool) -> str:
    marks = ''.join( 'x' if p else 'o' for p in symbols)
    numbers = ' '.join(
        str(len(mark) - 1)
        for mark in marks.split('o')
        if len(mark) > 0
    )
    return numbers

tape = Tape.from_pattern('xxxxxoxx')
program = Program.from_patterns(['oR0,oR2', 'xL3,xR2', 'oR4,xL3', 'oR0,oR0'])
robin = Operator(Machine(tape, program))
print(robin.admire(add_x))
```

Note how the function `add_x()` is passed to the `.admire()` method
to make it output an interpretation of the numbers in
the output table.
Namely `4 1` and `5`:

```txt
        ┌─┬─┬─┬─┬─┬─┬─┬─┐
4 1     │x│x│x│x│x│o│x│x│
        ├─┼─┼─┼─┼─┼─┼─┼─┤
5       │o│o│x│x│x│x│x│x│
        └─┴─┴─┴─┴─┴─┴─┴─┘
```

## Acknowledgment

Many thanks to [EloiSanchez](https://github.com/EloiSanchez)
(at [Nimbus Intelligence](https://nimbusintelligence.com))
for looking at my code and helping out with ideas and suggestions.

I was also very much inspired by an online
[Stanford Encyclopedia of Philosophy article](https://plato.stanford.edu/entries/turing-machine/)
by Liesbeth De Mol.

*This project was created using Python 3.11.*
