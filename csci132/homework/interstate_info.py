# jezzy jumble
# 2024-04-29
# CSCI132 Lab:  Interstate highway numbers

"""See basic info about a given US Interstate Highway."""

from abc import ABC, abstractmethod
from enum import StrEnum, auto

MAX_INTERSTATE_NUMBER = 999
MAX_PRIMARY_INTERSTATE_NUMBER = 100


class InterstateType(StrEnum):
    """Type of an Interstate."""

    PRIMARY = auto()
    AUXILIARY = auto()


class InterstateDirection(StrEnum):
    """Direction of a Primary Interstate."""

    NORTH_SOUTH = "north/south"
    EAST_WEST = "east/west"


class Interstate(ABC):
    """Abstract base class for Interstates."""

    @abstractmethod
    def __init__(self, number: int):
        self._number = number

    @property
    def number(self) -> int:
        """Designation number of the Interstate."""
        return self._number

    @property
    @abstractmethod
    def interstate_type(self) -> str:
        """Type of the Interstate (primary or auxiliary)."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.number})"


class PrimaryInterstate(Interstate):
    """Primary Interstates (numbered 1-99)."""

    def __init__(self, number: int):
        super().__init__(number)
        self.interstate_direction = self.get_direction(self.number)

    @property
    def interstate_type(self) -> InterstateType:
        """Primary."""
        return InterstateType.PRIMARY

    @staticmethod
    def get_direction(number: int) -> InterstateDirection:
        """Get the direction of the Primary Interstate based on its number.

        Odd numbers are north/south, even numbers are east/west.
        """
        if number % 2 == 1:
            return InterstateDirection.NORTH_SOUTH
        return InterstateDirection.EAST_WEST

    def __str__(self) -> str:
        return (
            f"I-{self.number} is {self.interstate_type}, "
            f"going {self.interstate_direction}."
        )


class AuxiliaryInterstate(Interstate):
    """Auxiliary Interstates (numbered 100-999)."""

    def __init__(self, number: int):
        super().__init__(number)
        self.primary_interstate = self.get_primary_interstate(self.number)

    @property
    def interstate_type(self) -> InterstateType:
        """Auxiliary."""
        return InterstateType.AUXILIARY

    @staticmethod
    def get_primary_interstate(number: int) -> PrimaryInterstate:
        """Retrieve the Primary Interstate based on the given number.

        :param number: the Primary Interstate designation number
        :return: Primary Interstate object
        """
        return PrimaryInterstate(number % 100)

    def __str__(self) -> str:
        return (
            f"I-{self.number} is {self.interstate_type}, "
            f"serving I-{self.primary_interstate.number}, "
            f"going {self.primary_interstate.interstate_direction}."
        )


def input_interstate_number() -> int:
    """Prompt user to input an Interstate designation number; validate and return it.

    :return: inputted Interstate designation number
    """
    while True:
        try:
            number = int(input("Enter Interstate designation number:\nI-"))
            if number < 1 or number > MAX_INTERSTATE_NUMBER:
                print(
                    "Error: Valid designation numbers are in the range of 1–999.",
                    end="\n\n",
                )
            elif (number % 100) == 0:
                print("Error: Designation numbers cannot end in 00.", end="\n\n")
            else:
                break
        except ValueError:
            print("Error: Please input a valid designation number.", end="\n\n")

    return number


def get_interstate(number: int) -> Interstate:
    """Return a Primary or Auxiliary Interstate based on given designation number.

    :param number: Interstate designation number
    :return: Primary or Auxiliary Interstate object
    """
    if number < MAX_PRIMARY_INTERSTATE_NUMBER:
        return PrimaryInterstate(number)
    return AuxiliaryInterstate(number)


def main() -> None:
    """Prompt user for an Interstate number and then print info about it."""
    print(get_interstate(input_interstate_number()))


if __name__ == "__main__":
    main()
