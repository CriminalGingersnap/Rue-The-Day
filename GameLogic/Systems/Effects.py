from . import PlayerSelect as Select


def removeEffect(fighter, effect):
    if effect not in ["Drain", "Fortify", "Heal", "Rally"]:
        Select.quickPrint("Effect " + fighter.effects[effect]["ability"] + " ends on " + fighter.props["name"] + ".")
    fighter.effects[effect] = {"dice": 0, "source": None, "ability": None, "additional": None}


def updateItemEffects(fighter):
    for effect in fighter.itemEffects:
        if fighter.itemEffects[effect]["duration"] > 0:
            fighter.itemEffects[effect]["duration"] -= 1

            if fighter.itemEffects[effect]["potency"] > 1:
                fighter.itemEffects[effect]["potency"] -= 1
                Select.clearPrint("Item effect: " + effect + " loses potency on " + fighter.props["name"] + ".")

        elif fighter.itemEffects[effect]["potency"] != 0: removeItemEffect(fighter, effect)


def removeItemEffect(fighter, effect) -> None:
    Select.clearPrint("Item effect: " + effect + " ends on " + fighter.props["name"] + ".")
    fighter.itemEffects["effect"] = {"duration": 0, "potency": 0, "additional": None}
    if effect == "Imbue": removeImbue(fighter)


def removeImbue(fighter) -> None:
    for element in fighter.atrb["cur_res"]:
        fighter.atrb["cur_res"][element] = fighter.atrb["nat_res"][element]
    
    fighter.atrb["cur_elm"] = fighter.atrb["base_elm"]