from Characters import AggressiveBeasts, AvoidantBeasts, Humans, Invertebrates, Insects, Reptiles, Totems
import random

# the low pass is a valley between two mountains. It crosses from the dry starting prairie into a lush bay.

def randomForestEncounters(environment):
    encounterRoll, encounterGroup = 0, []

    match environment["Spades"]:
        case "King": encounterRoll = random.randint(2, 4)
        case "Queen": encounterRoll = random.randint(5, 7)
        case "Jack": encounterRoll = random.randint(8, 12)

    match encounterRoll:
        case 2: encounterGroup = randomSoldiers("elite")
        case 3: encounterGroup = randomSoldiers("adept")
        case 4: encounterGroup = randomSoldiers("proficient")
        case 5: encounterGroup = randomBeasts("hound")
        case 6: encounterGroup = randomBeasts("lizard")
        case 7: encounterGroup = randomBeasts("wasp")
        case 8: encounterGroup = randomBeasts("beetle")
        case 9: encounterGroup = randomBeasts("isopod")
        case 10: encounterGroup = randomBeasts("urchin")
        case 11: encounterGroup = randomBeasts("deer")
        case 12: encounterGroup = randomBeasts("rabbit")

    return encounterGroup


def randomSoldiers(rank) -> list:
    quantity = random.randint(3, 6)
    soldierList = []

    totemType = random.choice(["hex", "sentry", "ward"])
    totemElement = random.choice(["Flame", "Fey", "Ice"])

    match rank:
        case "elite":
            quantity = random.randint(2, 3)
            match totemType:
                case "hex": soldierList += [Totems.hex(totemElement, "Standard")]
                case "sentry": soldierList += [Totems.sentry(totemElement, "Standard")]
                case "ward": soldierList += [Totems.ward(random.choice(["Flame", "Ice"]), "Standard")]
            soldierList[0].name += "[" + str(i) + "]"

        case "adept":
            quantity = random.randint(3, 4)
            for i in (6 - quantity):
                soldierList += [AggressiveBeasts.hound("Basic").ch]
                soldierList[i-1].name += "[" + str(i) + "]"

        case "proficient":
            quantity = random.randint(5, 6)
            match totemType:
                case "hex": soldierList += [Totems.hex(totemElement, "Totem")]
                case "sentry": soldierList += [Totems.sentry(totemElement, "Totem")]
                case "ward": soldierList += [Totems.ward(random.choice(["Flame", "Ice"]), "Totem")]
            soldierList[0].name += "[" + str(i) + "]"

    for i in quantity:
        type = random.choice(["archer", "knight", "mage"])
        match type:
            case "archer": soldierList += [Humans.archer(rank)]
            case "knight": soldierList += [Humans.knight(rank)]
            case "mage":
                element = random.choice(["Flame", "Fey", "Ice"])
                soldierList += [Humans.mage(rank, element)]
        soldierList[i-1].name += "[" + str(i) + "]"

    return soldierList


def randomBeasts(type) -> list:
    quantity = random.randint(3, 6)
    beastList = []

    match type:
        case "beetle":
            for i in quantity:
                beastList += [Insects.beetle("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"
        case "deer":
            for i in quantity:
                beastList += [AvoidantBeasts.deer("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"
        case "hound":
            for i in quantity:
                beastList += [AggressiveBeasts.hound("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"
        case "isopod":
            for i in quantity:
                beastList += [Insects.isopod("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"
        case "lizard":
            for i in quantity:
                beastList += [Reptiles.lizard("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"
        case "rabbit":
            for i in quantity:
                beastList += [AvoidantBeasts.rabbit("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"
        case "urchin":
            for i in quantity:
                beastList += [Invertebrates.urchin("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"
        case "wasp":
            for i in quantity:
                beastList += [Insects.waspNest("Basic").ch]
                beastList[i-1].name += "[" + str(i) + "]"

    return beastList