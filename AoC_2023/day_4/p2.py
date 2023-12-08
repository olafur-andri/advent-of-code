from dataclasses import dataclass
from typing import Iterable
from types import MappingProxyType
from collections.abc import Generator

@dataclass(frozen=True)
class Card:
    id: int
    nr_good_numbers: int

class CardCollection:
    def __init__(self, cards: Iterable[Card]):
        self.__card_dict = self.__build_card_dict(cards)
    
    def get_card_by_id(self, id: int):
        return self.__card_dict[id]
    
    def __iter__(self) -> Generator[Card, None, None]:
        for card in self.__card_dict.values():
            yield card
    
    def __len__(self):
        return len(self.__card_dict)

    def __build_card_dict(self, cards: Iterable[Card]):
        card_dict: dict[int, Card] = {}
        
        for card in cards:
            card_dict[card.id] = card

        return MappingProxyType(card_dict)

def find_nr_good_numbers(winning_numbers: Iterable[int], card_numbers: Iterable[int]):
    winning_numbers_set = set(winning_numbers)
    numbers_set = set(card_numbers)
    nr_good_numbers = len( winning_numbers_set.intersection(numbers_set) )
    
    return nr_good_numbers

def derive_card_id_from_input_line(input_line: str):
    card_id_str, _ = input_line.replace("Card", "").split(": ")
    return int(card_id_str.strip())

def derive_card_from_input_line(input_line: str):
    card_id = derive_card_id_from_input_line(input_line)

    _, all_numbers_str = input_line.split(": ")
    winning_numbers_str, numbers_str = all_numbers_str.split(" | ")
    winning_numbers = list(map(int, winning_numbers_str.split()))
    card_numbers = list(map(int, numbers_str.split()))

    return Card(card_id, find_nr_good_numbers(winning_numbers, card_numbers))

def get_card_collection_from_input(filepath: str):
    with open(filepath, "r") as input_file:
        cards = [derive_card_from_input_line(line) for line in input_file]
        return CardCollection(cards)

def get_card_counts(card_collection: CardCollection):
    card_counts: dict[int, int] = { card.id: 1 for card in card_collection }

    for card in card_collection:
        copy_start_id = card.id + 1
        copy_end_id = copy_start_id + card.nr_good_numbers

        for copy_card_id in range(copy_start_id, copy_end_id):
            card_counts[copy_card_id] += card_counts[card.id]

    return MappingProxyType(card_counts)

def main():
    card_collection = get_card_collection_from_input("2023/day_4/input.txt")
    card_counts = get_card_counts(card_collection)

    print(sum(card_counts.values()))

if __name__ == "__main__":
    main()
