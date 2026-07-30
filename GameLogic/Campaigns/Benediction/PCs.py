from Characters import Humans, AggressiveBeasts as Beasts
from Maps import World
from Systems import Equipment


def resetPlayer(player) -> None:
    player.atrb["corruption"], player.atrb["fatigue"], player.atrb["injury"] = 0, 0, 0
    player.props["rank"] = "player"
    if "echo" in player.inv: player.inv["echo"] = "None"

    player.atrb["cur_av"] = player.atrb["base_av"]
    player.atrb["cur_sp"] = player.atrb["base_sp"]

    player.atrb["cur_hp"] = player.atrb["base_hp"]
    halfHealth, quarterHealth = player.atrb["base_hp"] // 2, player.atrb["base_hp"] // 4
    player.atrb["half_hp"], player.atrb["quart_hp"] = halfHealth, quarterHealth
    player.atrb["endurance"] = player.atrb["stamina"] = player.atrb["tolerance"] = halfHealth

    player.equip = Equipment.setEquipment(player.abl["attacks"], player.cndt, player.atrb["base_elm"], player.props["job"],
                                           player.props["rank"], player.abl["specialty"] + player.abl["mastery"], "human")


def getBenedictionGroup() -> list:
    Fadia, Hassan, Layth = getFadia(), getHassan(), getLayth()
    benWorld = World.benedictionMap()
    benWorld.worldMap[14][7] = "w/!!↑"

    return {
        "campaign": "Benediction",
        "days": 0,
        "members": [Fadia, Hassan, Layth],
        "world": benWorld
    }


def getAkeem():
    Akeem = Humans.paladin("Adept").ch
    Akeem.props["name"], Akeem.props["initials"] = "Akeem", "A."
    Akeem.atrb["base_av"], Akeem.atrb["base_hp"], Akeem.atrb["base_sp"] = 9, 16, 4
    resetPlayer(Akeem)
    return Akeem

def getFadia():
    Fadia = Humans.mage("Dream", "Adept").ch
    Fadia.props["name"], Fadia.props["initials"] = "Fadia", "F."
    Fadia.atrb["base_av"], Fadia.atrb["base_hp"], Fadia.atrb["base_sp"] = 7, 14, 3
    resetPlayer(Fadia)
    return Fadia

def getHassan():
    Hassan = Humans.brute("Basic", "Adept").ch
    Hassan.props["name"], Hassan.props["initials"] = "Hassan", "H."
    Hassan.atrb["base_av"], Hassan.atrb["base_hp"], Hassan.atrb["base_sp"] = 8, 18, 3
    resetPlayer(Hassan)
    return Hassan

def getLayth():
    Layth = Beasts.lion("Basic", "Juvenile").ch
    Layth.props["name"], Layth.props["initials"] = "Layth", "L."
    Layth.atrb["base_av"], Layth.atrb["base_hp"], Layth.atrb["base_sp"] = 8, 15, 6
    resetPlayer(Layth)
    return Layth