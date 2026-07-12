from . import Boons_Apply as Boons, Reactions
from Systems import PlayerSelect as Select, Roll, Conditions, Damage


def attack(fighter, target, attack, dice) -> None:
    dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], attack)

    absorption = Boons.applyWreath(target, dmgType)
    baseDmg = Roll.roll(fighter, dice, attack, "magic")
    appliedDmg = max(0, baseDmg - absorption)

    Select.waitPrint(fighter.props["name"] + " inflicts " + str(appliedDmg) + " " + dmgType + " damage!")
    Conditions.takeDamage(target, dmgType, appliedDmg)

    if absorption > baseDmg: Reactions.applyRiposte(target, fighter, "Wreath")