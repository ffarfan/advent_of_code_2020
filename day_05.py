"""
https://adventofcode.com/2020/day/5
--- Day 5: Binary Boarding ---

You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is
yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport
control.

You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input);
perhaps you can find your seat through process of elimination.

Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like
FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0
through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows;
the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next
letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

    Start by considering the whole range, rows 0 through 127.
    F means to take the lower half, keeping rows 0 through 63.
    B means to take the upper half, keeping rows 32 through 63.
    F means to take the lower half, keeping rows 32 through 47.
    B means to take the upper half, keeping rows 40 through 47.
    B keeps rows 44 through 47.
    F keeps rows 44 through 45.
    The final F keeps the lower of the two, row 44.

The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane
(numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the
lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

    Start by considering the whole range, columns 0 through 7.
    R means to take the upper half, keeping columns 4 through 7.
    L means to take the lower half, keeping columns 4 through 5.
    The final R keeps the upper of the two, column 5.

So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID
44 * 8 + 5 = 357.

Here are some other boarding passes:

    BFFFBBFRRR: row 70, column 7, seat ID 567.
    FFFBBBFRRR: row 14, column 7, seat ID 119.
    BBFFBBFRLL: row 102, column 4, seat ID 820.

As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?

Your puzzle answer was 965.

--- Part Two ---

Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a
catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing
from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?

Your puzzle answer was 524.
"""

import advent_utils

AIRPLANE_ROWS = 128
AIRPLANE_COLS = 8

BACK = 'B'
FRONT = 'F'
RIGHT = 'R'
LEFT = 'L'


def puzzle_1(boarding_passes):
    max_id = 0
    for boarding_pass in boarding_passes:
        if boarding_pass['seat_id'] > max_id:
            max_id = boarding_pass['seat_id']

    return max_id


def puzzle_2(boarding_passes):
    seat_ids = []
    for boarding_pass in boarding_passes:
        seat_ids.append(boarding_pass['seat_id'])

    seat_ids = sorted(seat_ids)
    start_seat_id = seat_ids[0]

    for expected_seat_id, seat_id in enumerate(seat_ids, start=start_seat_id):
        if expected_seat_id != seat_id:
            return expected_seat_id


def load_boarding_passes_from_data(input_data):
    boarding_passes = [load_boarding_pass_from_data(line) for line in input_data]

    return boarding_passes


def load_boarding_pass_from_data(boarding_pass_data):
    row = get_position(boarding_pass_data[:7], 0, 0, AIRPLANE_ROWS, BACK, FRONT)
    col = get_position(boarding_pass_data[-3:], 0, 0, AIRPLANE_COLS, RIGHT, LEFT)

    boarding_pass = {
        'row': row,
        'column': col,
        'seat_id': row * 8 + col,
    }

    return boarding_pass


def get_position(seat_data, seat_data_idx, start, stop, left_bound, right_bound):
    if start == stop - 1:
        return start
    else:
        delta = int((stop - start) / 2)
        if seat_data[seat_data_idx] == left_bound:
            start += delta
        elif seat_data[seat_data_idx] == right_bound:
            stop -= delta

        seat_data_idx = seat_data_idx + 1

        return get_position(seat_data, seat_data_idx, start, stop, left_bound, right_bound)


if __name__ == '__main__':
    input_data = advent_utils.load_input_from_file('inputs/input_05.txt')
    boarding_passes = load_boarding_passes_from_data(input_data)

    print('puzzle_1: {s}'.format(s=puzzle_1(boarding_passes)))
    print('puzzle_2: {s}'.format(s=puzzle_2(boarding_passes)))
