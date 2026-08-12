from Characters import AggressiveBeasts, AvoidantBeasts, Birds, Invertebrates, Insects, Reptiles
import random


oneDie_Vrt = ["bat", "crow", "deer", "ferret", "hawk", "hound", "lizard", "seal", "sheep", "vulture"]
oneDie_Inv = ["ant", "hornet", "leech", "mussel", "urchin", "worm"]
twoDice_Vrt = ["camel", "eagle", "mole", "moose", "ostrich", "tortoise", "turtle", "wyrm"]
twoDice_Inv = ["beetle", "centipede", "crab", "isopod", "octopus"]
threeDice_Vrt = ["bear", "crocodile", "drake", "hydra", "lion", "terror bird"]
threeDice_Inv = ["anemone", "spider"]


def creatures(creatureType, element, majorBiome, diceBudget) -> list:
    beastList, firstCreature = [], True

    if creatureType == "random":
        if diceBudget == 2: creatureType = random.choice([oneDie_Vrt])
        elif diceBudget > 2: creatureType = random.choice([twoDice_Vrt])
        if creatureType in ["lizard", "wyrm"]: element == "Toxic"

    while diceBudget > 0:
        rankOptions = getAnimalRankOptions(majorBiome, diceBudget, creatureType, firstCreature)
        rankChoice, beast, creatureType = random.choice(rankOptions[0]), None, rankOptions[1]

        match creatureType:
            case "bear": beast = AggressiveBeasts.bear(element, rankChoice).ch      
            case "ferret": beast = AggressiveBeasts.ferret(element, rankChoice).ch
            case "hound": beast = AggressiveBeasts.hound(element, rankChoice).ch
            case "lion": beast = AggressiveBeasts.lion(element, rankChoice).ch
            case "moose": beast = AggressiveBeasts.moose(element, rankChoice).ch
            case "sheep": beast = AggressiveBeasts.sheep(element, rankChoice).ch

            case "bat": beast = AvoidantBeasts.bat(element, rankChoice).ch
            case "camel": beast = AvoidantBeasts.camel(element, rankChoice).ch
            case "deer": beast = AvoidantBeasts.deer(element, rankChoice).ch
            case "mole": beast = AvoidantBeasts.mole(element, rankChoice).ch
            case "seal": beast = AvoidantBeasts.seal(element, rankChoice).ch

            case "crow": beast = Birds.crow(element, rankChoice).ch
            case "eagle": beast = Birds.eagle(element, rankChoice).ch
            case "hawk": beast = Birds.hawk(element, rankChoice).ch
            case "ostrich": beast = Birds.ostrich(element, rankChoice).ch
            case "terror bird": beast = Birds.terrorBird(element, rankChoice).ch
            case "vulture": beast = Birds.vulture(element, rankChoice).ch

            case "crocodile": beast = Reptiles.crocodile(element, rankChoice).ch
            case "drake": beast = Reptiles.drake(element, rankChoice).ch
            case "hydra": beast = Reptiles.hydra(element, rankChoice).ch
            case "lizard": beast = Reptiles.lizard(element, rankChoice).ch
            case "tortoise": beast = Reptiles.tortoise(element, rankChoice).ch
            case "turtle": beast = Reptiles.turtle(element, rankChoice).ch
            case "wyrm": beast =Reptiles.wyrm(element, rankChoice).ch

            case "ant": beast = Insects.ant(element, rankChoice).ch
            case "beetle": beast = Insects.beetle(element, rankChoice).ch
            case "centipede": beast = Insects.centipede(element, rankChoice).ch
            case "hornet": beast = Insects.hornet(element, rankChoice).ch
            case "isopod": beast = Insects.isopod(element, rankChoice).ch
            case "spider": beast = Insects.spider(element, rankChoice).ch

            case "anemone": beast = Invertebrates.anemone(element, rankChoice).ch
            case "crab": beast = Invertebrates.crab(element, rankChoice).ch
            case "leech": beast = Invertebrates.leech(element, rankChoice).ch
            case "mussel": beast = Invertebrates.mussel(element, rankChoice).ch
            case "octopus": beast = Invertebrates.octopus(element, rankChoice).ch
            case "urchin": beast = Invertebrates.urchin(element, rankChoice).ch
            case "worm": beast = Invertebrates.worm(element, rankChoice).ch
    
        diceBudget -= (beast.atrb["base_mag"] + beast.atrb["base_mar"])
        beastList += [beast]

    return beastList


def getAnimalRankOptions(majorBiome, diceBudget, creatureType, firstCreature):
    rankOptions = []

    if creatureType in oneDie_Inv:
        rankOptions += ["Small"]
        if diceBudget > 1: rankOptions += ["Large"]
    elif creatureType in twoDice_Inv:
        if diceBudget > 1: rankOptions += ["Small"]
        if diceBudget > 2: rankOptions += ["Large"]
    elif creatureType in threeDice_Inv:
        if diceBudget > 2: rankOptions += ["Small"]
        if diceBudget > 3: rankOptions += ["Large"]
    
    elif creatureType in oneDie_Vrt:
        rankOptions += ["Juvenile"]
        if diceBudget > 1: rankOptions += ["Adult"]
        if majorBiome and (diceBudget > 2): rankOptions += ["Elder"]
    elif creatureType in twoDice_Vrt:
        if diceBudget > 1: rankOptions += ["Juvenile"]
        if diceBudget > 2: rankOptions += ["Adult"]
        if majorBiome and (diceBudget > 3): rankOptions += ["Elder"]
    elif creatureType in threeDice_Vrt:        
        if diceBudget > 2: rankOptions += ["Juvenile"]
        if diceBudget > 3: rankOptions += ["Adult"]
        if majorBiome and (diceBudget > 4): rankOptions += ["Elder"]

    if len(rankOptions) == 0:
        if firstCreature:
            firstCreature = False
            if creatureType in twoDice_Vrt + threeDice_Vrt: rankOptions += ["Juvenile"]
            elif creatureType in twoDice_Inv + threeDice_Inv: rankOptions += ["Small"]
        else:
            if creatureType in ["anemone", "crab", "isopod", "octopus"]: creatureType, rankOptions = "urchin", ["Small"]
            elif creatureType in ["beetle", "centipede", "drake", "spider"]: creatureType, rankOptions = "lizard", ["Juvenile"]
            elif creatureType in ["camel", "lion", "ostrich"]: creatureType, rankOptions = "vulture", ["Juvenile"]
            elif creatureType in ["crocodile", "hydra", "tortoise", "turtle", "wyrm"]: creatureType, rankOptions = "hawk", ["Juvenile"]
            elif creatureType in ["bear", "eagle", "mole", "moose", "terror bird"]: creatureType, rankOptions = "crow", ["Juvenile"]

    return [rankOptions, creatureType]