"""
https://adventofcode.com/2020/day/2
--- Day 2: Password Philosophy ---

Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via
toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we
can't log in!" You ask if you can take a look.

Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the
Official Toboggan Corporate Policy that was in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted
database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

Each line gives the password policy and then the password. The password policy indicates the lowest and highest
number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password
must contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but
needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of
their respective policies.

How many passwords are valid according to their policies?

Your puzzle answer was 454.

--- Part Two ---

While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate
Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job at
the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second
character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these
positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy
enforcement.

Given the same example list from above:

    1-3 a: abcde is valid: position 1 contains a and position 3 does not.
    1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
    2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

How many passwords are valid according to the new interpretation of the policies?

Your puzzle answer was 649.
"""


def puzzle_1(input_rules):
    valid_rules = 0

    for input_rule in input_rules:
        if is_p1_rule_valid(input_rule):
            valid_rules += 1

    print(valid_rules)


def puzzle_2(input_rules):
    valid_passwords = 0

    for input_rule in input_rules:
        if is_p2_password_valid(input_rule):
            valid_passwords += 1

    print(valid_passwords)


def get_password_rule(string_):
    rule_fields = string_.replace(':', '').split(' ')
    return rule_fields


def is_p1_rule_valid(input_rule):
    range_ = input_rule[0].split('-')
    low = int(range_[0])
    high = int(range_[1])
    character = input_rule[1]
    password = input_rule[2]

    if low <= password.count(character) and password.count(character) <= high:
        return True
    return False


def is_p2_password_valid(input_rule):
    range_ = input_rule[0].split('-')
    pos1 = int(range_[0]) - 1
    pos2 = int(range_[1]) - 1
    character = input_rule[1]
    password = input_rule[2]

    pass_pos1 = password[pos1] == character
    pass_pos2 = password[pos2] == character

    # XOR
    return pass_pos1 != pass_pos2


if __name__ == '__main__':
    input_rules = []
    with open('inputs/input_02.txt', 'r') as f_input:
        input_rules = [get_password_rule(line.strip()) for line in f_input.readlines()]

    puzzle_1(input_rules)
    puzzle_2(input_rules)
