from dataclasses import dataclass

@dataclass(frozen=True)
class Card:
    winning_numbers: list[int]
    numbers: list[int]

def derive_card_from_input_line(input_line: str):
    _, all_numbers_str = input_line.split(": ")
    winning_numbers_str, numbers_str = all_numbers_str.split(" | ")
    winning_numbers = list(map(int, winning_numbers_str.split()))
    numbers = list(map(int, numbers_str.split()))

    return Card(winning_numbers, numbers)

def derive_cards_from_input(filepath: str):
    with open(filepath, "r") as input_file:
        return [derive_card_from_input_line(line) for line in input_file]

def calculate_points(card: Card):
    winning_numbers_set = set(card.winning_numbers)
    numbers_set = set(card.numbers)
    nr_good_numbers = len( winning_numbers_set.intersection(numbers_set) )
    
    if nr_good_numbers == 0:
        return 0
    
    return 2 ** (nr_good_numbers - 1)

def main():
    cards = derive_cards_from_input("input.txt")
    print(sum(calculate_points(card) for card in cards))

if __name__ == "__main__":
    main()
