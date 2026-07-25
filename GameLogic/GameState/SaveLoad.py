from Characters import Characters
from Maps import World
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


def saveCharacter(fighter, campaign, name) -> None:
    if fighter.inv["echo"] == "None":
        setFilePath(campaign, name + "sEcho").unlink(missing_ok = True)
    else:
        saveCharacter(fighter.inv["echo"], campaign, name + "sEcho")
        fighter.inv["echo"] = "None"

    if fighter.inv["standard"] == "None":
        setFilePath(campaign, name + "sStandard").unlink(missing_ok = True)
    else:
        saveCharacter(fighter.inv["standard"], campaign, name + "sStandard")
        fighter.inv["standard"] = "None"
    
    save = {
        "abl": fighter.abl,
        "atrb": fighter.atrb,
        "cndt": fighter.cndt,
        "equip": fighter.equip,
        "inv": fighter.inv,
        "props": fighter.props
    }
    
    with open(setFilePath(campaign, name), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)

def loadCharacter(fighter, campaign, name) -> None:
    with open(setFilePath(campaign, name), 'r') as jsonFile:
        load = json.load(jsonFile)
        fighter.abl = load["abl"]
        fighter.atrb = load["atrb"]
        fighter.cndt = load["cndt"]
        fighter.equip = load["equip"]
        fighter.inv = load["inv"]
        fighter.props = load["props"]

    try:
        echo = nullCharacter()
        loadCharacter(echo, campaign, name + "sEcho")
        fighter.inv["echo"] = echo
    except FileNotFoundError: pass

    try:
        standard = nullCharacter()
        loadCharacter(standard, campaign, name + "sStandard")
        fighter.inv["standard"] = echo
    except FileNotFoundError: pass


def saveWorld(world, campaign)-> None:
    save = {
        "map": world.worldMap,
        "legend": world.legend,
        "start": world.marker.pos
    }
    
    with open(setFilePath(campaign, "World"), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)

def loadWorld(world, campaign) -> None:
    with open(setFilePath(campaign, "World"), 'r') as jsonFile:
        load = json.load(jsonFile)
        world.worldMap = load["map"]
        world.legend = load["legend"]
        world.start = load["start"]
        world.marker = World.mapMarker(load["map"], load["start"])


def saveGroup(group) -> None:
    memberNames = []
    for member in group["members"]:
        saveCharacter(member, group["campaign"], member.props["name"])
        memberNames += [member.props["name"]]
    
    saveWorld(group["world"], group["campaign"])

    save = {
        "campaign": group["campaign"],
        "days": group["days"],
        "members": memberNames,
    }

    with open(setFilePath(group["campaign"], "Group"), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)

def loadGroup(campaign) -> dict:
    nullWorld = nullWorld()

    group = {
        "campaign": "",
        "days": 0,
        "members": [],
        "world": nullWorld
    }

    with open(setFilePath(campaign, "Group"), 'r') as jsonFile:
        load = json.load(jsonFile)
        group["campaign"] = load["campaign"]
        group["days"] = load["days"]

        for name in load["members"]:
            nullPC = nullCharacter()
            loadCharacter(nullPC, "Metamorphosis", name)
            group["members"] += [nullPC]

    loadWorld(nullWorld, campaign, "Map")

    return group


def setFilePath(campaign, template) -> Path:
    fileName = campaign + '/' + template + '.json'
    save_dir = Path(__file__).resolve().parent
    return save_dir / fileName