import random

# Martin crafts a blunt weapon after their first encounter with a pierce resistant enemy
# If he equips the blunt weapon, his damage type changes from pierce to blunt.
# Swapping weapons requires him to expend an attack die.

class humanInventory:
    def __init__(self) -> None:
        pillBoxes = {
            "Capacity": 0,
            "Contents": {
                "Pills": {
                    "Flameblood": 0,
                    "Iceblood": 0,
                    "Feyblood": 0,
                    "Corpseblood": 0,
                    "Toxinblood": 0,
                    "Blessedblood": 0,
                    "Vigor": 0,
                },
                "Stones": {
                    "Corpse Core": 0,
                    "Flame Core": 0,
                    "Fey Core": 0,
                    "Ice Core": 0,
                    "Blessed Core": 0,
                    "Toxin Core": 0,
                    "Corpse Pearl": 0,
                    "Flame Pearl": 0,
                    "Fey Pearl": 0,
                    "Ice Pearl": 0,
                    "Blessed Pearl": 0,
                    "Toxin Pearl": 0,
                },
                "Unique": {
                    "Metamorphosis (Fey)": 0,
                    "Metamorphosis (Flame)": 0,
                    "Metamorphosis (Ice)": 0
                }
            }
        }

        vials = {
            "Capacity": 0,
            "Contents": {
                "Resin": {
                    "Basic": 0,
                },
                "Bloods": {
                    "Basic": 0,
                    "Corpse": 0,
                    "Flame": 0,
                    "Fey": 0,
                    "Ice": 0,
                    "Toxin": 0,
                    "Blessed": 0
                },
                "Dusts": {
                    "Corpse": 0,
                    "Flame": 0,
                    "Fey": 0,
                    "Ice": 0,
                    "Blessed": 0,
                    "Toxin": 0
                },
                "Tinctures": {
                    "Corpseblood": 0,
                    "Flameblood": 0,
                    "Iceblood": 0,
                    "Feyblood": 0,
                    "Toxinblood": 0,                    
                    "Blessedblood": 0,
                    "Vigor": 0,
                }      
            }     
        }

        gourd = {
            "Capacity": 20,
            "Contents": {
                "Water": 0
            }
        }

        self.inventory = {
            "Pill Box": pillBoxes,
            "Gourd": gourd,
            "Vials": vials
        }

# add method to set random human inventory based on job, rank, and element

class beastInventory:
    def __init__(self, hp, alignment, rank, type) -> None:
        drop, vitaVolume = {}, 0

        if alignment == "Corpse":
            match hp:
                case "mid": vitaVolume = 1
                case "high": vitaVolume = 2
                case "max": vitaVolume = 3      
        elif type not in ["insect", "invertebrate"]:
            match hp:
                case "min": vitaVolume = 1
                case "low": vitaVolume = 2
                case "mid": vitaVolume = 3
                case "high": vitaVolume = 4
                case "max": vitaVolume = 5
        else:
            match hp:
                case "low": vitaVolume = 1
                case "mid": vitaVolume = 2
                case "high": vitaVolume = 3
                case "max": vitaVolume = 4

        drop = {"Blood": {alignment: vitaVolume}}

        if alignment != "Basic":
            match rank:
                case "Juvenile" | "Fresh": drop["Stones"] = {alignment + " Pearl": 1}
                case "Adult" | "Wizened": drop["Stones"] = {alignment + " Pearl": 2}
                case "Elder" | "Ancient": drop["Stones"] = {alignment + " Core": 1}

        self.inventory = drop


class elementalInventory:
    def __init__(self, alignment, rank) -> None:
        drop = None

        if rank == "Lesser": drop = {"Stones": {alignment + " Pearl": 2}}
        else: drop = {"Stones": {alignment + " Core": 2}}

        self.inventory = drop

class totemInventory:
    def __init__(self, alignment, rank) -> None:
        drop = None

        match rank:
            case "Standard": drop = {"Stones": {alignment + " Pearl": 1}}
            case "Totem": drop = {"Stones": {alignment + " Pearl": 2}}
            case "Monument": drop = {"Stones": {alignment + " Core": 1}}           

        self.inventory = drop


class undeadInventory:
    def __init__(self, hp, rank) -> None:
        drop, vitaVolume = None, 0

        match rank:
            case "Undead": drop = {"Stones": {"Corpse Pearl": 1}}
            case "Ghoul": drop = {"Stones": {"Corpse Pearl": 2}}
            case "Ancient": drop = {"Stones": {"Corpse Core": 1}}
        
        match hp:
            case "mid": vitaVolume = 1
            case "high": vitaVolume = 2
            case "max": vitaVolume = 3

        drop["Blood"] = {"Corpse": vitaVolume}

        self.inventory = drop