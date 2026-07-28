from Systems import PlayerSelect as Select
from . import Map_Instantiate as iMap, Elevation
from rich.console import Console

console = Console()


def finishSpace(space, mapName) -> str:
    atmosphere = space[0]
    if atmosphere in ["_", "~", ".", "!"] + iMap.intStrings: atmosphere = " "

    character = " "
    if any(playerMark in space for playerMark in [".", "e", "s"]): character = "."
    elif "!" in space: character = "!"
    elif ("Sight Map" in mapName) and (space[2] in iMap.intStrings): character = "!"

    if "////" in space: space = iMap.wall
    elif "/" in space: space = "/" + character + " /" + "|"
    else: space = " " + character + " " + atmosphere + "|"

    return space


def printOptionsMap(instanceMap, mapName, mapHeight=12) -> None:
    Select.waitPrint("\n" + mapName + ":\n")

    for row in range(mapHeight):
        if "World" not in mapName:
            for column in range(12):
                space = instanceMap[row][column]
                topHalf = finishSpace(instanceMap[row][column], mapName)
                if any(intString in space for intString in iMap.intStrings):
                    console.print("[red]" + topHalf + "[/red]", end = "") 
                else: print(topHalf, end = "")            
            print()

        for column in range(12):
            space = instanceMap[row][column]
            if any(intString in space for intString in iMap.intStrings):
                console.print("[red]" + space + "[/red]", end = "") 
            else: print(space, end = "")
        print()
    print()


def printSightMap(battleMap, sightMap, mapName) -> None:
    Select.waitPrint("\n" + mapName + ":\n")
    for row in range(12):
        for column in range(12):
            sightSpace, battleSpace = sightMap[row][column], battleMap[row][column]
            topHalf = ""

            if "?" in sightSpace:
                topHalf = finishSpace(battleMap[row][column], mapName)
                print(topHalf, end = "")
            else:
                topHalf = finishSpace(sightMap[row][column], mapName)
                console.print("[red]" + topHalf + "[/red]", end = "")

        print()

        for column in range(12):
            sightSpace, battleSpace = sightMap[row][column], battleMap[row][column]

            if "?" in sightSpace: print(battleSpace, end = "")
            else: console.print("[red]" + sightSpace + "[/red]", end = "")
        print()
    print()


def printWorldMap(world) -> None:
    displayList = []

    Select.waitPrint("\nWorld Map:\n")
    for row in range(24):
        for column in range(12):
            biome = world.marker.sightMap[row][column][0]
            if biome not in displayList: displayList += biome

            worldSpace = world.worldMap[row][column]

            if "~" in worldSpace:
                if Elevation.doubleDown in worldSpace: console.print("[blue]" + worldSpace + "[/blue]", end = "")
                else: console.print("[cyan]" + worldSpace + "[/cyan]", end = "")
            elif "/" in worldSpace: console.print("[gray]" + worldSpace + "[/gray]", end = "")
            else: print(worldSpace, end = "")
        print()
    print()
            
    Select.quickPrint("Visible Biomes:")
    for letter in world.legend:
        if letter in displayList:
            Select.quickPrint("  | " + letter + " -> " + world.legend[letter])