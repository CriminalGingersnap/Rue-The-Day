# Design rule #1: One mystery per action

from Characters import Humans
from Loop import Encounters

Martin = Humans.knight("Elite").ch
Martin.rank, Martin.name, Martin.initials = "player", "Martin", "M."
# Martin.abl["items"] += ["Loot", "Transfer"]
# Martin.equipment["armor"] = None

# while True: Games.tracking(Martin, environment)
# biome = "Wild"

Laura = Humans.mage("Elite", "Flame").ch
Laura.rank, Laura.name, Laura.initials = "player", "Laura", "L."
# Laura.abl["items"] += ["Craft", "Transfer"]
# Laura.equipment["armor"] = None

Archer = Humans.archer("Master").ch
Archer.initials = "A1"

group1 = {"members": [Martin, Laura], "name": "questors"}
# beetles = LowPass.randomAvoidantForestBeasts() #[Avoidant.beetleWild().ch]
# enemyGroup = {"members": beetles, "name": "beetles"}
enemyGroup = {"members": [Archer], "name": "assassins"}

Encounters.encounterLoop(group1, enemyGroup)