from Systems import Damage, PlayerSelect as Select, Conditions
from . import Area_Set as Set, Area_Locate as Locate, Area_Apply as Apply
from Maps import Map_Update as uMap
from Loop import CombatPhases as Phases


def execute(fighter, category, element, application, groups, battleMap) -> None:
    end = "a condensed " + element + " " + category.split("s")[0] + "!"

    match application:
        case "Animate":
            Select.waitPrint(fighter.props["name"] + " animates " + end)
            animate(fighter, groups, battleMap)
        case "Detonate":
            Select.waitPrint(fighter.props["name"] + " throws " + end)
            Set.throwStone(fighter, category, element, groups, battleMap)
        case "Extract":
            Select.waitPrint(fighter.props["name"] + " absorbs the essence of " + end)
            if element == "Bleed": updateEffect(fighter, "Invigorate", category, battleMap)
            elif element == "Dream": updateEffect(fighter, "Obscure", category, battleMap)
            else: imbue(fighter, category, element, battleMap)            
            match category:
                case "pearls": Conditions.decrementTolerance(fighter, 2)
                case "cores": Conditions.decrementTolerance(fighter, 4)
        case "Plant":
            Select.waitPrint(fighter.props["name"] + " plants a standard!")
            plant(fighter, groups, battleMap)


def animate(fighter, groups, battleMap) -> None:
    echo = fighter.inv["echo"]
    tossSpace = Locate.findSpace(fighter, groups, 4, "echo")
    
    if tossSpace == "None": Select.waitPrint(fighter.props["name"] + " cancels a throw before animation.")
    else:
        echo.itemEffects["Animate"]["duration"] = 3
        echo.sightMap + Phases.setSight(echo, groups["fightingEnemies"], groups["fightingAllies"], battleMap, False)
        uMap.updatePlacement(battleMap, echo.sightMap, tossSpace[0], tossSpace[1], echo)
        fighter.inv["echo"] = "None"


def plant(fighter, groups, battleMap) -> None:
    standard = fighter.inv["standard"]
    plantSpace = Locate.findSpace(fighter, groups, 1, "standard")

    if plantSpace == "None":  Select.waitPrint(fighter.props["name"] + " defers planting a standard.")
    else:
        standard.pos = plantSpace
        standard.cndt["planted"] = True

        standard.sightMap = Phases.setSight(standard, groups["fightingEnemies"], groups["fightingAllies"], battleMap, False)
        uMap.updatePlacement(battleMap, standard.sightMap, plantSpace[0], plantSpace[1], standard)


def imbue(fighter, category, element, battleMap) -> None:
    potency, dmgCat1, dmgCat2 = 0, "", ""

    match category:
        case "pearls": potency = 1
        case "cores": potency = 2

    if fighter.itemEffects["Imbue"]["additional"] == element:
        potency = min(fighter.itemEffects["Imbue"]["potency"] + potency, 3)

    match element:
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

    atmosphere = Apply.getAtmosphere(1, element)
    battleMap[fighter.pos[0]][fighter.pos[1]] = atmosphere + battleMap[fighter.pos[0]][fighter.pos[1]][1:]


def invigorate(fighter) -> None:
    healing, potency = 0, fighter.itemEffects["Invigorate"]["potency"]

    if healing > 0:
        match potency:
            case 1: healing = fighter.atrb["quart_hp"]
            case 2: healing = fighter.atrb["half_hp"]
            case 3: healing = fighter.atrb["half_hp"] + fighter.atrb["quart_hp"]
            case 4: healing = fighter.atrb["base_hp"]

        Select.waitPrint("Blood essence activates!")
        Conditions.recoverHP(fighter, healing)
        Conditions.recoverStamina(fighter, healing)


def updateEffect(fighter, effect, category, battleMap) -> None:
    potency = 0

    match category:
        case "pearls": potency = 1
        case "cores": potency = 2

    if not fighter.cndt["lifeless"]:
        fighter.itemEffects[effect]["duration"] = 3
        fighter.itemEffects[effect]["potency"] = min(fighter.itemEffects[effect]["potency"] + potency, 4)

    atmosphere = "="
    match effect:
        case "Invigorate": atmosphere = ";"
        case "Obscure": atmosphere = "@"
    battleMap[fighter.pos[0]][fighter.pos[1]] = atmosphere + battleMap[fighter.pos[0]][fighter.pos[1]][1:]
