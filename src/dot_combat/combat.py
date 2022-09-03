"""Contains the Combat class."""
from typing import List

from . import combatant as c

class Combat:
    """Keeps a collection of Combatants and tracks progress of fight."""
    def __init__(self, combatant_list: List[c.Combatant]):
        self.has_started: bool = False
        self.has_finished: bool = False
        self.current_round: int = 0
        self.current_initiative: int = 0
        self.initiative_order: dict = {}
        self.combatant_list: List[c.Combatant] = combatant_list
        self.current_combatant: c.Combatant = None
        self.used_initiatives: List[int] = None

    def populate_used_initiatives(self) -> None:
        """Recreate the used_initiatives list."""
        self.used_initiatives = sorted(self.initiative_order.keys(), reverse=True)


    def fill_initiative_list(self) -> None:
        """Populates initiative_order dict.
        
        Each combatant in combatant_list generates its own initiative"""
        for combatant in self.combatant_list:
            initiative = combatant.roll_initiative(dex_modifier=0)
            if initiative in self.initiative_order:
                self.initiative_order[initiative].append(combatant)
            else:
                self.initiative_order[initiative] = [combatant]
        self.populate_used_initiatives()

    def add_combatant(self, new_combatant: c.Combatant) -> None:
        """Adds supplied combatant to combatant_list, and to initiative_order if that is populated."""
        self.combatant_list.append(new_combatant)
        if self.initiative_order:
            new_initiative = new_combatant.roll_initiative()
            if new_initiative in self.initiative_order:
                self.initiative_order[new_initiative].append(new_combatant)
            else:
                self.initiative_order[new_initiative] = [new_combatant]
        self.used_initiatives = sorted(self.initiative_order.keys(), reverse=True)

    def add_combatants(self, new_combatants: List[c.Combatant]) -> None:
        """Iteratively adds members of supplied list of combatants."""
        for new_combatant in new_combatants:
            self.add_combatant(new_combatant=new_combatant)

    def can_start_combat(self) -> bool:
        """True when all prerequisites are complete to begin combat."""
        if not self.combatant_list:
            print("empty combatant list")
            return False
        if not self.initiative_order:
            print("initiative order not populated")
            return False
        if self.current_round != 0:
            print("current round must be zero before starting")
            return False
        return True

    def start_combat(self) -> None:
        """Start the round counter, set the current initiative and current combatant."""
        self.current_round = 1
        self.current_initiative = self.used_initiatives[0]
        self.current_combatant = self.initiative_order[self.current_initiative][0]
        self.has_started = True

    def next_combatant(self) -> c.Combatant:
        """Return the combatant that will be next, without advancing current_combatant."""
        num_equal_initiative_combatants = len(self.initiative_order[self.current_initiative])
        if num_equal_initiative_combatants > 1 and self.initiative_order[self.current_initiative][-1] != self.current_combatant:
            for position, combatant in enumerate(self.initiative_order[self.current_initiative]):
                if combatant == self.current_combatant:
                    #return self.current_initiative, position
                    #return self.current_initiative, position, self.initiative_order
                    return self.initiative_order[self.current_initiative][position + 1]
        return self.initiative_order[self.next_initiative][0]

    def advance_combatant(self) -> c.Combatant:
        """Advance the combatant by one and return them."""
        self.current_combatant = self.next_combatant()
        return self.current_combatant

    def next_initiative(self) -> int:
        """Returns the next initiative value for the next combatant, without changing the current initiative."""
        for this_initiative in self.used_initiatives:
            if this_initiative < self.current_initiative:
                return this_initiative
        return max(self.used_initiatives)

    def advance_initiative(self) -> None:
        """Advance the initiative
        
        Goes to the next used initiative, or back to the highest if currently
        at the lowest used initiative."""
        self.current_initiative = self.next_initiative()

    def advance_round(self) -> int:
        """Increment the round number and return it."""
        self.current_round += 1
        return self.current_round
