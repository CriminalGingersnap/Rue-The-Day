from Systems import PlayerSelect as Select
from . import Cards
import random

slopes = ["right", "left", "lr", "up", "down", "ud", "craters", "hills", "canyons"]


def randomEnvironment(faceCards):
    Cards.showEnvironment(faceCards) 
    Select.waitPrint("\nDraw an ace to progress one environmental factor.")
    aces = Cards.setFronts("Aces")
    aceChoice = Cards.pickCard(aces, 1)[0]
    aceSuit = Cards.findSuit(aces[aceChoice][1])

    introduceEnvironment(faceCards, aceSuit)
    atmosphere = setEnvironment(faceCards, aceSuit)

    Select.waitPrint("\nDraw three numbered cards to determine obstructions, encounter, and slope.")
    numbers = Cards.setFronts("Numbers")
    numberChoices = Cards.pickCard(numbers, 3)
    wallNum, encounterNum, slopeNum = numberChoices[0], numberChoices[1], numberChoices[2]
    wallValue = Cards.findValue(numbers[wallNum][3])
    encounterValue = Cards.findValue(numbers[encounterNum][3])
    slopeValue = Cards.findValue(numbers[slopeNum][3])

    obstructions = {"wall": wallValue, "trap": 0, "pit": 0}
    slope = slopes[int(slopeValue) - 1]
    slope = "craters"

    return [obstructions, atmosphere, slope, encounterValue]


def introduceEnvironment(environment, aceSuit):
    Select.slowPrint(aceSuit + ": ")
    match aceSuit:
        case "Clubs": Select.conversationPrint("A new biome gains ascendancy.")
        case "Hearts": Select.conversationPrint("The weather changes.")
        case "Diamonds": Select.conversationPrint("The flow of magic shifts.")
        case "Spades": Select.conversationPrint("An omen reveals changing fortunes.")

    Select.waitPrint("Previous face: " + environment[aceSuit])
    match environment[aceSuit]:
        case "King": environment[aceSuit] = "Queen"
        case "Queen": environment[aceSuit] = "Jack"
        case "Jack": environment[aceSuit] = "King"
    Select.waitPrint("New face: " + environment[aceSuit] + "\n")

def setEnvironment(environment, aceSuit) -> dict:
    atmosphere = {"Blessed": 0, "Death": 0, "Dazzle": 0, "Mana": 0, "Rime": 0, "Smoke": 0, "Toxic": 0}
    type, extent = "None", 0

    match aceSuit:
        case "Clubs":
            match environment["Clubs"]:
                case "King":
                    Select.conversationPrint("Strange fragrance rolls across the fjord. Fey shadows flicker at the edge of sight.")
                    type = "Dazzle"
                case "Queen":
                    Select.conversationPrint("The glacier grinds forward. Bitter cold creeps across the valley.")
                    type = "Rime"
                case "Jack":
                    Select.conversationPrint("The volcano belches smoke. Warm wind carries its embers from afar.")
                    type = "Smoke"
        
        case "Diamonds":
            match environment["Diamonds"]:
                case "King":
                    Select.conversationPrint("Mana surges. Step carefully.")
                    extent = 3
                case "Queen":
                    Select.conversationPrint("Mana dissipates. Make use of what remains.")
                    extent = 2
                case "Jack":
                    Select.conversationPrint("Mana collapses, relative to its local norm.")
                    extent = 1
        
        case "Hearts":
            match environment["Hearts"]:
                case "King": Select.conversationPrint("Rain falls thick from heavy clouds. Water collects in deep pools.")
                case "Queen": Select.conversationPrint("The rain abates. Water recedes while fog accumulates.")
                case "Jack": Select.conversationPrint("The soil dries beneath warm sunlight. Clouds gather on the horizon.")
        
        case "Spades":
            match environment["Spades"]:
                case "King": Select.conversationPrint("Forces unfriendly to human life stir from their slumber.")
                case "Queen": Select.conversationPrint("The wilds seek blood. Hunger and ambition will find rewards.")
                case "Jack": Select.conversationPrint("Old powers recede, making space for younger threats.")   

    atmosphere[type] = extent
    atmosphere["Mana"] = extent
    return atmosphere