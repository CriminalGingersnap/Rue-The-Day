from Characters import Humans, Totems
from Campaigns.Benediction import PCs as B_PCs
from Maps import World


def getMetamorphosisGroup() -> list:
    Laura, Martin = getLaura(), getMartin()
    metWorld = World.metamorphosisMap()

    return {
        "campaign": "Metamorphosis",
        "days": 0,
        "members": [Laura, Martin],
        "world": metWorld
    }


def getLaura():
    Laura = Humans.mage("Flame", "Elite").ch
    Laura.props["name"], Laura.props["initials"] = "Laura", "L."
    B_PCs.resetPlayer(Laura)
    return Laura

def getMartin():
    Martin = Humans.knight("Basic", "Elite").ch
    Martin.props["name"], Martin.props["initials"] = "Martin", "M."
    B_PCs.resetPlayer(Martin)

    totem = Totems.guidance("Dream", "Standard").ch
    totem.cndt["planted"], totem.cndt["reposed"] = False, False
    totem.props["rank"], totem.props["initials"], totem.props["name"] = "player", "Ms", "Martin's Standard"
    Martin.inv["standard"] = totem

    return Martin

def getWillem():
    Willem = Humans.dragonslayer("Basic", "Master").ch
    Willem.props["name"], Willem.props["initials"] = "Willem", "W."
    B_PCs.resetPlayer(Willem)
    return Willem