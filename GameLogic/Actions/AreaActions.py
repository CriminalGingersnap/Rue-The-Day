from . import AttackActions as Attacks, BoonActions as Boons
from Abilities import Area_Set as Areas
from Systems import PlayerSelect as Select
import random


def pcSelectArea(fighter):
    areaOptions = usableAreas(fighter)
    answer = Select.pickOption(areaOptions, "area ability", False).split(" -> ")[0]
    return answer


def npcSelectArea(fighter, allies, enemies):
    areaOptions = []
    useful, usable = usefulAreas(fighter, allies, enemies), usableAreas(fighter)

    for option in useful:
        if (option in usable) and (option not in areaOptions): areaOptions += [option]

    if areaOptions != []: return random.choice(areaOptions)
    else: return "None"


def usableAreas(fighter):
    affordableAreas = []
    if (fighter.atrb["cur_mag"] > 0) and Attacks.weaponAllows(fighter, "Bring"):
        affordableAreas += fighter.abl["areas"]

    return affordableAreas


def usefulAreas(fighter, allies, enemies):
    areaPreferences = []
    enemiesDist, alliesDist = Boons.getDmgAndDistance(fighter, enemies), Boons.getDmgAndDistance(fighter, allies)
    alliesFar, alliesClose = alliesDist[1], alliesDist[2]
    enemiesFar, enemiesClose = enemiesDist[1], enemiesDist[2]
    
    rotEnemies = False
    for enemy in enemies:
        if enemy.atrb["cur_elm"] == "Rot": rotEnemies = True
    if rotEnemies and enemiesClose: areaPreferences += ["Bless"]

    unconcerned = not (fighter.cndt["social"] or fighter.cndt["sapient"])
    if unconcerned or not alliesClose:
        if enemiesClose: areaPreferences += ["Breath", "Infuse"]
        if enemiesFar: areaPreferences += ["Screen"]

    if fighter.cndt["skittish"] and enemiesClose: areaPreferences += ["Slip"]
    elif enemiesFar and not fighter.cndt["skittish"]: areaPreferences += ["Slip"]

    return areaPreferences