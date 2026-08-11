from Characters import Humans, Totems
from Campaigns.Benediction import PCs as B_PCs
from Maps import World


def getAvariceGroup() -> list:
    Laura, Martin = getLaura(), getMartin()
    avaWorld = World.AvariceMap()

    return {
        "campaign": "Avarice",
        "days": 1,
        "inventory": [],
        "members": [Laura, Martin],
        "world": avaWorld
    }


def getLaura():
    Laura = Humans.mage("Flame", "Master").ch
    Laura.props["name"], Laura.props["initials"], Laura.props["favored"] = "Laura", "L.", "human"
    Laura.atrb["base_av"], Laura.atrb["base_hp"], Laura.atrb["base_sp"] = 8, 15, 4
    Laura.abl["mastery"] = ["Bring"]
    
    B_PCs.resetPlayer(Laura)
    Laura.equip["armor"] = {"name": "None", "modifier": 0,  "element": "Basic"}
    return Laura

def getMartin():
    Martin = Humans.knight("Basic", "Master").ch
    Martin.props["name"], Martin.props["initials"], Martin.props["favored"] = "Martin", "M.", "beast"
    Martin.atrb["base_av"], Martin.atrb["base_hp"], Martin.atrb["base_sp"] = 9, 17, 5
    Martin.abl["mastery"] = ["Guard"]

    B_PCs.resetPlayer(Martin)
    Martin.equip["armor"] = {"name": "None", "modifier": 0,  "element": "Basic"}

    totem = Totems.guidance("Dream", "Standard").ch
    totem.cndt["planted"], totem.cndt["reposed"] = False, False
    totem.props["rank"], totem.props["initials"], totem.props["name"] = "player", "Ms", "Martin's Standard"
    Martin.inv["standard"] = totem

    return Martin

def getWillem():
    Willem = Humans.dragonslayer("Basic", "Master").ch
    Willem.props["name"], Willem.props["initials"], Willem.props["favored"] = "Willem", "W.", "reptile"
    Willem.atrb["base_av"], Willem.atrb["base_hp"], Willem.atrb["base_sp"] = 8, 14, 3
    Willem.abl["mastery"] = ["Bodkin"]
    
    B_PCs.resetPlayer(Willem)
    Willem.equip["armor"] = {"name": "None", "modifier": 0,  "element": "Basic"}

    return Willem