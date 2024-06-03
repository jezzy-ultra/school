# jezzy jumble
# 2024-04-08
# CSCI132 Lab:  Driving costs

"""Calculate cost of gas per <x> miles."""

INPUT_NUMBER_EXCEPTION_MESSAGE: str = "Error: Please input a number."


def input_gas_milage_per_gallon() -> float:
    """Prompt user to input their car's gas milage per gallon.

    :return: gas milage per gallon
    """
    while True:
        try:
            return float(
                input("Enter the gas milage of your car in miles per gallon: ")
            )
        except ValueError:
            print(INPUT_NUMBER_EXCEPTION_MESSAGE, end="\n\n")


def input_gas_price_per_gallon() -> float:
    """Prompt user to input the current price of gas per gallon.

    :return: gas price per gallon
    """
    while True:
        try:
            return float(input("Enter the current price of gas per gallon: "))
        except ValueError:
            print(INPUT_NUMBER_EXCEPTION_MESSAGE, end="\n\n")


def calculate_gas_cost(
    miles: int, milage_per_gallon: float, price_per_gallon: float
) -> float:
    """Return total cost of gas for x miles according to price per gallon.

    :param miles: number of miles driven
    :param milage_per_gallon: user's MPG
    :param price_per_gallon: current price of gas
    :return: cost of gas to drive <x> miles
    """
    return (miles / milage_per_gallon) * price_per_gallon


def main() -> None:
    """Calculate a user's gas costs for their car using their input."""
    milage: float = input_gas_milage_per_gallon()
    price: float = input_gas_price_per_gallon()

    print(
        f"{calculate_gas_cost(20, milage, price):.2f}"
        f"{calculate_gas_cost(75, milage, price):.2f}"
        f"{calculate_gas_cost(500, milage, price):.2f}"
    )


if __name__ == "__main__":
    main()
