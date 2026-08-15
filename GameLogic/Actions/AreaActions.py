from . import AttackActions as Attacks, BoonActions as Boons
from Abilities import Area_Set as Areas
from Systems import PlayerSelect as Select
import random


def pcSelectArea(fighter):
    areaOptions = usableAreas(fighter)
    answer = Select.pickOption(areaOptions, "area ability", False).split(" -> ")[0]
    return answer


def npcSelectArea(fighter, enemies):
    areaOptions = []
    useful, usable = usefulAreas(fighter, enemies), usableAreas(fighter)

    for option in useful:
        if (option in usable) and (option not in areaOptions): areaOptions += [option]

    if areaOptions != []: return random.choice(areaOptions)
    else: return "None"


def usableAreas(fighter):
    affordableAreas = []
    if (fighter.atrb["cur_mag"] > 0) and Attacks.weaponAllows(fighter, "Bring"):
        affordableAreas += Areas.areaAbilities

    return affordableAreas


def usefulAreas(fighter, enemies):
    areaPreferences = ["Screen"]
    dmgDist = Boons.getDmgAndDistance(fighter, enemies)
    someFar, anyClose = dmgDist[1], dmgDist[2]
    
    rotEnemies = False
    for enemy in enemies:
        if enemy.atrb["cur_elm"] == "Rot": rotEnemies = True
    if rotEnemies: areaPreferences += ["Bless"]

    if anyClose:
        areaPreferences += ["Breath"]
        if fighter.cndt["skittish"]: areaPreferences += ["Slip"]
    if someFar:
        areaPreferences += ["Shroud"]
        if not fighter.cndt["skittish"]: areaPreferences += ["Slip"]

    return areaPreferences