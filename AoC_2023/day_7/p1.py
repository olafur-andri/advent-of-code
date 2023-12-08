import functools
from collections import Counter
from enum import Enum
from types import MappingProxyType

CARD_STRENGTH = MappingProxyType({
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
})

class HandType(Enum):
    """Hand types are sorted according to strength, i.e., the strongest hand type has the
       highest corresponding integer value
    """
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

class Hand:
    def __init__(self, hand_str: str, bid: int):
        self.__hand_type = Hand.__derive_hand_type_from_str(hand_str)
        self.__hand_str = hand_str
        self.__bid = bid
    
    def hand_type(self):
        return self.__hand_type
    
    def bid(self):
        return self.__bid
    
    def hand_str(self):
        return self.__hand_str
    
    def __repr__(self):
        return f"Hand({self.__hand_str})"
    
    @staticmethod
    def __derive_hand_type_from_str(hand_str: str):
        hand_counts = tuple(sorted(Counter(hand_str).values()))

        if hand_counts == (5,):
            return HandType.FIVE_OF_A_KIND
        if hand_counts == (1, 4):
            return HandType.FOUR_OF_A_KIND
        if hand_counts == (2, 3):
            return HandType.FULL_HOUSE
        if hand_counts == (1, 1, 3):
            return HandType.THREE_OF_A_KIND
        if hand_counts == (1, 2, 2):
            return HandType.TWO_PAIR
        if hand_counts == (1, 1, 1, 2):
            return HandType.ONE_PAIR
        if hand_counts == (1, 1, 1, 1, 1):
            return HandType.HIGH_CARD
        
        raise ValueError(f"Cannot derive hand type from hand string '{hand_str}'")

def get_hands_from_input(filepath: str):
    with open(filepath, "r") as input_file:
        hands: list[Hand] = []

        for line in input_file:
            hand_str, bid_str = line.strip().split()
            hands.append(Hand(hand_str, int(bid_str)))
        
        return hands

def compare_hands(hand1: Hand, hand2: Hand):
    difference = hand1.hand_type().value - hand2.hand_type().value

    if difference != 0:
        return difference
    
    # hands have equal strength; time to compare cards
    for card1, card2 in zip(hand1.hand_str(), hand2.hand_str()):
        strength1, strength2 = CARD_STRENGTH[card1], CARD_STRENGTH[card2]

        if strength1 > strength2:
            return 1
        if strength1 < strength2:
            return -1
    
    # both hands must be the same
    return 0

def calculate_total_winnings(sorted_hands: list[Hand]):
    total_winnings = 0

    for index, hand in enumerate(sorted_hands):
        rank = index + 1
        bid = hand.bid()
        total_winnings += rank * bid
    
    return total_winnings

def main():
    hands = get_hands_from_input("2023/day_7/input.txt")
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare_hands))
    total_winnings = calculate_total_winnings(sorted_hands)

    print(total_winnings)

if __name__ == "__main__":
    main()
