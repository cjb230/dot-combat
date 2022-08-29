"""Test cases for the Combatant class."""
from src.dot_combat.combatant import Combatant
from src.dot_combat.helpers import DamageType


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
