import Systems.PlayerSelect as Select


magBoons = ["Focus", "Shroud", "Wreath"]
magHindrances = ["Disorient", "Misdirect", "Seal"]
marBoons = ["Guard"]
marHindrances = ["Harry"]


def checkSource(fighter, other, ability):
    newOption = False

    if ability in other.effects:
        source = other.effects[ability]["source"]

        if (source != fighter) and other.effects[ability]["dice"] > 0:
            if (abs(fighter.position[0] - source.position[0]) <= 1) and (abs(fighter.position[1] - source.position[1]) <= 1):
                newOption = True

    return newOption


def checkOptions(fighter, allies, enemies):
    donationOptions = []

    if fighter.type != "human": return []
    
    for ally in allies:
        if ally != fighter:
            if fighter.atrb["cur_mag"] > 0:
                for ability in magBoons:
                    if checkSource(fighter, ally, ability):
                        donationOptions += [[ally, ability]]

            if fighter.atrb["cur_mar"] > 0:
                for ability in marBoons:
                    if checkSource(fighter, ally, ability):
                        donationOptions += [[ally, ability]]
                    
    for enemy in enemies:
        if fighter.atrb["cur_mag"] > 0:
            for ability in magHindrances:
                if checkSource(fighter, enemy, ability):
                    donationOptions += [[enemy, ability]]

        if fighter.atrb["cur_mar"] > 0:
            for ability in marHindrances:
                if checkSource(fighter, enemy, ability):
                    donationOptions += [[enemy, ability]]

    return donationOptions


def chooseDonation(fighter, options):
    choices = []
    for option in options:
        choices += [options[1] + " " + options[0].name]

    Select.makeSelection(choices)

def donate(fighter, target, ability):
    dice = 0

    if ability in magBoons + magHindrances:
        dice = fighter.atrb["cur_mag"]
    elif ability in marBoons + marHindrances:
        dice = fighter.atrb["cur_mar"]
        
    target.effects[ability]["dice"] += dice