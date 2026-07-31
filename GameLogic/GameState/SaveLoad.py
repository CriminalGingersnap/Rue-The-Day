from Campaigns.Benediction import PCs as B_PCs
from Campaigns.Avarice import PCs as A_PCs
from Characters import Characters
from Maps import World
from Systems import PlayerSelect as Select
from pathlib import Path
import json


class nullCharacter:
    def __init__(self) -> None:        
        self.attackQueue, self.pos = [], []
        self.sightMap = [[], [], [], [], [], [], [], [], [], [], [], []]

        dicts = Characters.setDicts()
        self.commits, self.effects, self.itemEffects = dicts[0], dicts[1], dicts[2]

        self.abl = {}
        self.atrb = {}
        self.cndt = {}
        self.equip = {}
        self.inv = {}
        self.props = {}

class nullWorld:
    def __init__(self) -> None:
        self.worldMap = []
        self.legend = {}
        self.start = []
        self.marker = None


def saveCharacter(fighter, campaign, slot, name) -> None:
    if "echo" in fighter.inv:
        if fighter.inv["echo"] == "None":
            setFilePath(campaign, slot, name + "sEcho").unlink(missing_ok = True)
        else:
            saveCharacter(fighter.inv["echo"], campaign, slot, name + "sEcho")
            fighter.inv["echo"] = "None"

    if "standard" in fighter.inv:
        if fighter.inv["standard"] == "None":
            setFilePath(campaign, slot, name + "sStandard").unlink(missing_ok = True)
        else:
            saveCharacter(fighter.inv["standard"], campaign, slot, name + "sStandard")
            fighter.inv["standard"] = "None"
    
    save = {
        "abl": fighter.abl,
        "atrb": fighter.atrb,
        "cndt": fighter.cndt,
        "equip": fighter.equip,
        "inv": fighter.inv,
        "props": fighter.props
    }
    
    with open(setFilePath(campaign, slot, name), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)


def loadCharacter(fighter, campaign, slot, name) -> None:
    with open(setFilePath(campaign, slot, name), 'r') as jsonFile:
        load = json.load(jsonFile)
        fighter.abl = load["abl"]
        fighter.atrb = load["atrb"]
        fighter.cndt = load["cndt"]
        fighter.equip = load["equip"]
        fighter.inv = load["inv"]
        fighter.props = load["props"]

    try:
        echo = nullCharacter()
        loadCharacter(echo, campaign, slot, name + "sEcho")
        fighter.inv["echo"] = echo
    except FileNotFoundError: pass

    try:
        standard = nullCharacter()
        loadCharacter(standard, campaign, slot, name + "sStandard")
        fighter.inv["standard"] = standard
    except FileNotFoundError: pass

    Select.waitPrint(fighter.props["name"] + " loaded.")


def saveWorld(world, campaign, slot)-> None:
    save = {
        "ace": world.ace,
        "events": world.events,
        "map": world.worldMap,
        "legend": world.legend,
        "start": world.marker.pos
    }
    
    with open(setFilePath(campaign, slot, "World"), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)

def loadWorld(world, campaign, slot) -> None:
    with open(setFilePath(campaign, slot, "World"), 'r') as jsonFile:
        load = json.load(jsonFile)
        world.worldMap = load["ace"]
        world.worldMap = load["events"]
        world.worldMap = load["map"]
        world.legend = load["legend"]
        world.start = load["start"]
        world.marker = World.mapMarker(load["map"], load["start"])

    Select.waitPrint(campaign + " world loaded.")


def saveGroup(group) -> None:
    Select.waitPrint("Enter Save Slot (3 Per Campaign):")
    slot = str(Select.takeInput(1, 3))

    memberNames = []
    for member in group["members"]:
        if member.props["rank"] == "player":
            saveCharacter(member, group["campaign"], slot, member.props["name"])
            memberNames += [member.props["name"]]
    
    saveWorld(group["world"], group["campaign"], slot)

    save = {
        "campaign": group["campaign"],
        "days": group["days"],
        "members": memberNames,
    }

    with open(setFilePath(group["campaign"], slot, "Group"), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)


def loadGroup(campaign) -> dict:
    world = nullWorld()

    group = {
        "campaign": "",
        "days": 0,
        "members": [],
        "world": world
    }

    Select.waitPrint("Enter Save Slot (1-3):")
    slot = str(Select.takeInput(1, 3))

    try:
        with open(setFilePath(campaign, slot, "Group"), 'r') as jsonFile:
            load = json.load(jsonFile)
            group["campaign"] = load["campaign"]
            group["days"] = load["days"]

            for name in load["members"]:
                fighter = nullCharacter()
                loadCharacter(fighter, campaign, slot, name)
                group["members"] += [fighter]

        loadWorld(world, campaign, slot)

    except FileNotFoundError:
        Select.waitPrint("New Save File")
        Select.waitPrint("\nThis game does not save automatically. Save manually by resting between encounters.")
        input("Press enter to acknowledge.\n")

        match campaign:
            case "Avarice": group = A_PCs.getAvariceGroup()
            case "Benediction": group = B_PCs.getBenedictionGroup()

    return group


def setFilePath(campaign, slot, template) -> Path:
    fileName = campaign + '/' + slot + "/" + template + '.json'
    save_dir = Path(__file__).resolve().parent
    return save_dir / fileName