from Characters import AggressiveBeasts, Humans, Totems
import random


def warriors(warriorType, element, majorBiome, diceBudget) -> list:
    warriorList = []
    outlawRankOptions, soldierRankOptions = ["Novice", "Proficient", "Adept"], ["Proficient", "Adept", "Elite"]
    if majorBiome:
        outlawRankOptions += ["Elite"]
        soldierRankOptions += ["Master"]

    if diceBudget > 4:
        beast = AggressiveBeasts.hound(element, random.choice(["Adult", "Juvenile"])).ch
        diceBudget -= (beast.atrb["base_mag"] + beast.atrb["base_mar"])
        warriorList += [beast]

    if (diceBudget > 4) and (warriorType == "Soldier"):
        totemType = random.choice(["hex", "sentry", "ward"])
        totemElement = random.choice(["Flame", "Fey", "Ice"])
        totem = None
        match totemType:
            case "hex": totem = Totems.hex(totemElement, "Standard")
            case "sentry": totem = Totems.sentry(totemElement, "Standard")
            case "ward": totem = Totems.ward(totemElement, "Standard")

        diceBudget -= (totem.atrb["base_mag"] + totem.atrb["base_mar"])
        warriorList += [totem]

    while diceBudget > 0:
        warrior, type, rankChoice = None, "", ""
        match warriorType:
            case "Outlaw":
                rankChoice = random.choice(outlawRankOptions)
                type = random.choice(["archer", "brute", "warlock"])
            case "Soldier":
                rankChoice = random.choice(soldierRankOptions)
                type = random.choice(["archer", "knight", "mage"])

        warrior = randomHuman(rankChoice, type, element)
        diceBudget -= (warrior.atrb["base_mag"] + warrior.atrb["base_mar"])
        warriorList += [warrior]
        
    return warriorList


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