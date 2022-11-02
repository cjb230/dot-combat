"""Test cases for the Combatant class."""
import copy

import pytest

from dot_combat.attack import Attack
from dot_combat.combatant import Combatant
from dot_combat.helpers import DamageType
from dot_combat.helpers import FightingStatus
from dot_combat.helpers import RemovalConditions


def test_combatant_creation_hit_points(test_attack_list) -> None:
    """Current_hit_points defaults to max_hit_points."""
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    assert this_combatant.max_hit_points == 10
    assert this_combatant.current_hit_points == 10
    this_combatant = Combatant(
        max_hit_points=10,
        current_hit_points=9,
        armor_class=15,
        attacks=test_attack_list,
    )
    assert this_combatant.max_hit_points == 10
    assert this_combatant.current_hit_points == 9


def test_damage_is_recorded(test_attack_list) -> None:
    """Damage reduces hit points, but not below zero."""
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    this_combatant.take_damage(hp_damage=3, damage_type=DamageType.ACID)
    assert this_combatant.current_hit_points == 7
    this_combatant.take_damage(hp_damage=8, damage_type=DamageType.ACID)
    assert this_combatant.current_hit_points == 0


def test_combatants_unconscious_at_zero_hp(test_attack_list) -> None:
    """Combatant is conscious at >0 hp, and unconscious at 0hp."""
    this_combatant = Combatant(
        max_hit_points=1, armor_class=15, attacks=test_attack_list
    )
    assert this_combatant.current_hit_points == 1
    assert this_combatant.conscious is True
    this_combatant.take_damage(hp_damage=1, damage_type=DamageType.ACID)
    assert this_combatant.current_hit_points == 0
    assert this_combatant.conscious is False


def test_healing_is_recorded(test_attack_list) -> None:
    """Healing increases hit points, but not above max."""
    this_combatant = Combatant(
        max_hit_points=10,
        current_hit_points=6,
        armor_class=15,
        attacks=test_attack_list,
    )
    assert this_combatant.current_hit_points == 6
    this_combatant.heal(hp_heal=2)
    assert this_combatant.current_hit_points == 8
    this_combatant.heal(hp_heal=3)
    assert this_combatant.current_hit_points == 10


def test_removal_conditions_met(test_attack_list) -> None:
    """Are removal conditions reported accurately?"""
    this_combatant = Combatant(
        max_hit_points=10,
        fighting_status=FightingStatus.FIGHTING,
        armor_class=15,
        attacks=test_attack_list,
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


def test_roll_attack(mocker, test_attack_list):
    """Is the attack characterised correctly?"""
    attack_list_1 = copy.deepcopy(test_attack_list)
    mocker.patch("dot_combat.roll.single_die_roll", return_value=1)
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    attack_score, raw_score, is_critical = this_combatant.roll_attack(
        attack=this_combatant.attacks[0]
    )
    assert attack_score == 1
    assert raw_score == 1
    assert is_critical is False
    this_combatant.attacks[0].attack_bonus = 3
    attack_score, raw_score, is_critical = this_combatant.roll_attack(
        attack=this_combatant.attacks[0]
    )
    assert attack_score == 4
    assert raw_score == 1
    assert is_critical is False
    mocker.patch("dot_combat.roll.single_die_roll", return_value=19)
    attack_score, raw_score, is_critical = this_combatant.roll_attack(
        attack=this_combatant.attacks[0]
    )
    assert attack_score == 22
    assert raw_score == 19
    assert is_critical is False
    mocker.patch("dot_combat.roll.single_die_roll", return_value=20)
    attack_score, raw_score, is_critical = this_combatant.roll_attack(
        attack=this_combatant.attacks[0]
    )
    assert attack_score == 23
    assert raw_score == 20
    assert is_critical is True
    mocker.patch("dot_combat.roll.single_die_roll", side_effect=[1, 20, 1, 20])
    attack_score, raw_score, is_critical = this_combatant.roll_attack(
        attack=this_combatant.attacks[0], with_advantage=True
    )
    assert attack_score == 23
    assert raw_score == 20
    assert is_critical is True
    attack_score, raw_score, is_critical = this_combatant.roll_attack(
        attack=this_combatant.attacks[0], with_disadvantage=True
    )
    assert attack_score == 4
    assert raw_score == 1
    assert is_critical is False
    # Error when indicating both advantage and disadvantage
    with pytest.raises(ValueError):
        _, _, _ = this_combatant.roll_attack(
            attack=this_combatant.attacks[0],
            with_disadvantage=True,
            with_advantage=True,
        )
    # Error when using an attack that the combatant does not have
    with pytest.raises(ValueError):
        _, _, _ = this_combatant.roll_attack(attack=attack_list_1[0])


def test_roll_damage(mocker, test_attack_list):
    """Is damage calculated correctly?"""
    mocker.patch("dot_combat.roll.single_die_roll", return_value=1)
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    damage_amt, damage_type = this_combatant.roll_damage(
        attack=this_combatant.attacks[0], critical_hit=False
    )
    assert damage_amt == 1
    assert damage_type == DamageType.PIERCING
    damage_amt, damage_type = this_combatant.roll_damage(
        attack=this_combatant.attacks[0], critical_hit=True
    )
    assert damage_amt == 2
    assert damage_type == DamageType.PIERCING
    this_combatant.attacks[0].damage_bonus = 4
    this_combatant.attacks[0].damage_type = DamageType.ACID
    damage_amt, damage_type = this_combatant.roll_damage(
        attack=this_combatant.attacks[0], critical_hit=True
    )
    assert damage_amt == 6
    assert damage_type == DamageType.ACID


def test_combatants_dodging(test_attack_list):
    """Tests dodge() function and is_dodging attribute.

    1 - is_dodging is True from the Dodge action being taken until the start
    of the next turn.

    2 - Combatant cannot dodge() if they do not have an action available.
    """
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    assert this_combatant.is_dodging is False
    this_combatant.start_turn()
    this_combatant.dodge()
    assert this_combatant.is_dodging is True
    this_combatant.end_turn()
    assert this_combatant.is_dodging is True
    this_combatant.start_turn()
    assert this_combatant.is_dodging is False
    this_combatant.action_available = False
    with pytest.raises(ValueError):
        this_combatant.dodge()


def test_combatants_disengaging(test_attack_list):
    """Tests disengage() function and is_disengaging attribute.

    is_disengaging is True from the Disengage action being taken until the
    start of the next turn.

    2 - Combatants cannot disengage() if they do not have an action available.
    """
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    assert this_combatant.is_disengaging is False
    this_combatant.start_turn()
    this_combatant.disengage()
    assert this_combatant.is_disengaging is True
    this_combatant.end_turn()
    assert this_combatant.is_disengaging is True
    this_combatant.start_turn()
    assert this_combatant.is_disengaging is False
    this_combatant.action_available = False
    with pytest.raises(ValueError):
        this_combatant.disengage()


def test_combatants_readied(test_attack_list):
    """Tests make_ready() function and is_readied attribute.

    1 - is_readied is True from the Disengage action being taken until the
    start of the next turn.

    2 - Combatant cannot make_ready() if they do not have an action available.
    """
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    assert this_combatant.is_readied is False
    this_combatant.start_turn()
    this_combatant.make_ready()
    assert this_combatant.is_readied is True
    this_combatant.end_turn()
    assert this_combatant.is_readied is True
    this_combatant.start_turn()
    assert this_combatant.is_readied is False
    this_combatant.action_available = False
    with pytest.raises(ValueError):
        this_combatant.make_ready()


def test_take_readied_action(test_attack_list):
    """is_readied becomes False when take_readied_action() is called."""
    this_combatant = Combatant(
        max_hit_points=10, armor_class=15, attacks=test_attack_list
    )
    assert this_combatant.is_readied is False
    with pytest.raises(ValueError):
        this_combatant.take_readied_action()
    this_combatant.start_turn()
    this_combatant.make_ready()
    this_combatant.end_turn()
    assert this_combatant.is_readied is True
    this_combatant.take_readied_action()
    assert this_combatant.is_readied is False
