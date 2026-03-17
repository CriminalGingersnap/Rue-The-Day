from Characters import AggressiveBeasts, AvoidantBeasts, Invertebrates, Insects, Reptiles
import random


def creatures(type, majorBiome, element, diceBudget) -> list:
    beastList, rankOptions = [], getAnimalRankOptions(majorBiome)

    while diceBudget > 0:
        rankChoice, beast = random.choice(rankOptions), None
        match type:
            case "bear": beast = AggressiveBeasts.bear(element, rankChoice).ch      
            case "deer": beast = AvoidantBeasts.deer(element, rankChoice).ch
            case "ferret": beast = AggressiveBeasts.ferret(element, rankChoice).ch
            case "hound": beast = AggressiveBeasts.hound(element, rankChoice).ch
            case "sheep": beast = AggressiveBeasts.sheep(element, rankChoice).ch
            case "lion": beast = AggressiveBeasts.lion(element, rankChoice).ch
            case "moose": beast = AggressiveBeasts.moose(element, rankChoice).ch
            case "mole": beast = AvoidantBeasts.mole(element, rankChoice).ch
            case "rabbit": beast = AvoidantBeasts.rabbit(element, rankChoice).ch
            case "seal": beast = AvoidantBeasts.seal(element, rankChoice).ch

            case "crocodile": beast = Reptiles.crocodile(element, rankChoice).ch
            case "drake": beast = Reptiles.drake(element, rankChoice).ch
            case "lizard": beast = Reptiles.lizard(element, rankChoice).ch
            case "tortoise": beast = Reptiles.tortoise(element, rankChoice).ch
            case "turtle": beast = Reptiles.turtle(element, rankChoice).ch
            case "wyrm": beast =Reptiles.wyrm(element, rankChoice).ch

            case "ant": beast = Insects.ant(element, rankChoice).ch
            case "beetle": beast = Insects.beetle(element, rankChoice).ch
            case "centipede": beast = Insects.centipede(element, rankChoice).ch
            case "isopod": beast = Insects.isopod(element, rankChoice).ch
            case "wasp": beast = Insects.waspNest(element, rankChoice).ch

            case "crab": beast = Invertebrates.crab(element, rankChoice).ch
            case "leech": beast = Invertebrates.leech(element, rankChoice).ch
            case "octopus": beast = Invertebrates.octopus(element, rankChoice).ch
            case "urchin": beast = Invertebrates.urchin(element, rankChoice).ch
            case "worm": beast = Invertebrates.worm(element, rankChoice).ch
    
        diceBudget -= (beast.atrb["base_mag"] + beast.atrb["base_mar"])
        beastList += [beast]

    return beastList


def getAnimalRankOptions(majorBiome):
    rankOptions = ["Juvenile", "Adult"]
    if majorBiome: rankOptions += ["Elder"]
    return rankOptions