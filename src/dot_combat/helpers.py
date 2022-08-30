"""Helper classes including DamageType."""
from enum import Enum


class DamageType(Enum):
    """Enumerates the 13 types of damage, per PHB pg 196."""

    ACID = 1
    BLUDGEONING = 2
    COLD = 3
    FIRE = 4
    FORCE = 5
    LIGHTNING = 6
    NECROTIC = 7
    PIERCING = 8
    POISON = 9
    PSYCHIC = 10
    RADIANT = 11
    SLASHING = 12
    THUNDER = 13


class Conditions(Enum):
    """Enumerates conditions, per PHB pg 290."""

    BLINDED = 1
    CHARMED = 2
    DEAFENED = 3
    FRIGHTENED = 4
    GRAPPLED = 5
    INCAPACITATED = 6
    INVSIBLE = 7
    PARALYZED = 8
    PETRIFIED = 9
    POISONED = 10
    PRONE = 11
    RESTRAINED = 12
    STUNNED = 13
    UNCONSCIOUS = 14
