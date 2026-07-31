# Design rules
#  #1: One mystery per action. One challenge per reward.
#  #2: Complex outcomes from simple systems.
#  #3: Minimize interruptions and downtime.
#  #4: Only human/animal characters. No fantasy races or personified gods.

from Loop import Encounters
from Maps import World, Movement, Map_Print as Print
from Systems import PlayerSelect as Select
from GameState import SaveLoad as Save


def adventure(group):
    world = group["world"]

    marker, worldMap = world.marker, world.worldMap
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
            if letter == "~": letter = "s"
            biome = world.legend[letter]

            bespoke, event = False, None
            for eventOption in world.events:
                if world.events[eventOption]["location"] == marker.pos:
                    bespoke = True
                    event = eventOption
                    world.events[eventOption]["complete"] = True

            victory = False
            if bespoke: victory = Encounters.customLoop(group, biome, event)
            else: victory = Encounters.randomLoop(group, biome)

            if victory:
                marker.lastCleared.appendleft(marker.pos)
                marker.lastCleared.pop()

        elif marker.pos == marker.lastCleared[0]:
            if Select.yesNo("Rest and Save Game?"):
                Encounters.rest(group)
                Print.printWorldMap(world)


campaign = Select.pickOption(["Benediction", "Metamorphosis"], "Campaign")
group = Save.loadGroup(campaign)
adventure(group)