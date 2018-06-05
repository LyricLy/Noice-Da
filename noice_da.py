import sys
import argparse

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Pointer:
    def __init__(self, matrix, direction=0, value=0, coordinates=[0, 0]):
        self.direction = direction
        self.value = value
        self.moving = True
        self.coordinates = coordinates
        self.matrix = matrix
        self.exists = True
        self.move_this = True

    def __repr__(self):
        return [">", "v", "<", "^"][self.direction]

    def move(self):
        if self.moving:
            self.coordinates[0] += DIRECTIONS[self.direction][0]
            self.coordinates[1] += DIRECTIONS[self.direction][1]

    def place(self):
        if any([x < 0 for x in self.coordinates]):
            self.exists = False
            return
        try:
            return self.matrix[self.coordinates[0]][self.coordinates[1]]
        except IndexError:
            self.exists = False
            return

    def displace(self, dir):
        try:
            return [self.coordinates[0] + DIRECTIONS[dir][0], self.coordinates[1] + DIRECTIONS[dir][1]]
        except IndexError:
            return [-2, -2]  # any area out of range acts the same

    def displace_turn(self, turn):
        dir = (self.direction + turn) % len(DIRECTIONS)
        try:
            return [self.coordinates[0] + DIRECTIONS[dir][0], self.coordinates[1] + DIRECTIONS[dir][1]]
        except IndexError:
            return [-2, -2]

def print_pointers(pointers):
    print()
    map = [[[x for x in pointers if x.coordinates == [x_idx, y_idx]][0] if [x_idx, y_idx] in [x.coordinates for x in pointers] else "-" for y_idx, y in enumerate(x)] for x_idx, x in enumerate(pointers[0].matrix)] if pointers else []
    for x in map:
        for y in x:
            print(y, end=" ")
        print("\n")

def interpret_noice_de(program, stdin, stdout, input_type, output_type, debug):
    matrix = program.splitlines()
    if len(set([len(x) for x in matrix])) != 1:
        print("matrix not rectangular")
        return 1
    pointers = [Pointer(matrix)]

    output_type = input_type if output_type == "d" else output_type
    output_buffer = ""
    input_buffer = ""

    while True:
        if debug:
            print_pointers(pointers)
        if not [x for x in pointers if x.moving]:
            return 0
        for pointer in pointers:
            instr = pointer.place()
            if not pointer.exists:
                pointers.remove(pointer)
                continue
            if instr == "n":
                pointers.append(Pointer(matrix, 
                                        (pointer.direction - 1) % len(DIRECTIONS), 
                                        not pointer.value,
                                        pointer.displace_turn(-1)))
                pointers.append(Pointer(matrix, 
                                        pointer.direction, 
                                        not pointer.value,
                                        pointer.displace_turn(0)))
                pointers.append(Pointer(matrix, 
                                        (pointer.direction + 1) % len(DIRECTIONS), 
                                        not pointer.value,
                                        pointer.displace_turn(1)))
                pointers.remove(pointer)
            elif instr == "o":
                output_buffer += str(int(pointer.value))
                if output_type == "c":
                    if len(output_buffer) == 8:
                        stdout.write(chr(int(output_buffer, 2)))
                        stdout.flush()
                        output_buffer = ""
                elif output_type.isdigit():
                    if len(output_buffer) == int(output_type):
                        stdout.write(str(int(output_buffer, 2)))
                        stdout.flush()
                        output_buffer = ""
                else:
                    print("Invalid output type.")
                    return 1
            elif instr == "i":
                if not input_buffer:
                    if input_type == "c":
                        input_buffer = bin(ord(stdin.read(1)))[2:].zfill(8)
                    elif input_type.isdigit():
                        try:
                            given_input = bin(int(stdin.readline()))[2:]
                        except ValueError:
                            print(f"invalid input, expected a {input_type}-bit number but received a string")
                            return 1
                        if len(given_input) > int(input_type):
                            print(f"invalid input, expected a {input_type}-bit number but received a {len(given_input)}-bit number")
                            return 1
                        input_buffer = given_input.zfill(int(input_type))
                    else:
                        print("Invalid input type.")
                        return 1
                pointer.value = int(input_buffer[0])
                input_buffer = input_buffer[1:]
            elif instr == "c":
                if not pointer.value:
                    pointers.remove(pointer)
            elif instr == "e":
                pointer.moving = False
                other_pointers = [x for x in pointers if x.coordinates == pointer.coordinates]
                directions = [x.direction for x in other_pointers]
                if len(set(directions)) == 3:
                    ored_pointers = []
                    for dir in set(directions):
                        ored_pointers.append([x for x in other_pointers if x.direction == dir][0])
                    result = any([x.value for x in ored_pointers])
                    result_direction = ([x for x in (0, 1, 2, 3) if x not in directions][0] + 2) % len(DIRECTIONS)
                    pointers.append(Pointer(matrix, 
                                            result_direction, 
                                            result, 
                                            pointer.displace(result_direction)))
                    for ored_pointer in ored_pointers:
                        pointers.remove(ored_pointer)
            elif instr == " ":
                pass
            elif instr == "d":
                if pointer.move_this:
                    pointer.move_this = False
                else:
                    pointer.move_this = True
            elif instr == "a":
                return 0
            else:
                print("Invalid character found.")
                return 1
            if pointer.move_this:
                pointer.move()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", 
                        help="Filename to interpret.")
    parser.add_argument("-i", "--input", 
                        help="Method to take input. Can be c for string input, or an integer for n-bit integer input.",
                        default="c")
    parser.add_argument("-o", "--output", 
                        help="Method to take output. Can be d for the same as input, c for string output, or an integer for n-bit integer output.",
                        default="d")
    parser.add_argument("-d", "--debug",
                        help="Print debug information.",
                        action="store_true")
    args = parser.parse_args()

    with open(args.filename) as f:
        program = f.read()
    result = interpret_noice_de(program, sys.stdin, sys.stdout, args.input, args.output, args.debug)
    sys.exit(result)
