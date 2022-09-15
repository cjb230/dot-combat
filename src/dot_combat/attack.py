"""Information about an attack available to a Combatant."""
from dataclasses import dataclass

from . import helpers as h


@dataclass
class Attack:
    """An attack specific to a Combatant."""

    name: str
    attack_bonus: int
    damage_dice: str
    damage_bonus: int
    damage_type: h.DamageType
    range: int
    long_range: int
