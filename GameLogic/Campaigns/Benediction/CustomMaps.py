from Characters import Bosses, Humans, Elementals, Totems

def resetFighter(fighter, initials, position) -> None:
    fighter.atrb["corruption"], fighter.atrb["fatigue"], fighter.atrb["injury"] = 0, 0, 0
    fighter.props["name"], fighter.props["initials"] = fighter.props["name"] + "[" + initials + "]", initials
    fighter.pos = position


def shipMap(playerGroup) -> list:
    row1  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row2  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row3  = ["-~~~⇓","-~~~⇓","-~~~⇓","-___|","-___|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row4  = ["-~~~⇓","-~~~⇓","-___|","-___|","-_F.|","-___|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row5  = ["-~~~⇓","-___|","-___|","////↑","-___|","////↑","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row6  = ["-~~~⇓","-___|","-___|","////↑","-___|","////↑","-_32|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row7  = ["-~~~⇓","-~~~⇓","-___|","-_31|","-_H.|","-_15|","__16|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row8  = ["-~~~⇓","-~~~⇓","-~~~⇓","-_L.|","-_14|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row9  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row10 = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-_17|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","&~01⇓","-~~~⇓"]
    row11 = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-_13|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row12 = ["-~~~⇓","-~~~⇓","-~~~⇓","-_11|","-___|","////↑","-_12|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    Leviathan = Bosses.leviathan().ch
    resetFighter(Leviathan, "01", [9, 10])

    Sailor1, Sailor2 = Humans.knight("Basic", "Proficient").ch, Humans.brute("Basic", "Proficient").ch 
    resetFighter(Sailor1, "31", [6, 3])   
    resetFighter(Sailor2, "32", [5, 6])   

    Pirate1, Pirate2, Pirate3 = Humans.archer("Basic", "Proficient").ch, Humans.archer("Basic", "Novice").ch, Humans.archer("Basic", "Novice").ch    
    resetFighter(Pirate1, "11", [11, 3])   
    resetFighter(Pirate2, "12", [11, 6])   
    resetFighter(Pirate3, "13", [10, 4])   

    Pirate4, Pirate5, Pirate6, Pirate7 = Humans.brute("Basic", "Proficient").ch, Humans.brute("Basic", "Novice").ch, Humans.brute("Basic", "Novice").ch, Humans.brute("Basic", "Novice").ch    
    resetFighter(Pirate4, "14", [7, 4])   
    resetFighter(Pirate5, "15", [6, 5])   
    resetFighter(Pirate6, "16", [6, 6])   
    resetFighter(Pirate7, "17", [9, 5])   

    playerGroup += [Sailor1, Sailor2]
    group1 = [Leviathan]
    group2 = [Pirate1, Pirate2, Pirate3, Pirate4, Pirate5, Pirate6, Pirate7]

    return [group1, group2, battleMap]


def cryptMap(playerGroup) -> list:
    row1  = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","____↑","}_01↑","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row2  = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","____↑","____↑","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row3  = ["=)))⇓","=)))⇓","=)))⇓","__02↑","____↑","__04↑","__03↑","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row4  = ["=)))⇓","=)))⇓","=)))⇓","____|","____|","____|","____|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row5  = ["=)))⇓","=)))⇓","=)))⇓","____|","____|","____|","____|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row6  = ["=)))⇓","=)))⇓","____|","____|","____|","____|","____|","____|","=)))⇓","=)))⇓","-_12↓","-___↓"]
    row7  = ["-_14↓","-___↓","____|","____|","____|","____|","____|","____|","-___↓","-___↓","-___↓","-_11↓"]
    row8  = ["=)))⇓","=)))⇓","____|","____|","____|","____|","____|","____|","=)))⇓","=)))⇓","-_13↓","-___↓"]
    row9  = ["=)))⇓","=)))⇓","=)))⇓","____|","____|","____|","____|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row10 = ["=)))⇓","=)))⇓","=)))⇓","____|","__31|","__L.|","____|","=)))⇓","=)))⇓","=)))⇓","=)))⇓","-___↓"]
    row11 = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","-_A.↓","-_H.↓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    row12 = ["=)))⇓","=)))⇓","=)))⇓","=)))⇓","-_F.↓","-_32↓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓","=)))⇓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    Lich = Bosses.lich().ch
    resetFighter(Lich, "01", "Lich", [0, 5])

    Sphinx = Elementals.sphinx("Holy", "Greater")
    resetFighter(Sphinx, "31", [0, 5])

    Zombie1, Zombie2, Zombie3 = Humans.archer("Rot", "Proficient").ch, Humans.archer("Rot", "Adept").ch, Humans.knight("Rot", "Elite").ch    
    resetFighter(Zombie1, "02", [2, 3])
    resetFighter(Zombie2, "03", [2, 5])
    resetFighter(Zombie3, "04", [2, 6])

    Zombie1.pos, Zombie2.pos, Zombie3.pos = [11, 3], [11, 6], [10, 4]

    Elemental1, Elemental2, Elemental3, Elemental4 = Elementals.slime("Rot", "Lesser"), Elementals.wisp("Rot", "Greater"), Elementals.wisp("Rot", "Lesser"), Elementals.grotesquery("Rot", "Greater")
    resetFighter(Elemental1, "11", [6, 11])
    resetFighter(Elemental2, "12", [5, 10])
    resetFighter(Elemental3, "13", [7, 10])
    resetFighter(Elemental4, "14", [6, 0])

    playerGroup += [Sphinx]
    group1 = [Lich, Zombie1, Zombie2, Zombie3]
    group2 = [Elemental1, Elemental2, Elemental3, Elemental4]

    return [group1, group2, battleMap]


def manorMap(playerGroup) -> list:
    row1  = ["////|","////|","////|","////|","////|","////|","____|","__06↓","____↓","////|","////|","////|"]
    row2  = ["////|","////|","////|","////|","////|","////|","____|","////|","____↓","}_01↓","////|","////|"]
    row3  = ["////|","////|","____|","____|","////|","____|","____|","////|","____↓","____↓","////|","////|"]
    row4  = ["////|","////|","____|","__11|","__03|","____|","____|","__05↓","____↓","____↓","////|","////|"]
    row5  = ["////|","////|","__15|","____|","////|","____|","____|","////|","____↓","____↓","-___⇓","-_19⇓"]
    row6  = ["////|","////|","____|","____|","////|","__16|","____|","////|","////|","////|","-___⇓","-___⇓"]
    row7  = ["-_A.|","-_02|","____|","____|","////|","////|","////|","////|","////|","////|","-___⇓","-___⇓"]
    row8  = ["-_H.|","////|","____|","____|","////|","////|","////|","////|","__17↓","____↓","-___⇓","-_18⇓"]
    row9  = ["-_F.|","////|","____|","__12|","____|","__13|","____|","////|","____↓","____↓","-___⇓","-___⇓"]
    row10 = ["-_L.|","////|","____|","____|","____|","____|","__14|","////|","____↓","____↓","////|","////|"]
    row11 = ["-___|","////|","////|","////|","____|","____|","____|","__04|","____↓","____↓","////|","////|"]
    row12 = ["-___|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|","////|"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    Vampire = Bosses.vampire()
    resetFighter(Vampire, "01", [])
    Vampire.cndt["reposed"] = True

    Door1, Door2, Door3, Door4, Door5 = Totems.impedance("Dream", "Gate"), Totems.ward("Flame", "Door"), Totems.ward("Ice", "Door"), Totems.sentry("Rot", "Door"), Totems.sentry("Dream", "Door")
    resetFighter(Door1, "02", [])
    resetFighter(Door2, "03", [])
    resetFighter(Door3, "04", [])
    resetFighter(Door4, "05", [])
    resetFighter(Door5, "06", [])
    Door1.cndt["reposed"], Door2.cndt["reposed"], Door3.cndt["reposed"] = True, True, True

    Ghoul1, Ghoul2, Ghoul3, Ghoul4, Ghoul5 = Humans.brute("Rot", "Adept").ch, Humans.brute("Rot", "Proficient").ch, Humans.mage("Rot", "Adept").ch, Humans.knight("Rot", "Elite").ch, Humans.knight("Rot", "Novice").ch    
    resetFighter(Ghoul1, "11", [2, 3])
    resetFighter(Ghoul2, "12", [2, 5])
    resetFighter(Ghoul3, "13", [2, 6])
    resetFighter(Ghoul4, "14", [2, 6])
    resetFighter(Ghoul5, "15", [2, 6])
    Ghoul1.cndt["reposed"], Ghoul2.cndt["reposed"], Ghoul3.cndt["reposed"], Ghoul4.cndt["reposed"], Ghoul5.cndt["reposed"] = True, True, True, True, True

    Ghoul6, Ghoul7, Ghoul8, Ghoul9 = Humans.archer("Rot", "Adept").ch, Humans.mage("Rot", "Novice").ch, Humans.knight("Rot", "Master").ch, Humans.knight("Rot", "Novice").ch    
    resetFighter(Ghoul6, "16", [2, 5])
    resetFighter(Ghoul7, "17", [2, 6])
    resetFighter(Ghoul8, "18", [2, 6])
    resetFighter(Ghoul9, "19", [2, 6])
    Ghoul6.cndt["reposed"], Ghoul7.cndt["reposed"], Ghoul8.cndt["reposed"], Ghoul9.cndt["reposed"] = True, True, True, True

    group1 = [Vampire, Door1, Door2, Door3, Door4, Door5]
    group2 = [Ghoul1, Ghoul2, Ghoul3, Ghoul4, Ghoul5, Ghoul6, Ghoul7, Ghoul8, Ghoul9]

    return [group1, group2, battleMap]