# Design rules
#  #1: One mystery per action. One test per reward.
#  #2: Complex outcomes from simple systems
#  #3: Minimize interruptions and downtime

from Characters import Humans, Totems
from Loop import Encounters
from Maps import World, Movement, Map_Print as Print
from Systems import PlayerSelect as Select
from GameState import SaveLoad as Save


Martin = Humans.knight("Basic", "Elite").ch
Martin.atrb["corruption"], Martin.atrb["fatigue"], Martin.atrb["injury"] = 0, 0, 0
Martin.props["rank"], Martin.props["name"], Martin.props["initials"] = "player", "Martin", "M."
Martin.equip["armor"].update({"name": "None", "modifier": 0})
Martin.inv["echo"] = "None"

totem = Totems.guidance("Dream", "Standard").ch
totem.cndt["planted"] = False
totem.props["initials"], totem.props["name"] = "Ms", "Martin's Standard"
Martin.inv["standard"] = totem

Willem = Humans.dragonslayer("Basic", "Master").ch
Willem.atrb["corruption"], Willem.atrb["fatigue"], Willem.atrb["injury"] = 0, 0, 0
Willem.props["rank"], Willem.props["name"], Willem.props["initials"] = "player", "Willem", "W."
Willem.equip["armor"].update({"name": "None", "modifier": 0})
Willem.inv["echo"] = "None"

Laura = Humans.mage("Flame", "Elite").ch
Laura.atrb["corruption"], Laura.atrb["fatigue"], Laura.atrb["injury"] = 0, 0, 0
Laura.props["rank"], Laura.props["name"], Laura.props["initials"] = "player", "Laura", "L."
Laura.equip["armor"].update({"name": "None", "modifier": 0})
Laura.inv["echo"] = "None"


tutorialWorld = World.kingKillerMap()
worldMap = tutorialWorld.worldMap
marker = tutorialWorld.marker

worldMap[0][6] = "w___↑"
worldMap[2][6] = "w_..↑"
worldMap[2][7] = "w/!!↑"
marker.pos = [2, 6]

marker.lastCleared.appendleft(marker.pos)
marker.lastCleared.pop()

group1 = {
    "campaign": "Metamorphosis",
    "days": 0,
    "members": [Laura, Martin],
    "world": tutorialWorld
}


inTutorial = True

while True:
    marker.sightMap = World.createSightMap(worldMap, marker.pos, "world")
    Print.printWorldMap(tutorialWorld)
    Movement.moveFighter(marker, worldMap, None, None)
    marker.atrb["cur_sp"] = marker.atrb["base_sp"]

    if marker.pos not in marker.lastCleared:
        Select.waitPrint("Encounter triggered!!!")

        row, column = marker.pos[0], marker.pos[1]
        letter = worldMap[row][column][0]
        biome = tutorialWorld.legend[letter]
        Encounters.encounterLoop(group1, biome)

        marker.lastCleared.appendleft(marker.pos)
        marker.lastCleared.pop()

    elif marker.pos == marker.lastCleared[0]:
        takeRest = Select.yesNo("Rest and Save Game?")
        if takeRest: Encounters.takeRest(group1)

    if inTutorial and ([0, 6] in marker.lastCleared):
        inTutorial = False
        gameWorld = World.metamorphosisMap()
        worldMap = gameWorld.worldMap
        marker = gameWorld.marker