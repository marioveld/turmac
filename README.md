# TurMac: a Turing Machine emulation in object-oriented Python

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
