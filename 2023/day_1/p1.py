from typing import Iterable, Callable

class NoElementFoundError(ValueError):
    pass

def first[T](iterable: Iterable[T], predicate: Callable[[T], bool]):
    """Returns the first item in the given `iterable` that satisfies `predicate`. Raises an
       exception if no such element was found
    """
    for element in iterable:
        if predicate(element):
            return element
    
    raise NoElementFoundError("Could not find any element that satisfies the given predicate")

def construct_two_digit_number(line: str):
    first_digit = int( first(line, lambda c: c.isdigit()) )
    last_digit = int( first(reversed(line), lambda c: c.isdigit()) )
    
    return (10 * first_digit) + last_digit

def main():
    with open("input.txt", "r") as input_file:
        print(sum( construct_two_digit_number(line) for line in input_file ))


if __name__ == "__main__":
    main()
