"""Contains the Combatant class."""
from typing import List
from typing import Optional
from typing import Tuple

from . import attack as a
from . import helpers as h
from . import roll as r


class Combatant:
    """An agent in a combat. Has at least initiative, attacks, and hit points."""

    def __init__(
        self,
        max_hit_points: int,
        armor_class: int,
        attacks: List[a.Attack],
        current_hit_points: Optional[int] = None,
        control: str = "DM",
        faction: h.Faction = h.Faction.ENEMIES,
        fighting_status: h.FightingStatus = h.FightingStatus.FIGHTING,
        removal_condition: h.RemovalConditions = h.RemovalConditions.ZERO_HP,
    ):
        """New instance of a Combatant."""
        self.control: str = control
        self.max_hit_points: int = max_hit_points
        self.current_hit_points: int = (
            current_hit_points if current_hit_points else max_hit_points
        )
        self.armor_class = armor_class
        self.attacks = attacks
        self.conscious = self.current_hit_points > 0
        self.faction = faction
        self.fighting_status = fighting_status
        self.removal_condition = removal_condition
        self.movement_available = False
        self.action_available = False
        self.action_available = False
        self.reaction_available = True

    def take_damage(self, hp_damage: int, damage_type: h.DamageType) -> None:
        """Damage the combatant. Current_hit_points cannot fall below zero."""
        self.conscious = hp_damage < self.current_hit_points
        if self.conscious:
            self.current_hit_points -= hp_damage
        else:
            self.current_hit_points = 0

    def heal(self, hp_heal: int) -> None:
        """Heal the combatant. Current_hit_points cannot exceed max_hit_points."""
        if (self.current_hit_points + hp_heal) < self.max_hit_points:
            self.current_hit_points += hp_heal
        else:
            self.current_hit_points = self.max_hit_points

    def roll_initiative(self, dex_modifier: int = 0) -> int:
        """Returns _and_ stores initiative of d20 plus supplied modifier."""
        result = r.roll(full_roll_description="d20")
        result += dex_modifier
        self.initiative = result
        return result

    def removal_conditions_met(self) -> bool:
        """Should this Combatant be removed from combat?"""
        if self.fighting_status == h.FightingStatus.FLED:
            return True
        if self.removal_condition == h.RemovalConditions.ZERO_HP:
            if self.current_hit_points <= 0:
                return True
        return False

    def start_turn(self) -> None:
        """Enables flags for available movement, action, bonus action and reaction."""
        self.movement_available = True
        self.action_available = True
        self.action_available = True
        self.reaction_available = True

    def end_turn(self) -> None:
        """Disables flags for available movement, action, and bonus action."""
        self.movement_available = False
        self.action_available = False
        self.action_available = False

    def roll_attack(
        self,
        attack: a.Attack,
        with_advantage: bool = False,
        with_disadvantage: bool = False,
    ) -> Tuple[int, int, bool]:
        """Make an Attack roll with a given Attack."""
        if attack not in self.attacks:
            raise ValueError(f"{self} does not have this attack available: {attack}.")
        if with_advantage and with_disadvantage:
            raise ValueError("Cannot *roll* with advantage and disadvantge.")
        raw_dice_score = r.roll(full_roll_description="d20")
        if with_advantage or with_disadvantage:
            second_die = r.roll(full_roll_description="d20")
            if with_advantage:
                raw_dice_score = max(raw_dice_score, second_die)
            else:
                raw_dice_score = min(raw_dice_score, second_die)
        return (
            raw_dice_score + attack.attack_bonus,
            raw_dice_score,
            (raw_dice_score == 20),
        )

    def roll_damage(
        self, attack: a.Attack, critical_hit: bool = False
    ) -> Tuple[int, h.DamageType]:
        """Calculate damage and damage type from an Attack."""
        dice_damage: int = r.roll(full_roll_description=attack.damage_dice)
        if critical_hit:
            dice_damage += r.roll(full_roll_description=attack.damage_dice)
        return dice_damage + attack.damage_bonus, attack.damage_type
