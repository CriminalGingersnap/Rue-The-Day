from . import Visibility, Movement, Elevation, Map_Instantiate as iMap, MovementOptions as mOpts
from Abilities import Area_Set as Area, Boons_Apply as Boons
from Systems import PlayerSelect as Select, Conditions
from Loop import Environment
import random

majorHazards =     ["B", "C", "D", "F", "H", "I", "P", "R", "T"]
minorHazards =     ["b", "c", "d", "f", "h", "i", "p", "r", "t"]
lingeringHazards = [";",      "@", "#", "+", "%",      "}", "&"]
hazards = majorHazards + minorHazards + lingeringHazards


def setMarker(fighter, space):
    initial = fighter.props["initials"]
    atmosphere, terrain, elevation = space[0], space[1], space[-1]

    return atmosphere + terrain + initial + elevation

def updatePlacement(battleMap, sightMap, row, column, fighter):
    removeFighter(fighter, battleMap)
    removeFighter(fighter, sightMap)
    marker = setMarker(fighter, battleMap[row][column])
    battleMap[row][column] = marker

    fighter.pos = [row, column, 0]
    iMap.updateFighterHeight([fighter], battleMap)
    
    if fighter.props["rank"] == "Ascendant":
        Area.affectSpace([row, column], fighter.atrb["cur_elm"], 2, battleMap)
    elif (fighter.props["rank"] == "player") and ("*" in battleMap[row][column]):
        Select.waitPrint(fighter.props["name"] + " steps into a wellspring of fate!")

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

def hideVeiled(fighter, contingent, sightMap):
    for other in contingent:
        visibleDistance = fighter.effects["Veil"]["additional"]

        if (visibleDistance != None) and (visibleDistance > 0):
            if Movement.getTargetDistance(fighter, other) > visibleDistance:
                sightMap[other.pos[0]][other.pos[1]][0] = str(fighter.effects["Veil"]["additional"])

def hideTraps(fighter, sightMap):
    for row in range(12):
        for column in range(12):
            height = mOpts.heightDict[sightMap[row][column][-1]]
            distance = Movement.getSpaceDistance(fighter.pos[0], row, fighter.pos[1], column, fighter.pos[2], height)
            if (distance > 2) and ("]" in sightMap[row][column]):
                sightMap[row][column] = sightMap[row][column][:-1] + "|"


def identifyAtmosphere(atmosphere) -> str:
    dmgType = "None"
    match atmosphere:
        case "b" | "B" | ";": dmgType = "Bleed"
        case "c" | "C":       dmgType = "Crush"
        case "d" | "D" | "@": dmgType = "Dream"
        case "f" | "F" | "#": dmgType = "Flame"
        case "h" | "H" | "+": dmgType = "Holy"
        case "i" | "I" | "%": dmgType = "Ice"
        case "r" | "R" | "}": dmgType = "Rot"
        case "p" | "P":       dmgType = "Pierce"
        case "t" | "T" | "&": dmgType = "Toxic"

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
        Select.waitPrint(fighter.props["name"] + " is standing in a hazard space!")
        points, dmgType = 0, identifyAtmosphere(atmosphere)
        scale = getScale(atmosphere)

        if (fighter.props["type"] in ["elemental", "echo"]) and (fighter.atrb["cur_elm"] == dmgType):
            Select.waitPrint("The map causes " + str(points) + " healing for " + fighter.props["name"] + "!")
            Conditions.recoverHP(fighter, scale)
        elif dmgType != "None":
            match scale:
                case 3: points = random.randint(2, 12)
                case 2: points = random.randint(1, 6)
                case 1: points = 1

            absorption = Boons.applyWreath(fighter, dmgType)
            appliedDmg = max(0, points - absorption)

            Select.quickPrint("The map inflicts: ", "")
            Select.waitPrint(str(appliedDmg) + " " + dmgType + " damage against " + fighter.props["name"] + "!")
            Conditions.takeDamage(fighter, dmgType, appliedDmg)


def updateHazards(battleMap):
    for row in range(12):
        for column in range(12):
            atmosphere = battleMap[row][column][0]
            static = [atmosphere, atmosphere]

            if atmosphere != "/":
                dmgType, newAtmosphere = identifyAtmosphere(atmosphere), atmosphere
                scale = getScale(atmosphere)

                match dmgType:
                    case "Bleed": newAtmosphere = random.choice(static + ["="])
                    case "Dream":
                        match scale:
                            case 3: newAtmosphere = random.choice(static + majorHazards)
                            case 2: newAtmosphere = random.choice(static + minorHazards)
                            case 1: newAtmosphere = random.choice(static + lingeringHazards)
                    case "Flame":
                        match scale:
                            case 3: newAtmosphere = random.choice(static + ["f"])
                            case 2: newAtmosphere = random.choice(static + ["F", "#", "#"])
                            case 1: newAtmosphere = random.choice(static + ["f", "_", "_"])
                    case "Holy": 
                        match scale:
                            case 3: newAtmosphere = random.choice(static + ["h"])
                            case 2: newAtmosphere = random.choice(static + ["+"])
                            case 1: newAtmosphere = random.choice(static + ["H", "+", "_"])
                    case "Ice":
                        match scale:
                            case 3: newAtmosphere = random.choice(static + ["I", "I", "i"])
                            case 2: newAtmosphere = random.choice(static + ["i", "i", "%"])
                            case 1: newAtmosphere = random.choice(static + ["%", "%", "%", "%", "%", "_"])
                    case "Rot": 
                        match scale:
                            case 3: newAtmosphere = random.choice(static + ["r"])
                            case 2: newAtmosphere = random.choice(static + ["}"])
                            case 1: newAtmosphere = random.choice(static + ["}", "}", "}", "}", "}", "_"])
                    case "Toxic": 
                        match scale:
                            case 3: newAtmosphere = random.choice(static + ["t", "&"])
                            case 2: newAtmosphere = random.choice(static + ["&", "-"])
                            case 1: newAtmosphere = random.choice(static + ["-"])
                    case "Crush" | "Pierce": newAtmosphere = random.choice(static + ["_"])

                battleMap[row][column] = newAtmosphere + battleMap[row][column][1:]


def addHazards(battleMap, atmosphere):
    mapConditions = {"atmosphere": atmosphere,
                      "obstructions": {"wall": 0, "trap": 0, "pit": 0}}
    if any((atmosphere[atmo] > 0) for atmo in atmosphere):
        Select.clearPrint("Adding atmospheric effects...")
        iMap.placeOcclusions(mapConditions, battleMap)