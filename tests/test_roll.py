"""Test cases for the roll module."""
import pytest

from dot_combat import roll as r


def test_single_die_roll() -> None:
    """Result is an integer between 1 and sides."""
    assert r.single_die_roll(sides=1) == 1
    assert 1 <= r.single_die_roll(sides=2) <= 2


def test_dice_description_result(mocker) -> None:
    """Dice are "thrown" the correct number of times."""
    mocker.patch("dot_combat.roll.single_die_roll", return_value=1)
    assert r.dice_description_result(dice_num=4, dice_size=20) == 4


def test_dice_description_parser() -> None:
    """Strings correctly divided to number of dice and size of dice."""
    test_dice_num, test_dice_size = r.dice_description_parser(
        dice_roll_description="d20"
    )
    assert test_dice_num == 1
    assert test_dice_size == 20
    test_dice_num, test_dice_size = r.dice_description_parser(
        dice_roll_description="1d5"
    )
    assert test_dice_num == 1
    assert test_dice_size == 5
    test_dice_num, test_dice_size = r.dice_description_parser(
        dice_roll_description="6d8"
    )
    assert test_dice_num == 6
    assert test_dice_size == 8
    with pytest.raises(ValueError) as exception_info:
        test_dice_num, test_dice_size = r.dice_description_parser(
            dice_roll_description="2dO"
        )
    assert "Could not evaluate dice expression: 2dO" in str(exception_info)


def test_constant_evaluator() -> None:
    """String is correctly transformed to an int, respecting any supplied sign."""
    assert r.constant_evaluator(constant="3") == 3
    assert r.constant_evaluator(constant="-2") == -2
    assert r.constant_evaluator(constant="+1") == 1


def test_roll(mocker) -> None:
    """All dice are rolled and modifiers added."""
    mocker.patch("dot_combat.roll.single_die_roll", return_value=1)
    assert r.roll(full_roll_description="5") == 5
    assert r.roll(full_roll_description="-2") == -2
    assert r.roll(full_roll_description="+2") == 2
    assert r.roll(full_roll_description="d100") == 1
    assert r.roll(full_roll_description="4d100+4") == 8
    assert r.roll(full_roll_description="1d100-3") == -2
