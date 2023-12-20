from typing import Iterable, Sequence


def get_histories_from_input_file(input_filepath: str):
    histories: list[tuple[int, ...]] = []

    with open(input_filepath) as input_file:
        for line in input_file:
            new_history = tuple(map(int, line.split()))
            histories.append(new_history)
    
    return histories

def calculate_differences(numbers: Sequence[int]) -> tuple[int, ...]:
    differences: list[int] = []

    for i in range(len(numbers) - 1):
        differences.append(numbers[i + 1] - numbers[i])
    
    return tuple(differences)

def is_all_zeroes(numbers: Iterable[int]):
    return all(number == 0 for number in numbers)

def construct_number_pyramid(history: tuple[int, ...]):
    number_pyramid = [history]

    while True:
        differences = calculate_differences(number_pyramid[-1])

        number_pyramid.append(differences)

        if is_all_zeroes(differences):
            break

    return number_pyramid

def get_next_value(history: tuple[int, ...]):
    next_value = 0
    number_pyramid = construct_number_pyramid(history)

    for row in reversed(number_pyramid):
        next_value += row[-1]

    return next_value

def main():
    INPUT_FILEPATH = "AoC_2023/day_9/input.txt"

    histories = get_histories_from_input_file(INPUT_FILEPATH)

    next_values = [get_next_value(history) for history in histories]

    print(sum(next_values))

if __name__ == "__main__":
    main()
