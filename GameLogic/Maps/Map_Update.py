from . import Visibility, Movement, Elevation
from Abilities import Area_Set as Area
from Systems import PlayerSelect as Select, Conditions
import random

majorHazards =     ["B", "C", "D", "F", "H", "I", "P", "R", "T"]
minorHazards =     ["b", "c", "d", "f", "h", "i", "p", "r", "t"]
lingeringHazards = [          "@", "#", "+", "%",      "}", "&"]
hazards = majorHazards + minorHazards


def setMarker(fighter, space):
    initial = fighter.props["initials"]
    atmosphere, terrain, elevation = space[0], space[1], space[-1]

    return atmosphere + terrain + initial + elevation

def updatePlacement(battleMap, sightMap, row, column, fighter):
    removeFighter(fighter, battleMap)
    removeFighter(fighter, sightMap)
    marker = setMarker(fighter, battleMap[row][column])
    battleMap[row][column] = marker
    fighter.pos = [row, column]
    
    if fighter.props["rank"] == "Ascendant":
        Area.affectSpace(fighter, [row, column], fighter.atrb["cur_elm"], 2, battleMap)

    if battleMap[row][column][-1] == "]":
        dmgType = random.choice(["Crush", "Flame", "Ice", "Pierce", "Rot", "Toxic"])
        Select.waitPrint(fighter.props["name"] + " triggers a " + dmgType + " trap!")
        battleMap[row][column] = battleMap[row][column][:-1] + Elevation.down
        battleMap[row][column] = dmgType[0] + battleMap[row][column][1:]
    
    sightMap[row][column] = battleMap[row][column]

def removeFighter(fighter, instanceMap):
    atmosphere = instanceMap[fighter.pos[0]][fighter.pos[1]][0]
    terrain = instanceMap[fighter.pos[0]][fighter.pos[1]][1]
    elevation = instanceMap[fighter.pos[0]][fighter.pos[1]][-1]

    instanceMap[fighter.pos[0]][fighter.pos[1]] = atmosphere + terrain + terrain + terrain + elevation


def revealOthers(fighter, allies, enemies, sightMap):
    if fighter.props["rank"] == "player":
        for ally in allies:
            row, column = ally.pos[0], ally.pos[1]
            if (ally.props["name"] != fighter.props["name"]) and (Visibility.unseen in sightMap[row][column]):
                elevation = sightMap[row][column][-1]
                sightMap[row][column] = " ..?" + elevation
        for enemy in enemies:
            row, column = enemy.pos[0], enemy.pos[1]
            if Visibility.unseen in sightMap[row][column]:
                elevation = sightMap[row][column][-1]
                sightMap[row][column] = " !!?" + elevation

def hideVeiled(fighter, contingent, instanceMap):
    for other in contingent:
        visibleDistance = fighter.effects["Veil"]["additional"]

        if (visibleDistance != None) and (visibleDistance > 0):
            if Movement.getTargetDistance(fighter, other) > visibleDistance:
                removeFighter(other, instanceMap)

def hideTraps(fighter, sightMap):
    for row in range(12):
        for column in range(12):
            distance = Movement.getSpaceDistance(fighter.pos[0], row, fighter.pos[1], column)
            if (distance > 2) and ("]" in sightMap[row][column]):
                sightMap[row][column] = sightMap[row][column][:-1] + "|"


def identifyAtmosphere(atmosphere) -> str:
    dmgType = ""
    if atmosphere in ["b", "B"]: dmgType = "Bleed"
    if atmosphere in ["c", "C"]: dmgType = "Crush"
    elif atmosphere in ["d", "D", "@"]: dmgType = "Dream"
    if atmosphere in ["f", "F", "#"]: dmgType = "Flame"
    elif atmosphere in ["h", "H", "+"]: dmgType = "Holy"
    elif atmosphere in ["i", "I", "%"]: dmgType = "Ice"
    elif atmosphere in ["r", "R", "}"]: dmgType = "Rot"
    elif atmosphere in ["p", "P"]: dmgType == "Pierce"
    elif atmosphere in ["t", "T", "&"]: dmgType == "Toxic"
    elif atmosphere in ["-", "="]: dmgType == "None"

    return dmgType

def getScale(atmosphere) -> int:
    scale = 0
    if atmosphere in majorHazards: scale = 3
    elif atmosphere in minorHazards: scale = 2    
    elif atmosphere in lingeringHazards: scale = 1
    return scale


def activateHazards(fighter, battleMap):
    row, column = fighter.pos[0], fighter.pos[1]
    atmosphere = battleMap[row][column][0]

    if atmosphere in hazards:
        points, dmgType = 0, identifyAtmosphere(atmosphere)
        scale = getScale(atmosphere)
        
        if (fighter.props["type"] == "elemental") and (fighter.atrb["cur_elm"] == dmgType):
            Select.waitPrint("\nMap causes " + str(points) + " healing for " + fighter.props["name"] + "!")
            Conditions.recoverHP(fighter, scale)
        else:
            match scale:
                case 3: points = random.randint(2, 12)
                case 2: points = random.randint(1, 6)
                case 1: points = 1

            Select.waitPrint("\nMap inflicts " + str(points) + " " + dmgType + " damage against " + fighter.props["name"] + "!")
            Conditions.takeDamage(fighter, dmgType, points)


def updateHazards(battleMap):
    for row in range(12):
        for column in range(12):
            atmosphere = battleMap[row][column][0]

            if atmosphere != "/":
                dmgType, newAtmosphere = identifyAtmosphere(atmosphere), "_"
                scale = getScale(atmosphere)

                match dmgType:
                    case "Bleed": newAtmosphere = "="
                    case "Dream":
                        match scale:
                            case 3: newAtmosphere = random.choice(majorHazards)
                            case 2: newAtmosphere =  random.choice(minorHazards)
                            case 1: newAtmosphere = random.choice(lingeringHazards)
                    case "Flame":
                        match scale:
                            case 3: newAtmosphere = "f"
                            case 2: newAtmosphere = random.choice(["F", "#"])
                            case 1: newAtmosphere = random.choice(["f", "_"])
                    case "Holy": 
                        match scale:
                            case 3: newAtmosphere = "h"
                            case 2: newAtmosphere = "+"
                            case 1: newAtmosphere = random.choice(["H", "+", "_"])
                    case "Ice":
                        match scale:
                            case 3: newAtmosphere = random.choice(["I", "I", "i"])
                            case 2: newAtmosphere = random.choice(["i", "i", "%"])
                            case 1: newAtmosphere = random.choice(["%", "%", "_"])
                    case "None": newAtmosphere = random.choice(["=", "=", "-", "-", "-", "_"])
                    case "Rot": 
                        match scale:
                            case 3: newAtmosphere = "r"
                            case 2: newAtmosphere = random.choice(["r", "r", "}"])
                            case 1: newAtmosphere = "_"
                    case "Toxic": 
                        match scale:
                            case 3: newAtmosphere = random.choice(["t", "&"])
                            case 2: newAtmosphere = random.choice(["&", "-"])
                            case 1: newAtmosphere = "_"
                    case "Crush" | "Pierce": newAtmosphere = "_"

                battleMap[row][column] = newAtmosphere + battleMap[row][column][1:]