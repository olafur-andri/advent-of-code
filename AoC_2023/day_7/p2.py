import functools
from types import MappingProxyType
from HandType import HandType
from SimpleHand import SimpleHand

CARD_STRENGTH = MappingProxyType({
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
})

class Hand:
    def __init__(self, hand_str: str, bid: int):
        self.__best_hand_type = Hand.__derive_best_hand_type_from_str(hand_str)
        self.__hand_str = hand_str
        self.__bid = bid
    
    def best_hand_type(self):
        return self.__best_hand_type
    
    def bid(self):
        return self.__bid
    
    def hand_str(self):
        return self.__hand_str
    
    def __repr__(self):
        return f"Hand({self.__hand_str})"
    
    @staticmethod
    def __derive_best_hand_type_from_str(hand_str: str):
        nr_jokers_available = len([c for c in hand_str if c == "J"])
        hand_str_without_jokers = hand_str.replace("J", "")
        simple_hand = SimpleHand.from_hand_str(hand_str_without_jokers)

        # using `reversed(...)` to try strongest hand types first
        for target_hand_type in reversed(HandType):
            target_simple_hand = SimpleHand.from_hand_type(target_hand_type)
            nr_jokers_needed = simple_hand.min_nr_jokers_to_get(target_simple_hand)

            if nr_jokers_needed <= nr_jokers_available:
                return target_hand_type
        
        raise ValueError(f"Don't know derive hand type from hand string '{hand_str}'")

def get_hands_from_input(filepath: str):
    with open(filepath, "r") as input_file:
        hands: list[Hand] = []

        for line in input_file:
            hand_str, bid_str = line.strip().split()
            hands.append(Hand(hand_str, int(bid_str)))
        
        return hands

def compare_hands(hand1: Hand, hand2: Hand):
    difference = hand1.best_hand_type().value - hand2.best_hand_type().value

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
    hands = get_hands_from_input("AoC_2023/day_7/input.txt")
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare_hands))
    total_winnings = calculate_total_winnings(sorted_hands)

    print(total_winnings)

if __name__ == "__main__":
    main()
