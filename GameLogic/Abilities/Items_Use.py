from Systems import Damage, PlayerSelect as Select, Conditions
from . import Area_Set as Area, Area_Apply as Apply


def execute(fighter, category, element, application, groups, battleMap) -> None:
    end = "a condensed " + element + " " + category.split("s")[0] + "!"

    match application:
        case "Animate":
            Select.waitPrint(fighter.props["name"] + " animates " + end)
            animate(fighter, groups)
        case "Detonate":
            Select.waitPrint(fighter.props["name"] + " throws " + end)
            Area.throwStone(fighter, category, element, groups, battleMap)
        case "Extract":
            Select.waitPrint(fighter.props["name"] + " absorbs the essence of " + end)
            if element == "Bleed": invigorate(fighter, category, battleMap)
            else: imbue(fighter, category, element, battleMap)            
            match category:
                case "pearls": Conditions.decrementTolerance(fighter, 2)
                case "cores": Conditions.decrementTolerance(fighter, 4)


def animate(fighter, groups) -> None:
    echo = fighter.inv["echo"]
    echo.position = Area.findSpace(fighter, groups, 4)
    echo.itemEffects["Animate"]["duration"] = 3
    echo.itemEffects["Animate"]["additional"] = True


def imbue(fighter, category, element, battleMap) -> None:
    potency, dmgCat1, dmgCat2 = 0, "", ""

    match category:
        case "pearls": potency = 1
        case "cores": potency = 2

    if fighter.itemEffects["Imbue"]["additional"] == element:
        potency = min(fighter.itemEffects["Imbue"]["potency"] + potency, 3)

    match element:
        case "Dream": dmgCat1, dmgCat2 = ["Crush", "Pierce"], ["Dream", "Rot"]       
        case "Flame": dmgCat1, dmgCat2  = ["Flame"], ["Ice"]
        case "Holy": dmgCat1, dmgCat2 = ["Holy", "Rot"], []
        case "Ice": dmgCat1, dmgCat2 = ["Ice"], ["Flame"]
        case "Rot": dmgCat1, dmgCat2 = ["Rot", "Toxic"], ["Holy"]

    for dmgType in dmgCat1: Damage.modifyResistance(fighter, dmgType, potency, "positive")
    for dmgType in dmgCat2: Damage.modifyResistance(fighter, dmgType, potency, "negative")

    if element not in ["Holy", "Rot"]:
        if potency == 2: fighter.atrb["cur_res"]["Holy"] = "normal"
        else: fighter.atrb["cur_res"]["Holy"] = "resistant"

    fighter.itemEffects["Imbue"]["potency"] = potency
    fighter.itemEffects["Imbue"]["duration"] = 3
    fighter.itemEffects["Imbue"]["additional"] = element

    atmosphere = Apply.getAtmosphere(1, dmgType)
    battleMap[fighter.position[0]][fighter.position[1]] = atmosphere + battleMap[fighter.position[0]][fighter.position[1]][1:]


def invigorate(fighter, category, battleMap) -> None:
    potency = 0

    match category:
        case "pearls": potency = 1
        case "cores": potency = 2

    if not fighter.cndt["lifeless"]:
        fighter.itemEffects["Invigorate"]["duration"] = 3
        fighter.itemEffects["Invigorate"]["potency"] = min(fighter.itemEffects["Invigorate"]["potency"] + potency, 4)

    battleMap[fighter.position[0]][fighter.position[1]] = "=" + battleMap[fighter.position[0]][fighter.position[1]][1:]


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

