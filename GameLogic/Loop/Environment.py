from Systems import PlayerSelect as Select
from . import Cards
import random


def randomEnvironment(faceCards, biome):
    atmosphere = setAtmosphere(faceCards, biome)
    mapContours = setMapContours()
    slope = mapContours[1]
    obstructions = mapContours[0]

    return [obstructions, atmosphere, slope]


def updateFaceCard(faceCards, biome):
    Cards.showEnvironment(faceCards) 
    Select.waitPrint("\nDraw an ace to progress one environmental factor.")    
    aceSuit = Cards.drawAce()

    if aceSuit == "Diamonds":
        upperTier = ["Volcano", "Glacier", "Ghostwood", "Desert"]
        middleTier = ["Bay", "Caves", "Fjord", "Peninsula"]
        match faceCards[aceSuit]:
            case "King": faceCards[aceSuit] = "Queen"
            case "Queen":
                if biome in upperTier: faceCards[aceSuit] = "King"
                else: faceCards[aceSuit] = "Jack"
            case "Jack":
                if biome in (upperTier + middleTier): faceCards[aceSuit] = "King"
                else: faceCards[aceSuit] = "Queen"
    elif aceSuit == "Clubs":
        match faceCards[aceSuit]:
            case "King": faceCards[aceSuit] = "Jack"
            case "Queen": faceCards[aceSuit] = "King"
            case "Jack": faceCards[aceSuit] = "Queen"
    else:
        match faceCards[aceSuit]:
            case "King": faceCards[aceSuit] = "Queen"
            case "Queen": faceCards[aceSuit] = "Jack"
            case "Jack": faceCards[aceSuit] = "King"
    
    Select.slowPrint(aceSuit + ": ")
    match aceSuit:
        case "Clubs":
            Select.conversationPrint("An omen reveals changing fortunes.")
            match faceCards["Clubs"]:
                case "King": Select.conversationPrint("Foes amass in great number. Tension hangs heavy.")
                case "Queen": Select.conversationPrint("Hostile forces congregate. Worse will come.")
                case "Jack": Select.conversationPrint("The day grows calm. All seems to be at peace.")
        case "Hearts":
            Select.conversationPrint("The weather shifts.")
            match faceCards["Hearts"]:
                case "King": Select.conversationPrint("Rain falls thick from heavy clouds. Water collects in deep pools.")
                case "Queen": Select.conversationPrint("The rain abates. Water recedes while fog accumulates.")
                case "Jack": Select.conversationPrint("The soil dries beneath warm sunlight. Clouds gather on the horizon.")
        case "Diamonds":
            Select.conversationPrint("The flow of magic alters.")
            match faceCards["Diamonds"]:
                case "King": Select.conversationPrint("Mana surges to extremes. Step carefully.")
                case "Queen": Select.conversationPrint("Mana exceeds safe levels. Remain watchful.")
                case "Jack": Select.conversationPrint("Mana dissipates. Make use of what remains.")
        case "Spades": 
            Select.conversationPrint("An omen reveals changing fortunes.")
            match faceCards["Spades"]:
                case "King": Select.conversationPrint("Elder things stir. Hunger and ambition will find ample reward.")
                case "Queen": Select.conversationPrint("The wilds awaken. Experienced hunters roam.")
                case "Jack": Select.conversationPrint("Old powers return to slumber. Young powers emerge.")

    Cards.showEnvironment(faceCards)


def setMapContours():
    Select.waitPrint("\nDraw two numbered card to determine map slope and obstruction density.")   
    slopeOptions = ["right", "lr", "up", "down", "ud", "craters", "hills", "ruin"] 
    obstructions = {"wall": 0, "trap": 0, "pit": 0}
    
    numberValues = Cards.drawNumbers(2)
    slope = slopeOptions[numberValues[0] - 1]
    obstructionValue = numberValues[1]

    if slope == "ruin": obstructions["pit"] = obstructionValue
    else: obstructions["wall"] = obstructionValue

    return [obstructions, slope]


def setAtmosphere(faceCards, biome) -> dict:
    atmosphere = {"Blessed": 0, "Death": 0, "Dazzle": 0, "Mana": 0, "Rime": 0, "Smoke": 0, "Toxin": 0}
    extent = 0

    match faceCards["Diamonds"]:
        case "King": extent = 6
        case "Queen": extent = 4
        case "Jack": extent = 2

    match biome:
        case "Caves": atmosphere["Toxin"] = extent
        case "Crypt": atmosphere["Death"] = extent
        case "Desert": atmosphere["Blessed"] = extent
        case "Ghostwood": atmosphere["Dazzle"] = extent
        case "Glacier": atmosphere["Rime"] = extent
        case "Volcano": atmosphere["Smoke"] = extent

    atmosphere["Mana"] = extent
    return atmosphere