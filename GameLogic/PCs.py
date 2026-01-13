# Design rule #1: One mystery per action

from Characters import Humans, AvoidantBeasts as Avoidant
from Systems import PlayerSelect as Select, Combat
import Campaigns.Metamorphosis.Encounters.Wild1_ValleyPass as LowPass
from Maps import Map_Instantiate as iMap, Map, Dungeon_Instantiate as dMap
import random


Martin = Humans.knight("Elite").ch
Martin.rank = "player"
# Evolutions.evolve(Martin, "FlameHeart")
Martin.name = "Martin"
Martin.initials = "M."
Martin.abl["items"] += ["Loot", "Transfer"]
# Martin.equipment["armor"] = None

environment = {"Clubs": "", "Diamonds": "", "Hearts": "Queen", "Spades": ""}
# while True: Games.tracking(Martin, environment)

# biome = "Wild"
# Games.chooseEnvironment(environment, biome)
# Games.chooseMiracle(fighter)
# Games.alchemy(Martin)
# input("Sto")


Laura = Humans.mage("Elite", "Flame").ch
Laura.rank = "player"
# Evolutions.evolve(Laura, "FeyHeart")
Laura.name = "Laura"
Laura.initials = "L."
Laura.abl["items"] += ["Craft", "Transfer"]
# Laura.equipment["armor"] = None



Archer = Humans.archer("Master").ch
Archer.initials = "A1"

group1 = {"members": [Martin, Laura], "name": "questors"}
# beetles = LowPass.randomAvoidantForestBeasts() #[Avoidant.beetleWild().ch]
# enemyGroup = {"members": beetles, "name": "beetles"}
enemyGroup = {"members": [Archer], "name": "assassins"}

obstructions = {"wall": 0, "trap": 0, "pit": 0}
atmosphere = {"Fog": 0, "Mana": 0, "Mist": 0, "Rime": 0, "Smoke": 0}
slope = random.choice(["right", "left", "lr", "up", "down", "ud"])
print("Slope: " + slope)
# battleMap = dMap.createMap(group1["members"], enemyGroup["members"], [obstructions, atmosphere], "flat")
battleMap = iMap.createMap(group1["members"], enemyGroup["members"], [obstructions, atmosphere], environment, slope)
# printMap = Map.printMap(battleMap, "Starting Map")

Map.printMap(battleMap, "Battle Map")

deserters = Combat.engage(group1, enemyGroup, battleMap)
for deserter in deserters: print(deserter.name) # let players hunt them down

# King = Humans.mage("master").ch
# Evolutions.evolve(King, "King")
# King.name = "King"
# Fadia = Humans.dreamMage("elite").ch
# Fadia.name = "Fadia"
# Archer = Humans.archer("elite").ch

# group3 = {"members": [King], "name": "enemyGroup"}
