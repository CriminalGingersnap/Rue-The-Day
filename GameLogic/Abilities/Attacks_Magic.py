from . import Boons_Apply as Boons
from Systems import PlayerSelect as Select, Roll, Conditions, Damage


def attack(fighter, target, attack, dice) -> None:
    dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], attack)

    baseDmg = Roll.roll(fighter, target, dice, attack, "magic")
    absorption = Boons.applyWreath(target, dmgType)
    appliedDmg = max(0, baseDmg - absorption)

    Select.waitPrint(fighter.props["name"] + " inflicts " + str(appliedDmg) + " " + dmgType + " damage against " + target.props["name"] + "!")
    Conditions.takeDamage(target, dmgType, appliedDmg)