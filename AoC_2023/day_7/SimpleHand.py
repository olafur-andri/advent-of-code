from collections import Counter

from HandType import HandType

class SimpleHand:
    """Represents a so-called "hand count", which is a representation of a hand that makes it easier
       to work with.
    """
    def __init__(self, simple_hand: tuple[int, ...]):
        self.__simple_hand = tuple( sorted(simple_hand) )

    @staticmethod
    def from_hand_str(hand_str: str):
        if "J" in hand_str:
            raise ValueError("A simple hand cannot contain a joker")

        simple_hand = tuple( sorted(Counter(hand_str).values()) )
        return SimpleHand(simple_hand)
    
    @staticmethod
    def from_hand_type(hand_type: HandType):
        simple_hand: tuple[int, ...] = ()

        if hand_type == HandType.FIVE_OF_A_KIND:
            simple_hand = (5,)
        if hand_type == HandType.FOUR_OF_A_KIND:
            simple_hand = (1, 4)
        if hand_type == HandType.FULL_HOUSE:
            simple_hand = (2, 3)
        if hand_type == HandType.THREE_OF_A_KIND:
            simple_hand = (1, 1, 3)
        if hand_type == HandType.TWO_PAIR:
            simple_hand = (1, 2, 2)
        if hand_type == HandType.ONE_PAIR:
            simple_hand = (1, 1, 1, 2)
        if hand_type == HandType.HIGH_CARD:
            simple_hand = (1, 1, 1, 1, 1)

        if simple_hand == ():
            raise ValueError(f"Don't know how to derive a SimpleHand from hand type: '{hand_type}'")

        return SimpleHand(simple_hand)
    
    def min_nr_jokers_to_get(self, target: "SimpleHand"):
        IMPOSSIBLE = 1_000_000

        # the fact that a simple hand maintains its counts in a sorted fashion makes this method
        # possible

        # it is impossible to remove cards
        # if I have a greater nr. of unique cards then I'd have to remove cards
        my_nr_unique_cards = len(self.__simple_hand)
        target_nr_unique_cards = len(target.__simple_hand)
        if my_nr_unique_cards > target_nr_unique_cards:
            return IMPOSSIBLE
        
        # if I have a greater nr. of a specific card than the target hand, I'd have to remove cards
        for my_count, target_count in zip(self.__simple_hand, target.__simple_hand):
            if my_count > target_count:
                return IMPOSSIBLE
        
        # now we can start counting jokers
        min_nr_jokers = 0

        for my_count, target_count in zip(self.__simple_hand, target.__simple_hand):
            min_nr_jokers += target_count - my_count
        
        for i in range(len(self.__simple_hand), len(target.__simple_hand)):
            min_nr_jokers += target.__simple_hand[i]
        
        return min_nr_jokers
