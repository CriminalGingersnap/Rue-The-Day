from Characters import AggressiveBeasts, Humans, Totems
from . import RandomCreatures as Creatures
import random


def getSoldierRankOptions(environment):
    rankOptions = ["Proficient"]
    match environment["Spades"]:
        case "Queen": rankOptions += ["Adept"]
        case "King": rankOptions += ["Elite"]

    return rankOptions

def getOutlawRankOptions(environment):
    rankOptions = ["Novice"]
    match environment["Spades"]:
        case "Queen": rankOptions += ["Proficient"]
        case "King": rankOptions += ["Adept"]

    return rankOptions


def outlaws(environment, element) -> list:
    outlawList, rankOptions = [], getOutlawRankOptions(environment)
    quantity = Creatures.getQuantity(environment, rankOptions)

    if quantity > 3:
        quantity -= 1
        soldierList += [AggressiveBeasts.hound(element, random.choice["Adult", "Juvenile"]).ch]
        
    for i in quantity:
        rankChoice = random.choice(rankOptions)
        type = random.choice(["archer", "brute", "warlock"])
        outlawList += [randomHuman(rankChoice, type, element)]
        
    return outlawList


def soldiers(environment, element) -> list:
    soldierList, rankOptions = [], getSoldierRankOptions(environment)
    quantity = Creatures.getQuantity(environment, rankOptions) - 1
    
    type = random.choice(["archer", "knight", "mage"])
    match environment["Spades"]:
        case "King": soldierList += [randomHuman("Master", type, element)]
        case "Queen": soldierList += [randomHuman("Elite", type, element)]
        case "Jack": soldierList += [randomHuman("Adept", type, element)]

    if quantity > 2:
        quantity -= 1
        soldierList += [AggressiveBeasts.hound(element, "Adult").ch]
    if quantity > 3:
        quantity -= 1
        totemType = random.choice(["hex", "sentry", "ward"])
        totemElement = random.choice(["Flame", "Fey", "Ice"])
        match totemType:
            case "hex": soldierList += [Totems.hex(totemElement, "Standard")]
            case "sentry": soldierList += [Totems.sentry(totemElement, "Standard")]
            case "ward": soldierList += [Totems.ward(totemElement, "Standard")]

    for i in quantity:
        rankChoice = random.choice(rankOptions)
        type = random.choice(["archer", "knight", "mage"])
        soldierList += [randomHuman(rankChoice, type, element)]
        
    return soldierList


def randomHuman(rank, type, element):
    match type:
        case "archer": return Humans.archer(element, rank).ch
        case "brute": return Humans.brute(element, rank).ch
        case "knight": return Humans.knight(element, rank).ch

    if element == "Basic": 
        element = random.choice(["Flame", "Fey", "Ice"])
        
    match type:
        case "mage": return Humans.mage(element, rank).ch
        case "warlock": return Humans.warlock(element, rank).ch