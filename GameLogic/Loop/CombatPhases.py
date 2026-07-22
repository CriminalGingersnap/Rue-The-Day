from Actions import MoveActions as Move, AbilityActions_Player as PlayerAbl, AbilityActions_NPC as NPCAbl
from Maps import Visibility, Map_Update as uMap, Map_Print as Print
from Systems import PlayerSelect as Select, Sort, Conditions, Effects, Commitments
from Abilities import Reactions, Items_Use as Items


def resetFighter(fighter) -> None:
    fighter.atrb["cur_sp"] = fighter.atrb["base_sp"] - fighter.atrb["fatigue"]
    fighter.atrb["cur_mag"], fighter.atrb["cur_mar"] = fighter.atrb["base_mag"], fighter.atrb["base_mar"]

    if fighter.props["type"] == "human":
        speedLoss = (fighter.equip["armor"]["modifier"] + fighter.equip["shield"]["modifier"] + fighter.equip["weapon"]["modifier"] 
                   + fighter.inv["spares"]["shield"]["modifier"] + fighter.inv["spares"]["weapon"]["modifier"]
                  ) - 2
        if speedLoss > 0: fighter.atrb["cur_sp"] -= speedLoss

        if fighter.itemEffects["Invigorate"]["duration"] > 0:
            fighter.atrb["cur_sp"] += fighter.itemEffects["Invigorate"]["potency"]

    match fighter.atrb["injury"]:
        case 1: fighter.atrb["cur_sp"] -= fighter.atrb["cur_sp"] // 4
        case 2: fighter.atrb["cur_sp"] -= fighter.atrb["cur_sp"] // 2
        case 3: fighter.atrb["cur_sp"] = min(fighter.atrb["base_sp"], 1)

    fighter.atrb["cur_sp"] = max(0, fighter.atrb["cur_sp"])

    Commitments.clearCommitments(fighter)
    Effects.updateItemEffects(fighter)


def setSight(fighter, enemies, allies, battleMap):
    sightMap = Visibility.createSightMap(battleMap, fighter.position, fighter.props["rank"])
    uMap.hideShrouded(fighter, enemies + allies, sightMap)

    if fighter.props["rank"] == "player":
        uMap.revealOthers(fighter, allies, enemies, sightMap)
        uMap.hideTraps(fighter, sightMap)
    else:
        Select.waitPrint("\n" + fighter.props["name"] + "'s turn")

    Print.printSightMap(battleMap, sightMap, fighter.props["name"] + "'s Sight Map")

    return sightMap


def outro(fighter, allyGroup, battleMap):
    Items.regenerate(fighter)
    alive = Sort.setAlive(fighter)

    if alive:
        intensity = max(0, (fighter.atrb["base_mag"] - fighter.atrb["cur_mag"]) + (fighter.atrb["base_mar"] - fighter.atrb["cur_mar"]))
        if fighter.cndt["running"]:
            fighter.cndt["running"] = False
            intensity += 1
        Conditions.decrementStamina(fighter, intensity)
        Reactions.applySocial(fighter, allyGroup)
    Reactions.applyReinforcements(fighter, allyGroup, battleMap)


def movementStage(fighter, enemies, allies, battleMap) -> None:
    if (fighter.atrb["cur_sp"] > 0) or ((fighter.atrb["base_mag"] > 1) or (fighter.atrb["base_mar"] > 1)):
        groups = Sort.getGroups(fighter, enemies, allies)
        Move.moveAction(fighter, groups, battleMap)

        if "echo" in fighter.inv:
            echo = fighter.inv["echo"]
            if (echo != "None") and (echo.itemEffects["Animate"]["duration"] == 3):
                allies += [echo]
                fighter.inv["echo"] = "None"


def abilityStage(fighter, enemies, allies) -> None:
    groups = Sort.getGroups(fighter, enemies, allies)
    reachable, fightingEnemies = groups["reachable"], groups["fightingEnemies"]

    if fighter.cndt["reposed"]: fighter.atrb["cur_mar"], fighter.atrb["cur_mag"] = 0, 0
    elif len(fightingEnemies) > 0:
        if fighter.props["rank"] == "player":
            actionChoice = PlayerAbl.chooseAction(fighter, reachable)
            PlayerAbl.takeAction(fighter, actionChoice, reachable)
        else: NPCAbl.npcAction(fighter, groups)