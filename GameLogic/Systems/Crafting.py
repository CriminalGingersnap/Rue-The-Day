from . import PlayerSelect as Select


def craftLoop(fighter):
    answer, choices = "", ["View Recipes", "Craft", "Exit"]
    options = getCraftOptions(fighter)

    while (len(options) > 0) and (answer != "Exit"):
        answer = Select.makeSelection(choices)
        if answer == "View Recipes": printRecipes()
        elif answer == "Craft": alchemy(fighter, options)

        options = getCraftOptions(fighter)


def alchemy(fighter, options):
    categoryOptions, categoryChoice = [], ""
    
    for category in options:
        if len(options[category] == 0): options.remove(category)
        else: categoryOptions += [category]

    if len(categoryOptions) == 1: categoryChoice = categoryOptions[0]
    else: categoryChoice = Select.makeSelection(categoryOptions)


    itemChoice = Select.makeSelection(options[categoryChoice] + ["None"])

    match categoryChoice:
        case "Tincture": fighter.inventory["Gourd"]["Contents"]["Water"] -= 1
        case "Pills": fighter.inventory["Vials"]["Contents"]["Resin"] -= 1

    if categoryChoice == "Bloods":
        if itemChoice in ["Corpse->Basic", "Flame->Basic", "Fey->Basic", "Ice->Basic"]:
            fighter.inventory["Vials"]["Contents"]["Bloods"]["Basic"] += 1 
            match itemChoice:
                case "Corpse->Basic":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Corpse"] -= 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Blessed"] -= 1
                case "Flame->Basic":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Flame"] -= 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Ice"] -= 1
                case "Fey->Basic":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Fey"] -= 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Corpse"] -= 1
                case "Ice->Basic":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Ice"] -= 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Flame"] -= 1

        else:
            fighter.inventory["Vials"]["Contents"]["Bloods"]["Basic"] -= 1 
            match itemChoice:
                case "Corpse":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Corpse"] += 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Corpse"] -= 1
                case "Flame":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Flame"] += 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Flame"] -= 1
                case "Fey":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Fey"] += 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Fey"] -= 1
                case "Ice":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Ice"] += 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Ice"] -= 1
                case "Blessed":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Blessed"] += 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Blessed"] -= 1
                case "Toxin":
                    fighter.inventory["Vials"]["Contents"]["Bloods"]["Toxin"] += 1
                    fighter.inventory["Vials"]["Contents"]["Dusts"]["Toxin"] -= 1


    if categoryChoice in ["Core Dusts", "Pearl dusts"]:
        # match categoryChoice:
        #     case "Core Dusts": increase = min(dustRemaining, 3)
        #     case "Pear Dusts": increase = min(dustRemaining, 1)

        match itemChoice:
            case "Corpse": fighter.inventory["Vials"]["Contents"]["Dusts"]["Corpse"] += increase
            case "Fey": fighter.inventory["Vials"]["Contents"]["Dusts"]["Fey"] += increase
            case "Flame": fighter.inventory["Vials"]["Contents"]["Dusts"]["Flame"] += increase
            case "Ice": fighter.inventory["Vials"]["Contents"]["Dusts"]["Ice"] += increase


def getCraftOptions(fighter, dustTotal) -> list:
    craftingOptions = {
        "Bloods": [],
        "Core Dusts": [],
        "Pearl Dusts": [],
        "Pills": [],
        "Tinctures": []
    }

    gourd = fighter.inventory["Gourd"]["Contents"]
    vials = fighter.inventory["Vials"]["Contents"]
    boxes = fighter.inventory["Pill Box"]["Contents"]
    bloods, dusts, stones = vials["Bloods"], vials["Dusts"], boxes["Stones"]
    
    vialsCapacity, vialsFilled = fighter.inventory["Vials"]["Capacity"], 0
    for substanceType in vials:
        for substance in vials[substanceType]: vialsFilled += vials[substanceType][substance]
    
    boxesCapacity, boxesFilled = fighter.inventory["Pill Box"]["Capacity"], 0
    for substanceType in boxes:
        for substance in boxes[substanceType]: vialsFilled += boxes[substanceType][substance]

    if (gourd["Water"] > 0) and (vialsFilled <= vialsCapacity):
        if bloods["Basic"] > 0: craftingOptions["Tinctures"] += ["Vigor"]
        if bloods["Corpse"] > 0: craftingOptions["Tinctures"] += ["Corpseblood"]
        if bloods["Flame"] > 0: craftingOptions["Tinctures"] += ["Flameblood"]
        if bloods["Fey"] > 0: craftingOptions["Tinctures"] += ["Feyblood"]
        if bloods["Ice"] > 0: craftingOptions["Tinctures"] += ["Iceblood"]
        if bloods["Toxin"] > 0: craftingOptions["Tinctures"] += ["Toxinblood"]
        if bloods["Blessed"] > 0: craftingOptions["Tinctures"] += ["Blessedblood"]
    if vials["Resin"] > 0 and (boxesFilled < boxesCapacity):
        if bloods["Basic"] > 1: craftingOptions["Pills"] += ["Vigor"]
        if bloods["Corpse"] > 1: craftingOptions["Pills"] += ["Corpseblood"]
        if bloods["Flame"] > 1: craftingOptions["Pills"] += ["Flameblood"]
        if bloods["Fey"] > 1: craftingOptions["Pills"] += ["Feyblood"]
        if bloods["Ice"] > 1: craftingOptions["Pills"] += ["Iceblood"]
        if bloods["Blessed"] > 1: craftingOptions["Pills"] += ["Blessedblood"]

    if (bloods["Corpse"] > 0) and (dusts["Blessed"] > 0): craftingOptions["Blood"] += ["Corpse->Basic"]
    if (bloods["Flame"] > 0) and (dusts["Ice"] > 0): craftingOptions["Blood"] += ["Flame->Basic"]
    if (bloods["Fey"] > 0) and (dusts["Corpse"] > 0): craftingOptions["Blood"] += ["Fey->Basic"]
    if (bloods["Ice"] > 0) and (dusts["Flame"] > 0): craftingOptions["Blood"] += ["Ice->Basic"]

    if bloods["Basic"] > 0:
        if dusts["Corpse"] > 0: craftingOptions["Blood"] += ["Corpse"]
        if dusts["Flame"] > 0: craftingOptions["Blood"] += ["Flame"]
        if dusts["Fey"] > 0: craftingOptions["Blood"] += ["Fey"]
        if dusts["Ice"] > 0: craftingOptions["Blood"] += ["Ice"]
        if dusts["Blessed"] > 0: craftingOptions["Blood"] += ["Blessed"]
        if dusts["Toxin"] > 0: craftingOptions["Blood"] += ["Toxin"]

    if stones["Corpse Core"] > 0: craftingOptions["Core Dusts"] += ["Corpse"]
    if stones["Corpse Pearl"] > 0: craftingOptions["Pearl Dusts"] += ["Corpse"]
    if stones["Flame Core"] > 0: craftingOptions["Core Dusts"] += ["Flame"]
    if stones["Flame Pearl"] > 0: craftingOptions["Pearl Dusts"] += ["Flame"]
    if stones["Fey Core"] > 0: craftingOptions["Core Dusts"] += ["Fey"]
    if stones["Fey Pearl"] > 0: craftingOptions["Pearl Dusts"] += ["Fey"]
    if stones["Ice Core"] > 0: craftingOptions["Core Dusts"] += ["Ice"]
    if stones["Ice Pearl"] > 0: craftingOptions["Pearl Dusts"] += ["Ice"]
    if stones["Toxin Core"] > 0: craftingOptions["Core Dusts"] += ["Toxin"]
    if stones["Toxin Pearl"] > 0: craftingOptions["Pearl Dusts"] += ["Toxin"]
    if stones["Blessed Core"] > 0: craftingOptions["Core Dusts"] += ["Blessed"]
    if stones["Blessed Pearl"] > 0: craftingOptions["Pearl Dusts"] += ["Blessed"]

    return craftingOptions


def printRecipes():
    bloodCost, dustCost = "One vial blood", "One pinch magic dust"
    tinctureCost, pillCost = "Tincture: One vial water. ", "Pill: One vial resin. "
    basic, elemental = "(basic). ", "(elemental). "

    vigorTincture = "Vigor " + tinctureCost + bloodCost + basic
    vigorPill = "Vigor " + pillCost + bloodCost + basic
    elementalPill = "Elemental " + pillCost + bloodCost + elemental
    elementalTincture = "Elemental " + tinctureCost + bloodCost + elemental

    basicBloodVial = "Basic Blood: " + bloodCost + elemental + dustCost + "(opposite). "
    elementalBloodVial = "Elemental Blood: " + bloodCost + basic + dustCost + elemental

    pearlDust = "Pearl Dust: 1 per elemental pearl. "
    coreDust = "Core Dust: 3 per elemental core. "

    potionList = [vigorTincture, vigorPill, elementalTincture, elementalPill, basicBloodVial, elementalBloodVial, pearlDust, coreDust]

    for potion in potionList: Select.waitPrint(potion)