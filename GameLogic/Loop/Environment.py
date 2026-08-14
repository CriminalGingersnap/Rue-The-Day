from Systems import PlayerSelect as Select, Roll
from . import Cards


def updateAce(ace, biome):
    aces = Cards.setFronts("Aces")
    backs = Cards.setBacks(4)

    Select.waitPrint("Rolling to determine change in weather.")
    threshold = 0

    match biome:
        case "Holy Desert" | "Rot Locus" | "Ice Peak":
            match ace:
                case "Spades" | "Clubs": threshold = 3
                case "Hearts": threshold = 5
                case "Diamonds": threshold = 12
        case "Holy Scrubland" | "Ice Glacier" | "Rot Encroachment":
            match ace:
                case "Spades" | "Clubs": threshold = 5
                case "Hearts": threshold = 7
                case "Diamonds": threshold = 9
        case "Dream Sea-Cave" | "Ice Fjord" | "Marshland" | "Marsh Depths" | "Shoreline Dunes" | "Shoreline Nests": 
            match ace:
                case "Spades" | "Clubs": threshold = 9
                case "Hearts": threshold = 5
                case "Diamonds": threshold = 3
        case _: threshold = 7

    Select.waitPrint("Rolling to trigger change in weather. Current threshold: " + str(threshold))
    roll = Roll.roll(None, None, 2, None, None)

    if roll >= threshold:
        phrase1, phrase2 = "", ""
        match ace:
            case "Spades":
                ace = "Clubs"
                backs[0] = aces[0]
                phrase1 = "Tides rise, rivers flood, ice melts, or rain falls thick from heavy clouds."
                phrase2 = "Water collects in deep pools."
            case "Clubs":
                ace = "Hearts"
                backs[1] = aces[1]
                phrase1 = "Rain abates, melting ceases, or tides and rivers recede."    
                phrase2 = "Water levels drop while heavy fog accumulates."    
            case "Hearts":
                ace = "Diamonds"
                backs[2] = aces[2]
                phrase1 = "Fog and mist linger quietly over the land."
                phrase2 = "Standing water is nowhere to be seen."
            case "Diamonds":
                ace = "Spades"
                backs[3] = aces[3]
                phrase1 = "Strong winds or bright sunlight drive out what remains of moisture."
                phrase2 = "Water vanishes even from the air."

        Select.conversationPrint("The weather shifts.")
        Cards.printDeck(backs)
        Select.waitPrint(phrase1)
        Select.waitPrint(phrase2)

    else: Select.conversationPrint("The weather holds.")

    return ace


def randomEnvironment(ace, biome):
    mapConditions = setMapConditions(ace, biome)

    return {"atmosphere": mapConditions[0],
             "obstructions": mapConditions[1],
              "slope": mapConditions[2],
               "budget": mapConditions[3],
                "luck": mapConditions[4]}


def setMapConditions(ace, biome):
    slopeOptions = ["right", "lr", "up", "down", "ud", "craters", "hills", "ruin"] 
    obstructions = {"wall": 0, "trap": 0, "pit": 0}
    
    Select.waitPrint("\nDraw five numbered cards.")   
    Select.quickPrint("The first three determine topographical slope, obstruction density, and atmospheric density.")   
    Select.quickPrint("The next pair determines enemy dice budgets.")
    Select.waitPrint("The final face-down card modifies enemy type.")
    
    numberValues = Cards.drawNumbers(5)
    drawn, faceDown = numberValues[0], numberValues[1]
    slope = slopeOptions[drawn[0] - 2]
    obstructionValue = drawn[1]
    atmosphereValue = drawn[2]
    budget = [drawn[3], drawn[4]]

    if (slope == "ruin") or (biome == "Rot Locus"): obstructions["pit"] = obstructionValue
    elif biome == "Flame Volcano":
        obstructions["pit"] = (obstructionValue // 3) * 2
        obstructions["wall"] = obstructionValue - obstructions["pit"]
    elif biome == "Ice Glacier": obstructions["wall"] = obstructionValue * 2
    else: obstructions["wall"] = obstructionValue
    
    atmosphere = setAtmosphere(ace, biome, atmosphereValue)

    return [atmosphere, obstructions, slope, budget, faceDown]


def setAtmosphere(ace, biome, extent) -> dict:
    atmosphere = {"}": 0, "@": 0, "=": 0, "-": 0, "&": 0, "%": 0, "+": 0, ";": 0, "#": 0}

    if biome in ["Dreamwood Depths", "Flame Volcano", "Holy Desert", "Ice Glacier", "Ice Peak", "Rot Locus"]: extent += 3
    
    match biome:
        case "Dreamwood Periphery" | "Dreamwood Depths" | "Dream Sea-Cave": atmosphere["@"] = extent
        case "Flame Volcano" | "Flame Peninsula" | "Flame Lowland": atmosphere["#"] = extent
        case "Holy Desert" | "Holy Scrubland": atmosphere["+"] = extent
        case "Ice Glacier" | "Ice Fjord" | "Ice Highland": atmosphere["%"] = extent
        case "Marsh": atmosphere["&"] = extent
        case "Rot Locus" | "Rot Encroachment": atmosphere["}"] = extent

    match ace:
        case "Hearts": atmosphere["="] = 4
        case "Diamonds": atmosphere["="], atmosphere["-"] = 1, 2
        case "Clubs": atmosphere["-"] = 5
    
    return atmosphere