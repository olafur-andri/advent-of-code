from enum import Enum
from types import MappingProxyType # immutable dict

ALPHA_TO_DIGIT = MappingProxyType({
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
})


class SearchType(Enum):
    FIRST = 1
    LAST = 2


class NoDigitFoundError(ValueError):
    pass


def derive_digit_at_start_of(s: str):
    """Tries to derive a digit from the given string, raises an error if none could be found"""
    all_digit_names = tuple(ALPHA_TO_DIGIT.keys())

    if s[0].isdigit():
        return int(s[0])

    for digit_name in all_digit_names:
        if s.startswith(digit_name):
            return ALPHA_TO_DIGIT[digit_name]

    raise NoDigitFoundError()


def find_digit(line: str, search_type: SearchType):
    if search_type == SearchType.FIRST:
        loop_range = range(len(line) - 1)
    elif search_type == SearchType.LAST:
        loop_range = range(len(line) - 1, -1, -1)

    for substring_start_index in loop_range:
        current_substring = line[substring_start_index::]

        try:
            digit = derive_digit_at_start_of(current_substring)
            return digit
        except NoDigitFoundError:
            pass
    
    raise NoDigitFoundError()


def construct_two_digit_number(line: str):
    first_digit = find_digit(line, SearchType.FIRST)
    last_digit = find_digit(line, SearchType.LAST)
    
    return (10 * first_digit) + last_digit


def main():
    with open("input.txt", "r") as input_file:
        print(sum( construct_two_digit_number(line) for line in input_file ))


if __name__ == "__main__":
    main()
