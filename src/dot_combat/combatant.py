"""Contains the Combatant class"""
from typing import Optional
from unittest.mock import NonCallableMagicMock

from . import helpers as h


class Combatant:
    def __init__(
        self,
        max_hit_points: int,
        current_hit_points: Optional[int] = None,
        control: str = "DM",
    ):
        """New instance of a Combatant. Needs"""
        self.control: str = control
        self.max_hit_points: int = max_hit_points
        self.current_hit_points: int = (
            current_hit_points if current_hit_points else max_hit_points
        )
        self.conscious = self.current_hit_points > 0

    def is_conscious(self) -> bool:
        return self.current_hit_points > 0

    def take_damage(
        self, hp_damage: int, damage_type: h.DamageType
    ) -> None:
        """Damage the combatant. Combatants become unconscious at zero current_hit_points"""
        self.conscious = hp_damage < self.current_hit_points
        if self.conscious:
            self.current_hit_points -= hp_damage
        else:
            self.current_hit_points = 0

    def heal(self, hp_heal: int) -> None:
        """Heal the combatant. Cannot exceed max_hit_points."""
        if (self.current_hit_points + hp_heal) < self.max_hit_points:
            self.current_hit_points += hp_heal
        else:
            self.current_hit_points = self.max_hit_points