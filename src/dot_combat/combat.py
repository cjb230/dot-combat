"""Contains the Combat class."""
from typing import List
from typing import Union

from . import combatant as c
from . import helpers as h


class Combat:
    """Keeps a collection of Combatants and tracks progress of fight."""

    def __init__(self, combatant_list: List[c.Combatant]):
        """New instance with the supplied list of Combatants."""
        self.has_started: bool = False
        self.has_finished: bool = False
        self.current_round: int = 0
        self.current_initiative: int = 0
        self.initiative_order: dict = {}
        self.combatant_list: List[c.Combatant] = combatant_list
        self.current_combatant: Union[c.Combatant, None] = None
        self.used_initiatives: List[int] = []
        self.narrative_log: str = ""
        self.technical_log: str = ""

    def narrative_log_comment(self, comment: str) -> None:
        """Append line to narrative log."""
        log_line = (
            f"R: {str(self.current_round)}  "
            f"I:{str(self.current_initiative)} {comment}\n"
        )
        self.narrative_log += log_line

    def technical_log_comment(self, comment: str) -> None:
        """Append line to technical log."""
        log_line = (
            f"R: {str(self.current_round)}  "
            f"I:{str(self.current_initiative)} {comment}\n"
        )
        self.technical_log += log_line

    def populate_used_initiatives(self) -> None:
        """Recreate the used_initiatives list."""
        self.technical_log_comment("Repopulated used initiative list.")
        self.used_initiatives = sorted(self.initiative_order.keys(), reverse=True)

    def fill_initiative_list(self) -> None:
        """Populates initiative_order dict.

        Each combatant in combatant_list generates its own initiative
        """
        self.technical_log_comment("Filled initiative order.")
        for combatant in self.combatant_list:
            initiative = combatant.roll_initiative(dex_modifier=0)
            if initiative in self.initiative_order:
                self.initiative_order[initiative].append(combatant)
            else:
                self.initiative_order[initiative] = [combatant]
        self.populate_used_initiatives()

    def add_combatant(self, new_combatant: c.Combatant) -> None:
        """Adds supplied combatant to combatant_list.

        Also adds combatant to initiative_order if that is populated.
        """
        self.narrative_log_comment(
            comment=f"Combatant {str(new_combatant)} joined the combat."
        )
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
        self.technical_log_comment(f"Adding {len(new_combatants)} new combatants.")
        for new_combatant in new_combatants:
            self.add_combatant(new_combatant=new_combatant)

    def can_start_combat(self) -> bool:
        """True when all prerequisites are complete to begin combat."""
        if not self.combatant_list:
            self.technical_log_comment(
                "Cannot start combat as there are no combatants."
            )
            return False
        if not self.initiative_order:
            self.technical_log_comment(
                "Cannot start combat as the initiative order is not populated."
            )
            return False
        if self.current_round != 0:
            self.technical_log_comment(
                f"Cannot start combat as current round = {str(self.current_round)}."
            )
            return False
        self.technical_log_comment("Can start combat.")
        return True

    def remove_combatant(self, combatant_to_remove: c.Combatant) -> None:
        """Remove Combatant from this combat.

        Combatant removed from combatant_list, and from initiative_order if it
        is populated. Combat finished automatically if combat_over() is True.
        """
        self.narrative_log_comment(
            comment=f"Removing Combatant {str(combatant_to_remove)}."
        )
        try:
            self.combatant_list.remove(combatant_to_remove)
        except ValueError as ve:
            raise ValueError(
                f"Combatant {str(combatant_to_remove)} not found in combatant list."
            ) from ve
        if self.initiative_order:
            combatant_initiative: int
            for initiative, combatants in self.initiative_order.items():
                if combatant_to_remove in combatants:
                    combatants.remove(combatant_to_remove)
                    combatant_initiative = initiative
                    break
            else:  # I finally used it.
                raise ValueError(
                    f"Combatant {str(combatant_to_remove)} not found in "
                    "initiative order."
                )
            if len(self.initiative_order[combatant_initiative]) == 0:
                del self.initiative_order[combatant_initiative]
        if self.combat_over():
            self.end_combat()

    def start_combat(self) -> None:
        """Start the round counter, set the current initiative and current combatant."""
        self.technical_log_comment("Starting combat.")
        self.current_round = 1
        self.current_initiative = self.used_initiatives[0]
        self.current_combatant = self.initiative_order[self.current_initiative][0]
        self.has_started = True

    def next_combatant(self) -> c.Combatant:
        """Return the combatant that will be next."""
        self.technical_log_comment("Getting next combatant.")
        num_equal_initiative_combatants = len(
            self.initiative_order[self.current_initiative]
        )
        if (
            num_equal_initiative_combatants > 1
            and self.initiative_order[self.current_initiative][-1]
            != self.current_combatant
        ):
            for position, combatant in enumerate(
                self.initiative_order[self.current_initiative]
            ):
                if combatant == self.current_combatant:
                    return self.initiative_order[self.current_initiative][position + 1]
            raise ValueError(
                f"next_combatant() could not find {str(self.current_combatant)}"
                f" in the list for initiative {self.current_initiative}"
            )
        return self.initiative_order[self.next_initiative()][0]

    def advance_combatant(self) -> c.Combatant:
        """Advance the combatant by one and return them."""
        self.technical_log_comment(f"Moving to Combatant {str(self.next_combatant())}.")
        self.current_combatant = self.next_combatant()
        return self.current_combatant

    def next_initiative(self) -> int:
        """Returns the next initiative value.

        Goes to the next used initiative, or back to the highest if currently
        at the lowest used initiative.
        """
        for this_initiative in self.used_initiatives:
            if this_initiative < self.current_initiative:
                return this_initiative
        return max(self.used_initiatives)

    def advance_initiative(self) -> None:
        """Advance the initiative."""
        self.technical_log_comment(
            f"Moving to initiative {str(self.next_initiative())}."
        )
        self.current_initiative = self.next_initiative()

    def advance_round(self) -> int:
        """Increment the round number and return it."""
        self.technical_log_comment(f"Starting round {str(self.current_round+1)}.")
        self.current_round += 1
        return self.current_round

    def combat_over(self) -> bool:
        """Should the combat be finished?"""
        if not self.has_started:
            self.technical_log_comment("Combat cannot end because it has not started.")
            return False

        # are multiple factions present?
        enemies_present: bool = False
        pcs_present: bool = False
        for combatant in self.combatant_list:
            if combatant.faction == h.Faction.ENEMIES:
                enemies_present = True
            else:
                pcs_present = True
            if enemies_present and pcs_present:
                self.technical_log_comment(
                    "Combat cannot end because multiple factions are still present."
                )
                return False
        self.technical_log_comment("Combat can end.")
        return True

    def end_combat(self) -> None:
        """End the combat."""
        self.technical_log_comment("Ending the combat.")
        self.has_finished = True
        print()
        print(self.narrative_log)
        print()
        print(self.technical_log)
