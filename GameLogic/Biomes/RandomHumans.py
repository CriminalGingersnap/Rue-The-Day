from Characters import AggressiveBeasts, Humans, Totems
from . import RandomCreatures as Creatures
import random


def getOutlawRankOptions(environment):
    rankOptions = ["Proficient"]

    match environment["Spades"]:
        case "Queen": rankOptions += ["Adept"]
        case "King": rankOptions += ["Elite"]

    return rankOptions

def outlaws(environment) -> list:
    outlawList, rankOptions = [], getOutlawRankOptions(environment)
    quantity = Creatures.getQuantity(environment, rankOptions)

    if quantity > 3:
        quantity -= 1
        soldierList += [AggressiveBeasts.hound("Basic", random.choice["Adult", "Juvenile"]).ch]
        
    for i in quantity:
        rankChoice = random.choice(rankOptions)
        type = random.choice(["archer", "brute", "warlock"])
        outlawList += [randomHuman(rankChoice, type)]
        
    return outlawList


def soldiers(rank, environment) -> list:
    quantity = Creatures.getQuantity(environment, [rank]) - 1
    type = random.choice(["archer", "knight", "mage"])
    
    match environment["Spades"]:
        case "King": soldierList += [randomHuman("Master", type)]
        case "Queen": soldierList += [randomHuman("Elite", type)]
        case "Jack": soldierList += [randomHuman("Adept", type)]

    if quantity > 2:
        quantity -= 1
        soldierList += [AggressiveBeasts.hound("Basic", "Adult").ch]
    if quantity > 3:
        quantity -= 1
        totemType = random.choice(["hex", "sentry", "ward"])
        totemElement = random.choice(["Flame", "Fey", "Ice"])
        match totemType:
            case "hex": soldierList += [Totems.hex(totemElement, "Standard")]
            case "sentry": soldierList += [Totems.sentry(totemElement, "Standard")]
            case "ward": soldierList += [Totems.ward(totemElement, "Standard")]

    for i in quantity:
        type = random.choice(["archer", "knight", "mage"])
        soldierList += [randomHuman(rank, type)]
        
    return soldierList


def randomHuman(rank, type):
    element = random.choice(["Flame", "Fey", "Ice"])
    match type:
        case "archer": return Humans.archer(rank).ch
        case "brute": return Humans.brute(rank).ch
        case "knight": return Humans.knight(rank).ch
        case "mage": return Humans.mage(rank, element).ch
        case "warlock": return Humans.warlock(rank, element).ch