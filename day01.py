"""
--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""


def prob1():
    # get calibtration val from each line and add them all up
    total = 0
    with open("day01_input.txt", "r") as f:
        for line in f.readlines():
            total += getCalibration(line)
    return total


def getCalibration(string):
    # find all indices in 'line' that are digits, then concat first and last to get calibration
    indices = []  # indices w/ digits at them
    for i in range(len(string)):
        if string[i].isdigit():
            indices.append(i)
    return int(string[indices[0]] + string[indices[-1]])


"""
--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

# GOT IT !!! overlapping strings of numbers BOTH count, so twone counts as two AND one
# just replace so that first/last letters in spelled numbers dont change, so overlaps dont mess up anything


def prob2():
    # get calibtration val from each line and add them all up
    total = 0
    with open("day01_input.txt", "r") as f:
        for line in f.readlines():
            total += getTrueCalibration(line)
    return total


# jk doesnt replace in order, will have to go thru one by one
def getTrueCalibration(string):
    string = spelledToRealDigits(string, 0)
    return getCalibration(string)


def replaceSpelledDigit(string, index):
    # replace spelled digit in string at index w/ actual digit
    stringNums = ["one", "two", "three", "four",
                  "five", "six", "seven", "eight", "nine"]
    digNums = ["o1e", "t2o", "th3ee", "f4ur",
               "f5ve", "s6x", "se7en", "ei8ht", "n9ne"]
    for i in range(len(stringNums)):
        if (string.find(stringNums[i]) == index):
            # replace first occurence of stringNums[i] w/ digNums[i]
            return string.replace(stringNums[i], digNums[i], 1)

    return string


def spelledToRealDigits(string, index):
    if (index >= len(string)):
        return string
    string = replaceSpelledDigit(string, index)
    return spelledToRealDigits(string, index + 1)


if __name__ == "__main__":
    print(prob1())
    print(prob2())
