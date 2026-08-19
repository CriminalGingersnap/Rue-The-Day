from Characters import Humans, AggressiveBeasts as Beasts
from Maps import World
from Systems import Equipment


def resetPlayer(player) -> None:
    player.atrb["corruption"], player.atrb["fatigue"], player.atrb["injury"] = 0, 0, 0
    player.props["rank"] = "player"

    player.atrb["cur_av"] = player.atrb["base_av"]
    player.atrb["cur_sp"] = player.atrb["base_sp"]

    player.atrb["cur_hp"] = player.atrb["base_hp"]
    player.atrb["quart_hp"] = player.atrb["base_hp"] // 4
    player.atrb["half_hp"] = player.atrb["endurance"] = player.atrb["stamina"] = player.atrb["tolerance"] = player.atrb["base_hp"] // 2

    player.equip = Equipment.setEquipment(player.abl["attacks"], player.cndt, player.atrb["base_elm"], player.props["job"],
                                           player.props["rank"], player.abl["specialty"] + player.abl["mastery"], "human")

    if player.inv["echo"] != "None":
        player.inv["echo"].props["rank"] = "player"
        player.inv["echo"].props["name"] = player.props["name"] + "'s Echo"
        player.inv["echo"].props["initials"] = player.props["name"][0] + "e"
    if player.inv["standard"] != "None":
        player.inv["standard"].props["rank"] = "player"
        player.inv["standard"].props["name"] = player.props["name"] + "'s Standard"
        player.inv["standard"].props["initials"] = player.props["name"][0] + "s"


def getBenedictionGroup() -> list:
    Fadia, Hassan, Layth = getFadia(), getHassan(), getLayth()
    benWorld = World.benedictionMap()
    benWorld.worldMap[14][7] = "w/!!↑"

    return {
        "campaign": "Benediction",
        "days": 0,
        "doubleDays": False,
        "inventory": [],
        "members": [Fadia, Hassan, Layth],
        "world": benWorld
    }


def getAkeem():
    Akeem = Humans.paladin("Holy", "Elite").ch
    Akeem.props["name"], Akeem.props["initials"], Akeem.props["favored"] = "Akeem", "A.", "human"
    Akeem.atrb["base_av"], Akeem.atrb["base_hp"], Akeem.atrb["base_sp"] = 17, 16, 4
    Akeem.abl["specialty"] = ["Bless"]

    resetPlayer(Akeem)
    return Akeem

def getFadia():
    Fadia = Humans.witch("Dream", "Adept").ch
    Fadia.props["name"], Fadia.props["initials"], Fadia.props["favored"] = "Fadia", "F.", "bird"
    Fadia.atrb["base_av"], Fadia.atrb["base_hp"], Fadia.atrb["base_sp"] = 14, 14, 3
    Fadia.abl["specialty"] = ["Compel"]

    resetPlayer(Fadia)
    return Fadia

def getHassan():
    Hassan = Humans.brute("Basic", "Adept").ch
    Hassan.props["name"], Hassan.props["initials"], Hassan.props["favored"] = "Hassan", "H.", "invertebrate"
    Hassan.atrb["base_av"], Hassan.atrb["base_hp"], Hassan.atrb["base_sp"] = 15, 18, 5
    Hassan.abl["specialty"] = ["Bash"]

    resetPlayer(Hassan)
    return Hassan

def getLayth():
    Layth = Beasts.lion("Basic", "Juvenile").ch
    Layth.props["name"], Layth.props["initials"], Layth.props["favored"] = "Layth", "L.", "insect"
    Layth.atrb["base_av"], Layth.atrb["base_hp"], Layth.atrb["base_sp"] = 8, 15, 6
    Layth.abl["specialty"] = ["Claw"]
    
    resetPlayer(Layth)
    return Layth