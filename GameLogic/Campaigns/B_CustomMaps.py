from Characters import Bosses, Humans


def shipMap(playerGroup) -> list:
    row1  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row2  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row3  = ["-~~~⇓","-~~~⇓","-~~~⇓","-___|","-___|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row4  = ["-~~~⇓","-~~~⇓","-___|","-___|","-_F.|","-___|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row5  = ["-~~~⇓","-___|","-___|","-___|","////|","-___|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row6  = ["-~~~⇓","-___|","-___|","-___|","////|","__H.|","-_32|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row7  = ["-~~~⇓","-~~~⇓","-___|","-_31|","-_L.|","-_15|","__16|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row8  = ["-~~~⇓","-~~~⇓","-~~~⇓","-___|","-_14|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row9  = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row10 = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-_17|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","&~01⇓","-~~~⇓"]
    row11 = ["-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-_13|","-___|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    row12 = ["-~~~⇓","-~~~⇓","-~~~⇓","-_11|","-___|","////|","-_12|","-___|","-~~~⇓","-~~~⇓","-~~~⇓","-~~~⇓"]
    battleMap = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]

    Leviathan = Bosses.leviathan().ch
    Leviathan.atrb["corruption"], Leviathan.atrb["fatigue"], Leviathan.atrb["injury"] = 0, 0, 0
    Leviathan.props["name"], Leviathan.props["initials"] = "Leviathan", "01"
    Leviathan.pos = [9, 10]

    Sailor1, Sailor2 = Humans.knight("Basic", "Proficient").ch, Humans.brute("Basic", "Proficient").ch    
    Sailor1.props["name"], Sailor1.props["initials"] = Sailor1.props["name"] + "[31]", "31"
    Sailor2.props["name"], Sailor2.props["initials"] = Sailor2.props["name"] + "[32]", "32"
    Sailor1.pos, Sailor2.pos = [6, 3], [5, 6]

    Pirate1, Pirate2, Pirate3 = Humans.archer("Basic", "Proficient").ch, Humans.archer("Basic", "Novice").ch, Humans.archer("Basic", "Novice").ch    
    Pirate1.props["name"], Pirate1.props["initials"] = Pirate1.props["name"] + "[11]", "11"
    Pirate2.props["name"], Pirate2.props["initials"] = Pirate2.props["name"] + "[12]", "12"
    Pirate3.props["name"], Pirate3.props["initials"] = Pirate3.props["name"] + "[13]", "13"
    Pirate1.pos, Pirate2.pos, Pirate3.pos = [11, 3], [11, 6], [10, 4]

    Pirate4, Pirate5, Pirate6, Pirate7 = Humans.brute("Basic", "Proficient").ch, Humans.brute("Basic", "Novice").ch, Humans.brute("Basic", "Novice").ch, Humans.brute("Basic", "Novice").ch    
    Pirate4.props["name"], Pirate4.props["initials"] = Pirate4.props["name"] + "[14]", "14"
    Pirate5.props["name"], Pirate5.props["initials"] = Pirate5.props["name"] + "[15]", "15"
    Pirate6.props["name"], Pirate6.props["initials"] = Pirate6.props["name"] + "[16]", "16"
    Pirate7.props["name"], Pirate7.props["initials"] = Pirate7.props["name"] + "[17]", "17"
    Pirate4.pos, Pirate5.pos, Pirate6.pos, Pirate7.pos = [7, 4], [6, 5], [6, 6], [9, 5]

    playerGroup += [Sailor1, Sailor2]
    group1 = [Leviathan]
    group2 = [Pirate1, Pirate2, Pirate3, Pirate4, Pirate5, Pirate6, Pirate7]

    return [group1, group2, battleMap]