from enum import Enum


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
