"""Basic die roller"""
import random as rnd
from typing import Tuple


def single_die_roll(sides: int) -> int:
    """Roll a die of a given size."""
    return rnd.randrange(1, sides + 1, 1)


def dice_description_result(dice_num: int, dice_size: int) -> int:
    """Returns the total from dice_num rolls of dice_size."""
    return sum(single_die_roll(sides=dice_size) for _ in range(dice_num))


def dice_description_parser(dice_roll_description: str) -> Tuple[int, int]:
    """Breaks string expression like "2d10" into tuple of ints[2, 10]."""
    dice_num_str, dice_size_str = dice_roll_description.split("d")
    try:
        dice_num = int(dice_num_str) if dice_num_str else 1
        dice_size = int(dice_size_str)
    except ValueError:
        raise ValueError(f"Could not evaluate dice expression: {dice_roll_description}")
    return dice_num, dice_size


def constant_evaluator(constant: str) -> int:
    """Turns result modifier into an integer."""
    return int(constant)


def roll(full_roll_description: str) -> int:
    """Return a result for a standard notation die description.

    Expected format is "xdy+c" where:
        x is the number of die to roll and can be omitted
        d is mandatory if y is present
        y is the number of faces on the dice
        c is a constant, which can be negative, and can be omitted
    """
    dice_score: int = 0
    modifier_score: int = 0
    dice_roll_description: str = ""
    constant_str: str = ""
    sign: str = ""

    sign_present = set("+-").intersection(set(full_roll_description))
    if sign_present and "d" in full_roll_description:
        sign = sign_present.pop()
        assert len(sign_present) == 0, (
            "Received roll_description without multiple +- signs: "
            + full_roll_description
        )
        dice_roll_description, constant_str = full_roll_description.split(sign)
    elif "d" in full_roll_description:
        dice_roll_description = full_roll_description
    else:  # constant expression
        constant_str = full_roll_description

    if dice_roll_description:
        dice_num, dice_size = dice_description_parser(
            dice_roll_description=dice_roll_description
        )
        dice_score = dice_description_result(dice_num=dice_num, dice_size=dice_size)
    if constant_str:
        if sign:
            constant_str = sign + constant_str
        modifier_score = constant_evaluator(constant=constant_str)

    return dice_score + modifier_score
