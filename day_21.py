"""
https://adventofcode.com/2020/day/21
--- Day 21: Allergen Assessment ---

You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't
even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your
journey.

You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in
a language you do understand. You should be able to use this information to determine which ingredient contains which
allergen and work out which foods are safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's
ingredients list followed by some or all of the allergens the food contains.

Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always
marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains
each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed,
the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was
labeled in a language you don't know.

For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and
nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward:
dairy and fish.

The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list.
In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of
times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which
appears twice.

Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those
ingredients appear?

Your puzzle answer was 2635.

--- Part Two ---

Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient
contains which allergen.

In the above example:

  - mxmxvkd contains dairy.
  - sqjhc contains fish.
  - fvjkl contains soy.

Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous
ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) In the above example,
this would be mxmxvkd,sqjhc,fvjkl.

Time to stock your raft with supplies. What is your canonical dangerous ingredient list?

Your puzzle answer was xncgqbcp,frkmp,qhqs,qnhjhn,dhsnxr,rzrktx,ntflq,lgnhmx.

"""

from collections import defaultdict
import re

import z3

import advent_utils


def puzzle_1(all_ingredients, all_allergens):
    total = 0
    inert_ingredients = set()

    for ingredient, ing_values in all_ingredients.items():
        is_allergen = False
        for allergen, all_values in all_allergens.items():
            if all_values < ing_values:
                is_allergen = True
        if not is_allergen:
            total += len(all_ingredients[ingredient])
            inert_ingredients.add(ingredient)

    return total, inert_ingredients


def puzzle_2(all_ingredients, all_allergens, inert_ingredients):
    possible_ingredients = list(set(all_ingredients.keys()) - inert_ingredients)
    possible_allergens = list(set(all_allergens.keys()))

    solver = z3.Solver()

    assignments = z3.IntVector('allergen', len(possible_allergens))
    for assignment in assignments:
        solver.add(0 <= assignment)
        solver.add(assignment < len(possible_allergens))
    solver.add(z3.Distinct(assignments))

    for ai, allergen in enumerate(possible_allergens):
        conditions = []
        for ii, ingredient in enumerate(possible_ingredients):
            if all_ingredients[ingredient] >= all_allergens[allergen]:
                conditions.append(assignments[ii] == ai)
        solver.add(z3.Or(conditions))

    solver.check()
    model = solver.model()

    matches = []
    for ii, _ in enumerate(assignments):
        matches.append((possible_allergens[model.evaluate(assignments[ii]).as_long()], possible_ingredients[ii]))

    matches.sort()
    return(','.join(match[1] for match in matches))


def load_recipes(input_data):
    all_ingredients = defaultdict(set)
    all_allergens = defaultdict(set)

    for i, line in enumerate(input_data):
        ingredients, allergens = line.split('contains', 1)
        ingredients = re.findall(r'\w+', ingredients)
        allergens = re.findall(r'\w+', allergens)

        for ingredient in ingredients:
            all_ingredients[ingredient].add(i)
        for allergen in allergens:
            all_allergens[allergen].add(i)

    return all_ingredients, all_allergens


if __name__ == '__main__':
    input_data = advent_utils.load_input_from_file('inputs/input_21.txt')
    # input_data = advent_utils.load_input_from_file('inputs/test_21.txt')
    all_ingredients, all_allergens = load_recipes(input_data)

    count, inert = puzzle_1(all_ingredients, all_allergens)
    print('puzzle_1: {s}'.format(s=count))
    print('puzzle_2: {s}'.format(s=puzzle_2(all_ingredients, all_allergens, inert)))
