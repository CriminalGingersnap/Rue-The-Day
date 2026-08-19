from Characters import AggressiveBeasts, Birds, Humans, Totems
import random


def warriors(warriorType, element, majorBiome, diceBudget) -> list:
    warriorList = []

    if majorBiome:
        outlawRankOptions += ["Elite"]
        soldierRankOptions += ["Master"]

    if diceBudget > 4:
        beast = None
        match random.choice(["hawk", "hound"]):
            case "hawk": beast = Birds.hawk(element, random.choice(["Adult", "Juvenile"])).ch
            case "hound": beast = AggressiveBeasts.hound(element, random.choice(["Adult", "Juvenile"])).ch
        diceBudget -= (beast.atrb["base_mag"] + beast.atrb["base_mar"])
        warriorList += [beast]

    if (diceBudget > 4) and (warriorType == "Soldier"):
        totemElement = random.choice(["Flame", "Ice"])
        totem = None
        match random.choice(["guidance", "impedance", "sentry", "ward"]):
            case "guidance": totem = Totems.guidance("Dream", "Standard").ch
            case "impedance": totem = Totems.impedance("Dream", "Standard").ch
            case "sentry": totem = Totems.sentry(totemElement, "Standard").ch
            case "ward": totem = Totems.ward(totemElement, "Standard").ch

        totem.cndt["reposed"] = False
        diceBudget -= totem.atrb["base_mag"]
        warriorList += [totem]

    outlawJobOptions, soldierJobOptions = ["archer", "brute", "witch"], ["archer", "knight", "mage"]

    while diceBudget > 0:
        warrior, type, rank = None, "", ""

        rankOptions = []
        if diceBudget > 1: rankOptions += ["Proficient", "Adept"]
        if diceBudget > 2: rankOptions += ["Elite"]

        match warriorType:
            case "Outlaw":
                rankOptions += ["Novice"]
                type = random.choice(outlawJobOptions)
            case "Soldier":
                if diceBudget > 3: rankOptions += ["Master"]
                type = random.choice(soldierJobOptions)

        if len(rankOptions) > 0:
            rank = random.choice(rankOptions)
            warrior = randomHuman(rank, type, element)
            diceBudget -= (warrior.atrb["base_mag"] + warrior.atrb["base_mar"])
            warriorList += [warrior]
        else:            
            beast = AggressiveBeasts.hound(element, "Juvenile").ch
            diceBudget -= (beast.atrb["base_mag"] + beast.atrb["base_mar"])
            warriorList += [beast]
        
    return warriorList


def randomHuman(rank, type, element):
    match type:
        case "archer": return Humans.archer(element, rank).ch
        case "brute": return Humans.brute(element, rank).ch
        case "knight": return Humans.knight(element, rank).ch
        case "mage":
            if element == "Basic": element = random.choice(["Flame", "Ice"])
            return Humans.mage(element, rank).ch
        case "witch":
            if element == "Basic": element = "Dream"
            return Humans.witch(element, rank).ch