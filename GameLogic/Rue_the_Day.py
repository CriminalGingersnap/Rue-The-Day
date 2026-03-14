# Design rule #1: One mystery per action

from Characters import Humans
from Loop import Encounters
# from Maps import World

# worldMap = World.metamorphosisMap()
# World.printWorldMap(worldMap)
# input("L")

Martin = Humans.knight("Master").ch
Martin.rank, Martin.name, Martin.initials = "player", "Martin", "M."
# Martin.abl["items"] += ["Loot", "Transfer"]
# Martin.equipment["armor"] = None

# while True: Games.tracking(Martin, environment)
# biome = "Wild"

Laura = Humans.mage("Master", "Flame").ch
Laura.rank, Laura.name, Laura.initials = "player", "Laura", "L."
# Laura.abl["items"] += ["Craft", "Transfer"]
# Laura.equipment["armor"] = None

group1 = [Martin, Laura]
# beetles = LowPass.randomAvoidantForestBeasts() #[Avoidant.beetleWild().ch]
# enemyGroup = beetles

Encounters.encounterLoop(group1, "Wild")