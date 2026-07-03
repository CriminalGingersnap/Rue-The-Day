# Design rule #1: One mystery per action

from Characters import Humans
from Loop import Encounters
from Maps import World, Movement
from Systems import PlayerSelect as Select


Martin = Humans.knight("Basic", "Master").ch
Martin.rank, Martin.name, Martin.initials = "player", "Martin", "M."
# Martin.abl["items"] += ["Loot", "Transfer"]
Martin.equipment["armor"] = {"name": None, "modifier": 0}

Laura = Humans.mage("Flame", "Master").ch
Laura.rank, Laura.name, Laura.initials = "player", "Laura", "L."
# Laura.abl["items"] += ["Craft", "Transfer"]
Laura.equipment["armor"] = {"name": None, "modifier": 0}

group1 = [Martin, Laura]

tutorialWorld = World.kingKillerMap()
worldMap = tutorialWorld.worldMap
marker = tutorialWorld.marker

worldMap[0][6] = "w___↑"
worldMap[2][6] = "w_..↑"
worldMap[2][7] = "w_!!↑"
marker.position = [2, 6]
# World.printWorldMap(tutorial)

inTutorial = True

while True:
    marker.sightMap = World.createSightMap(worldMap, marker.position, "world")
    Movement.moveFighter(marker, worldMap, None, None)
    marker.atrb["cur_sp"] = marker.atrb["base_sp"]

    if marker.position not in marker.lastCleared:
        Select.waitPrint("Encounter triggered!!!")

        row, column = marker.position[0], marker.position[1]
        letter = worldMap[row][column][0]
        biome = tutorialWorld.legend[letter]
        Encounters.encounterLoop(group1, biome)

    marker.lastCleared.appendleft(marker.position)
    marker.lastCleared.pop()

    if inTutorial and ([0, 6] in marker.lastCleared):
        inTutorial = False
        gameWorld = World.metamorphosisMap()
        worldMap = gameWorld.worldMap
        marker = gameWorld.marker