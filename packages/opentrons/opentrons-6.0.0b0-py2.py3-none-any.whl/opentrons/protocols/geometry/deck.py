import functools
import logging
from collections import UserDict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, List, Dict, Set

from opentrons import types
from opentrons.protocol_api.labware import load as load_lw, Labware
from opentrons.protocols.api_support.constants import deck_type
from opentrons.protocols.api_support.labware_like import LabwareLike
from opentrons.protocols.geometry.deck_item import DeckItem
from opentrons.hardware_control.modules.types import ModuleType
from opentrons.protocols.geometry.module_geometry import (
    ModuleGeometry,
    ThermocyclerGeometry,
)
from opentrons_shared_data.deck import (
    DEFAULT_DECK_DEFINITION_VERSION,
    load as load_deck,
)

if TYPE_CHECKING:
    from opentrons_shared_data.deck.dev_types import (
        SlotDefV3,
    )

MODULE_LOG = logging.getLogger(__name__)


# Amount of slots in a single deck row
ROW_LENGTH = 3
FIXED_TRASH_ID = "fixedTrash"


@dataclass
class CalibrationPosition:
    """
    A point on the deck of a robot that is used to calibrate
    aspects of the robot's movement system as defined by
    opentrons/shared-data/deck/schemas/2.json
    """

    id: str
    position: List[float]
    displayName: str


class Deck(UserDict):
    def __init__(self, load_name: Optional[str] = None) -> None:
        super().__init__()
        row_offset = 90.5
        col_offset = 132.5
        for idx in range(1, 13):
            self.data[idx] = None
        self._positions = {
            idx + 1: types.Point((idx % 3) * col_offset, idx // 3 * row_offset, 0)
            for idx in range(12)
        }
        self._highest_z = 0.0
        if not load_name:
            load_name = deck_type()
        self._definition = load_deck(load_name, DEFAULT_DECK_DEFINITION_VERSION)
        self._load_fixtures()
        self._thermocycler_present = False

    def _load_fixtures(self):
        for f in self._definition["locations"]["fixtures"]:
            slot_name = self._check_name(f["slot"])  # type: ignore
            loaded_f = load_lw(
                f["labware"], self.position_for(slot_name)  # type: ignore
            )
            self.__setitem__(slot_name, loaded_f)

    @staticmethod
    @functools.lru_cache(20)
    def _assure_int(key: object) -> int:
        if isinstance(key, str):
            return int(key)
        elif isinstance(key, int):
            return key
        else:
            raise TypeError(type(key))

    def _check_name(self, key: object) -> int:
        should_raise = False
        try:
            key_int = Deck._assure_int(key)
        except Exception:
            MODULE_LOG.exception("Bad slot name: {}".format(key))
            should_raise = True
        should_raise = should_raise or key_int not in self.data
        if should_raise:
            raise ValueError("Unknown slot: {}".format(key))
        else:
            return key_int

    def __getitem__(self, key: types.DeckLocation) -> DeckItem:
        return self.data[self._check_name(key)]

    def __delitem__(self, key: types.DeckLocation) -> None:
        checked_key = self._check_name(key)
        old = self.data[checked_key]
        self.data[checked_key] = None
        if old:
            self.recalculate_high_z()
            # Update the thermocycler present member
            self._thermocycler_present = any(
                isinstance(item, ThermocyclerGeometry) for item in self.data.values()
            )

    def __setitem__(self, key: types.DeckLocation, val: DeckItem) -> None:
        slot_key_int = self._check_name(key)
        item = self.data.get(slot_key_int)

        overlapping_items = self._get_collisions_for_item(slot_key_int, val)
        if item is not None:
            if slot_key_int == 12:
                if FIXED_TRASH_ID in item.parameters.get("quirks", []):
                    pass
                else:
                    raise ValueError(f"Deck slot {key} is for fixed trash only")
            else:
                raise ValueError(
                    f"Deck slot {key} already"
                    f" has an item: {self.data[slot_key_int].load_name}"
                )
        elif overlapping_items:
            flattened_overlappers = [
                f"{item.load_name} in slot {slot}"
                for slot, sublist in overlapping_items.items()
                for item in sublist
            ]
            raise ValueError(
                f"Could not load {val} because it would"
                f" interfere with {', '.join(flattened_overlappers)}"
            )
        self.data[slot_key_int] = val
        self._highest_z = max(val.highest_z, self._highest_z)
        self._thermocycler_present = any(
            isinstance(item, ThermocyclerGeometry) for item in self.data.values()
        )

    def __contains__(self, key: object) -> bool:
        try:
            key_int = self._check_name(key)
        except ValueError:
            return False
        return key_int in self.data

    def is_edge_move_unsafe(self, mount: types.Mount, target: "Labware") -> bool:
        """
        Check if slot next to target labware contains a module. Only relevant
        depending on the mount you are using and the column you are moving
        to inside of the labware.
        """
        slot = LabwareLike(target).first_parent()
        if not slot:
            return False
        if mount is types.Mount.RIGHT:
            other_labware = self.left_of(slot)
        else:
            other_labware = self.right_of(slot)

        return isinstance(other_labware, ModuleGeometry)

    def right_of(self, slot: str) -> Optional[DeckItem]:
        if int(slot) % ROW_LENGTH == 0:
            # We know we're at the right-most edge
            # of the given row
            return None
        else:
            idx = int(slot) + 1
            return self[str(idx)]

    def left_of(self, slot: str) -> Optional[DeckItem]:
        if int(slot) - 1 % ROW_LENGTH == 0:
            # We know we're at the left-most edge
            # of the given row
            return None
        idx = int(slot) - 1
        if idx < 1:
            return None
        return self[str(idx)]

    def position_for(self, key: types.DeckLocation) -> types.Location:
        key_int = self._check_name(key)
        return types.Location(self._positions[key_int], str(key))

    def recalculate_high_z(self) -> None:
        self._highest_z = 0.0
        for item in [lw for lw in self.data.values() if lw]:
            self._highest_z = max(item.highest_z, self._highest_z)

    def get_slot_definition(self, slot_name) -> "SlotDefV3":
        slots = self._definition["locations"]["orderedSlots"]
        slot_def = next((slot for slot in slots if slot["id"] == slot_name), None)
        if not slot_def:
            slot_ids = [slot["id"] for slot in slots]
            raise ValueError(
                f"slot {slot_name} could not be found,"
                f"valid deck slots are: {slot_ids}"
            )
        return slot_def

    def get_slot_center(self, slot_name) -> types.Point:
        defn = self.get_slot_definition(slot_name)
        return types.Point(
            defn["position"][0] + defn["boundingBox"]["xDimension"] / 2,
            defn["position"][1] + defn["boundingBox"]["yDimension"] / 2,
            defn["position"][2] + defn["boundingBox"]["zDimension"] / 2,
        )

    def resolve_module_location(
        self, module_type: ModuleType, location: Optional[types.DeckLocation]
    ) -> types.DeckLocation:
        dn_from_type = {
            ModuleType.MAGNETIC: "Magnetic Module",
            ModuleType.THERMOCYCLER: "Thermocycler",
            ModuleType.TEMPERATURE: "Temperature Module",
            ModuleType.HEATER_SHAKER: "Heater-Shaker",
        }
        if isinstance(location, str) or isinstance(location, int):
            slot_def = self.get_slot_definition(str(location))
            compatible_modules = slot_def["compatibleModuleTypes"]
            if module_type.value in compatible_modules:
                return location
            else:
                raise AssertionError(
                    f"A {dn_from_type[module_type]} cannot be loaded"
                    f" into slot {location}"
                )
        else:
            valid_slots = [
                slot["id"]
                for slot in self.slots
                if module_type.value in slot["compatibleModuleTypes"]
            ]
            if len(valid_slots) == 1:
                return valid_slots[0]
            elif not valid_slots:
                raise ValueError(
                    "A {dn_from_type[module_type]} cannot be used with this deck"
                )
            else:
                raise AssertionError(
                    f"{dn_from_type[module_type]}s do not have default"
                    " location, you must specify a slot"
                )

    @property
    def highest_z(self) -> float:
        """Return the tallest known point on the deck."""
        return self._highest_z

    @property
    def slots(self) -> List["SlotDefV3"]:
        """Return the definition of the loaded robot deck."""
        return self._definition["locations"]["orderedSlots"]

    @property
    def calibration_positions(self) -> List[CalibrationPosition]:
        raw_positions = self._definition["locations"]["calibrationPoints"]
        return [CalibrationPosition(**pos) for pos in raw_positions]

    def get_calibration_position(self, id: str) -> CalibrationPosition:
        calibration_position = next(
            (pos for pos in self.calibration_positions if pos.id == id), None
        )
        if not calibration_position:
            pos_ids = [pos.id for pos in self.calibration_positions]
            raise ValueError(
                f"calibration position {id} "
                "could not be found, "
                f"valid calibration position ids are: {pos_ids}"
            )
        return calibration_position

    def get_fixed_trash(self) -> Optional[Labware]:
        fixtures = self._definition["locations"]["fixtures"]
        ft = next((f for f in fixtures if f["id"] == FIXED_TRASH_ID), None)
        return self.data[self._check_name(ft.get("slot"))] if ft else None

    def get_non_fixture_slots(self) -> List[types.DeckLocation]:
        fixtures = self._definition["locations"]["fixtures"]
        fixture_slots = {
            self._check_name(f.get("slot")) for f in fixtures if f.get("slot")
        }
        return [s for s in self.data.keys() if s not in fixture_slots]

    def _get_collisions_for_item(
        self, slot_key: types.DeckLocation, item: DeckItem
    ) -> Dict[types.DeckLocation, List[DeckItem]]:
        """Return the loaded deck items that collide with the given item."""

        def get_item_covered_slot_keys(sk, i) -> Set[str]:
            if isinstance(i, ThermocyclerGeometry):
                return i.covered_slots
            elif i is not None:
                return set([sk])
            else:
                return set()

        item_slot_keys = get_item_covered_slot_keys(slot_key, item)
        colliding_items: Dict[types.DeckLocation, List[DeckItem]] = {}

        for slot_key, existing_item in self.data.items():
            occupied_slot_keys = get_item_covered_slot_keys(slot_key, existing_item)
            conflicting_slot_keys = occupied_slot_keys & item_slot_keys

            if len(conflicting_slot_keys) > 0:
                for conflict in conflicting_slot_keys:
                    colliding_items.setdefault(conflict, []).append(existing_item)

        return colliding_items

    @property
    def thermocycler_present(self) -> bool:
        """Is a thermocycler present on the deck."""
        return self._thermocycler_present
