from Characters import AggressiveBeasts, AvoidantBeasts, Humans, Invertebrates, Insects, Reptiles, Totems
import random

# the low pass is a valley between two mountains. It crosses from the dry starting prairie into a lush bay.

def randomEncounters(encounterRoll, environment) -> list:
    encounterGroup = []

    match encounterRoll:
        case 2: encounterGroup = randomSoldiers("elite", environment)
        case 3: encounterGroup = randomSoldiers("Adept", environment)
        case 4: encounterGroup = randomSoldiers("proficient", environment)
        case 5: encounterGroup = randomBeasts("hound", environment, "Basic")
        case 6: encounterGroup = randomBeasts("lizard", environment, "Basic")
        case 7: encounterGroup = randomBeasts("wasp", environment, "Toxin")
        case 8: encounterGroup = randomBeasts("beetle", environment, "Basic")
        case 9: encounterGroup = randomBeasts("isopod", environment, "Basic")
        case 10: encounterGroup = randomBeasts("urchin", environment, "Basic")
        case 11: encounterGroup = randomBeasts("deer", environment, "Basic")
        case 12: encounterGroup = randomBeasts("rabbit", environment, "Basic")

    for i in len(encounterGroup): encounterGroup[i].name += "[" + str(i) + "]"

    return encounterGroup


def randomSoldiers(rank, environment) -> list:
    quantity = getQuantity(environment, [rank])
    soldierList = [randomHuman("elite"), AggressiveBeasts.hound("Basic", rank).ch]

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


def randomBeasts(type, environment, element) -> list:
    beastList, rankOptions = [], getAnimalRankOptions(environment)
    quantity = getQuantity(environment, rankOptions)

    match type:
        case "beetle":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.beetle(element, rankChoice).ch]
        case "deer":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AvoidantBeasts.deer(element, rankChoice).ch]
        case "hound":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.hound(element, rankChoice).ch]
        case "isopod":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.isopod(element, rankChoice).ch]
        case "lizard":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.lizard(element, rankChoice).ch]
        case "rabbit":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AvoidantBeasts.rabbit(element, rankChoice).ch]
        case "urchin":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Invertebrates.urchin(element, rankChoice).ch]
        case "wasp":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.waspNest(element, rankChoice).ch]

    return beastList


def getAnimalRankOptions(environment):
    rankOptions = ["Juvenile"]

    match environment["Spades"]:
        case "Queen": rankOptions += ["Adult"]
        case "King": rankOptions += ["Adult", "Elder"]

    return rankOptions

def getQuantity(environment, rankOptions):
    quantity = 0

    match environment["Clubs"]:
        case "King": quantity = 3
        case "Queen": quantity = 2
        case "Jack": quantity = 1
    
    if all(["Elder", "Elite", "Greater", "Ancient"] not in rankOptions): 
        if all(["Adept", "Adult", "Lesser"] not in rankOptions): quantity *= 3
        else: quantity *= 2

    return quantity