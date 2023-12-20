"""
--- Day 8: Haunted Wasteland ---
You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you 
turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about 
ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) 
about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents 
contains a list of left/right instructions, and the rest of the documents seem to describe some kind of 
network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have 
the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are 
now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
Starting with AAA, you need to look up the next element based on the next left/right instruction in your 
input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L 
means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 
steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole 
sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is 
a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

"""


def prob1():
    directions, dict = getDirectionsDict("day08_input.txt")
    # now follow directions until we get to ZZZ
    current = 'AAA'
    steps = 0
    while (current != 'ZZZ'):
        for d in directions:
            steps += 1
            if (d == 'L'):
                current = dict[current][0]
            else:
                current = dict[current][1]
            if current == 'ZZZ':
                break
    return steps


def getDirectionsDict(file):
    dict = {}
    with open(file) as f:
        lines = f.readlines()
        directions = lines[0].replace("\n", "")
        for line in lines[2:]:
            # save in a dictionary where the key is the location - the value is an array [left, right]
            # remove punctuation
            line = line.replace(",", "").replace(
                "=", "").replace("(", "").replace(")", "")
            line = line.split()
            dict[line[0]] = [line[1], line[2]]

    return (directions, dict)


"""
--- Part Two ---
The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow 
the instructions, but you've barely left your starting position. It's going to take significantly more 
steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of 
spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with 
names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at 
every node that ends with A and follow all of the paths at the same time until they all simultaneously end 
up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each 
left/right instruction, use that instruction to simultaneously navigate away from both nodes you're 
currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the 
nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would 
proceed as follows:

Step 0: You are at 11A and 22A.
Step 1: You choose all of the left paths, leading you to 11B and 22B.
Step 2: You choose all of the right paths, leading you to 11Z and 22C.
Step 3: You choose all of the left paths, leading you to 11B and 22Z.
Step 4: You choose all of the right paths, leading you to 11Z and 22B.
Step 5: You choose all of the left paths, leading you to 11B and 22C.
Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes 
that end with Z?
"""


def prob2():
    directions, dict = getDirectionsDict("day08_input.txt")
    currents = endsInA(dict)
    # brute forcing takes a billion years, instead find # steps for each location in currents to get to a
    # location ending in z and then find least common multiple of all the steps
    steps = [getSteps(i, dict, directions) for i in currents]
    return lcm(steps)


def lcm(numbers):
    # if numbers = a, b, c then lcm(a, b, c) = lcm(a, lcm(b, c))
    if len(numbers) == 2:
        return int((numbers[0] * numbers[1]) / gcd(numbers[0], numbers[1]))
    elif len(numbers) > 2:
        num2 = lcm(numbers[1:])
        return int((numbers[0] * num2) / gcd(numbers[0], num2))


def gcd(a, b):
    while (a % b > 0):
        r = a % b
        a = b
        b = r
    return b


def endsInA(dictionary):
    # returns a list of all keys that end in A
    a = []
    for k in dictionary.keys():
        if k[-1] == 'A':
            a.append(k)
    return a


def getSteps(current, dictionary, directions):
    # given currentn location, find how many steps it takes (following the directions)
    # to get to a location that ends in Z
    steps = 0
    while (current[-1] != 'Z'):
        for d in directions:
            steps += 1
            if (d == 'L'):
                current = dictionary[current][0]
            else:
                current = dictionary[current][1]
            if (current[-1] == 'Z'):
                break
    return steps


if __name__ == "__main__":
    print(prob1())
    print(prob2())
