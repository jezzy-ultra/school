# jezzy jumble
# 2024-04-29
# CSCI132 Lab:  Exact change

"""Show the fewest coins needed to represent a given amount of USD."""

change = int(input())
change_strs = []

if change == 0:
    change_strs.append("No change")
else:
    if (change // 100) != 0:
        if 100 <= change < 200:
            change_strs.append("1 Dollar")
        else:
            change_strs.append(f"{change // 100} Dollars")
        change %= 100

    if (change // 25) != 0:
        if 25 <= change < 50:
            change_strs.append("1 Quarter")
        else:
            change_strs.append(f"{change // 25} Quarters")
        change %= 25

    if (change // 10) != 0:
        if 10 <= change < 20:
            change_strs.append("1 Dime")
        else:
            change_strs.append(f"{change // 10} Dimes")
        change %= 10

    if (change // 5) != 0:
        if 5 <= change < 10:
            change_strs.append("1 Nickel")
        else:
            change_strs.append(f"{change // 5} Nickels")
        change %= 5

    if change > 0:
        if change == 1:
            change_strs.append("1 Penny")
        else:
            change_strs.append(f"{change} Pennies")

for string in change_strs:
    print(string)
