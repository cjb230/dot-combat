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
    ):
        """New instance of a Combatant."""
        self.control: str = control
        self.max_hit_points: int = max_hit_points
        self.current_hit_points: int = (
            current_hit_points if current_hit_points else max_hit_points
        )
        self.conscious = self.current_hit_points > 0

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
