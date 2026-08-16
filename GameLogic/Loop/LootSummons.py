from Systems import PlayerSelect as Select, Inventory
from . import CombatPhases as Phases


def lootStandards(players, standards):
    Select.waitPrint("Broken standards can be repaired.")
    for player in players:
        carryWeight = player.atrb["base_sp"] - Phases.getSpeedLoss(player)

        if (carryWeight > 2) and Select.yesNo("Equip a new standard to " + player.props["name"] + "?"):
            standard = Select.targetSelect(standards)
            if standard != "None":
                standard.cndt["planted"], standard.cndt["reposed"] = False, False
                standard.props["initials"] = player.props["name"][0] + "s"
                standard.props["name"] = player.props["name"] + "'s Standard"
                standard.props["rank"] = "player"

                player.inv["standard"] = standard
                
                standards.remove(standard)


def lootEchos(players, creatures) -> None:
    recentDead = []
    for enemy in creatures:
        if not (enemy.cndt["lifeless"] or (enemy.props["type"] in ["insect", "invertebrate"])): recentDead += [enemy]

    if len(recentDead) > 0:
        Select.waitPrint("Echos of the slain linger within their fallen bodies.")
        for player in players:
            if len(recentDead) > 1: phrase = "Bind a new echo to " + player.props["name"] + "?"
            elif len(recentDead) == 1: phrase = "Bind the remaining echo to " + player.props["name"] + "?"
            else: break

            if Select.yesNo(phrase):
                echo = Select.targetSelect(recentDead)
                if echo != "None":
                    Inventory.setLifeless(echo)
                    echo.cndt["reposed"] = False
                    echo.props["initials"] = player.props["name"][0] + "e"
                    echo.props["name"] = player.props["name"] + "'s Echo"
                    echo.props["rank"] = "player"
                    echo.props["type"] = "echo"

                    player.inv["echo"] = echo
                    
                    creatures.remove(echo)
                    recentDead.remove(echo)