from . import PlayerSelect as Select


def removeEffect(fighter, effect):
    Select.waitPrint("Effect " + fighter.effects[effect]["ability"] + " ends on " + fighter.props["name"] + ".\n")
    fighter.effects[effect] = {"dice": 0, "source": None, "ability": None, "additional": None}


def updateItemEffects(fighter):
    for effect in fighter.itemEffects:
        duration = fighter.itemEffects[effect]["duration"]

        if duration == 0:
            if fighter.itemEffects[effect]["potency"] != 0: removeItemEffect(fighter, effect)
        else: fighter.itemEffects[effect]["duration"] -= 1


def removeItemEffect(fighter, effect) -> None:
    Select.waitPrint(effect + " ends on " + fighter.props["name"] + ".")

    match effect:
        case "Imbue": removeImbue(fighter)

    fighter.itemEffects.update({"duration": 0, "potency": 0, "additional": None})


def removeImbue(fighter) -> None:
    for element in fighter.atrb["cur_res"]:
        fighter.atrb["cur_res"][element] = fighter.atrb["nat_res"][element]
    
    fighter.atrb["cur_elm"] = fighter.atrb["base_elm"]