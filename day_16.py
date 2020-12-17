"""
https://adventofcode.com/2020/day/16
--- Day 16: Ticket Translation ---

As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is
on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should
probably figure out what it says before you get to the train station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure
out the fields these tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the
same train service (via the airport security cameras) together into a single document you can reference (your puzzle
input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values
for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class
and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the
order they appear; every ticket has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'

Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,
303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've
extracted just the numbers in such a way that the first number is always the same specific field, the second number is
always a different specific field, and so on - you just don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for
any field. Ignore your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12

It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only
whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket
are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are
are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate:
4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

Your puzzle answer was 22073.

--- Part Two ---

Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid
tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent
between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9

Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and
the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What
do you get if you multiply those six values together?

Your puzzle answer was 1346570764607.

"""

import collections
import re


def puzzle_1(ticket_notes, nearby_tickets):
    ticket_error_rate = 0

    for ticket in nearby_tickets:
        ticket_error_rate += scan_ticket(ticket_notes, ticket)

    return ticket_error_rate


def puzzle_2(ticket_notes, my_ticket, nearby_tickets):
    valid_tickets = [my_ticket]

    for ticket in nearby_tickets:
        if scan_ticket(ticket_notes, ticket) == 0:
            valid_tickets.append([int(ln) for ln in ticket.split(',')])

    over_under = collections.defaultdict(list)
    num_fields = len(valid_tickets[0])
    for field in range(num_fields):
        over_under[field] = [ticket[field] for ticket in valid_tickets]

    memory = {}
    assign = {}
    assign_back = {}
    while len(ticket_notes) > len(assign):
        for field_idx in range(num_fields):
            if field_idx in assign_back.keys():
                continue
            ticket = []
            for field_name in ticket_notes.keys():
                if field_name in assign.keys():
                    continue
                if can_match(ticket_notes, over_under, memory, field_name, field_idx):
                    ticket.append(field_name)
            if len(ticket) == 1:
                assign[ticket[0]] = field_idx
                assign_back[field_idx] = ticket[0]

    product = 1
    for field_name, field_idx in assign.items():
        if field_name.startswith('departure'):
            print(field_name, my_ticket[field_idx])
            product *= my_ticket[field_idx]

    return product


def scan_ticket(ticket_notes, ticket):
    ticket_error_rate = 0
    all_ticket_ranges = []
    for ticket_note in ticket_notes:
        all_ticket_ranges.extend(ticket_notes[ticket_note])

    nums = [int(ln) for ln in ticket.split(',')]
    for num in nums:
        if any(a <= num <= b for a, b in all_ticket_ranges):
            pass
        else:
            ticket_error_rate += num

    return ticket_error_rate


def can_match(ticket_notes, over_under, memory, field_name, field_idx):
    k = (field_name, field_idx)
    if k in memory:
        return memory[k]
    match = all(any(a <= v <= b for a, b in ticket_notes[field_name]) for v in over_under[field_idx])
    memory[k] = match

    return match


def parse_data(filename):
    ranges, my_ticket, nearby_tickets = [line.rstrip('\n') for line in open(filename).read().split('\n\n')]

    ticket_notes = collections.defaultdict(list)
    for line in ranges.splitlines():
        note = line.split(': ')[0]
        for a, b in re.findall(r'(\d+)-(\d+)', line):
            ticket_notes[note].append((int(a), int(b)))

    my_ticket = [int(num) for num in my_ticket.splitlines()[1].split(',')]
    nearby_tickets = nearby_tickets.splitlines()[1:]

    return ticket_notes, my_ticket, nearby_tickets


if __name__ == '__main__':
    filename = 'inputs/input_16.txt'
    # filename = 'inputs/test_16_1.txt'
    # filename = 'inputs/test_16_2.txt'

    ticket_notes, my_ticket, nearby_tickets = parse_data(filename)

    print('puzzle_1: {s}'.format(s=puzzle_1(ticket_notes, nearby_tickets)))
    print('puzzle_2: {s}'.format(s=puzzle_2(ticket_notes, my_ticket, nearby_tickets)))
