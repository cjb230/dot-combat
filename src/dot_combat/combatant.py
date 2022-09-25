"""Contains the Combatant class."""
from typing import Optional

from . import helpers as h
from . import roll as r


class Combatant:
    """An agent in a combat. Has at least initiative, attacks, and hit points."""

    def __init__(
        self,
        max_hit_points: int,
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
