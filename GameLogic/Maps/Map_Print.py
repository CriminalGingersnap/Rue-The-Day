from Systems import PlayerSelect as Select
from . import Map_Instantiate as iMap
from rich.console import Console

console = Console()


def finishSpace(space, mapName) -> str:
    atmosphere = space[0]
    if atmosphere in ["_", "~"]: atmosphere = " "

    character = " "
    if "." in space: character = "."
    elif "!" in space: character = "!"
    elif ("Sight Map" in mapName) and (space[2] in iMap.intStrings): character = "!"

    if "////" in space: space = iMap.wall
    elif ")()(" in space: space = iMap.pit
    elif "/" in space: space = atmosphere + character + " /" + "|"
    else: space = atmosphere + character + " " + atmosphere + "|"

    return space


def printOptionsMap(instanceMap, mapName) -> None:
    Select.waitPrint("\n" + mapName + ":\n")

    for row in range(12):
        for column in range(12):
            space = instanceMap[row][column]
            topHalf = finishSpace(instanceMap[row][column], mapName)
            if space[2] in iMap.intStrings: console.print("[red]" + topHalf + "[/red]", end = "") 
            else: print(topHalf, end = "")            
        print()

        for column in range(12):
            space = instanceMap[row][column]
            if space[2] in iMap.intStrings: console.print("[red]" + space + "[/red]", end = "") 
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