from . import Attacks_Magic as Magic, Attacks_Martial as Martial
from Systems import PlayerSelect as Select, Conditions
import random


closeMartialAttack = ["Bash", "Bite", "Claw", "Gore", "Kick", "Peck", "Pinch", "Ram", "Stab", "Sting"]
midMartialAttack = ["Bodkin", "Spit", "Spray"]
farMartialAttack = ["Broadhead", "Sling"]
martialAttack = closeMartialAttack + midMartialAttack + farMartialAttack

magicAttack= ["Bring"]


def commitDice(attack, fighter, attackTarget):
    dice, diceCap, dType = 0, 0, ""
    attackComment(fighter, attackTarget, attack)

    if attack in martialAttack: dType = "cur_mar"
    elif attack in magicAttack: dType = "cur_mag"
    diceCap = fighter.atrb[dType]

    if fighter.cndt["blitzing"]:
        if (fighter.props["rank"] == "player"):
            Select.waitPrint("Commit dice(" + str(diceCap) + "):")
            dice = Select.takeInput(1, diceCap)
        else: dice = random.randint(1, diceCap)
    else: dice = diceCap

    fighter.attackQueue += [[attack, attackTarget, dice]]
    fighter.atrb[dType] -= dice


def execute(fighter, target, attack, dice) -> dict:
    print()
    if attack in martialAttack: Martial.attack(fighter, target, attack, dice)
    elif attack in magicAttack: Magic.attack(fighter, target, attack, dice)
    Conditions.setInjury(target)
    input("\nPress Enter.\n")


def attackComment(fighter, target, attack):
    phrase, end = fighter.props["name"], target.props["name"] + "!"
        
    if attack == "Bring":
        match fighter.atrb["cur_elm"]:
            case "Rot": phrase += " rots " + end
            case "Flame": phrase += " burns " + end
            case "Dream": phrase += " spins dreams into the mind of " + end
            case "Holy": phrase += " calls holy wrath upon " + end
            case "Ice": phrase += " freezes " + end

    else:
        match attack:
            case "Bash": phrase += " bashes at " + end
            case "Bite": phrase += " bites at " + end
            case "Bodkin": phrase += " looses a bodkin arrow at " + end
            case "Broadhead": phrase += " looses a broadhead arrow at " + end
            case "Claw": phrase += " claws at " + end
            case "Gore": phrase += " tries to gore " + end
            case "Kick": phrase += " kicks at " + end
            case "Peck": phrase += " pecks at " + end
            case "Pinch": phrase += " pinches at " + end
            case "Ram": phrase += " tries to ram " + end
            case "Sling": phrase += " slings a stone at " + end
            case "Spray": phrase += " sprays venom at " + end
            case "Spit": phrase += " spits at " + end
            case "Stab": phrase += " stabs at " + end
            case "Sting": phrase += " stings at " + end

    Select.waitPrint(phrase)
