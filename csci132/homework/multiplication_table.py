# jezzy jumble
# 2024-05-09
# CSCI132 Assigment:  Loops

"""Print a multiplication table up to a given number (e.g. 9x9)."""

MAX_SIZE = 99


def calculate_padding(table_size: int) -> int:
    """Determine amount of spaces needed for table cells based on the biggest factor.

    :param table_size: biggest factor in the multiplication table
    :return: number of spaces to pad cells with
    """
    return len(str(table_size**2))


def print_header(table_size: int, padding: int) -> None:
    """Print the header for the multiplication table.

    :param table_size: biggest factor in the multiplication table
    :param padding: number of fill spaces
    """
    print(f"{"":{len(str(table_size))}}  \t", end="")
    for number in range(1, table_size + 1):
        print(f"{number:^{padding}}\t", end="")
    print()

    # separator row
    print(f"{"":{len(str(table_size))}}  \t", end="")
    num_digits = len(str(table_size**2))
    separator = "—" * num_digits
    for _i in range(table_size):
        print(f"{separator:^{padding}}\t", end="")
    print()


def print_row(row_number: int, table_size: int, padding: int) -> None:
    """Print a row in the multiplication table.

    :param row_number: a factor in the multiplication table
    :param table_size: biggest factor in the multiplication table
    :param padding: number of fill spaces
    """
    # heading
    print(f"{row_number:>{len(str(table_size))}} |\t", end="")

    for column_number in range(1, table_size + 1):
        print(f"{(row_number * column_number):^{padding}}\t", end="")
    print()


def print_table(table_size: int, padding: int) -> None:
    """Print formatted multiplication table of given size.

    :param table_size: biggest factor in the multiplication table
    :param padding: number of fill spaces
    """
    print_header(table_size, padding)
    for number in range(1, table_size + 1):
        print_row(number, table_size, padding)
    print()


def input_table_size() -> int:
    """Prompt user to input what number the multiplication table should go up to.

    :return: number the multiplication table will stop at
    """
    while True:
        try:
            size = int(input("size? "))
            if size < 1 or size > MAX_SIZE:
                raise ValueError
        except ValueError:
            print("error: please type a single integer (1–99)")
        else:
            return size


def main() -> None:
    """Print a multiplication table of inputted size."""
    table_size = input_table_size()
    print()
    print_table(table_size, calculate_padding(table_size))


if __name__ == "__main__":
    main()
