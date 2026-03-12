from Characters import AggressiveBeasts, AvoidantBeasts, Elementals, Invertebrates, Insects, Reptiles
from . import Wild1_Pass as Pass, Wild2_Bay as Bay, Ice1_Fjord as Fjord
import random

# The peninsula is a humid jungle. The volcano's magic warms the area, and the humid sea breeze carries frequent rain.
# These factors create a biome that feels wholly out of place in its environment. To Laura and Martin, it looks like another world.

# Slow rivers of lava flow down the mountain side, impeding their hike.
# They observe some of the native animals dashing across the narrowest sections.


def randomEncounters(roll, environment) -> list:
    members, element = [], "Flame"

    match roll:
        case 1: members = randomElementals("ooze", environment, element, False)
        case 2: members = randomElementals("puffer", environment, element, False)
        case 3: members = randomBeasts("drake", environment, element)
        case 4: members = Bay.randomBeasts("wyrm", environment, "Toxin")
        case 5: members = Pass.randomBeasts("lizard", environment, "Basic")
        case 6: members = Pass.randomBeasts("wasp", environment, "Toxin")
        case 7: members = Pass.randomBeasts("beetle", environment, element)
        case 8: members = Pass.randomBeasts("isopod", environment, "Basic")
        case 9: members = randomBeasts("centipede", environment, "Toxin")
        case 10: members = Pass.randomBeasts("ant", environment, element)
        case 11: members = randomBeasts("turtle", environment, "Basic")
        # case 12: members = randomBeasts()

    if environment["Diamonds"] == "King":
        members += [Elementals.wisp("Random", "Random").ch]

    for i in len(members): members[i].name += "[" + str(i) + "]"

    return members


def randomElementals(type, environment, element, majorBiome):
    elementalList, rankOptions = [], Fjord.getElementalRankOptions(majorBiome, environment)
    quantity = Pass.getQuantity(environment, rankOptions)

    match type:
        case "ooze":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.ooze(element, rankChoice).ch]
        case "puffer":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.puffer(element, rankChoice).ch]
        
    return elementalList


def randomBeasts(type, environment, element) -> list:
    beastList, rankOptions = [], Pass.getAnimalRankOptions(environment)
    quantity = Pass.getQuantity(environment, rankOptions)

    match type:
        case "centipede":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.centipede(element, rankChoice).ch]
        case "drake":
            for i in quantity:
                rankChoice = random.choice([rankOptions])
                beastList += [AggressiveBeasts.drake(element, rankChoice).ch]
        case "turtle":
            for i in quantity: 
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.turtle(element, rankChoice)]

    return beastList