from . import Flame1_Peninsula as Peninsula
from . import Wild1_Pass as Pass, Wild2_Bay as Bay
from . import Ice1_Fjord as Fjord, Ice2_Glacier as Glacier
from Systems import Roll, PlayerSelect as Select


def setFoes(biome, faceCards) -> list:
    Select.waitPrint("Rolling dice to determine encounter number.")
    rolls = [Roll.castDice(2), Roll.castDice(2)]
    index, groups = 0, [[], []]
    
    for roll in rolls:
        members = []
        match biome:
            case "Pass": members = Pass.randomEncounters(roll, faceCards)
            case "Bay": members = Bay.randomEncounters(roll, faceCards)
            case "Fjord": members = Fjord.randomEncounters(roll, faceCards)
            case "Glacier": members = Glacier.randomEncounters(roll, faceCards)
            # case "Ghostwood": members = Ghostwood.randomEncounters(roll, faceCards)
            case "Peninsula": members = Peninsula.randomEncounters(roll, faceCards)
            # case "Volcano": members = Volcano.randomEncounters(roll, faceCards)

        groups[index] = {"members": members, "name": "Foes_" + str(index + 1)}
        index += 1

    return groups