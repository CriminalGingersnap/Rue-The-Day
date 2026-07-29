from Characters import AggressiveBeasts, Humans, Totems
import random


def warriors(warriorType, element, majorBiome, diceBudget) -> list:
    warriorList = []
    outlawRankOptions, soldierRankOptions = ["Novice", "Proficient", "Adept"], ["Proficient", "Adept", "Elite"]
    outlawJobOptions, soldierJobOptions = ["archer", "brute"], ["archer", "knight", "mage"]

    if majorBiome:
        outlawRankOptions += ["Elite"]
        soldierRankOptions += ["Master"]

    if diceBudget > 4:
        beast = AggressiveBeasts.hound(element, random.choice(["Adult", "Juvenile"])).ch
        diceBudget -= (beast.atrb["base_mag"] + beast.atrb["base_mar"])
        warriorList += [beast]

    if (diceBudget > 4) and (warriorType == "Soldier"):
        totemElement = random.choice(["Flame", "Dream", "Ice"])
        totem = None
        match random.choice(["guidance", "impedance", "sentry", "ward"]):
            case "guidance": totem = Totems.guidance("Dream", "Standard").ch
            case "impedance": totem = Totems.impedance("Dream", "Standard").ch
            case "sentry": totem = Totems.sentry(totemElement, "Standard").ch
            case "ward": totem = Totems.ward(totemElement, "Standard").ch

        totem.cndt["reposed"] = False
        diceBudget -= totem.atrb["base_mag"]
        warriorList += [totem]

    while diceBudget > 0:
        warrior, type, rank = None, "", ""
        if warriorType == "Outlaw":
            rank = random.choice(outlawRankOptions)
            type = random.choice(outlawJobOptions)
        else:
            rank = random.choice(soldierRankOptions)
            type = random.choice(soldierJobOptions)

        warrior = randomHuman(rank, type, element)
        diceBudget -= (warrior.atrb["base_mag"] + warrior.atrb["base_mar"])
        warriorList += [warrior]
        
    return warriorList


def randomHuman(rank, type, element):
    match type:
        case "archer": return Humans.archer(element, rank).ch
        case "brute": return Humans.brute(element, rank).ch
        case "knight": return Humans.knight(element, rank).ch
        case "mage":
            if element == "Basic": element = random.choice(["Flame", "Dream", "Ice"])
            return Humans.mage(element, rank).ch