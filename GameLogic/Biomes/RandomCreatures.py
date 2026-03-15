from Characters import AggressiveBeasts, AvoidantBeasts, Invertebrates, Insects, Reptiles
import random


def creatures(type, environment, element) -> list:
    beastList, rankOptions = [], getAnimalRankOptions(environment)
    quantity = getQuantity(environment, rankOptions)

    match type:
        case "bear":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.bear(element, rankChoice).ch]
        case "deer":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AvoidantBeasts.deer(element, rankChoice).ch]
        case "ferret":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.ferret(element, rankChoice).ch]
        case "hound":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.hound(element, rankChoice).ch]
        case "sheep":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AvoidantBeasts.sheep(element, rankChoice).ch]
        case "lion":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.lion(element, rankChoice).ch]
        case "moose":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.moose(element, rankChoice).ch]
        case "mole":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.mole(element, rankChoice).ch]
        case "rabbit":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AvoidantBeasts.rabbit(element, rankChoice).ch]
 

        case "crocodile":
            for i in quantity:
                rankChoice = random.choice([rankOptions])
                beastList += [Reptiles.crocodile(element, rankChoice).ch]
        case "drake":
            for i in quantity:
                rankChoice = random.choice([rankOptions])
                beastList += [Reptiles.drake(element, rankChoice).ch]
        case "lizard":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.lizard(element, rankChoice).ch]
        case "tortoise":
            for i in quantity: 
                rankChoice = random.choice(rankOptions)
        case "turtle":
            for i in quantity: 
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.turtle(element, rankChoice)]
        case "wyrm":
            for i in quantity: 
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.wyrm(element, rankChoice)]


        case "ant":
            for i in quantity: 
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.ant(element, rankChoice)]
        case "beetle":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.beetle(element, rankChoice).ch]
        case "centipede":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.centipede(element, rankChoice).ch]
        case "isopod":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.isopod(element, rankChoice).ch]
        case "wasp":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Insects.waspNest(element, rankChoice).ch]


        case "crab":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Invertebrates.crab(element, rankChoice).ch]
        case "leech":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Invertebrates.leech(element, rankChoice).ch]
        case "octopus":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Invertebrates.octopus(element, rankChoice).ch]
        case "urchin":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Invertebrates.urchin(element, rankChoice).ch]
        case "worm":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Invertebrates.worm(element, rankChoice).ch]

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
    
    if all(ranks not in rankOptions for ranks in ["Elder", "Elite", "Greater", "Ancient", "Master"]): 
        if all(ranks not in rankOptions for ranks in ["Adept", "Adult", "Lesser"]): quantity *= 3
        else: quantity *= 2

    return quantity