from Characters import Humans, AggressiveBeasts as Beasts
from Maps import World


def resetPlayer(player) -> None:
    player.atrb["corruption"], player.atrb["fatigue"], player.atrb["injury"] = 0, 0, 0
    player.props["rank"] = "player"
    player.equip["armor"].update({"name": "None", "modifier": 0})
    if "echo" in player.inv: player.inv["echo"] = "None"


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
    resetPlayer(Akeem)
    return Akeem

def getFadia():
    Fadia = Humans.mage("Dream", "Adept").ch
    Fadia.props["name"], Fadia.props["initials"] = "Fadia", "F."
    resetPlayer(Fadia)
    return Fadia

def getHassan():
    Hassan = Humans.brute("Basic", "Adept").ch
    Hassan.props["name"], Hassan.props["initials"] = "Hassan", "H."
    resetPlayer(Hassan)
    return Hassan

def getLayth():
    Layth = Beasts.lion("Basic", "Juvenile").ch
    Layth.props["name"], Layth.props["initials"] = "Layth", "L."
    resetPlayer(Layth)
    return Layth