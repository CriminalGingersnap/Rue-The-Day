from Systems import PlayerSelect as Select
from . import Cards
import random


def randomEnvironment(faceCards):
    updateFaceCard(faceCards)
    atmosphere = setAtmosphere(faceCards)
    mapContours = setMapContours()
    slope = mapContours[0]
    obstructions = mapContours[1]

    return [obstructions, atmosphere, slope]


def updateFaceCard(faceCards):
    Cards.showEnvironment(faceCards) 
    Select.waitPrint("\nDraw an ace to progress one environmental factor.")    
    aceSuit = Cards.drawAce()

    match faceCards[aceSuit]:
        case "King": faceCards[aceSuit] = "Queen"
        case "Queen": faceCards[aceSuit] = "Jack"
        case "Jack": faceCards[aceSuit] = "King"

    Select.slowPrint(aceSuit + ": ")
    match aceSuit:
        case "Clubs":
            Select.conversationPrint("")
            match faceCards["Clubs"]:
                case "King": Select.conversationPrint("")
                case "Queen": Select.conversationPrint("")
                case "Jack": Select.conversationPrint("")
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


def setMapContours():
    Select.waitPrint("\nDraw two numbered card to determine map slope and obstruction density.")   
    slopeOptions = ["right", "lr", "up", "down", "ud", "craters", "hills", "ruin"] 
    obstructions = {"wall": 0, "trap": 0, "pit": 0}
    
    numberValues = Cards.drawNumbers(2)
    slope = slopeOptions[numberValues[0] - 1]
    obstructionValue = numberValues[1]

    if slope == "ruin": obstructions["pit"] = obstructionValue
    else: obstructions["wall"] = obstructionValue

    return [slope, obstructions]


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