from Characters import Characters
from Maps import World
from pathlib import Path
import json


class nullWorld:
    def __init__(self) -> None:
        self.worldMap = []
        self.legend = {}
        self.start = []
        self.marker = None

class nullCharacter:
    def __init__(self) -> None:        
        self.actionQueue, self.position = [], []
        self.sightMap = [[], [], [], [], [], [], [], [], [], [], [], []]

        dicts = Characters.setDicts()
        self.commits, self.effects, self.itemEffects = dicts[0], dicts[1], dicts[2]

        self.abl = {}
        self.atrb = {}
        self.cndt = {}
        self.equip = {}
        self.inv = {}
        self.props = {}


def saveCharacter(fighter, campaign, template) -> None:
    if fighter.inv["Echos"] == None:
        setFilePath(campaign, template + "sEcho").unlink(missing_ok = True)
    else:
        saveCharacter(fighter.inv["Echos"], campaign, template + "sEcho")
        fighter.inv["Echos"] = None
    
    save = {
        "abl": fighter.abl,
        "atrb": fighter.atrb,
        "cndt": fighter.cndt,
        "equip": fighter.equip,
        "inv": fighter.inv,
        "props": fighter.props
    }
    
    with open(setFilePath(campaign, template), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)

def loadCharacter(fighter, campaign, template) -> None:
    with open(setFilePath(campaign, template), 'r') as jsonFile:
        load = json.load(jsonFile)
        fighter.abl = load["abl"]
        fighter.atrb = load["atrb"]
        fighter.cndt = load["cndt"]
        fighter.equip = load["equip"]
        fighter.inv = load["inv"]
        fighter.props = load["props"]

    try:
        echo = nullCharacter()
        loadCharacter(echo, "Metamorphosis", template + "sEcho")
        fighter.inv["Echos"] = echo
    except FileNotFoundError: pass


def saveWorld(world, campaign, template)-> None:
    save = {
        "map": world.worldMap,
        "legend": world.legend,
        "start": world.marker.position
    }
    
    with open(setFilePath(campaign, template), 'w') as jsonFile:
        json.dump(save, jsonFile, indent=4)

def loadWorld(world, campaign, template) -> None:
    with open(setFilePath(campaign, template), 'r') as jsonFile:
        load = json.load(jsonFile)
        world.worldMap = load["map"]
        world.legend = load["legend"]
        world.start = load["start"]
        world.marker = World.mapMarker(load["map"], load["start"])


def setFilePath(campaign, template) -> Path:
    fileName = campaign + '/' + template + '.json'
    save_dir = Path(__file__).resolve().parent
    return save_dir / fileName