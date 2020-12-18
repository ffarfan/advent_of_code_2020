"""
https://adventofcode.com/2020/day/18
--- Day 18: Operation Order ---

As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted
by the child sitting next to you. They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*),
and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before
it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator,
and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the
operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71

Parentheses can override this order; for example, here is what happens if parentheses are added to form
1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51

Here are a few more examples:

  - 2 * 3 + (4 * 5) becomes 26.
  - 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
  - 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
  - ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the
homework; what is the sum of the resulting values?

Your puzzle answer was 16332191652452.

--- Part Two ---

You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the
next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with.
Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231

Here are the other examples from above:

  - 1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
  - 2 * 3 + (4 * 5) becomes 46.
  - 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
  - 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
  - ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

What do you get if you add up the results of evaluating the homework problems using these new rules?

"""

import advent_utils


def puzzle_1(input_data):
    result = 0

    for expression in input_data:
        result += calculate_1(expression)

    return result


def puzzle_2(input_data):
    result = 0

    for expression in input_data:
        result += calculate_2(expression)

    return result


def calculate_1(expression):
    val_stack = []
    op_stack = []

    for current in expression.split():
        if current.isdigit():
            if op_stack and op_stack[-1] in '+*':
                exec_operation_1(val_stack, op_stack, int(current))
            else:
                val_stack.append(int(current))
        elif current in '+*(':
            op_stack.append(current)
        elif current == ')':
            if op_stack and op_stack[-1] == '(':
                op_stack.pop()
            if op_stack and op_stack[-1] in '+*':
                exec_operation_1(val_stack, op_stack, val_stack.pop())

    return val_stack[0]


def calculate_2(expression):
    val_stack = []
    op_stack = []

    for current in expression.split():
        if current.isdigit():
            val_stack.append(int(current))
        elif current == '*':
            if op_stack and op_stack[-1] in '*+':
                exec_operation_2(val_stack, op_stack)
            op_stack.append(current)
        elif current == '+':
            if op_stack and op_stack[-1] == '+':
                exec_operation_2(val_stack, op_stack)
            op_stack.append(current)
        elif current == '(':
            op_stack.append('(')
        elif current == ')':
            while op_stack and op_stack[-1] in '*+':
                exec_operation_2(val_stack, op_stack)
            if op_stack and op_stack[-1] == '(':
                op_stack.pop()
            while op_stack and op_stack[-1] == '+':
                exec_operation_2(val_stack, op_stack)
    while op_stack and op_stack[-1] in '*+':
        exec_operation_2(val_stack, op_stack)

    return val_stack[0]


def exec_operation_1(val_stack, op_stack, number):
    val_stack[-1] = val_stack[-1] * number if op_stack.pop() == '*' else val_stack[-1] + number


def exec_operation_2(val_stack, op_stack):
    n = val_stack.pop()
    val_stack[-1] = val_stack[-1] * n if op_stack.pop() == '*' else val_stack[-1] + n


if __name__ == '__main__':
    input_data = advent_utils.load_input_from_file('inputs/input_18.txt')
    # input_data = advent_utils.load_input_from_file('inputs/test_18.txt')

    # Make life easier while sweeping string
    input_data = [line.replace('(', '( ').replace(')', ' )') for line in input_data]

    print('puzzle_1: {s}'.format(s=puzzle_1(input_data)))
    print('puzzle_2: {s}'.format(s=puzzle_2(input_data)))
