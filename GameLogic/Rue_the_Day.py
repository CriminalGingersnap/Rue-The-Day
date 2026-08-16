# Design rules
#  #1: One mystery per action. One challenge per reward.
#  #2: Complex outcomes from simple systems.
#  #3: Minimize interruptions and downtime.
#  #4: Only human/animal characters. No fantasy races or personified gods.

from Loop import Encounters, CustomEncounters
from Maps import World, Movement, Map_Print as Print
from Systems import PlayerSelect as Select
from GameState import SaveLoad as Save


def adventure(group):
    world = group["world"]

    marker, worldMap = world.marker, world.worldMap
    marker.sightMap = World.setMarkerSight(worldMap, marker.pos)
    Print.printWorldMap(world)

    while True:
        if world.events["Finale"]["location"] == marker.pos: break

        marker.sightMap = World.setMarkerSight(worldMap, marker.pos)
        Movement.moveFighter(marker, worldMap, None, 24, "world")
        marker.atrb["cur_sp"] = marker.atrb["base_sp"]

        row, column = marker.pos[0], marker.pos[1]
        letter = worldMap[row][column][0]
        if letter == "~": letter = "s"
        biome = world.legend[letter]
        
        if marker.pos not in marker.lastCleared:
            Select.waitPrint("Encounter triggered!!!")

            bespoke, event = False, None
            for eventOption in world.events:
                eventRow, eventCol = world.events[eventOption]["location"][0], world.events[eventOption]["location"][1]
                if (eventRow == marker.pos[0]) and (eventCol == marker.pos[1]) and not (world.events[eventOption]["complete"]):
                    bespoke = True
                    event = eventOption
                    world.events[eventOption]["complete"] = True

            victory = False
            if bespoke: victory = CustomEncounters.customLoop(group, biome, event)
            else: victory = Encounters.randomLoop(group, biome)

            if victory:
                marker.lastCleared.appendleft(marker.pos)
                marker.lastCleared.pop()

        elif marker.pos == marker.lastCleared[0]:
            if Select.yesNo("Rest and Save Game?"):
                Encounters.rest(group, biome)
                Print.printWorldMap(world)

    Select.clearPrint("Congratulations! You beat the game!")
    if Select.yesNo("Would you like to load a save and continue playing?"):
        group = Save.loadGroup(group["campaign"])
        adventure(group)
    else: Select.clearPrint("Thanks for playing! This window will remain open until you close it.")


campaign = Select.pickOption(["Avarice", "Benediction"], "Campaign")
group = Save.loadGroup(campaign)
adventure(group)