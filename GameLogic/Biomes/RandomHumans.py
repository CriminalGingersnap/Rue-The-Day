from Characters import AggressiveBeasts, Humans, Totems
from . import RandomCreatures as Creatures
import random


def soldiers(rank, environment) -> list:
    quantity = Creatures.getQuantity(environment, [rank]) - 1
    soldierList = [AggressiveBeasts.hound("Basic", rank).ch]
    
    match environment["Spades"]:
        case "King": soldierList += [randomHuman("Master")]
        case "Queen": soldierList += [randomHuman("Elite")]
        case "Jack": soldierList += [randomHuman("Adept")]

    if quantity > 3:
        quantity -= 1
        totemType = random.choice(["hex", "sentry", "ward"])
        totemElement = random.choice(["Flame", "Fey", "Ice"])
        match totemType:
            case "hex": soldierList += [Totems.hex(totemElement, "Standard")]
            case "sentry": soldierList += [Totems.sentry(totemElement, "Standard")]
            case "ward": soldierList += [Totems.ward(totemElement, "Standard")]

    for i in quantity: soldierList += [randomHuman(rank)]
        
    return soldierList

def randomHuman(rank):
    type = random.choice(["archer", "knight", "mage"])
    match type:
        case "archer": return Humans.archer(rank).ch
        case "knight": return Humans.knight(rank).ch
        case "mage":
            element = random.choice(["Flame", "Fey", "Ice"])
            return Humans.mage(rank, element).ch