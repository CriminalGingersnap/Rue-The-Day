from Systems import PlayerSelect as Select, Roll
from . import Cards


def updateAce(ace, biome):
    aces = Cards.setFronts("Aces")
    backs = Cards.setBacks(4)

    Select.waitPrint("Rolling to determine change in weather.")
    threshold = 0

    match biome:
        case "Holy Desert" | "Rot Locus":
            match ace:
                case "Spades" | "Clubs": threshold = 3
                case "Hearts": threshold = 5
                case "Diamonds": threshold = 12
        case "Holy Scrubland" | "Frozen Glacier" | "Rot Encroachment":
            match ace:
                case "Spades" | "Clubs": threshold = 5
                case "Hearts": threshold = 7
                case "Diamonds": threshold = 9
        case "Dream Sea-Cave" | "Frozen Fjord" | "Marshland" | "Shoreline": 
            match ace:
                case "Spades" | "Clubs": threshold = 9
                case "Hearts": threshold = 5
                case "Diamonds": threshold = 3
        case _: threshold = 7

    Select.waitPrint("Rolling to trigger change in weather. Current threshold: " + str(threshold))
    roll = Roll.roll(None, 2, None, None)

    if roll >= threshold:
        Select.conversationPrint("The weather shifts.")

        match ace:
            case "Spades":
                ace = "Clubs"
                backs[0] = aces[0]
                Select.conversationPrint("Tides rise, or rain falls thick from heavy clouds. Whatever its source, water collects in deep pools.")
            case "Clubs":
                ace = "Hearts"
                backs[1] = aces[1]
                Select.conversationPrint("Rain abates, or tides recede. Water levels drop while heavy fog accumulates.")    
            case "Hearts":
                ace = "Diamonds"
                backs[2] = aces[2]
                Select.conversationPrint("Fog and mist linger quietly over the land, though standing water is nowhere to be seen.")
            case "Diamonds":
                ace = "Spades"
                backs[3] = aces[3]
                Select.conversationPrint("Strong winds or bright sunlight drive out what remains of moisture. Water vanishes even from the air.")

        Cards.printDeck(backs)
    else: "The weather holds."

    return ace


def randomEnvironment(biome):
    mapConditions = setMapConditions(biome)

    return {"atmosphere": mapConditions[0],
             "obstructions": mapConditions[1],
              "slope": mapConditions[2],
               "budget": mapConditions[3],
                "curse": mapConditions[4]}


def setMapConditions(biome):
    slopeOptions = ["right", "lr", "up", "down", "ud", "craters", "hills", "ruin"] 
    obstructions = {"wall": 0, "trap": 0, "pit": 0}
    
    Select.waitPrint("\nDraw five numbered cards.")   
    Select.quickPrint("The first three determine topographical slope, obstruction density, and atmospheric density.")   
    Select.quickPrint("The next pair determines enemy dice budgets.")
    Select.waitPrint("The final face-down card determines curse status.")
    
    numberValues = Cards.drawNumbers(5)
    drawn, faceDown = numberValues[0], numberValues[1]
    slope = slopeOptions[drawn[0] - 2]
    obstructionValue = drawn[1]
    atmosphereValue = drawn[2]
    budget = [drawn[3], drawn[4]]

    if slope == "ruin": obstructions["pit"] = obstructionValue
    else: obstructions["wall"] = obstructionValue
    atmosphere = setAtmosphere(biome, atmosphereValue)

    return [atmosphere, obstructions, slope, budget, faceDown]


def setAtmosphere(biome, extent) -> dict:
    atmosphere = {"Sacred": 0, "Death": 0, "Dazzle": 0, "Mana": 0, "Rime": 0, "Smoke": 0}
    majorBiomes = ["Icy Volcano", "Dreamwood Depths", "Icy Glacier", "Holy Desert", "Rot Locus"]

    if biome in majorBiomes:
        atmosphere["Mana"] = extent
        extent += 3
    
    match biome:
        case "Rot Locus" | "Rot Encroachment": atmosphere["Death"] = extent
        case "Holy Desert" | "Holy Scrubland": atmosphere["Sacred"] = extent
        case "Dreamwood Periphery" | "Dreamwood Depths" | "Dream Sea-Cave": atmosphere["Dazzle"] = extent
        case "Icy Glacier" | "Icy Fjord": atmosphere["Rime"] = extent
        case "Flaming Volcano" | "Flaming Peninsula": atmosphere["Smoke"] = extent
    
    return atmosphere