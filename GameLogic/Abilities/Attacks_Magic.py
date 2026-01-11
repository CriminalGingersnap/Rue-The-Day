from . import DamageTypes as Damage, Boons_Apply as Boons, Reactions
from Systems import PlayerSelect as Select, Roll, Conditions


def attack(fighter, target, attack, dice) -> None:
    dmgType = Damage.identifyDamageType(fighter, attack)["base"]

    absorption = Boons.applyWreath(target, fighter, dmgType)
    baseDmg = Roll.roll(fighter, dice, attack, "magic") + (dice * fighter.equipment["weapon"]["modifier"])
    appliedDmg = min(0, baseDmg - absorption)

    Select.waitPrint(fighter.name + " inflicts " + str(appliedDmg) + " " + dmgType + " damage!")
    Conditions.takeDamage(target, dmgType, appliedDmg, False)

    if absorption > baseDmg: Reactions.applyRiposte(target, fighter, "Wreath")