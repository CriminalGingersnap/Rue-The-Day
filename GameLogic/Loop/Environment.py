from Systems import PlayerSelect as Select
from . import Cards
import random


def randomEnvironment(faceCards):
    updateFaceCard(faceCards)
    atmosphere = setAtmosphere(faceCards)

    slope = random.choice(["right", "left", "lr", "up", "down", "ud", "craters", "hills", "ruin"])
    obstructions = setObstructions(faceCards["Clubs"], slope)

    return [obstructions, atmosphere, slope]


def updateFaceCard(faceCards):
    Cards.showEnvironment(faceCards) 
    Select.waitPrint("\nDraw an ace to progress one environmental factor.")    

    aces = Cards.setFronts("Aces")
    aceChoice = Cards.pickCard(aces, 1)[0]
    aceSuit = Cards.findSuit(aces[aceChoice][1])

    match faceCards[aceSuit]:
        case "King": faceCards[aceSuit] = "Queen"
        case "Queen": faceCards[aceSuit] = "Jack"
        case "Jack": faceCards[aceSuit] = "King"

    Select.slowPrint(aceSuit + ": ")
    match aceSuit:
        case "Clubs":
            Select.conversationPrint("The prevalence of obstructions changes.")
            match faceCards["Clubs"]:
                case "King": Select.conversationPrint("Natural structures crowd together. Little can be seen at range.")
                case "Queen": Select.conversationPrint("Clearings open, gaps widen, and sight-lines expand.")
                case "Jack": Select.conversationPrint("Trees and rocks grow sparse. Visibility increases.")
        case "Hearts":
            Select.conversationPrint("The weather shifts.")
            match faceCards["Hearts"]:
                case "King": Select.conversationPrint("Rain falls thick from heavy clouds. Water collects in deep pools.")
                case "Queen": Select.conversationPrint("The rain abates. Water recedes while fog accumulates.")
                case "Jack": Select.conversationPrint("The soil dries beneath warm sunlight. Clouds gather on the horizon.")
        case "Diamonds":
            Select.conversationPrint("The flow of magic alters.")
            match faceCards["Diamonds"]:
                case "King": Select.conversationPrint("Mana surges. Step carefully.")
                case "Queen": Select.conversationPrint("Mana dissipates. Make use of what remains.")
                case "Jack": Select.conversationPrint("Mana collapses, relative to its local norm.")
        case "Spades": 
            Select.conversationPrint("An omen reveals changing fortunes.")
            match faceCards["Spades"]:
                case "King": Select.conversationPrint("Forces unfriendly to human life stir from their slumber.")
                case "Queen": Select.conversationPrint("The wilds seek blood. Hunger and ambition will find rewards.")
                case "Jack": Select.conversationPrint("Old powers recede, making space for younger threats.")   

    Cards.showEnvironment(faceCards)

    
def setObstructions(clubFace, slope) -> dict:
    obstructions = {"wall": 0, "trap": 0, "pit": 0}
    minValue, maxValue = 0, 0

    if slope == "ruin":
        minValue, maxValue = 0, 3
        obstructions["pit"] = random.randint(minValue, maxValue)
        # obstructions["trap"] = random.randint(minValue, maxValue)
    else:
        match clubFace:
            case "King": minValue, maxValue = 6, 9
            case "Queen": minValue, maxValue = 3, 6
            case "Jack": minValue, maxValue = 0, 3
        obstructions["wall"] = random.randint(minValue, maxValue)

    return obstructions

def setAtmosphere(faceCards, biome) -> dict:
    atmosphere = {"Blessed": 0, "Death": 0, "Dazzle": 0, "Mana": 0, "Rime": 0, "Smoke": 0, "Toxic": 0}
    extent = 0

    match faceCards["Diamonds"]:
        case "King": extent = 6
        case "Queen": extent = 4
        case "Jack": extent = 2

    match biome:
        case "Caves": atmosphere["Toxic"] = extent
        case "Crypt": atmosphere["Death"] = extent
        case "Desert": atmosphere["Blessed"] = extent
        case "Ghostwood": atmosphere["Dazzle"] = extent
        case "Glacier": atmosphere["Rime"] = extent
        case "Volcano": atmosphere["Smoke"] = extent

    atmosphere["Mana"] = extent
    return atmosphere