from Characters import Bosses, Humans, Elementals, Totems, AggressiveBeasts as Beasts, Birds
from Maps import Map_Instantiate as iMap
from . import PCs as B_PCs


def placeFighter(fighter, initials, position) -> None:
    fighter.props["name"], fighter.props["initials"] = fighter.props["name"] + "[" + initials + "]", initials
    fighter.pos = position + [0]


def shipMap(players) -> list:
    row1  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row2  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row3  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","#~~~⇓","#~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row4  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","#~~~⇓","f~~~⇓","#~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row5  = ["-~~~⇓","-___↑","-_F.↑","-___↑","-___↑","-___↑","#___↑","#___↑","#~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row6  = ["-___↑","-___↑","-___↑","////⇑","-_L.↑","////⇑","-_32↑","-___↑","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row7  = ["-~~~⇓","-___↑","-_33↑","-_31↑","-_H.↑","#_15↑","#_16↑","#___↑","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row8  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","#___↑","f~~~⇓","#~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row9  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","#___↑","#~~~⇓","#~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row10 = ["-~~~⇓","-~~~⇓","-~~~⇓","-___↑","-___↑","-_17↑","-_12↑","-___↑","-___↑","-~~~⇓","-~~~⇓","-~~~⇓"]
    row11 = ["-~~~⇓","-~~~⇓","-~~~⇓","-_11↑","-_13↑","-_14↑","////⇑","-___↑","-___↑","-~~~⇓","&~01⇓","-~~~⇓"]
    row12 = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos, players[2].pos = [4, 2, 0], [6, 4, 0], [5, 4, 0]

    Leviathan = Bosses.leviathan().ch
    placeFighter(Leviathan, "01", [10, 10])

    Sailor1, Sailor2, Sailor3 = Humans.knight("Basic", "Proficient").ch, Humans.brute("Basic", "Proficient").ch, Humans.archer("Basic", "Novice").ch 
    Sailor1.props["name"], Sailor2.props["name"], Sailor3.props["name"] = "Sailor", "Sailor", "Sailor"
    placeFighter(Sailor1, "31", [6, 3])
    placeFighter(Sailor2, "32", [5, 6])
    placeFighter(Sailor3, "33", [6, 2])

    Pirate1, Pirate2, Pirate3 = Humans.archer("Basic", "Proficient").ch, Humans.archer("Basic", "Novice").ch, Humans.archer("Basic", "Novice").ch    
    Pirate1.props["name"], Pirate2.props["name"], Pirate3.props["name"] = "Pirate", "Pirate", "Pirate"
    placeFighter(Pirate1, "11", [10, 3])
    placeFighter(Pirate2, "12", [9, 6])
    placeFighter(Pirate3, "13", [10, 4])

    Pirate4, Pirate5, Pirate6, Pirate7 = Humans.brute("Basic", "Proficient").ch, Humans.brute("Basic", "Novice").ch, Humans.brute("Basic", "Novice").ch, Humans.brute("Basic", "Novice").ch    
    Pirate4.props["name"], Pirate5.props["name"], Pirate6.props["name"], Pirate7.props["name"] = "Pirate", "Pirate", "Pirate", "Pirate"
    placeFighter(Pirate4, "14", [10, 5])
    placeFighter(Pirate5, "15", [6, 5])
    placeFighter(Pirate6, "16", [6, 6])
    placeFighter(Pirate7, "17", [9, 5])

    players += [Sailor1, Sailor2, Sailor3]
    group1 = [Leviathan]
    group2 = [Pirate1, Pirate2, Pirate3, Pirate4, Pirate5, Pirate6, Pirate7]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {"-": 5}]


def villageMap(players) -> list:
    row1  = ["////|","////|","__14|","////|","____|","__05|","____|","////|","__08|","____|","____|","____|"]
    row2  = ["____|","////|","____|","////|","____|","____|","__07|","////|","____|","__15|","____|","____|"]
    row3  = ["____|","____|","____|","////|","____|","__06|","////|","////|","////|","////|","____|","____|"]
    row4  = ["__01|","////|","____|","////|","____|","////|","////|","____|","____|","////|","____|","////|"]
    row5  = ["____|","////|","____|","____|","}___|","____|","____|","____|","____|","____|","____|","____|"]
    row6  = ["__02|","////|","____|","__11|","____|","____|","____|","____|","____|","____|","____|","__A.|"]
    row7  = ["////|","////|","____|","____|","____|","____|","____|","____|","____|","////|","____|","////|"]
    row8  = ["____|","__L.|","____|","____|","____|","____|","__13|","____|","////|","////|","____|","////|"]
    row9  = ["__F.|","__H.|","____|","____|","____|","____|","____|","____|","////|","____|","____|","____|"]
    row10 = ["////|","////|","____|","////|","____|","////|","____|","____|","////|","__09|","____|","____|"]
    row11 = ["____|","____|","____|","////|","____|","////|","////|","__12|","////|","____|","____|","____|"]
    row12 = ["__03|","____|","____|","////|","__04|","____|","////|","____|","////|","____|","____|","____|"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    Akeem = B_PCs.getAkeem()
    players += [Akeem]
    players[0].pos, players[1].pos, players[2].pos, players[3].pos = [8, 0, 0], [8, 1, 0], [7, 1, 0], [5, 11, 0]
    
    Zombie1, Zombie2, Zombie3 = Humans.brute("Rot", "Novice").ch, Humans.brute("Rot", "Novice").ch, Humans.knight("Rot", "Novice").ch
    Zombie4, Zombie5, Zombie6 = Humans.brute("Rot", "Novice").ch, Humans.brute("Rot", "Novice").ch, Humans.knight("Rot", "Novice").ch
    Zombie7, Zombie8, Zombie9 = Humans.archer("Rot", "Novice").ch, Humans.mage("Rot", "Novice").ch, Humans.knight("Rot", "Novice").ch
    placeFighter(Zombie1, "01", [3, 0])
    placeFighter(Zombie2, "02", [5, 0])
    placeFighter(Zombie3, "03", [11, 0])
    placeFighter(Zombie4, "04", [11, 4])
    placeFighter(Zombie5, "05", [0, 5])
    placeFighter(Zombie6, "06", [2, 5])
    placeFighter(Zombie7, "07", [1, 6])
    placeFighter(Zombie8, "08", [0, 8])
    placeFighter(Zombie9, "09", [9, 9])

    Crow1, Crow2, Vulture = Birds.crow("Basic", "Juvenile").ch, Birds.crow("Basic", "Adult").ch, Birds.vulture("Basic", "Adult").ch
    Dog1, Dog2 = Beasts.hound("Basic", "Juvenile").ch, Beasts.hound("Basic", "Adult").ch
    placeFighter(Crow1, "11", [5, 3])
    placeFighter(Crow2, "12", [10, 7])
    placeFighter(Vulture, "13", [7, 6])
    placeFighter(Dog1, "14", [0, 2])
    placeFighter(Dog2, "15", [1, 9])
    
    group1 = [Zombie1, Zombie2, Zombie3, Zombie4, Zombie5, Zombie6, Zombie7, Zombie8, Zombie9]
    group2 = [Crow1, Crow2, Vulture, Dog1, Dog2]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {"}": 1}]


def templeMap(players) -> list:
    row1  = ["____|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|"]
    row2  = ["____|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|"]
    row3  = ["____|","#___|","#___|","#___|","____|","////|","#___↑","////|","#___|","////|","____|","____|"]
    row4  = ["____|","#___|","////|","#___|","____|","____|","#___|","f___|","#___|","////|","____|","////|"]
    row5  = ["____|","____|","____|","____|","____|","____|","#___|","#___|","#___|","////|","____|","____|"]
    row6  = ["____|","__A.|","////|","____|","____|","__01|","____|","____↑","____↑","////|","____|","////|"]
    row7  = ["__H.|","____|","____|","____|","__03|","____|","____|","____↑","F_11↑","////|","____|","____|"]
    row8  = ["____|","__L.|","////|","____|","____|","__02|","____|","____↑","____↑","////|","____|","////|"]
    row9  = ["__F.|","____|","____|","____|","____|","____|","____|","____|","____|","////|","____|","____|"]
    row10 = ["____|","____|","////|","____|","____|","____|","____|","__04|","#___|","////|","#___|","////|"]
    row11 = ["____|","____|","____|","____|","____|","////|","____↑","////|","#___|","#___|","#___|","____|"]
    row12 = ["____|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos, players[2].pos, players[3].pos = [8, 0, 0], [6, 0, 0], [7, 1, 0], [5, 1, 0]

    Paladin, Knight1, Knight2, Mage = Humans.paladin("Rot", "Adept").ch, Humans.knight("Rot", "Proficient").ch, Humans.knight("Rot", "Proficient").ch, Humans.mage("Rot", "Proficient").ch
    placeFighter(Paladin, "01", [5, 5])
    placeFighter(Knight1, "02", [7, 5])
    placeFighter(Knight2, "03", [6, 4])
    placeFighter(Mage, "04", [9, 7])

    Elemental = Elementals.ooze("Flame", "Lesser").ch
    placeFighter(Elemental, "11", [0, 5])
    
    group1 = [Paladin, Knight1, Knight2, Mage]
    group2 = [Elemental]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {"#": 2}]


def cryptMap(players, events) -> list:
    row1  = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","____↑","}_01↑","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row2  = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","____↑","____↑","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row3  = ["=)))⇓","=)))⇓","=)))⇓","__02↑","____↑","__04↑","__03↑","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row4  = ["=)))⇓","=)))⇓","=)))⇓","____|","____|","____|","____|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row5  = ["=)))⇓","=)))⇓","=)))⇓","____|","____|","____|","____|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row6  = ["=)))⇓","=)))⇓","}___|","____|","____|","}___|","____|","____|","=)))⇓","=)))⇓","-_12↓","-___↓"]
    row7  = ["-_14↓","-___↓","____|","____|","____|","____|","____|","____|","-___↓","-___↓","-___↓","-_11↓"]
    row8  = ["=)))⇓","=)))⇓","____|","____|","____|","____|","____|","____|","=)))⇓","=)))⇓","-_13↓","-___↓"]
    row9  = ["=)))⇓","=)))⇓","=)))⇓","____|","____|","____|","____|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row10 = ["=)))⇓","=)))⇓","=)))⇓","____|","____|","__L.|","}___|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row11 = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","-_A.↓","-_H.↓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row12 = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","-_F.↓","-___↓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos, players[2].pos, players[3].pos = [8, 4, 0], [11, 5, 0], [10, 5, 0], [11, 4, 0]

    Lich = Bosses.lich().ch
    Lich.atrb["injury"], Lich.cndt["planted"] = 1, True
    placeFighter(Lich, "01", [0, 5])

    if events["Ally"]["complete"]:
        Sphinx = Elementals.sphinx("Holy", "Greater").ch
        placeFighter(Sphinx, "31", [8, 4])
        battleMap[8][4] = "__31"
        players += [Sphinx]

    Zombie1, Zombie2, Zombie3 = Humans.archer("Rot", "Proficient").ch, Humans.archer("Rot", "Adept").ch, Humans.knight("Rot", "Elite").ch    
    placeFighter(Zombie1, "02", [2, 3])
    placeFighter(Zombie2, "03", [2, 5])
    placeFighter(Zombie3, "04", [2, 6])

    Elemental1, Elemental2, Elemental3, Elemental4 = Elementals.slime("Rot", "Lesser").ch, Elementals.wisp("Rot", "Greater").ch, Elementals.wisp("Rot", "Lesser").ch, Elementals.grotesquery("Rot", "Greater").ch
    placeFighter(Elemental1, "11", [6, 11])
    placeFighter(Elemental2, "12", [5, 10])
    placeFighter(Elemental3, "13", [7, 10])
    placeFighter(Elemental4, "14", [6, 0])

    group1 = [Lich, Zombie1, Zombie2, Zombie3]
    group2 = [Elemental1, Elemental2, Elemental3, Elemental4]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {"}": 3}]


def manorMap(players) -> list:
    row1  = ["////|","////|","////|","////|","////|","////|","____|","__06↓","-___↓","////|","////|","////|"]
    row2  = ["////|","////|","////|","////|","////|","////|","____|","////|","-___↓",";_01↓","////|","////|"]
    row3  = ["////|","////|","____|","____|","////|","____]","____|","////|","-___↓","-___↓","////|","////|"]
    row4  = ["////|","////|","____|","__11|","__03|","____]","____|","__05↓","-___↓","-___↓","////|","////|"]
    row5  = ["////|","////|","__15|","____|","////|","____]","____|","////|","-___↓","-___↓","%___⇓","%_19⇓"]
    row6  = ["////|","////|","____|","____|","////|","__16|","____|","////|","////|","////|","%___⇓","%___⇓"]
    row7  = ["-_A.|","-_02|","____|","____|","////|","////|","////|","////|","////|","////|","%___⇓","%___⇓"]
    row8  = ["-_H.|","////|","____|","____|","////|","////|","////|","////|","-_17↓","-___↓","%___⇓","%_18⇓"]
    row9  = ["-_F.|","////|","____|","__12|","____|","__13|","____|","////|","-___↓","-___↓","%___⇓","%___⇓"]
    row10 = ["-_L.|","////|","____|","____|","____|","____|","__14|","////|","-___↓","-___↓","////|","////|"]
    row11 = ["-___|","////|","////|","////|","____|","____|","____|","__04|","-___↓","-___↓","////|","////|"]
    row12 = ["-___|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos, players[2].pos, players[3].pos = [8, 0, 0], [7, 0, 0], [9, 0, 0], [6, 0, 0]

    Vampire = Bosses.vampire().ch
    placeFighter(Vampire, "01", [])
    Vampire.cndt["reposed"] = True

    Door1, Door2, Door3, Door4, Door5 = Totems.impedance("Dream", "Gate").ch, Totems.ward("Flame", "Door").ch, Totems.ward("Ice", "Door").ch, Totems.sentry("Rot", "Door").ch, Totems.sentry("Dream", "Door").ch
    placeFighter(Door1, "02", [])
    placeFighter(Door2, "03", [])
    placeFighter(Door3, "04", [])
    placeFighter(Door4, "05", [])
    placeFighter(Door5, "06", [])
    Door1.cndt["reposed"], Door2.cndt["reposed"], Door3.cndt["reposed"] = True, True, True

    Ghoul1, Ghoul2, Ghoul3, Ghoul4, Ghoul5 = Humans.brute("Rot", "Adept").ch, Humans.brute("Rot", "Proficient").ch, Humans.mage("Rot", "Adept").ch, Humans.knight("Rot", "Elite").ch, Humans.knight("Rot", "Novice").ch    
    placeFighter(Ghoul1, "11", [2, 3])
    placeFighter(Ghoul2, "12", [2, 5])
    placeFighter(Ghoul3, "13", [2, 6])
    placeFighter(Ghoul4, "14", [2, 6])
    placeFighter(Ghoul5, "15", [2, 6])
    Ghoul1.cndt["reposed"], Ghoul2.cndt["reposed"], Ghoul3.cndt["reposed"], Ghoul4.cndt["reposed"], Ghoul5.cndt["reposed"] = True, True, True, True, True

    Ghoul6, Ghoul7, Ghoul8, Ghoul9 = Humans.archer("Rot", "Adept").ch, Humans.mage("Rot", "Novice").ch, Humans.knight("Rot", "Master").ch, Humans.knight("Rot", "Novice").ch    
    placeFighter(Ghoul6, "16", [2, 5])
    placeFighter(Ghoul7, "17", [2, 6])
    placeFighter(Ghoul8, "18", [2, 6])
    placeFighter(Ghoul9, "19", [2, 6])
    Ghoul6.cndt["reposed"], Ghoul7.cndt["reposed"], Ghoul8.cndt["reposed"], Ghoul9.cndt["reposed"] = True, True, True, True

    group1 = [Vampire, Door1, Door2, Door3, Door4, Door5]
    group2 = [Ghoul1, Ghoul2, Ghoul3, Ghoul4, Ghoul5, Ghoul6, Ghoul7, Ghoul8, Ghoul9]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {";": 2, "%": 2}]