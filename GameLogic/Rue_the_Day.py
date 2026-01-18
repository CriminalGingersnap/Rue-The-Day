# Design rule #1: One mystery per action

from Characters import Humans, AvoidantBeasts as Avoidant
from Systems import PlayerSelect as Select, Combat
import Campaigns.Metamorphosis.Encounters.Wild1_ValleyPass as LowPass
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
import random


Martin = Humans.knight("Elite").ch
Martin.rank, Martin.name, Martin.initials = "player", "Martin", "M."
# Martin.abl["items"] += ["Loot", "Transfer"]
# Martin.equipment["armor"] = None

# while True: Games.tracking(Martin, environment)

# biome = "Wild"
# Games.chooseEnvironment(environment, biome)
# Games.chooseMiracle(fighter)
# Games.alchemy(Martin)
# input("Sto")

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

wall = random.randint(1, 8)
slope = random.choice(["right", "left", "lr", "up", "down", "ud"])
heartCard = random.choice(["Jack", "Queen", "King"])
environment = {"Clubs": "", "Diamonds": "", "Hearts": heartCard, "Spades": ""}

# slope = "flat"
Select.quickPrint("Slope: " + slope + ", Wall: " + str(wall) + ", Hearts: " + heartCard)

obstructions = {"wall": wall, "trap": 0, "pit": 0}
atmosphere = {"Fog": 0, "Mana": 0, "Mist": 0, "Rime": 0, "Smoke": 0}

# battleMap = dMap.createMap(group1["members"], enemyGroup["members"], [obstructions, atmosphere], "flat")
battleMap = iMap.createMap(group1["members"], enemyGroup["members"], [obstructions, atmosphere], environment, slope)

deserters = Combat.engage(enemyGroup, group1, battleMap)
for deserter in deserters: Select.quickPrint(deserter.name) # let players hunt them down