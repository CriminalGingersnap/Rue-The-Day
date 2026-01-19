from Maps import Movement


def execute(fighter, target, action) -> dict:
    match action:
        case "Loot": loot(fighter, target)
        case "Transfer": transfer(fighter, target)


def loot(fighter, target):
    # If fighter is standing next to slain target, and fighter has max mag and max mar, fighter plunders target inventory
    return


def transfer(fighter, target):
    distance = Movement.getTargetDistance(fighter, target)

    if distance == 1:
        if "Transfer" in fighter.abl["items"]:
            return
    # Characters pass items/components
    return