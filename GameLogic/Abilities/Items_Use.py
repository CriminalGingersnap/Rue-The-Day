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


def imbue(fighter, category, item) -> None:
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

    if potency >= 2: fighter.atrb["cur_elm"] = item.split('blood')[0]

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


def invigorate(fighter, category) -> None:
    phrase, potency = fighter.name + " consumes a vigor " + category, 0

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

def regenerate(fighter) -> None:
    healing, potency = 0, fighter.itemEffects["Invigorate"]["potency"]

    if healing > 0:
        match potency:
            case 1: healing = fighter.atrb["quart_hp"]
            case 2: healing = fighter.atrb["half_hp"]
            case 3: healing = fighter.atrb["half_hp"] + fighter.atrb["quart_hp"]
            case 4: healing = fighter.atrb["base_hp"]

        Select.waitPrint("Vigor consumable activates!")
        Conditions.recoverHP(fighter, healing)