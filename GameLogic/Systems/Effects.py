from . import PlayerSelect as Select


def removeEffect(fighter, effect):
    if effect not in ["Drain", "Fortify", "Heal", "Rally"]:
        Select.quickPrint("Effect " + fighter.effects[effect]["ability"] + " ends on " + fighter.props["name"] + ".")
    fighter.effects[effect] = {"dice": 0, "source": None, "ability": None, "additional": None}


def updateItemEffects(fighter):
    for effect in fighter.itemEffects:
        duration = fighter.itemEffects[effect]["duration"]

        if duration == 0:
            if fighter.itemEffects[effect]["potency"] != 0: removeItemEffect(fighter, effect)
        else: fighter.itemEffects[effect]["duration"] -= 1


def removeItemEffect(fighter, effect) -> None:
    Select.quickPrint(effect + " ends on " + fighter.props["name"] + ".")

    match effect:
        case "Imbue": removeImbue(fighter)

    fighter.itemEffects.update({"duration": 0, "potency": 0, "additional": None})


def removeImbue(fighter) -> None:
    for element in fighter.atrb["cur_res"]:
        fighter.atrb["cur_res"][element] = fighter.atrb["nat_res"][element]
    
    fighter.atrb["cur_elm"] = fighter.atrb["base_elm"]