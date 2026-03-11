from Characters import Elementals, AggressiveBeasts, AvoidantBeasts, Invertebrates
from . import Wild1_Pass as Pass, Wild2_Bay as Bay, Ice1_Fjord as Fjord
import random

# Glacier tube battleMaps have the highest obstruction count in the game. 17?
# Glacier boss map changes as the worm carves new tunnels

def randomEncounters(encounterRoll, environment) -> list:
    encounterGroup, element = [], "Ice"

    match encounterRoll:
        case 2: encounterGroup = randomElementals("obelisk", environment, element, True)
        case 3: encounterGroup = Fjord.randomElementals("dancer", environment, element, True)
        case 4: encounterGroup = Fjord.randomElementals("hulk", environment, element, True)
        case 5: encounterGroup = Fjord.randomElementals("wisps", environment, element, True)
        case 6: encounterGroup = Bay.randomBeasts("bear", environment, element)
        case 7: encounterGroup = randomBeasts("mole", environment, element)
        case 8: encounterGroup = randomBeasts("ferret", environment, element)
        case 9: encounterGroup = randomBeasts("gopher", environment, "Flame")
        case 10: encounterGroup = randomBeasts("sheep", environment, element)
        case 11: encounterGroup = Pass.randomBeasts("urchin", environment, element)
        case 12: encounterGroup = randomBeasts("worm", environment, element)

    if (environment["Diamonds"] == "King"):
        encounterGroup += [Elementals.wisp(element, "Random").ch]

    for i in len(encounterGroup): encounterGroup[i].name += "[" + str(i) + "]"

    return encounterGroup

def randomElementals(type, environment, element, majorBiome):
    elementalList, rankOptions = [], Fjord.getElementalRankOptions(majorBiome, environment)
    quantity = Pass.getQuantity(environment, rankOptions)

    match type:
        case "obelisk":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.obelisk(element, rankChoice).ch]


def randomBeasts(type, environment, element) -> list:
    beastList, rankOptions = [], Pass.getAnimalRankOptions(environment)
    quantity = Pass.getQuantity(environment, rankOptions)

    match type:
        case "ferret":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.ferret(element, rankChoice).ch]
        case "gopher":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AvoidantBeasts.gopher(element, rankChoice).ch]
        case "sheep":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AvoidantBeasts.sheep(element, rankChoice).ch]
        case "mole":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.mole(element, rankChoice).ch]
        case "worm":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Invertebrates.worm(element, rankChoice).ch]

    return beastList