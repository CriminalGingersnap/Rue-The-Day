# Design rules
#  #1: One mystery per action. One test per reward.
#  #2: Complex outcomes from simple systems
#  #3: Minimize interruptions and downtime

from Loop import Encounters
from Maps import World, Movement, Map_Print as Print
from Systems import PlayerSelect as Select
from GameState import SaveLoad as Save
from Campaigns import M_PCs, B_PCs


def adventure(group):
    world = group["world"]

    marker, worldMap = world.marker, world.worldMap
    marker.lastCleared.appendleft(marker.pos)
    marker.lastCleared.pop()

    marker.sightMap = World.createSightMap(worldMap, marker.pos, "world")
    Print.printWorldMap(world)

    while True:
        marker.sightMap = World.createSightMap(worldMap, marker.pos, "world")
        Movement.moveFighter(marker, worldMap, None, None, 24, "world")
        marker.atrb["cur_sp"] = marker.atrb["base_sp"]

        if marker.pos not in marker.lastCleared:
            Select.waitPrint("Encounter triggered!!!")

            row, column = marker.pos[0], marker.pos[1]
            letter = worldMap[row][column][0]
            biome = world.legend[letter]
            Encounters.encounterLoop(group, biome)

            marker.lastCleared.appendleft(marker.pos)
            marker.lastCleared.pop()

        elif marker.pos == marker.lastCleared[0]:
            takeRest = Select.yesNo("Rest and Save Game?")
            if takeRest:
                Encounters.takeRest(group)
                Print.printWorldMap(world)


# B_group = B_PCs.getBenedictionGroup()
M_group = M_PCs.getMetamorphosisGroup()
adventure(M_group)