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

"""

import collections
import re


def puzzle_1(ticket_data):
    ticket_error_rate = 0
    for ticket in ticket_data['nearby_tickets']:
        ticket_error_rate += scan_ticket(ticket_data, ticket)

    return ticket_error_rate


def puzzle_2(ticket_data):
    valid_tickets = []
    my_ticket = ticket_data['my_ticket']

    for ticket in ticket_data['nearby_tickets']:
        if scan_ticket(ticket_data, ticket) == 0:
            valid_tickets.append(ticket)

    note_order = {}
    for i in range(len(ticket_data['ticket_notes'])):
        note_order[i] = set()

    for ticket in valid_tickets:
        for i, ticket_value in enumerate(ticket):
            notes = set()
            for note in ticket_data['ticket_notes']:
                for note_value in ticket_data['ticket_notes'][note]:
                    if is_value_in_range(ticket_value, note_value):
                        notes.add(note)
            if len(note_order[i]) == 0:
                note_order[i] = notes
            else:
                note_order[i] = note_order[i].intersection(notes)

    for note in ticket_data['ticket_notes']:
        note_ = []
        for ni in note_order:
            if note in note_order[ni]:
                note_.append(ni)

        print(note, note_)

    print(note_order)
    departure_value = 1

    for ticket_note in ticket_data['ticket_notes']:
        if ticket_note.startswith('departure'):
            departure_value *= my_ticket[note_order[ticket_note]]

    return departure_value


def scan_ticket(ticket_data, ticket):
    for ticket_value in ticket:
        value_found = False
        for note in ticket_data['ticket_notes']:
            for note_value in ticket_data['ticket_notes'][note]:
                if is_value_in_range(ticket_value, note_value):
                    value_found = True
                    break

        if not value_found:
            return ticket_value

    return 0


def parse_tickets_from_data(input_data):
    ticket_data = {
        'ticket_notes': {},
        'my_ticket': [],
        'nearby_tickets': []
    }

    reading_properties = True
    reading_ticket = False
    reading_nearby_tickets = False
    for line in input_data:
        if reading_properties:
            if line == '':
                reading_properties = False
                reading_ticket = True
            else:
                props = line.split(':')
                ticket_data['ticket_notes'][props[0]] = props[1].split(' or ')
        elif reading_ticket:
            if line == 'your ticket:':
                pass
            elif line == '':
                reading_ticket = False
                reading_nearby_tickets = True
            else:
                ticket_data['my_ticket'] = [int(v) for v in line.split(',')]
        elif reading_nearby_tickets:
            if line == 'nearby tickets:' or line == '':
                pass
            else:
                ticket_data['nearby_tickets'].append([int(v) for v in line.split(',')])

    return ticket_data


def is_value_in_range(the_value, the_range):
    min_val, max_val = [int(v) for v in the_range.split('-')]
    return min_val <= the_value <= max_val


def parse_data(filename):
    ranges, my_ticket, nearby_tickets = [line.rstrip('\n') for line in open(filename).read().split('\n\n')]

    note_ranges = []
    ticket_notes = collections.defaultdict(list)
    for line in ranges.splitlines():
        note = line.split(': ')[0]
        for a, b in re.findall(r'(\d+)-(\d+)', line):
            note_ranges.append((int(a), int(b), note))
            ticket_notes[note].append((int(a), int(b)))

    return ticket_notes, my_ticket, nearby_tickets


if __name__ == '__main__':
    # filename = 'inputs/input_16.txt'
    # filename = 'inputs/test_16_1.txt'
    filename = 'inputs/test_16_2.txt'

    ticket_notes, my_ticket, nearby_tickets = parse_data(filename)

    print('puzzle_1: {s}'.format(s=puzzle_1(ticket_data)))
    # print('puzzle_2: {s}'.format(s=puzzle_2(ticket_data)))
