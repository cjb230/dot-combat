"""Test cases for the Combatant class."""
from dot_combat.combatant import Combatant
from dot_combat.helpers import DamageType
from dot_combat.helpers import FightingStatus
from dot_combat.helpers import RemovalConditions


def test_combatant_creation_hit_points() -> None:
    """Current_hit_points defaults to max_hit_points."""
    this_combatant = Combatant(max_hit_points=10)
    assert this_combatant.max_hit_points == 10
    assert this_combatant.current_hit_points == 10
    this_combatant = Combatant(max_hit_points=10, current_hit_points=9)
    assert this_combatant.max_hit_points == 10
    assert this_combatant.current_hit_points == 9


def test_damage_is_recorded() -> None:
    """Damage reduces hit points, but not below zero."""
    this_combatant = Combatant(max_hit_points=10)
    this_combatant.take_damage(hp_damage=3, damage_type=DamageType.ACID)
    assert this_combatant.current_hit_points == 7
    this_combatant.take_damage(hp_damage=8, damage_type=DamageType.ACID)
    assert this_combatant.current_hit_points == 0


def test_combatants_unconscious_at_zero_hp() -> None:
    """Combatant is conscious at >0 hp, and unconscious at 0hp."""
    this_combatant = Combatant(max_hit_points=1)
    assert this_combatant.current_hit_points == 1
    assert this_combatant.conscious is True
    this_combatant.take_damage(hp_damage=1, damage_type=DamageType.ACID)
    assert this_combatant.current_hit_points == 0
    assert this_combatant.conscious is False


def test_healing_is_recorded() -> None:
    """Healing increases hit points, but not above max."""
    this_combatant = Combatant(max_hit_points=10, current_hit_points=6)
    assert this_combatant.current_hit_points == 6
    this_combatant.heal(hp_heal=2)
    assert this_combatant.current_hit_points == 8
    this_combatant.heal(hp_heal=3)
    assert this_combatant.current_hit_points == 10


def test_removal_conditions_met() -> None:
    """Are removal conditions reported accurately?"""
    this_combatant = Combatant(
        max_hit_points=10, fighting_status=FightingStatus.FIGHTING
    )
    assert this_combatant.removal_conditions_met() is False
    this_combatant.fighting_status = FightingStatus.FLED
    assert this_combatant.removal_conditions_met() is True
    this_combatant.fighting_status = FightingStatus.FIGHTING
    this_combatant.current_hit_points = 0
    this_combatant.removal_condition = RemovalConditions.ZERO_HP
    assert this_combatant.removal_conditions_met() is True
    this_combatant.removal_condition = RemovalConditions.DEAD
    assert this_combatant.removal_conditions_met() is False