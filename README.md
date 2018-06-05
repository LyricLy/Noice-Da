# Noice-Da
Fungeoid based on Galaxtone's Roie.

## Language
Noice-Da works in turns, and every program is a grid. Every program must be a rectangle of some kind, meaning right-padding with spaces is often needed.
There are a variable number of pointers that move every turn across and perform some operation.

Every turn, each pointer will perform an operation based on its current space, and then move forwards (if it hasn't been deleted). Each pointer also has a value, which is either 1 and 0, and a direction, which dictates where they move each turn.

### Operations

`n` - logical NOT and duplicator. Creates three other pointers moving away that have the opposite value as the current pointer.

`o` - output as a single bit. Output is described later.

`i` - take input as a single bit. Input is described later.

`c` - destroy the pointer if its value is 0, otherwise do nothing.

`e` - logical OR with three values. If there are two other pointers here, perform OR on all of the pointers, delete said pointers and send the result to the only side not hit by a pointer going in. Otherwise, stop moving and wait for more pointers.

` ` - perform no operation.

`d` - delay. Do not move this turn.

`a` - close the program.

### Input / Output and flags
Input is handled with a buffer, which at the start is empty. Every time input is taken, it is taken from the buffer. If the buffer is empty, new input will be taken and placed into the buffer. Output is done in a similar way. The buffer is originally empty, and output is only performed once the buffer is full. Both buffers are by default 8-bit, and input is taken as a character code point. 

However, with the `-i` and `-o` flags, it is possible to change the size of the buffers.

The `-i` flag defaults to `c`, for character input, and can be changed to an integer to change input to numbers of n-bits. For example, for a program that performs logical OR, it would be most convenient to run it with `-i 1`, to make it so that input is taken as 1-bit numbers (0 and 1) as only 0 and 1 are expected to be input. For a larger, more complicated program such as addition, you would probably need a number with more bits, such as 8 or 16.

The `-o` flag defaults to `d`, which will set it to the same setting as whatever `-i` is set to. It has the same function as the `-i` flag except for input, and in most cases leaving it at `d` and only changing `-i` is sufficient.

There is also a `-d` flag for debugging, which will show you the movement of the pointers as the program is executed.
