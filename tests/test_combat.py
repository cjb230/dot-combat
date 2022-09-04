"""Test cases for the Combat class."""
import pytest

from dot_combat.combat import Combat
from dot_combat.combatant import Combatant


@pytest.fixture
def test_combatant():
    """A Combatant with one hit point."""
    return Combatant(max_hit_points=1, current_hit_points=1, control="DM")


@pytest.fixture
def test_combat(test_combatant):
    """A Combat with two combatants. Initiative list not yet filled."""
    combatant_2 = Combatant(max_hit_points=2, current_hit_points=2, control="DM")
    combatant_list = [test_combatant, combatant_2]
    test_combat = Combat(combatant_list=combatant_list)
    return test_combat


def test_fill_initiative_list(mocker, test_combat):
    """All combatants are added to the initiative order."""
    mocker.patch("dot_combat.roll.single_die_roll", return_value=1)
    assert len(test_combat.initiative_order) == 0
    test_combat.fill_initiative_list()
    assert len(test_combat.initiative_order) == 1
    assert len(test_combat.initiative_order[1]) == 2
    assert test_combat.used_initiatives == [1]


def test_add_combatant(mocker, test_combat):
    """New combatants are added to the combatant list.

    Also added to the initiative order if that has been populated.
    """
    mocker.patch("dot_combat.roll.single_die_roll", return_value=1)
    additional_combatant_1 = Combatant(
        max_hit_points=3, current_hit_points=1, control="DM"
    )
    additional_combatant_2 = Combatant(
        max_hit_points=4, current_hit_points=1, control="DM"
    )
    assert len(test_combat.combatant_list) == 2
    test_combat.add_combatant(new_combatant=additional_combatant_1)
    assert len(test_combat.combatant_list) == 3
    assert len(test_combat.initiative_order) == 0
    test_combat.fill_initiative_list()
    assert len(test_combat.initiative_order[1]) == 3
    test_combat.add_combatant(new_combatant=additional_combatant_2)
    assert len(test_combat.combatant_list) == 4
    assert len(test_combat.initiative_order[1]) == 4
    mocker.patch("dot_combat.roll.single_die_roll", return_value=2)
    additional_combatant_3 = Combatant(
        max_hit_points=5, current_hit_points=1, control="DM"
    )
    test_combat.add_combatant(new_combatant=additional_combatant_3)


def test_add_combatants(test_combat):
    """Lists of Combatants can be added to the Combat."""
    additional_combatant_1 = Combatant(
        max_hit_points=3, current_hit_points=1, control="DM"
    )
    additional_combatant_2 = Combatant(
        max_hit_points=4, current_hit_points=1, control="DM"
    )
    new_combatant_list = [additional_combatant_1, additional_combatant_2]
    test_combat.add_combatants(new_combatants=new_combatant_list)
    assert len(test_combat.combatant_list) == 4


def test_can_start_combat(test_combat):
    """Can_start_combat() correctly determines when an unstarted Combat can start."""
    assert Combat(combatant_list=[]).can_start_combat() is False
    assert test_combat.can_start_combat() is False
    test_combat.fill_initiative_list()
    assert test_combat.can_start_combat() is True
    test_combat.current_round = 1
    assert test_combat.can_start_combat() is False
    test_combat.current_round = 0
    assert test_combat.can_start_combat() is True


def test_start_combat(mocker, test_combat):
    """Only True when conditions are met.

    Current_round should be set to 1
    Current_initative should be set correctly
    Has_started should be True.
    """
    mocker.patch("dot_combat.roll.single_die_roll", return_value=20)
    test_combat.fill_initiative_list()
    assert test_combat.current_round == 0
    test_combat.start_combat()
    assert test_combat.current_round == 1
    assert test_combat.current_initiative == 20
    assert test_combat.current_combatant == test_combat.combatant_list[0]
    assert test_combat.has_started is True


def test_next_combatant(test_combat, test_combatant):
    """Correctly determines which Combatant is next."""
    test_combatant_3 = Combatant(max_hit_points=3, current_hit_points=1, control="DM")
    test_combatant_4 = Combatant(max_hit_points=4, current_hit_points=1, control="DM")
    test_combat.initiative_order = {
        17: [test_combat.combatant_list[0]],
        13: [test_combat.combatant_list[1], test_combatant_3],
        10: [test_combatant_4],
    }

    test_combat.populate_used_initiatives()
    test_combat.current_initiative = 10
    assert test_combat.next_combatant() == test_combat.combatant_list[0]
    test_combat.current_initiative = 13
    with pytest.raises(ValueError):
        _ = test_combat.next_combatant()
    test_combat.current_combatant = test_combat.combatant_list[1]
    assert test_combat.next_combatant() == test_combatant_3
    test_combat.current_combatant = test_combatant_3
    assert test_combat.next_combatant() == test_combatant_4

    test_combat.initiative_order = {
        10: [
            test_combat.combatant_list[0],
            test_combat.combatant_list[1],
            test_combatant_3,
            test_combatant_4,
        ],
    }
    test_combat.populate_used_initiatives()
    test_combat.current_initiative = 10
    test_combat.current_combatant = test_combat.combatant_list[0]
    assert test_combat.next_combatant() == test_combat.combatant_list[1]
    test_combat.current_combatant = test_combat.combatant_list[1]
    assert test_combat.next_combatant() == test_combatant_3
    test_combat.current_combatant = test_combatant_3
    assert test_combat.next_combatant() == test_combatant_4


def test_advance_combatant(mocker, test_combat):
    """Should turn next_combatant() into current_combatant."""
    mocker.patch("dot_combat.roll.single_die_roll", return_value=10)
    test_combat.fill_initiative_list()
    test_combat.start_combat()
    assert test_combat.current_combatant == test_combat.combatant_list[0]
    assert test_combat.next_combatant() == test_combat.combatant_list[1]
    test_combat.advance_combatant()
    assert test_combat.current_combatant == test_combat.combatant_list[1]
    assert test_combat.next_combatant() == test_combat.combatant_list[0]


def test_next_initiative(test_combat):
    """What's next in the initiative order.

    Loops back after reaching the lowest value.
    """
    test_combat.initiative_order = {5: [], 10: [], 15: []}
    test_combat.populate_used_initiatives()
    test_combat.current_initiative = 15
    assert test_combat.next_initiative() == 10
    test_combat.current_initiative = 10
    assert test_combat.next_initiative() == 5
    test_combat.current_initiative = 5
    assert test_combat.next_initiative() == 15


def test_advance_initiative(test_combat):
    """Current_initiative shhould change correctly."""
    test_combat.initiative_order = {5: [], 10: [], 15: []}
    test_combat.populate_used_initiatives()
    test_combat.current_initiative = 15
    test_combat.advance_initiative()
    assert test_combat.current_initiative == 10
    test_combat.advance_initiative()
    assert test_combat.current_initiative == 5
    test_combat.advance_initiative()
    assert test_combat.current_initiative == 15


def test_advance_round(test_combat):
    """Can we add one to a number?"""
    test_combat.current_round = 5
    test_combat.advance_round()
    assert test_combat.current_round == 6
