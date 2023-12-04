"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water 
source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone!
 The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. 
If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of 
numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, 
is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) 
and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine 
schematic?
"""


def prob1():
    schematic = getSchematic("day03_input.txt")
    total = 0
    # find numbers
    for row in range(len(schematic)):
        numbers = getNumbers(schematic[row])
        for (start, end, num) in numbers:
            if isPartNumber(start, end, schematic, row):
                total += num
    return total


def getSchematic(file):
    schematic = []
    with open(file) as f:
        for line in f.readlines():
            arr = [char for char in line if char != '\n']
            schematic.append(arr)

    return schematic


def getNumbers(array):
    # get numbers in the character array 'array'
    numbers = []
    isInNumber = False
    startIndex = 0
    endIndex = 0
    num = ""
    for c in range(len(array)):
        if (isDigit(array[c])):
            # if continuing the current number
            if (isInNumber):
                endIndex += 1
                num += array[c]
            # else is starting a new number
            else:
                isInNumber = True
                startIndex = endIndex = c
                num += array[c]
        # else is not a digit but is ending the current num - finish and add to numbers
        elif (isInNumber):
            isInNumber = False
            numbers.append((startIndex, endIndex, int(num)))
            num = ""

    # make sure it adds any numbers that are at the end of the line!!
    if (isInNumber):
        numbers.append((startIndex, endIndex, int(num)))

    return numbers


def isPartNumber(start, end, schematic, row):
    # given a number in schematic[row][col] starting at index 'start' and ending at 'end'
    # is it adjacent to a symbol?
    for i in range(start, end + 1):
        adjacents = getAdjacentChars(i, schematic, row)
        for c in adjacents:
            if ((not isDigit(c)) and c != '.'):
                return True

    return False


def isDigit(character):
    return str(character) in "0123456789"


def getAdjacentChars(index, schematic, row):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    chars = []
    for (dx, dy) in directions:
        if ((0 <= row + dx < len(schematic)) and (0 <= index + dy < len(schematic[row]))):
            chars.append(schematic[row + dx][index + dy])
    return chars


"""
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump
in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a 
phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, 
holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the 
station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that 
is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out 
which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its 
gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 
is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

"""


def prob2():
    schematic = getSchematic("day03_input.txt")
    numbers = []
    # find and store numbers and their start and end indices
    for row in range(len(schematic)):
        numbers.append(getNumbers(schematic[row]))

    # look for a star, get gear ratio at each star and sum them all up
    ratios = 0
    for row in range(len(schematic)):
        for col in range(len(schematic[row])):
            if schematic[row][col] == '*':
                ratios += getGearRatio(schematic, row, col, numbers)

    return ratios


def getGearRatio(schematic, row, col, numbers):
    # list of tuples representing parts in the form (startIndex, endIndex, number)
    parts = set()

    # find all gears adjacent to star in schematic[row][col] - if are exactly 2, return product
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    for (dx, dy) in directions:
        # if theres a number at the adj. index, add it to parts
        num = isNumberAt(schematic, row + dx, col + dy, numbers)
        if (num):
            parts.add(num)

    if (len(parts) == 2):
        return parts.pop()[2] * parts.pop()[2]
    else:
        return 0


def isNumberAt(schematic, row, col, numbers):
    # is there a number that occupies schematic[row][col] ?
    # if not valid coords, return none
    if (not (0 <= row < len(schematic) and 0 <= col < len(schematic[row]))):
        return None

    for (start, end, num) in numbers[row]:
        if (start <= col and end >= col):
            return (start, end, num)

    return None


if __name__ == "__main__":
    print(prob1())
    print(prob2())
