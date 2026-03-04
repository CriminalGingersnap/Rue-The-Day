from Systems import PlayerSelect as Select, Conditions
from . import Area_Set as Area, DamageTypes as Damage


def execute(fighter, itemChoice, groups, battleMap) -> None:
    category, item = itemChoice[0], itemChoice[1]

    if item in ["Flameblood", "Iceblood", "Feyblood", "Corpseblood", "Toxinblood", "Blessedblood"]: imbue(fighter, category, item)
    elif item in ["Flameheart", "Iceheart", "Feyheart"]: evolve(fighter, item)
    elif item == "Vigor": invigorate(fighter, category)
    else:
        match category:
            case "Stones": Area.throwStone(fighter, item, groups, battleMap)
            case "Dusts": Area.enchant(fighter, battleMap)
        
    match category:
        case "Tinctures": Conditions.decrementTolerance(fighter, 2)
        case "Pills": Conditions.decrementTolerance(fighter, 4)

    fighter.itemUse -= 1


def evolve(fighter, item) -> None:
    fighter.atrb["base_mar"] += 2
    fighter.atrb["base_mag"] += 2

    fighter.atrb["base_hp"] += 12
    fighter.atrb["endurance"] += 12
    fighter.boons += ["Animate"]
    fighter.boons += ["Regenerate"]
    fighter.hindrance += ["Seal"]
    fighter.cndt["inviolable"] = True

    match item:
        case "Flameheart": fighter.atrb["base_elm"] = "Flame"
        case "Feyheart": fighter.atrb["base_elm"] = "Fey"
        case "Iceheart": fighter.atrb["base_elm"] = "Ice"

    Select.waitPrint(fighter.name + " begins" + item + " evolution.")
    Select.waitPrint(fighter.name + " adopts the " + fighter.atrb["base_elm"] + " element!")
    Select.waitPrint(fighter.name + " gains:")
    for buff in ["12 HP", "12 Endurance", "2 Martial Dice", "2 Magic Dice", "The 'Animate' Item Action", "The 'Regenerate' Boon", "The 'Seal' Hindrance"]:
        Select.waitPrint(buff)
    Select.waitPrint("And the 'Inviolable' condition!")

def imbue(fighter, category, item):
    phrase = fighter.name + " consumes an " + item + " "
    potency, dmgCat1, dmgCat2, dmgCat3 = 0, "", "", ""

    match category:
        case "Tinctures":
            phrase += "tincture"
            potency = 1
        case "Pills":
            phrase += "pill"
            potency = 2

    if fighter.itemEffects["Imbue"]["additional"] == item:
        potency = min(fighter.itemEffects["Imbue"]["potency"] + potency, 3)

    if potency >= 2:
        match item:
            case "Corpseblood": fighter.atrb["cur_elm"] = "Corpse"
            case "Flameblood": fighter.atrb["cur_elm"] = "Flame"
            case "Feyblood": fighter.atrb["cur_elm"] = "Fey"
            case "Iceblood": fighter.atrb["cur_elm"] = "Ice"
            case "Blessedblood": fighter.atrb["cur_elm"] = "Blessed"
            case "Toxinblood": fighter.atrb["cur_elm"] = "Toxin"

    match item:
        case "Corpseblood": dmgCat1, dmgCat2, dmgCat3 = ["Rot"], ["Venom"], ["Holy"]
        case "Flameblood": dmgCat1, dmgCat2, dmgCat3  = ["Burn"], ["Venom"], ["Freeze"]
        case "Feyblood": dmgCat1, dmgCat2, dmgCat3 = ["Dream"], ["Crush", "Pierce", "Venom"], ["Rot"]       
        case "Iceblood": dmgCat1, dmgCat2, dmgCat3 = ["Freeze"], ["Venom"], ["Burn"]
        case "Blessedblood": dmgCat1, dmgCat2, dmgCat3 = ["Holy", "Rot"], ["Venom"], []
        case "Toxinblood": dmgCat1, dmgCat2, dmgCat3 = ["Venom"], ["Rot"], []

    for dmgType in dmgCat1: Damage.modifyResistance(fighter, dmgType, potency, "positive")
    for dmgType in dmgCat2: Damage.modifyResistance(fighter, dmgType, 1, "positive")
    for dmgType in dmgCat3: Damage.modifyResistance(fighter, dmgType, potency, "negative")

    fighter.itemEffects["Imbue"]["potency"] = potency
    fighter.itemEffects["Imbue"]["duration"] = 3
    fighter.itemEffects["Imbue"]["additional"] = item

    Select.waitPrint(phrase + "!")


def invigorate(fighter, category):
    phrase = fighter.name + " consumes a vigor " + category
    healing, potency = 0, 0

    match category:
        case "Tinctures":
            phrase += "tincture"
            potency = 1
        case "Pills":
            phrase += "pill"
            healing = fighter.atrb["half_hp"]
            potency = 2


    if not fighter.cndt["lifeless"]:
        fighter.itemEffects["Invigorate"]["duration"] = 3
        fighter.itemEffects["Invigorate"]["potency"] = min(fighter.itemEffects["Invigorate"]["potency"] + potency, 4)
    
    Select.waitPrint(phrase + "!")

def regenerate(fighter):
    healing, phrase = 0, fighter.name + " regenerates "
    potency = fighter.itemEffects["Invigorate"]["potency"]

    if potency > 0:
        match potency:
            case 1:
                healing = fighter.atrb["quart_hp"]
                phrase += "a quarter of their health"
            case 2:
                healing = fighter.atrb["half_hp"]
                phrase += "half of their health"
            case 3:
                healing = fighter.atrb["half_hp"] + fighter.atrb["quart_hp"]
                phrase += "three quarters of their health"
            case 4:
                healing = fighter.atrb["base_hp"]
                phrase += "their full health"

        fighter.atrb["cur_hp"] = min(fighter.atrb["base_hp"], fighter.atrb["cur_hp"] + healing)
        Select.waitPrint(phrase + " from the effects of a vigor consumable!")