"""
https://adventofcode.com/2020/day/7
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some
food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents;
bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible
for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant
plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be
valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

 - A bright white bag, which can hold your shiny gold bag directly.
 - A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
 - A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny
   gold bag.
 - A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold
   bag.

So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag?

Your puzzle answer was 274.

--- Part Two ---

It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of
bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

    faded blue bags contain 0 other bags.
    dotted black bags contain 0 other bags.
    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the
11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all
of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?

Your puzzle answer was 158730.

"""

import advent_utils

TARGET_BAG = 'shiny gold'


def puzzle_1(bag_rules):
    bag_count = 0

    for bag_rule in bag_rules:
        if bag_rule != TARGET_BAG:
            if fits_bag(bag_rules, bag_rule):
                bag_count += 1

    return bag_count


def puzzle_2(bag_rules):
    inner_bags = bag_rules[TARGET_BAG]

    total_bag_count = 0
    for inner_bag in inner_bags:
        total_bag_count += count_inner_bags(bag_rules, inner_bag['bag_color'], inner_bag['amount'])

    return total_bag_count


def fits_bag(bag_rules, bag_rule):
    if bag_rule == TARGET_BAG:
        return True
    if len(bag_rules[bag_rule]) == 0:
        return False
    fits_in_children = False
    for new_bag_rule in bag_rules[bag_rule]:
        if new_bag_rule['bag_color'] == TARGET_BAG:
            return True

        fits_in_children = fits_in_children or fits_bag(bag_rules, new_bag_rule['bag_color'])

    return fits_in_children


def count_inner_bags(bag_rules, bag_color, count):
    if len(bag_rules[bag_color]) == 0:
        return count

    level_count = 0
    for inner_bag_rule in bag_rules[bag_color]:
        level_count += count_inner_bags(bag_rules, inner_bag_rule['bag_color'], inner_bag_rule['amount'])

    return level_count * count + count


def load_bag_rules_from_data(input_data):
    bag_rules = {}

    for line in input_data:
        k, v = load_bag_rule_from_data(line.strip())
        bag_rules[k] = v

    return bag_rules


def get_parse_edge(adjacent_pattern):
    return lambda txt: adjacent_pattern.search(txt).groups()


def load_bag_rule_from_data(bag_rule_data):
    bag_rule_data = bag_rule_data.replace('bags', '').replace('bag', '').replace('.', '')
    bag_rule_parts = bag_rule_data.split(' contain ')

    bag_key = bag_rule_parts[0].strip()
    bags_contained_data = bag_rule_parts[1]
    bags_contained_data = bags_contained_data.replace('no other', '')
    bags_contained_data = bags_contained_data.split(',')

    bags_contained = []
    for bag_contained in bags_contained_data:
        bag_contained = bag_contained.strip()
        amount = 0
        bag = None
        if len(bag_contained) > 0:
            amount = bag_contained[0]
            bag = bag_contained[2:]
        if bag:
            bags_contained.append({
                'bag_color': bag,
                'amount': int(amount),
            })

    return (bag_key, bags_contained)


if __name__ == '__main__':
    input_data = advent_utils.load_input_from_file('inputs/input_07.txt')
    # input_data = advent_utils.load_input_from_file('inputs/test_07.txt')

    bag_rules = load_bag_rules_from_data(input_data)

    print('puzzle_1: {s}'.format(s=puzzle_1(bag_rules)))
    print('puzzle_2: {s}'.format(s=puzzle_2(bag_rules)))
