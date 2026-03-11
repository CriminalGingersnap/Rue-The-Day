from Characters import AggressiveBeasts, AvoidantBeasts, Humans, Invertebrates, Insects, Reptiles, Totems
import random

# the low pass is a valley between two mountains. It crosses from the dry starting prairie into a lush bay.

def randomForestEncounters(encounterRoll, threatLevel):
    encounterGroup, quantity = [], 0

    match threatLevel:
        case "King": quantity = 3
        case "Queen": quantity = 2
        case "Jack": quantity = 1

    match encounterRoll:
        case 2: encounterGroup = randomSoldiers("elite", quantity)
        case 3: encounterGroup = randomSoldiers("adept", quantity)
        case 4: encounterGroup = randomSoldiers("proficient", quantity)
        case 5: encounterGroup = randomBeasts("hound", quantity)
        case 6: encounterGroup = randomBeasts("lizard", quantity)
        case 7: encounterGroup = randomBeasts("wasp", quantity)
        case 8: encounterGroup = randomBeasts("beetle", quantity)
        case 9: encounterGroup = randomBeasts("isopod", quantity)
        case 10: encounterGroup = randomBeasts("urchin", quantity)
        case 11: encounterGroup = randomBeasts("deer", quantity)
        case 12: encounterGroup = randomBeasts("rabbit", quantity)

    for i in len(encounterGroup): encounterGroup[i].name += "[" + str(i) + "]"

    return encounterGroup


def randomSoldiers(rank, quantity) -> list:
    soldierList = [AggressiveBeasts.hound("Basic").ch]

    totemType = random.choice(["hex", "sentry", "ward"])
    totemElement = random.choice(["Flame", "Fey", "Ice"])
    match totemType:
        case "hex": soldierList += [Totems.hex(totemElement, "Standard")]
        case "sentry": soldierList += [Totems.sentry(totemElement, "Standard")]
        case "ward": soldierList += [Totems.ward(totemElement, "Standard")]

    match rank:
        case "adept": quantity *= 2
        case "proficient": quantity *= 3

    for i in quantity:
        type = random.choice(["archer", "knight", "mage"])
        match type:
            case "archer": soldierList += [Humans.archer(rank)]
            case "knight": soldierList += [Humans.knight(rank)]
            case "mage":
                element = random.choice(["Flame", "Fey", "Ice"])
                soldierList += [Humans.mage(rank, element)]

    return soldierList


def randomBeasts(type, quantity) -> list:
    quantity *= 2
    beastList = []

    match type:
        case "beetle":
            for i in quantity: beastList += [Insects.beetle("Basic").ch]
        case "deer":
            for i in quantity: beastList += [AvoidantBeasts.deer("Basic").ch]
        case "hound":
            for i in quantity: beastList += [AggressiveBeasts.hound("Basic").ch]
        case "isopod":
            for i in quantity: beastList += [Insects.isopod("Basic").ch]
        case "lizard":
            for i in quantity: beastList += [Reptiles.lizard("Basic").ch]
        case "rabbit":
            for i in quantity: beastList += [AvoidantBeasts.rabbit("Basic").ch]
        case "urchin":
            for i in quantity: beastList += [Invertebrates.urchin("Basic").ch]
        case "wasp":
            for i in quantity: beastList += [Insects.waspNest("Basic").ch]

    return beastList