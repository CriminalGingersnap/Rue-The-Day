from Actions import MoveActions as Move, AbilityActions_Player as PlayerAbl, AbilityActions_NPC as NPCAbl
from Maps import Visibility, Map_Update as uMap, Map_Print as Print
from Systems import PlayerSelect as Select, Sort, Conditions, Effects, Commitments
from Abilities import Items_Use as Items, Boons_Apply as Boons, Hindrances_Apply as Hindrances


def getEquipLoad(equipment) -> int:
    if equipment["name"] == "None": return 0
    elif ("element" in equipment) and (equipment["element"] == "Dream"): return 0
    else:
        equipLoad = equipment["modifier"]
        if equipment["tier"] == "Masterwork": equipLoad /= 2
        return equipLoad

def getSpeedLoss(fighter) -> int:
        armorLoss = getEquipLoad(fighter.equip["armor"])
        shieldLoss = getEquipLoad(fighter.equip["shield"])
        spareLoss = getEquipLoad(fighter.inv["spares"]["shield"])
        weaponLoss = getEquipLoad(fighter.equip["weapon"])
        weaponSpareLoss = getEquipLoad(fighter.inv["spares"]["weapon"])
        
        speedLoss = (armorLoss + shieldLoss + spareLoss + weaponLoss + weaponSpareLoss)
        if (fighter.inv["standard"] != "None") and not fighter.inv["standard"].cndt["planted"]: speedLoss += 2

        return speedLoss
        

def resetFighter(fighter) -> None:
    fighter.attackQueue = []
    fighter.cndt["blitzing"] = False

    fighter.atrb["cur_sp"] = fighter.atrb["base_sp"] - fighter.atrb["fatigue"]
    fighter.atrb["cur_mag"], fighter.atrb["cur_mar"] = fighter.atrb["base_mag"], fighter.atrb["base_mar"]

    if fighter.atrb["cur_hp"] < fighter.atrb["base_hp"]: fighter.cndt["reposed"] = False

    if fighter.props["type"] == "human":
        speedLoss = getSpeedLoss(fighter) - 3
        if speedLoss > 0: fighter.atrb["cur_sp"] -= speedLoss

    match fighter.atrb["injury"]:
        case 1: fighter.atrb["cur_sp"] -= fighter.atrb["cur_sp"] // 4
        case 2: fighter.atrb["cur_sp"] -= fighter.atrb["cur_sp"] // 2
        case 3: fighter.atrb["cur_sp"] = fighter.atrb["cur_sp"] // 4
        case 4: fighter.atrb["cur_sp"] = min(fighter.atrb["base_sp"], 1)

    fighter.atrb["cur_sp"] = max(0, fighter.atrb["cur_sp"])

    Commitments.clearCommitments(fighter)
    Effects.updateItemEffects(fighter)


def setSight(fighter, enemies, allies, battleMap, print):
    playerRank = fighter.props["rank"] == "player"
    if playerRank and ("*" in battleMap[fighter.pos[0]][fighter.pos[1]]): fighter.cndt["insightful"] = True

    sightMap = Visibility.createSightMap(battleMap, fighter.pos, playerRank, fighter.cndt["insightful"])
    uMap.hideVeiled(fighter, enemies + allies, sightMap)

    if playerRank:
        uMap.revealOthers(fighter, allies, enemies, sightMap)
        uMap.hideTraps(fighter, sightMap)
        if print: Print.printSightMap(battleMap, sightMap, fighter.props["name"] + "'s Sight Map")

    return sightMap


def outro(fighter):
    Boons.applyHeal(fighter)
    Hindrances.applyDrain(fighter)
    Items.invigorate(fighter)
    alive = Sort.setAlive(fighter)

    if alive:
        Boons.applyFortify(fighter)
        Boons.applyRally(fighter)
        Boons.applyVeil(fighter)

        if fighter.props["rank"] != "Ascendant":
            fighter.cndt["insightful"] = False


def movementStage(fighter, enemies, allies, battleMap) -> None:
    if (fighter.atrb["cur_sp"] > 0) or ((fighter.atrb["base_mag"] > 1) or (fighter.atrb["base_mar"] > 1)):
        groups = Sort.getGroups(fighter, enemies, allies)
        Move.moveAction(fighter, groups, battleMap)


def abilityStage(fighter, enemies, allies, battleMap) -> None:
    groups = Sort.getGroups(fighter, enemies, allies)
    fightingEnemies = groups["fightingEnemies"]

    if fighter.cndt["reposed"]: Select.waitPrint(fighter.props["name"] + " waits in repose.")
    elif (len(fightingEnemies) > 0) and ((fighter.atrb["cur_mag"] > 0) or (fighter.atrb["cur_mar"] > 0)):
        if fighter.props["rank"] == "player": PlayerAbl.playerAction(fighter, groups, battleMap)
        else: NPCAbl.npcAction(fighter, groups, battleMap)

        if fighter.cndt["blitzing"] and ((fighter.atrb["cur_mag"] > 0) or (fighter.atrb["cur_mar"] > 0)):
            fighter.cndt["blitzing"] = False
            abilityStage(fighter, enemies, allies, battleMap)
    else:
        Select.waitPrint("No ability options.")