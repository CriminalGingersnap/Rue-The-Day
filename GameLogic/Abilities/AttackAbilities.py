from . import Attacks_Magic as Magic, Attacks_Martial as Martial
from Systems import PlayerSelect as Select


closeMartialAttack = ["Bash", "Bite", "Claw", "Gore", "Kick", "Ram", "Stab"]
midMartialAttack = ["Bodkin", "Spray"]
farMartialAttack = ["Broadhead", "Sling", "Sting"]
martialAttack = closeMartialAttack + midMartialAttack + farMartialAttack

magicAttack= ["Bring"]


def commitDice(attack, fighter, attackTarget):
    dice = 0
    attackComment(fighter, attackTarget, attack)

    if attack in martialAttack: dice = fighter.atrb["cur_mar"]
    elif attack in magicAttack: dice = fighter.atrb["cur_mag"]

    fighter.actionQueue += [["attack", attack, attackTarget, dice]]


def execute(fighter, target, attack, dice) -> dict:
    print()
    if attack in martialAttack: Martial.attack(fighter, target, attack, dice)
    elif attack in magicAttack: Magic.attack(fighter, target, attack, dice)


def attackComment(fighter, target, attack):
    phrase, end = fighter.name, target.name + "!"
        
    if attack in magicAttack:
        match attack:
            case "Burn": phrase += " burns " + end
            case "Dream": phrase += " spins dreams into the mind of " + end
            case "Freeze": phrase += " freezes " + end
            case "Rot": phrase += " rots " + end

    else:
        match attack:
            case "Bash": phrase += " bashes at " + end
            case "Bite": phrase += " bites at " + end
            case "Bodkin": phrase += " looses a bodkin arrow at " + end
            case "Broadhead": phrase += " looses a broadhead arrow at " + end
            case "Claw": phrase += " claws at " + end
            case "Gore": phrase += " tries to gore " + end
            case "Kick": phrase += " kicks at " + end
            case "Ram": phrase += " tries to ram " + end
            case "Sling": phrase += " slings a stone at " + end
            case "Stab": phrase += " stabs at " + end
            case "Spray": phrase += " sprays venom at " + end

    Select.waitPrint(phrase)
