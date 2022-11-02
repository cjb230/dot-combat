import pytest

import dot_combat.helpers as h
from dot_combat.attack import Attack
from dot_combat.combat import Combat
from dot_combat.combatant import Combatant


@pytest.fixture
def test_attack_list():
    """Fixture for a one-item Attack list."""
    shortsword: Attack = Attack(
        name="Shortsword",
        attack_bonus=0,
        damage_dice="d6",
        damage_type=h.DamageType.PIERCING,
        damage_bonus=0,
        range=5,
        long_range=None,
    )
    return [shortsword]


@pytest.fixture
def test_combatant(test_attack_list):
    """A Combatant with one hit point."""
    return Combatant(
        max_hit_points=1,
        current_hit_points=1,
        control="DM",
        armor_class=15,
        attacks=test_attack_list,
    )


@pytest.fixture
def test_combat(test_combatant, test_attack_list):
    """A Combat with two combatants. Initiative list not yet filled."""
    combatant_2 = Combatant(
        max_hit_points=2,
        current_hit_points=2,
        control="DM",
        armor_class=15,
        attacks=test_attack_list,
    )
    combatant_list = [test_combatant, combatant_2]
    test_combat = Combat(combatant_list=combatant_list)
    return test_combat
