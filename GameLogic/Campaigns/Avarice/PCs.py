from Characters import Humans
from Campaigns.Benediction import PCs as B_PCs
from Maps import World
from Systems import Inventory


def getAvariceGroup(doubleDays) -> list:
    Laura, Martin = getLaura(), getMartin()
    avaWorld = World.AvariceMap()

    return {
        "campaign": "Avarice",
        "days": 0,
        "doubleDays": doubleDays,
        "inventory": [],
        "members": [Laura, Martin],
        "world": avaWorld
    }


def getLaura():
    Laura = Humans.mage("Flame", "Master").ch
    Laura.props["name"], Laura.props["initials"], Laura.props["favored"] = "Laura", "L.", "human"
    Laura.atrb["base_av"], Laura.atrb["base_hp"], Laura.atrb["base_sp"] = 17, 20, 5
    Laura.abl["mastery"] = ["Bring"]
    
    B_PCs.resetPlayer(Laura)
    Laura.equip["armor"] = {"name": "None", "modifier": 0,  "element": "Basic", "tier": "Standard"}
    return Laura

def getMartin():
    Martin = Humans.knight("Basic", "Master").ch
    Martin.props["name"], Martin.props["initials"], Martin.props["favored"] = "Martin", "M.", "beast"
    Martin.atrb["base_av"], Martin.atrb["base_hp"], Martin.atrb["base_sp"] = 16, 23, 6
    Martin.abl["mastery"] = ["Guard"]

    B_PCs.resetPlayer(Martin)
    Martin.equip["armor"] = {"name": "None", "modifier": 0,  "element": "Basic", "tier": "Standard"}
    return Martin

def getWillem():
    Willem = Humans.dragonslayer("Basic", "Master").ch
    Willem.props["name"], Willem.props["initials"], Willem.props["favored"] = "Willem", "W.", "reptile"
    Willem.atrb["base_av"], Willem.atrb["base_hp"], Willem.atrb["base_sp"] = 13, 19, 4
    Willem.abl["mastery"] = ["Bodkin"]
    
    B_PCs.resetPlayer(Willem)
    Willem.equip["armor"] = {"name": "None", "modifier": 0,  "element": "Basic", "tier": "Standard"}
    Willem.inv = Inventory.humanInventory("Basic", "Novice")

    return Willem