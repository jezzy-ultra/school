# jezzy jumble
# 2024-04-24
# CSCI132 Assigment:  If/Else

"""Input and sort a list of numbers."""

import inflect

p = inflect.engine()


def input_numbers(amount: int) -> list[float]:
    """Prompt user to input an amount of numbers and return as tuple.

    :param amount: how many numbers to input
    :return: list of inputted numbers
    """
    numbers: list[float] = []
    while len(numbers) < amount:
        ordinal = p.ordinal(len(numbers) + 1)
        try:
            number = float(input(f"{ordinal} number: "))
            # remove ".0" from ints in printed display
            numbers.append(int(number) if number.is_integer() else number)
        except ValueError:
            print("Error: Must be a valid number.")

    return numbers


def sort_numbers(numbers: list[float]) -> list[float]:
    """Sort a tuple of numbers in ascending order and return as new tuple.

    :param numbers: pre-sorted list of numbers
    :return: sorted list of numbers (ascending)
    """
    minimum: float = numbers[0]
    sorted_numbers: list[float] = [minimum]
    for num in numbers[1::]:
        if num < minimum:
            sorted_numbers.insert(0, num)
            minimum = num
        else:
            sorted_numbers.append(num)

    return sorted_numbers


def main() -> None:
    """Prompt user to input 3 numbers and then print them sorted."""
    print(f"\n{sort_numbers(input_numbers(3))}")


if __name__ == "__main__":
    main()
