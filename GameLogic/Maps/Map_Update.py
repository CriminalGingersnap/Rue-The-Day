from . import Visibility, Movement, Elevation
from Systems import PlayerSelect as Select, Conditions
from Abilities import DamageTypes as Damage
import random

majorHazards =     ["B", "D", "C", "F", "H", "P", "R", "V"]
minorHazards =     ["b", "d", "c", "f", "h", "p", "r", "v"]
lingeringHazards = ["#", "@",      "%", "+",      "}", "&"]
hazards = majorHazards + minorHazards


def setMarker(fighter, space):
    initial = fighter.initials
    atmosphere, terrain, elevation = space[0], space[1], space[-1]    
    return atmosphere + terrain + initial + elevation

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
    atmosphere = instanceMap[fighter.position[0]][fighter.position[1]][0]
    terrain = instanceMap[fighter.position[0]][fighter.position[1]][1]
    elevation = instanceMap[fighter.position[0]][fighter.position[1]][-1]

    instanceMap[fighter.position[0]][fighter.position[1]] = atmosphere + terrain + terrain + terrain + elevation


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
    elif atmosphere in ["m", "M", "*"]: dmgType == "Mana"

    return dmgType

def getScale(atmosphere) -> int:
    scale = 0
    if atmosphere in majorHazards: scale = 3
    elif atmosphere in minorHazards: scale = 2    
    elif atmosphere in lingeringHazards: scale = 1
    return scale


def activateHazards(fighter, battleMap):
    fighterDmgType = Damage.convertElmToDmg(fighter.atrb["cur_elm"])
    row, column = fighter.position[0], fighter.position[1]
    atmosphere = battleMap[row][column][0]

    if atmosphere in hazards:
        points, dmgType = 0, identifyAtmosphere(atmosphere)
        scale = getScale(atmosphere)
        
        if (fighter.type == "elemental") and (fighterDmgType == dmgType): Conditions.recoverHP(fighter, scale)
        else:
            match scale:
                case 3: points = random.randint(2, 12)
                case 2: points = random.randint(1, 6)      
                case 1: points = 1 
            Conditions.takeDamage(fighter, dmgType, points)
    else:
        match atmosphere:
            case "M": 
                fighter.atrb["cur_mag"] += 2
                Conditions.decrementTolerance(fighter, 2)
            case "m": 
                fighter.atrb["cur_mag"] += 1
                Conditions.decrementTolerance(fighter, 1)


def updateHazards(battleMap):
    for row in range(12):
        for column in range(12):
            atmosphere = battleMap[row][column][0]
            if atmosphere not in ["/", ")", "-", "="]:
                dmgType, newAtmosphere = identifyAtmosphere(atmosphere), "_"
                scale = getScale(atmosphere)

                match dmgType:
                    case "Burn":
                        match scale:
                            case 3: newAtmosphere = "b"
                            case 2: newAtmosphere = random.choice(["B", "b", "#"])
                    case "Dream":
                        match scale:
                            case 3: newAtmosphere = "d"
                            case 2: newAtmosphere = "@"
                            case 1: newAtmosphere = random.choice("*" + lingeringHazards)
                    case "Freeze":
                        match scale:
                            case 3: newAtmosphere = random.choice(["F", "f"])
                            case 2: newAtmosphere = random.choice(["f", "%"])
                    case "Holy": 
                        match scale:
                            case 3: newAtmosphere = "h"
                            case 2: newAtmosphere = "+"
                            case 1: newAtmosphere = random.choice(["H", "+"])
                    case "Mana":
                        match scale:
                            case 3: newAtmosphere = "m"
                            case 2: newAtmosphere = "*"
                    case "Rot": 
                        match scale:
                            case 3: newAtmosphere = "r"
                            case 2: newAtmosphere = random.choice(["r", "r", "}"])
                    case "Venom": 
                        match scale:
                            case 3: newAtmosphere = random.choice(["v", "&"])
                            case 2: newAtmosphere = "&"
                    case "Crush" | "Pierce": newAtmosphere = "_"

                battleMap[row][column] = newAtmosphere + battleMap[row][column][1:]