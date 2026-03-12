from Characters import Elementals, AggressiveBeasts, AvoidantBeasts, Invertebrates
from . import Wild1_Pass as Pass, Wild2_Bay as Bay, Ice1_Fjord as Fjord
import random

# Glacier tube battleMaps have the highest obstruction count in the game. 17?
# Glacier boss map changes as the worm carves new tunnels

def randomEncounters(roll, environment) -> list:
    members, element = [], "Ice"

    match roll:
        case 1: members = randomElementals("obelisk", environment, element, True)
        case 2: members = Fjord.randomElementals("dancer", environment, element, True)
        case 3: members = Fjord.randomElementals("hulk", environment, element, True)
        case 4: members = Fjord.randomElementals("wisps", environment, element, True)
        case 5: members = Bay.randomBeasts("bear", environment, element)
        case 6: members = randomBeasts("ferret", environment, element)
        case 7: members = randomBeasts("mole", environment, element)
        case 8: members = randomBeasts("gopher", environment, "Flame")
        case 9: members = randomBeasts("sheep", environment, element)
        case 10: members = Pass.randomBeasts("urchin", environment, element)
        case 11: members = randomBeasts("worm", environment, element)
        # case 12: members = randomBeasts()

    if (environment["Diamonds"] == "King"):
        members += [Elementals.wisp(element, "Random").ch]

    for i in len(members): members[i].name += "[" + str(i) + "]"

    return members

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