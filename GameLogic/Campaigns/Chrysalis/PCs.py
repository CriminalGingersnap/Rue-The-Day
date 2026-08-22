from Characters import Humans, AggressiveBeasts as Beasts
from Campaigns.Benediction import PCs as B_PCs
from Maps import World


def getAvariceGroup(doubleDays) -> list:
    Aditya, Halim, Wira = getAditya(), getHalim(), getWira()
    chrWorld = World.chrysalisMap()

    return {
        "campaign": "Chrysalis",
        "days": 0,
        "doubleDays": doubleDays,
        "inventory": [],
        "members": [Aditya, Halim, Wira],
        "world": chrWorld
    }


def getAditya():
    Aditya = Humans.archer("Basic", "Novice").ch
    Aditya.props["name"], Aditya.props["initials"], Aditya.props["favored"] = "Aditya", "A.", "reptile"
    Aditya.atrb["base_av"], Aditya.atrb["base_hp"], Aditya.atrb["base_sp"] = 12, 19, 4
    
    B_PCs.resetPlayer(Aditya)
    return Aditya

def getHalim():
    Halim = Humans.doctor("Basic", "Master").ch
    Halim.props["name"], Halim.props["initials"], Halim.props["favored"] = "Halim", "H.", "human"
    Halim.atrb["base_av"], Halim.atrb["base_hp"], Halim.atrb["base_sp"] = 14, 22, 5
    Halim.abl["mastery"] = ["Fortify"]
    
    B_PCs.resetPlayer(Halim)
    return Halim

def getWira():
    Wira = Beasts.hound("Dream", "Elder").ch
    Wira.props["name"], Wira.props["initials"], Wira.props["favored"] = "Wira", "W.", "beast"
    Wira.atrb["base_av"], Wira.atrb["base_hp"], Wira.atrb["base_sp"] = 11, 20, 3
    Wira.abl["specialty"] = ["Rally"]
    
    B_PCs.resetPlayer(Wira)
    return Wira