"""
https://adventofcode.com/2020/day/4
--- Day 4: Passport Processing ---

You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While
these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually
valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport
scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at the same
time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all required
fields. The expected fields are as follows:

    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of
key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in

The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the
Height field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials,
not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat
this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so
this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file,
how many passports are valid?

Your puzzle answer was 235.

--- Part Two ---

The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data
are getting through. Better add some data validation, quick!

You can continue to ignore the cid field, but each other field has strict rules about what values are valid for
automatic validation:

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

Your job is to count the passports where all required fields are both present and valid according to the above rules.
Here are some example values:

byr valid:   2002
byr invalid: 2003

hgt valid:   60in
hgt valid:   190cm
hgt invalid: 190in
hgt invalid: 190

hcl valid:   #123abc
hcl invalid: #123abz
hcl invalid: 123abc

ecl valid:   brn
ecl invalid: wat

pid valid:   000000001
pid invalid: 0123456789

Here are some invalid passports:

eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

Here are some valid passports:

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719

Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as
optional. In your batch file, how many passports are valid?

Your puzzle answer was 194.
"""

import re


def puzzle_1(passports):
    valid_passport_count = 0

    for passport in passports:
        if is_valid_passport(passport):
            valid_passport_count += 1

    print(valid_passport_count)


def puzzle_2(passports):
    valid_passport_count = 0
    valid_passports = []

    for passport in passports:
        if is_valid_passport(passport) and all_passport_fields_valid(passport):
            valid_passports.append(passport)
            valid_passport_count += 1

    print(valid_passport_count)


def load_passports_from_file(input_filename):
    passports = []
    with open(input_filename, 'r') as f_input:
        passport_data = [line.strip() for line in f_input.readlines()]

        current_passport_data = []
        for line in passport_data:
            if line:
                current_passport_data.extend(line.split(' '))
            elif not line and current_passport_data:
                passports.append(load_passport_from_data(current_passport_data))
                current_passport_data = []

        passports.append(load_passport_from_data(current_passport_data))

    return passports


def load_passport_from_data(passport_data):
    passport = {
        'pid': '',
        'byr': '',
        'iyr': '',
        'eyr': '',
        'hgt': '',
        'hcl': '',
        'ecl': '',
        'cid': '',
    }

    for item in passport_data:
        props = item.split(':')
        passport[props[0]] = props[1]

    return passport


def is_valid_passport(passport):
    if passport['byr'] != '' and passport['iyr'] != '' and passport['eyr'] != '' and passport['hgt'] != '' \
            and passport['hcl'] != '' and passport['ecl'] != '' and passport['pid'] != '':
        return True
    else:
        return False


def all_passport_fields_valid(passport):
    return is_byr(passport['byr']) and is_iyr(passport['iyr']) and is_eyr(passport['eyr']) and is_hgt(passport['hgt']) \
        and is_hcl(passport['hcl']) and is_ecl(passport['ecl']) and is_pid(passport['pid'])


def is_pid(value):
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    match = re.search(r'^\d{9}$', value)
    return bool(match)


def is_byr(value):
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    return validate_year(value, 1920, 2002)


def is_iyr(value):
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    return validate_year(value, 2010, 2020)


def is_eyr(value):
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    return validate_year(value, 2020, 2030)


def is_hgt(value):
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    if value == '':
        return False
    try:
        height = int(value[:-2])
        units = value[-2:]
    except ValueError:
        return False

    if units not in ['cm', 'in']:
        return False
    if units == 'cm':
        return height >= 150 and height <= 193
    if units == 'in':
        return height >= 59 and height <= 76


def is_hcl(value):
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
    return bool(match)


def is_ecl(value):
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def validate_year(value, min_value, max_value):
    if len(value) != 4:
        return False

    value = int(value)
    return value >= min_value and value <= max_value


def _test_validations():
    print('\nis_byr')
    assert is_byr('2002'), 'Error asserting byr valid: 2002'
    assert is_byr('2003') is False, 'Error asserting byr invalid: 2003'

    print('\nis_iyr')
    assert is_iyr('2010'), 'Error asserting iyr valid: 2010'
    assert is_iyr('2023') is False, 'Error asserting iyr invalid: 2023'

    print('\nis_eyr')
    assert is_eyr('2029'), 'Error asserting eyr valid: 2029'
    assert is_eyr('1972') is False, 'Error asserting eyr invalid: 1972'

    print('\nis_hgt')
    assert is_hgt('60in'), 'Error asserting hgt valid: 60in'
    assert is_hgt('190cm'), 'Error asserting hgt valid: 190cm'
    assert is_hgt('190in') is False, 'Error asserting hgt invalid: 190in'
    assert is_hgt('190') is False, 'Error asserting hgt invalid: 190'

    print('\nis_hcl')
    assert is_hcl('#123abc'), 'Error asserting hcl valid: #123abc'
    assert is_hcl('#123abz') is False, 'Error asserting hcl invalid: #123abz'
    assert is_hcl('123abc') is False, 'Error asserting hcl invalid: 123abc'

    print('\nis_ecl')
    assert is_ecl('brn'), 'Error asserting ecl valid: brn'
    assert is_ecl('wat') is False, 'Error asserting ecl invalid: wat'

    print('\nis_pid')
    assert is_pid('000000001'), 'Error asserting pid valid: 000000001'
    assert is_pid('0123456789') is False, 'Error asserting pid invalid: 0123456789'


def _test_passports():
    print('Invalid passports')
    ip1 = {
        'eyr': '1972',
        'cid': '100',
        'hcl': '#18171d',
        'ecl': 'amb',
        'hgt': '170',
        'pid': '186cm',
        'iyr': '2018',
        'byr': '1926',
    }
    assert all_passport_fields_valid(ip1) is False, 'Assert ip1 failed'

    ip2 = {
        'iyr': '2019',
        'hcl': '#602927',
        'eyr': '1967',
        'hgt': '170cm',
        'ecl': 'grn',
        'pid': '012533040',
        'byr': '1946',
    }
    assert all_passport_fields_valid(ip2) is False, 'Assert ip2 failed'

    ip3 = {
        'hcl': 'dab227',
        'iyr': '2012',
        'ecl': 'brn',
        'hgt': '182cm',
        'pid': '021572410',
        'eyr': '2020',
        'byr': '1992',
        'cid': '277',
    }
    assert all_passport_fields_valid(ip3) is False, 'Assert ip3 failed'

    ip4 = {
        'hgt': '59cm',
        'ecl': 'zzz',
        'eyr': '2038',
        'hcl': '74454a',
        'iyr': '2023',
        'pid': '3556412378',
        'byr': '2007',
    }
    assert all_passport_fields_valid(ip4) is False, 'Assert ip4 failed'

    print('Valid passports')

    vp1 = {
        'pid': '087499704',
        'hgt': '74in',
        'ecl': 'grn',
        'iyr': '2012',
        'eyr': '2030',
        'byr': '1980',
        'hcl': '#623a2f',
    }
    assert all_passport_fields_valid(vp1), 'Assert vp1 failed'

    vp2 = {
        'eyr': '2029',
        'ecl': 'blu',
        'cid': '129',
        'byr': '1989',
        'iyr': '2014',
        'pid': '896056539',
        'hcl': '#a97842',
        'hgt': '165cm',
    }
    assert all_passport_fields_valid(vp2), 'Assert vp2 failed'

    vp3 = {
        'hcl': '#888785',
        'hgt': '164cm',
        'byr': '2001',
        'iyr': '2015',
        'cid': '88',
        'pid': '545766238',
        'ecl': 'hzl',
        'eyr': '2022',
    }
    assert all_passport_fields_valid(vp3), 'Assert vp3 failed'

    vp4 = {
        'iyr': '2010',
        'hgt': '158cm',
        'hcl': '#b6652a',
        'ecl': 'blu',
        'byr': '1944',
        'eyr': '2021',
        'pid': '093154719',
    }
    assert all_passport_fields_valid(vp4), 'Assert vp4 failed'


if __name__ == '__main__':
    # _test_validations()
    passports = load_passports_from_file('inputs/input_04.txt')
    # passports = load_passports_from_file('inputs/test_04_2.txt')

    # puzzle_1(passports)
    puzzle_2(passports)
