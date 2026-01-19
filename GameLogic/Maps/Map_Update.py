from . import Visibility, Movement, Elevation
from Systems import PlayerSelect as Select, Conditions
import random

majorHazards = ["B", "D", "C", "F", "H", "P", "R", "V"]
minorHazards = ["b", "d", "c", "f", "h", "p", "r", "v"]
lingeringHazards = ["#", "@", "%", "+", "}", "&"]
hazards = majorHazards + minorHazards

def setMarker(fighter, space):
    marker, initial = [], fighter.initials

    atmosphere, elevation = space[0], space[-1]

    if fighter.rank == "player": marker = atmosphere + initial + "_" + elevation
    elif fighter.cndt["massive"]: marker = atmosphere + initial + "/" + elevation
    else: marker = atmosphere + initial + "!" + elevation
    
    return marker

def updatePlacement(battleMap, sightMap, row, column, fighter):
    removeFighter(fighter, battleMap)
    removeFighter(fighter, sightMap)
    marker = setMarker(fighter, battleMap[row][column])
    battleMap[row][column] = marker
    fighter.position = [row, column]

    if battleMap[row][column][-1] == "]":
        dmgType = random.choice(["Burn", "Crush", "Freeze", "Pierce", "Rot", "Venom"])
        Select.waitPrint(fighter.name + " triggers a " + dmgType + " trap!")
        battleMap[row][column] = battleMap[row][column][:-1] + Elevation.down
        battleMap[row][column] = dmgType[0] + battleMap[row][column][1:]
    
    sightMap[row][column] = battleMap[row][column]

def removeFighter(fighter, instanceMap):
    elevation = instanceMap[fighter.position[0]][fighter.position[1]][-1]
    atmosphere = instanceMap[fighter.position[0]][fighter.position[1]][0]
    instanceMap[fighter.position[0]][fighter.position[1]] = atmosphere + "___" + elevation


def revealOthers(fighter, allies, enemies, sightMap):
    if fighter.rank == "player":
        for ally in allies:
            row, column = ally.position[0], ally.position[1]
            if (ally.name != fighter.name) and (Visibility.unseen in sightMap[row][column]):
                elevation = sightMap[row][column][-1]
                sightMap[row][column] = " ..?" + elevation
        for enemy in enemies:
            row, column = enemy.position[0], enemy.position[1]
            if Visibility.unseen in sightMap[row][column]:
                elevation = sightMap[row][column][-1]
                sightMap[row][column] = " !!?" + elevation

def hideShrouded(fighter, contingent, instanceMap):
    for other in contingent:
        visibleDistance = fighter.effects["Shroud"]["additional"]

        if (visibleDistance != None) and (visibleDistance > 0):
            if Movement.getTargetDistance(fighter, other) > visibleDistance:
                removeFighter(other, instanceMap)

def hideTraps(fighter, sightMap):
    for row in range(12):
        for column in range(12):
            distance = Movement.getSpaceDistance(fighter.position[0], row, fighter.position[1], column)
            if (distance > 1) and ("]" in sightMap[row][column]):
                sightMap[row][column] = sightMap[row][column][:-1] + "|"


def identifyAtmosphere(atmosphere) -> str:
    dmgType = ""
    if atmosphere in ["b", "B", "#"]: dmgType = "Burn"
    if atmosphere in ["c", "C"]: dmgType = "Crush"
    elif atmosphere in ["d", "D", "@"]: dmgType = "Dream"
    elif atmosphere in ["f", "F", "%"]: dmgType = "Freeze"
    elif atmosphere in ["h", "H", "+"]: dmgType = "Holy"
    elif atmosphere in ["r", "R", "}"]: dmgType = "Rot"
    elif atmosphere in ["p", "P"]: dmgType == "Pierce"
    elif atmosphere in ["v", "V", "&"]: dmgType == "Venom"

    return dmgType

def activateHazards(fighter, battleMap):
    row, column = fighter.position[0], fighter.position[1]
    atmosphere = battleMap[row][column][0]
    damage, dmgType = 1, identifyAtmosphere(atmosphere)

    if atmosphere in hazards:
        if atmosphere in majorHazards: damage = random.randint(2, 12)
        elif atmosphere in minorHazards: damage = random.randint(1, 6)      
        elif atmosphere in minorHazards: damage = random.randint(1, 6)      
        elif atmosphere in lingeringHazards: damage = 1      
        Conditions.takeDamage(fighter, dmgType, damage, False)

def updateHazards(battleMap):
    for row in range(12):
        for column in range(12):
            atmosphere = battleMap[row][column][0]
            if atmosphere not in ["/", ")"]:
                dmgType, newAtmosphere = identifyAtmosphere(atmosphere), "_"

                match dmgType:
                    case "Burn": newAtmosphere = "#"
                    case "Dream": newAtmosphere = "@"
                    case "Freeze": newAtmosphere = "%"
                    case "Holy": newAtmosphere = "+"
                    case "Rot": newAtmosphere = "}"
                    case "Venom": newAtmosphere = "&"
                    case "Crush" | "Pierce": newAtmosphere = "_"

                battleMap[row][column] = newAtmosphere + battleMap[row][column][1:]