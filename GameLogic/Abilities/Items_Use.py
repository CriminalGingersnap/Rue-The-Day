from Systems import Damage, PlayerSelect as Select, Conditions
from . import Area_Set as Area


def execute(fighter, category, element, application, groups, battleMap) -> None:
    end = " a condensed " + element + " " + category + "!"

    match application:
        case "Detonate":
            Select.waitPrint(fighter.props["name"] + " throws " + end)
            Area.throwStone(fighter, category, element, groups, battleMap)
        case "Extract":
            Select.waitPrint(fighter.props["name"] + " consumes the essence of " + end)
            if element == "Bleed": invigorate(fighter, category)
            else: imbue(fighter, category, element)            
            match category:
                case "pearls": Conditions.decrementTolerance(fighter, 2)
                case "cores": Conditions.decrementTolerance(fighter, 4)


def imbue(fighter, category, element) -> None:
    potency, dmgCat1, dmgCat2, dmgCat3 = 0, "", "", ""

    match category:
        case "pearls": potency = 1
        case "cores": potency = 2

    if fighter.itemEffects["Imbue"]["additional"] == element:
        potency = min(fighter.itemEffects["Imbue"]["potency"] + potency, 3)

    match element:
        case "Rot": dmgCat1, dmgCat2, dmgCat3 = ["Rot"], ["Toxic"], ["Holy"]
        case "Flame": dmgCat1, dmgCat2, dmgCat3  = ["Flame"], ["Toxic"], ["Ice"]
        case "Dream": dmgCat1, dmgCat2, dmgCat3 = ["Dream"], ["Crush", "Pierce", "Toxic"], ["Rot"]       
        case "Ice": dmgCat1, dmgCat2, dmgCat3 = ["Ice"], ["Toxic"], ["Flame"]
        case "Holy": dmgCat1, dmgCat2, dmgCat3 = ["Holy", "Rot"], ["Toxic"], []
        case "Toxic": dmgCat1, dmgCat2, dmgCat3 = ["Toxic"], ["Rot"], []

    for dmgType in dmgCat1: Damage.modifyResistance(fighter, dmgType, potency, "positive")
    for dmgType in dmgCat2: Damage.modifyResistance(fighter, dmgType, 1, "positive")
    for dmgType in dmgCat3: Damage.modifyResistance(fighter, dmgType, potency, "negative")

    fighter.itemEffects["Imbue"]["potency"] = potency
    fighter.itemEffects["Imbue"]["duration"] = 3
    fighter.itemEffects["Imbue"]["additional"] = element


def invigorate(fighter, category) -> None:
    potency = 0

    match category:
        case "pearls": potency = 1
        case "cores": potency = 2

    if not fighter.cndt["lifeless"]:
        fighter.itemEffects["Invigorate"]["duration"] = 3
        fighter.itemEffects["Invigorate"]["potency"] = min(fighter.itemEffects["Invigorate"]["potency"] + potency, 4)


def regenerate(fighter) -> None:
    healing, potency = 0, fighter.itemEffects["Invigorate"]["potency"]

    if healing > 0:
        match potency:
            case 1: healing = fighter.atrb["quart_hp"]
            case 2: healing = fighter.atrb["half_hp"]
            case 3: healing = fighter.atrb["half_hp"] + fighter.atrb["quart_hp"]
            case 4: healing = fighter.atrb["base_hp"]

        Select.waitPrint("Blood essence activates!")
        Conditions.recoverHP(fighter, healing)

        
def evolve(fighter, item) -> None:
    fighter.atrb["base_mar"] += 2
    fighter.atrb["base_mag"] += 2

    fighter.atrb["base_hp"] += 12
    fighter.atrb["endurance"] += 12
    fighter.boons += ["Regenerate"]
    fighter.hindrance += ["Seal"]
    fighter.cndt["inviolable"] = True

    match item:
        case "Flameheart": fighter.atrb["base_elm"] = "Flame"
        case "Dreamheart": fighter.atrb["base_elm"] = "Dream"
        case "Iceheart": fighter.atrb["base_elm"] = "Ice"

    Select.waitPrint(fighter.props["name"] + " begins" + item + " evolution.")
    Select.waitPrint(fighter.props["name"] + " adopts the " + fighter.atrb["base_elm"] + " element!")
    Select.waitPrint(fighter.props["name"] + " gains:")
    for buff in ["12 HP", "12 Endurance", "2 Martial Dice", "2 Magic Dice", "The 'Regenerate' Boon", "The 'Seal' Hindrance"]:
        Select.waitPrint(buff)
    Select.waitPrint("And the 'Inviolable' condition!")

