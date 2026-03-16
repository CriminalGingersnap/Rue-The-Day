from Systems import PlayerSelect as Select
from . import Cards


def updateAce(ace, biome):
    aces = Cards.setFronts("Aces")
    backs = Cards.setBacks(4)

    Select.conversationPrint("The weather shifts.")

    match ace:
        case "Spades":
            ace = "Clubs"
            backs[0] = aces[0]
            Select.conversationPrint("Rain falls thick from heavy clouds. Water collects in deep pools.")
        case "Clubs":
            ace = "Hearts"
            backs[1] = aces[1]
            Select.conversationPrint("The rain abates. Water recedes while fog accumulates.")    
        case "Hearts":
            ace = "Diamonds"
            backs[2] = aces[2]
            Select.conversationPrint("Fog and mist linger over the land, though standing water is nowhere to be seen.")
        case "Diamonds":
            ace = "Spades"
            backs[3] = aces[3]
            Select.conversationPrint("The soil dries beneath warm sunlight. Water vanishes even from the air.")

    Cards.printDeck(backs)
    return ace


def randomEnvironment(biome):
    mapConditions = setMapConditions(biome)
    obstructions = mapConditions[0]
    slope = mapConditions[1]
    budget = mapConditions[2]
    atmosphere = mapConditions[3]

    return {"atmosphere": atmosphere, "obstructions": obstructions, "slope": slope, "budget": budget}


def setMapConditions(biome):
    slopeOptions = ["right", "lr", "up", "down", "ud", "craters", "hills", "ruin"] 
    obstructions = {"wall": 0, "trap": 0, "pit": 0}
    
    Select.waitPrint("\nDraw five numbered cards.")   
    Select.waitPrint("The first three determine topographical slope, obstruction density, and atmospheric density.")   
    Select.waitPrint("The final pair determines enemy dice budgets.")
    
    numberValues = Cards.drawNumbers(5)
    slope = slopeOptions[numberValues[0] - 1]
    obstructionValue = numberValues[1]
    atmosphereValue = numberValues[2]
    budget = [numberValues[3], numberValues[4]]

    if slope == "ruin": obstructions["pit"] = obstructionValue
    else: obstructions["wall"] = obstructionValue
    atmosphere = setAtmosphere(biome, atmosphereValue)

    return [obstructions, slope, budget, atmosphere]


def setAtmosphere(biome, extent) -> dict:
    atmosphere = {"Sacred": 0, "Death": 0, "Dazzle": 0, "Mana": 0, "Rime": 0, "Smoke": 0, "Toxin": 0}

    match biome:
        case "Rot Locus" | "Rot Encroachment": atmosphere["Death"] = extent
        case "Holy Desert" | "Holy Scrubland": atmosphere["Sacred"] = extent
        case "Dreamwood Periphery" | "Dreamwood Depths" | "Dream Sea-Cave": atmosphere["Dazzle"] = extent
        case "Frozen Glacier" | "Frozen Fjord": atmosphere["Rime"] = extent
        case "Burning Volcano" | "Burning Peninsula": atmosphere["Smoke"] = extent

    atmosphere["Mana"] = extent
    return atmosphere