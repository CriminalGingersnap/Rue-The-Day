# Design rules
#  #1: One mystery per action
#  #2: Complex outcomes from simple systems
#  #3: Minimize interruptions and downtime

from Characters import Humans
from Loop import Encounters, Loot
from Maps import World, Movement
from Systems import PlayerSelect as Select
from GameState import SaveLoad as Save


# Martin = Save.nullCharacter()
# Save.saveCharacter(Willem, "Metamorphosis", "Willem")
# Save.loadCharacter(Martin, "Metamorphosis", "Willem")

# testWorld = Save.nullWorld()
# Save.saveWorld(tutorialWorld, "Metamorphosis", "Map")
# Save.loadWorld(testWorld, "Metamorphosis", "Map")

Martin = Humans.knight("Basic", "Master").ch
Martin.props["rank"], Martin.props["name"], Martin.props["initials"] = "player", "Martin", "W."
Martin.equip["armor"] = {"name": None, "modifier": 0}

Willem = Humans.dragonslayer("Basic", "Master").ch
Willem.props["rank"], Willem.props["name"], Willem.props["initials"] = "player", "Willem", "W."
Willem.equip["armor"] = {"name": None, "modifier": 0}

Laura = Humans.mage("Flame", "Master").ch
Laura.props["rank"], Laura.props["name"], Laura.props["initials"] = "player", "Laura", "L."
Laura.equip["armor"] = {"name": None, "modifier": 0}

# group1 = [Martin, Laura]
group1 = [Laura]
group2 = [Martin, Willem]


tutorialWorld = World.kingKillerMap()
worldMap = tutorialWorld.worldMap
marker = tutorialWorld.marker

worldMap[0][6] = "w___↑"
worldMap[2][6] = "w_..↑"
worldMap[2][7] = "w_!!↑"
marker.position = [2, 6]

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