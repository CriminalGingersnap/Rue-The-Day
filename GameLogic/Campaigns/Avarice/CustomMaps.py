from Characters import Bosses, AggressiveBeasts as Beasts, Birds, Reptiles, Humans, Elementals, Insects, Totems
from Campaigns.Benediction import CustomMaps as B_Maps
from Campaigns.Avarice import PCs as A_Pcs
from Abilities import Area_Apply as Area
from Maps import Map_Instantiate as iMap

def archerMap(players) -> list:
    row1  = ["____↑","____↑","=___↓","____↑","////⇑","____↑","////⇑","____↑","=___↓","____↑","____↑","=___↓"]
    row2  = ["____↑","=___↓","____↑","=___↓","____↑","=_11↓","____↑","=___↓","____↑","=___↓","=___↓","____↑"]
    row3  = ["////⇑","____↑","////⇑","____↑","=___↓","____↑","____↑","____↑","____↑","____↑","____↑","=___↓"]
    row4  = ["____↑","=___↓","____↑","////⇑","____↑","=___↓","____↑","____↑","////⇑","____↑","=___↓","____↑"]
    row5  = ["=___↓","____↑","////⇑","_***↑","____↑","____↑","=___↓","____↑","____↑","////⇑","____↑","=___↓"]
    row6  = ["____↑","=___↓","____↑","=___↓","=___↓","____↑","____↑","=___↓","=___↓","__01↑","=___↓","____↑"]
    row7  = ["=_L.↓","____↑","=___↓","____↑","____↑","=___↓","____↑","____↑","____↑","=___↓","__04↑","////⇑"]
    row8  = ["__M.↑","=___↓","____↑","____↑","____↑","____↑","____↑","____↑","____↑","____↑","=___↓","____↑"]
    row9  = ["=___↓","____↑","____↑","////⇑","____↑","____↑","____↑","////⇑","=_02↓","____↑","____↑","=___↓"]
    row10 = ["____↑","____↑","////⇑","____↑","=___↓","=___↓","=___↓","____↑","____↑","=___↓","____↑","____↑"]
    row11 = ["=___↓","=___↓","____↑","=___↓","____↑","____↑","____↑","=_03↓","____↑","____↑","=___↓","____↑"]
    row12 = ["____↑","____↑","=___↓","____↑","=___↓","=___↓","____↑","____↑","////⇑","____↑","____↑","=___↓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos = [6, 0, 0], [7, 0, 0]

    Archer = Humans.archer("Basic", "Master").ch
    Hound1, Hound2 = Beasts.hound("Basic", "Adult").ch, Beasts.hound("Basic", "Adult").ch
    Standard = Totems.ward("Ice", "Standard").ch

    Archer.atrb["fatigue"], Archer.atrb["injury"] = 1, 0
    Hound1.atrb["fatigue"], Hound1.atrb["injury"] = 1, 0
    Hound2.atrb["fatigue"], Hound2.atrb["injury"] = 1, 0
    Standard.cndt["reposed"] = False

    B_Maps.placeFighter(Archer, "01", [5, 9])
    B_Maps.placeFighter(Hound1, "02", [8, 8])
    B_Maps.placeFighter(Hound2, "03", [10, 7])
    B_Maps.placeFighter(Standard, "04", [6, 10])

    Wyrm = Reptiles.wyrm("Flame", "Juvenile").ch
    B_Maps.placeFighter(Wyrm, "11", [1, 5])

    group1 = [Archer, Hound1, Hound2, Standard]
    group2 = [Wyrm]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {}]


def glacierMap(players) -> list:
    row1  = ["////⇑","////⇑","%___⇓","////⇑","////⇑","////⇑","////⇑","////⇑","%___⇓","////⇑","%___⇓","%___⇓"]
    row2  = ["////⇑","%___⇓","////⇑","%___⇓","////⇑","%___⇓","////⇑","%___⇓","////⇑","%___⇓","%_01⇓","%___⇓"]
    row3  = ["%_18⇓","////⇑","////⇑","////⇑","%_14⇓","////⇑","////⇑","%_12⇓","////⇑","////⇑","////⇑","%___⇓"]
    row4  = ["////⇑","%___⇓","////⇑","////⇑","////⇑","%___⇓","%___⇓","////⇑","////⇑","////⇑","%___⇓","////⇑"]
    row5  = ["%___⇓","////⇑","////⇑","////⇑","////⇑","////⇑","%___⇓","%___⇓","////⇑","////⇑","////⇑","%___⇓"]
    row6  = ["////⇑","%___⇓","////⇑","%___⇓","%_15⇓","////⇑","////⇑","%___⇓","%___⇓","////⇑","%_11⇓","////⇑"]
    row7  = ["////⇑","////⇑","%___⇓","////⇑","////⇑","%___⇓","////⇑","%_13⇓","////⇑","%___⇓","////⇑","////⇑"]
    row8  = ["////⇑","%___⇓","////⇑","////⇑","////⇑","%___⇓","////⇑","////⇑","////⇑","%___⇓","%___⇓","////⇑"]
    row9  = ["%___⇓","////⇑","////⇑","////⇑","////⇑","////⇑","////⇑","%___↑","%___⇓","////⇑","////⇑","%___⇓"]
    row10 = ["%___⇓","////⇑","////⇑","////⇑","%___⇓","%___⇓","%_16⇓","////⇑","////⇑","%___⇓","////⇑","%___⇓"]
    row11 = ["%_M.⇓","%_L.⇓","////⇑","%_19⇓","////⇑","////⇑","////⇑","%___⇓","////⇑","%___⇓","%_17⇓","////⇑"]
    row12 = ["////⇑","////⇑","%___⇓","////⇑","%___⇓","%___⇓","////⇑","////⇑","////⇑","////⇑","%___⇓","%___⇓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos = [10, 1, 0], [10, 0, 0]

    Worm = Bosses.worm().ch
    B_Maps.placeFighter(Worm, "01", [1, 10])
    
    Elemental1, Elemental2, Elemental3, Elemental4 = Elementals.dancer("Ice", "Greater").ch, Elementals.hulk("Ice", "Greater").ch, Elementals.wraith("Ice", "Greater").ch, Reptiles.wraith("Ice", "Random").ch
    Elemental5, Elemental6, Elemental7, Elemental8 = Elementals.dancer("Ice", "Random").ch, Elementals.hulk("Ice", "Random").ch, Elementals.wisp("Ice", "Random").ch, Reptiles.wisp("Ice", "Random").ch
    Elemental9 = Elementals.wisp("Ice", "Random").ch
    B_Maps.placeFighter(Elemental1, "11", [5, 10])
    B_Maps.placeFighter(Elemental2, "12", [2, 7])
    B_Maps.placeFighter(Elemental3, "13", [4, 11])
    B_Maps.placeFighter(Elemental4, "14", [8, 8])
    B_Maps.placeFighter(Elemental5, "15", [5, 4])
    B_Maps.placeFighter(Elemental6, "16", [9, 6])
    B_Maps.placeFighter(Elemental7, "17", [10, 10])
    B_Maps.placeFighter(Elemental8, "18", [0, 2])
    B_Maps.placeFighter(Elemental9, "19", [10, 3])

    group1 = [Worm]
    group2 = [Elemental1, Elemental2, Elemental3, Elemental4, Elemental5, Elemental6, Elemental7, Elemental8, Elemental9]
    for elemental in group2: elemental.cndt["reposed"] = True
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {"%": 2}]


def volcanoMap(players) -> list:
    row1  = ["////⇑","////⇑","////⇑","#)))⇓","#)))⇓","////⇑","#)))⇓","////⇑","#)))⇓","////⇑","____⇑","____⇑"]
    row2  = ["____↑","////⇑","#)))⇓","#)))⇓","#)))⇓","____⇑","#)))⇓","#)))⇓","#)))⇓","____⇑","____⇑","____⇑"]
    row3  = ["__L.|","____↑","____↑","#)))⇓","////⇑","#)))⇓","____⇑","#)))⇓","#)))⇓","#)))⇓","____⇑","____⇑"]
    row4  = ["____|","__M.|","____↑","#)))⇓","#)))⇓","____⇑","____⇑","#)))⇓","#)))⇓","#)))⇓","////⇑","____⇑"]
    row5  = ["#___|","____|","#___|","#)))⇓","____↑","____↑","____⇑","____⇑","__11⇑","#)))⇓","____⇑","__13⇑"]
    row6  = ["#)))⇓","#___|","____↑","#)))⇓","____↑","____↑","____↑","#___|","#___|","#)))⇓","#___|","____↑"]
    row7  = ["#)))⇓","#)))⇓","////⇑","#)))⇓","____↑","____⇑","____↑","#___|","#)))⇓","#___|","#___|","____↑"]
    row8  = ["#)))⇓","#)))⇓","#)))⇓","#)))⇓","////⇑","__12⇑","____↑","#___|","#)))⇓","#)))⇓","#___|","____|"]
    row9  = ["#___|","#)))⇓","#)))⇓","////⇑","////⇑","////⇑","____↑","#___↑","#_14|","#___|","#___|","#_01|"]
    row10 = ["#___|","#)))⇓","#)))⇓","////⇑","////⇑","____⇑","____↑","____|","////⇑","____|","____|","____|"]
    row11 = ["////⇑","#___|","#)))⇓","#)))⇓","____↑","////⇑","____↑","____|","////⇑","____|","____|","////⇑"]
    row12 = ["////⇑","////⇑","#)))⇓","#)))⇓","____↑","____↑","____↑","////⇑","////⇑","////⇑","____|","____|"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos = [2, 0, 0], [3, 1, 0]

    LavaBug = Bosses.strider().ch
    B_Maps.placeFighter(LavaBug, "01", [8, 11])
    
    Lizard1, Lizard2, Lizard3, Tortoise1 = Reptiles.lizard("Flame", "Adult").ch, Reptiles.lizard("Flame", "Adult").ch, Reptiles.lizard("Flame", "Adult").ch, Reptiles.tortoise("Flame", "Juvenile").ch
    B_Maps.placeFighter(Lizard1, "11", [4, 8])   
    B_Maps.placeFighter(Lizard2, "12", [7, 5])   
    B_Maps.placeFighter(Lizard3, "13", [4, 11])   
    B_Maps.placeFighter(Tortoise1, "14", [8, 8])   

    group1 = [LavaBug]
    group2 = [Lizard1, Lizard2, Lizard3, Tortoise1]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {"#": 3}]


def woodsMap(players) -> list:
    row1  = ["=___↓","=___↓","////⇑","////⇑","=___↓","=___↓","=_12|","=___|","@___↓","=___↓","=___↓","=___↓"]
    row2  = ["=___|","=___↓","////⇑","////⇑","=___↓","=_11|","=___|","=___↓","=___↓","////⇑","////⇑","=___↓"]
    row3  = ["=___|","=___↓","=___↓","=___↓","=___↓","=___|","=___|","=___↓","////⇑","////⇑","////⇑","////⇑"]
    row4  = ["@___|","=_M.|","=___|","=___|","=___|","=___|","=___|","=_13↓","////⇑","////⇑","@_01⇓","////⇑"]
    row5  = ["=___|","=_L.|","=___|","=___|","=_15↓","=___↓","=___↓","=___↓","////⇑","////⇑","////⇑","=_02↓"]
    row6  = ["=___|","=___|","=___|","=___↓","=___↓","////⇑","=___↓","=___↓","=___↓","////⇑","////⇑","=___↓"]
    row7  = ["=___|","=___|","=___|","=___↓","////⇑","////⇑","////⇑","=___↓","=___↓","=___↓","=_03↓","=___↓"]
    row8  = ["=___|","=___|","=___|","=___↓","////⇑","////⇑","////⇑","=___↓","=___|","=___|","=___|","=___|"]
    row9  = ["=___↓","=___↓","=___|","=___↓","=___↓","////⇑","=___↓","=___↓","@___|","=___|","=___|","=___|"]
    row10 = ["////⇑","=___↓","=___↓","=___|","=_14↓","=___↓","=___↓","=___|","=___|","=___|","=___|","=___|"]
    row11 = ["////⇑","////⇑","=___↓","=___|","=___|","=___|","=___|","=___↓","=___↓","=___↓","=___|","=___|"]
    row12 = ["////⇑","////⇑","=___↓","=___|","@___|","=___|","=___↓","=___↓","////⇑","=___↓","=___↓","=___|"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    players[0].pos, players[1].pos = [4, 1, 0], [3, 1, 0]

    Giant = Bosses.giant().ch
    B_Maps.placeFighter(Giant, "01", [3, 10])
    Giant.cndt["reposed"] = True

    Bear, Crow = Beasts.bear("Dream", "Elder").ch, Birds.crow("Dream", "Elder").ch
    B_Maps.placeFighter(Bear, "02", [4, 11])
    B_Maps.placeFighter(Crow, "03", [6, 10])
    
    Wolf1, Wolf2, Wolf3, Wolf4, Wolf5 = Beasts.wolf("Rot", "Random").ch, Beasts.wolf("Rot", "Random").ch, Beasts.wolf("Rot", "Random").ch, Beasts.wolf("Rot", "Random").ch, Beasts.wolf("Rot", "Random").ch
    B_Maps.placeFighter(Wolf1, "11", [4, 8])
    B_Maps.placeFighter(Wolf2, "12", [7, 5])
    B_Maps.placeFighter(Wolf3, "13", [4, 11])
    B_Maps.placeFighter(Wolf4, "14", [8, 8])

    group1 = [Giant, Bear, Crow]
    group2 = [Wolf1, Wolf2, Wolf3, Wolf4, Wolf5]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {"@": 4}]


def campMap(players) -> list:
    row1  = ["////|","////|","////|","____|","____|","____↓","____|","__11|","____|","____|","____|","////|"]
    row2  = ["////|","____|","////|","////|","____|","____↓","____|","____|","____|","#___|","____|","////|"]
    row3  = ["__L.|","____|","__02|","////|","____|","____↓","____|","____|","____|","f)))|","__09|","____|"]
    row4  = ["__M.|","____|","__W.|","____|","____|","____↓","____|","____|","____|","____|","____|","////|"]
    row5  = ["____|","__01|","__03|","////|","__06|","____↓","____|","____|","____|","__08|","____|","////|"]
    row6  = ["////|","____|","////|","////|","____|","____↓","____|","____|","____|","____|","____|","____|"]
    row7  = ["////|","////|","////|","____|","____|","____↓","_***]","____|","____|","____|","____|","____|"]
    row8  = ["____|","____|","____|","____|","____|","____↓","____|","____|","____|","____|","____|","____|"]
    row9  = ["____|","____|","____|","____|","____|","____↓","____|","____|","////|","////|","____|","////|"]
    row10 = ["____|","____|","____|","____|","____|","____↓","____|","////|","////|","____|","____|","____|"]
    row11 = ["____|","////|","////|","____|","____|","____↓","____|","////|","____|","____|","____|","__07|"]
    row12 = ["__04|","____|","////|","////|","____|","____↓","____|","////|","////|","__05|","____|","____|"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    Willem = A_Pcs.getWillem()
    players += [Willem]
    players[0].pos, players[1].pos, players[2].pos = [2, 0, 0], [3, 0, 0], [3, 2, 0]

    Bandit1, Bandit2, Bandit3 = Humans.brute("Basic", "Elite").ch, Humans.brute("Basic", "Adept").ch, Humans.brute("Basic", "Adept").ch    
    Bandit4, Bandit5, Bandit6 = Humans.archer("Basic", "Proficient").ch, Humans.mage("Flame", "Elite").ch, Humans.brute("Basic", "Novice").ch    
    Bandit7, Bandit8, Bandit9 = Humans.brute("Basic", "Proficient").ch, Humans.archer("Basic", "Elite").ch, Humans.archer("Basic", "Novice").ch    
    B_Maps.placeFighter(Bandit1, "01", [4, 1])
    B_Maps.placeFighter(Bandit2, "02", [2, 2])
    B_Maps.placeFighter(Bandit3, "03", [4, 2])
    B_Maps.placeFighter(Bandit4, "04", [11, 0])
    B_Maps.placeFighter(Bandit5, "05", [11, 9])
    B_Maps.placeFighter(Bandit6, "06", [4, 4])
    B_Maps.placeFighter(Bandit7, "07", [10, 11])
    B_Maps.placeFighter(Bandit8, "08", [4, 9])
    B_Maps.placeFighter(Bandit9, "09", [3, 10])

    Bandit1.props["name"] = "Bandit Lord"
    Bandit1.atrb["injury"], Bandit1.atrb["fatigue"] = 0, 0
    Bandit1.equip["weapon"]["tier"] = "Masterwork"
    Bandit1.equip["weapon"]["modifier"] *= 2

    Insect1 = Insects.isopod("Basic", "Small").ch
    B_Maps.placeFighter(Insect1, "11", [0, 7])

    group1 = [Bandit1, Bandit2, Bandit3, Bandit4, Bandit5, Bandit6, Bandit7, Bandit8, Bandit9]
    group2 = [Insect1]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {}]


def portMap(players, element) -> list:
    row1  = ["////↑","__L.|","____|","____|","////↑","_*01|","____|","__02|","__07|","__03|","__13|","__18|"]
    row2  = ["____↑","__M.|","____|","____|","////↑","____|","____|","____|","____|","__05|","____|","____|"]
    row3  = ["////↑","__W.↑","____|","____|","////↑","____|","____|","____|","____|","////↑","____|","____|"]
    row4  = ["~~~~⇓","////↑","____|","____|","////↑","____|","__04|","____|","____|","////↑","____|","____|"]
    row5  = ["~~~~⇓","____↑","____|","____|","__08|","____|","____|","____|","____|","////↑","__19|","____|"]
    row6  = ["~~~~⇓","////↑","____|","__11|","__09|","____|","__06|","____|","____|","////↑","____|","____|"]
    row7  = ["~~~~⇓","__16↑","____|","____|","////↑","____|","____|","____|","__12|","////↑","____|","__14|"]
    row8  = ["~~~~⇓","////↑","____|","____|","////↑","////↑","////↑","////↑","____↑","////↑","____|","____|"]
    row9  = ["~~~~⇓","____↑","____|","____|","____|","____|","____|","____|","____|","____|","____|","____|"]
    row10 = ["~~~~⇓","////↑","__17↑","____|","____|","____|","____|","____|","____|","__15|","____|","____|"]
    row11 = ["~~~~⇓","~~~~⇓","////↑","____↑","////↑","____↑","////↑","____↑","////↑","____↑","////↑","____↑"]
    row12 = ["~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓","~~~~⇓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    atmosphere = Area.getAtmosphere(1, element)

    for row in range(12):
        for column in range(12):
            if "__" in battleMap[row][column]:
                battleMap[row][column] = atmosphere + battleMap[row][column][1:]

    players[0].pos, players[1].pos, players[2].pos = [0, 1, 0], [1, 1, 0], [2, 1, 0]

    Duke = Humans.doctor("Basic", "Adept")
    Duke.props["name"] = "Usurper Duke"
    Duke.equip["armor"]["tier"] = "Masterwork"
    Duke.equip["armor"]["modifier"] *= 2

    Knight1, Knight2, Knight3 = Humans.knight("Basic", "Elite").ch, Humans.knight("Basic", "Master").ch, Humans.knight("Basic", "Adept").ch    
    Mage1, Mage2 = Humans.mage("Ice", "Adept").ch, Humans.mage("Flame", "Adept").ch   
    Archer, Door1, Door2 = Humans.brute("Basic", "Proficient").ch, Totems.impedance("Dream", "Door").ch, Totems.impedance("Dream", "Door").ch    
    B_Maps.placeFighter(Duke, "01", [3, 10])
    B_Maps.placeFighter(Knight1, "02", [0, 7])
    B_Maps.placeFighter(Knight2, "03", [0, 9])
    B_Maps.placeFighter(Knight3, "04", [3, 6])
    B_Maps.placeFighter(Mage1, "05", [1, 9])
    B_Maps.placeFighter(Mage2, "06", [5, 6])
    B_Maps.placeFighter(Archer, "07", [0, 8])
    B_Maps.placeFighter(Door1, "08", [4, 4])
    B_Maps.placeFighter(Door2, "09", [5, 4])

    Elemental1, Elemental2, Elemental3 = Elementals.wisp(element, "Random").ch, Elementals.wisp(element, "Random").ch, Elementals.wisp(element, "Random").ch
    Elemental4, Elemental5, Elemental6, Elemental7, Elemental8, Elemental9 = None, None, None, None, None, None, None, None, None
    atmo = ""

    match element:
        case "Dream":
            atmo = "@"
            Elemental4, Elemental5 = Elementals.nymph("Dream", "Random").ch, Elementals.nymph("Dream", "Random").ch
            Elemental6, Elemental7 = Elementals.satyr("Dream", "Random").ch, Elementals.satyr("Dream", "Random").ch
            Elemental8, Elemental9 = Elementals.ogre("Dream", "Random").ch, Elementals.ogre("Dream", "Random").ch
        case "Flame":
            atmo = "#"
            Elemental4, Elemental5 = Elementals.ooze("Flame", "Random"), Elementals.ooze("Flame", "Random")
            Elemental6, Elemental7 = Elementals.hive("Flame", "Random"), Elementals.hive("Flame", "Random")
            Elemental8, Elemental9 = Elementals.puffer("Flame", "Random"), Elementals.puffer("Flame", "Random")
        case "Ice":
            atmo = "%"
            Elemental4, Elemental5 = Elementals.dancer("Ice", "Random"), Elementals.dancer("Ice", "Random")
            Elemental6, Elemental7 = Elementals.hulk("Ice", "Random"), Elementals.hulk("Ice", "Random")
            Elemental8, Elemental9 = Elementals.wraith("Ice", "Random"), Elementals.wraith("Ice", "Random")

    B_Maps.placeFighter(Elemental1, "11", [5, 3])
    B_Maps.placeFighter(Elemental2, "12", [6, 8])
    B_Maps.placeFighter(Elemental3, "13", [0 ,10])
    B_Maps.placeFighter(Elemental4, "14", [6, 11])
    B_Maps.placeFighter(Elemental5, "15", [9, 9])
    B_Maps.placeFighter(Elemental6, "16", [6, 1])
    B_Maps.placeFighter(Elemental7, "17", [9, 2])
    B_Maps.placeFighter(Elemental8, "18", [0, 11])
    B_Maps.placeFighter(Elemental9, "19", [4, 10])

    group1 = [Duke, Knight1, Knight2, Knight3, Mage1, Mage2, Archer, Door1, Door2]
    group2 = [Elemental1, Elemental2, Elemental3, Elemental4, Elemental5, Elemental6, Elemental7, Elemental8, Elemental9]
    iMap.updateFighterHeight(players + group1 + group2, battleMap)

    return [group1, group2, battleMap, {atmo: 5}]