from Systems import PlayerSelect as Select, Inventory
from . import CombatPhases as Phases


def lootStandards(players, standards):
    for player in players:
        carryWeight = player.atrb["base_sp"] - Phases.getSpeedLoss(player)

        if (carryWeight > 2) and Select.yesNo("Equip a new standard to " + player.props["name"] + "?"):
            standard = Select.targetSelect(standards)

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
        for player in players:
            playerEcho = []
            if player.inv["echo"] != "None": playerEcho = [player.inv["echo"]]

            if Select.yesNo("Bind an echo to " + player.props["name"] + "?"):
                echo = Select.targetSelect(recentDead + playerEcho)
                if echo != player.inv["echo"]:
                    Inventory.setLifeless(echo)
                    echo.cndt["reposed"] = False
                    echo.props["initials"] = player.props["name"][0] + "e"
                    echo.props["name"] = player.props["name"] + "'s Echo"
                    echo.props["rank"] = "player"
                    echo.props["type"] = "echo"

                    player.inv["echo"] = echo
                    creatures.remove(echo)
                    recentDead.remove(echo)