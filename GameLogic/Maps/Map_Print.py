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


def colorPrint(comparisonSpace, printingSpace) -> None:
    if "~" in comparisonSpace:
        if Elevation.doubleDown in comparisonSpace: console.print("[blue]" + printingSpace + "[/blue]", end = "")
        else: console.print("[cyan]" + printingSpace + "[/cyan]", end = "")
    elif "/" in comparisonSpace: console.print("[gray]" + printingSpace + "[/gray]", end = "")
    elif ")" in comparisonSpace: console.print("[purple]" + printingSpace + "[/purple]", end = "")
    elif "*" in comparisonSpace:
        if "]" in comparisonSpace: console.print("[green]" + printingSpace[:-1] + "|" + "[/green]" , end = "")
        else: console.print("[green]" + printingSpace + "[/green]" , end = "")
    elif "]" in comparisonSpace: print(printingSpace[:-1] + "|", end = "")
    else: print(printingSpace, end = "")


def printOptionsMap(instanceMap, mapName, mapHeight=12) -> None:
    Select.clearPrint(mapName + ":")

    for row in range(mapHeight):
        if "World" not in mapName:
            for column in range(12):
                optionSpace = instanceMap[row][column]
                topHalf = finishSpace(instanceMap[row][column], mapName)
                if any(intString in optionSpace for intString in iMap.intStrings):
                    console.print("[red]" + topHalf + "[/red]", end = "") 
                else: colorPrint(optionSpace, topHalf)
            print()

        for column in range(12):
            optionSpace = instanceMap[row][column]
            if any(intString in optionSpace for intString in iMap.intStrings):
                console.print("[red]" + optionSpace + "[/red]", end = "") 
            else: colorPrint(optionSpace, optionSpace)
        print()
    print()


def printSightMap(battleMap, sightMap, mapName) -> None:
    Select.clearPrint(mapName + ":")
    for row in range(12):
        for column in range(12):
            sightSpace, battleSpace = sightMap[row][column], battleMap[row][column]
            topHalf = ""

            if "?" in sightSpace:
                topHalf = finishSpace(battleMap[row][column], mapName)
                colorPrint(battleSpace, topHalf)
            else:
                topHalf = finishSpace(sightMap[row][column], mapName)
                if "*" in sightSpace: colorPrint(sightSpace, topHalf)
                else: console.print("[red]" + topHalf + "[/red]", end = "")

        print()

        for column in range(12):
            sightSpace, battleSpace = sightMap[row][column], battleMap[row][column]

            if "?" in sightSpace: colorPrint(battleSpace, battleSpace)
            elif "*" in sightSpace: colorPrint(sightSpace, sightSpace)
            else: console.print("[red]" + sightSpace + "[/red]", end = "")
        print()
    print()


def printWorldMap(world) -> None:
    displayList = []

    Select.clearPrint("World Map:")
    for row in range(24):
        for column in range(12):
            biome = world.marker.sightMap[row][column][0]
            if biome not in displayList: displayList += biome

            worldSpace = world.worldMap[row][column]
            colorPrint(worldSpace, worldSpace)
        print()
    print()
            
    Select.quickPrint("Visible Biomes:")
    for letter in world.legend:
        if letter in displayList:
            Select.quickPrint("  | " + letter + " -> " + world.legend[letter])