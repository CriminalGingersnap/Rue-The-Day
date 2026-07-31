from . import AvariceBiomes as Avarice, KingKillerBiomes as Kingdom
from . import BenedictionBiomes as Benediction, InfestationBiomes as Infestation
from Systems import Roll, PlayerSelect as Select
from Loop import Cards


def setFoes(biome, budgets, luckCard) -> list:
    Select.waitPrint("Rolling to determine encounter number.")
    Select.quickPrint("First roll:")
    roll1 = Roll.roll(None, 1, None, None)

    Select.quickPrint("Second roll:")
    roll2 = Roll.roll(None, 1, None, None)

    Select.waitPrint("Applying luck card:")
    Cards.printDeck([luckCard])
    roll2 += Cards.findValue(luckCard)
    Select.waitPrint("Modified second roll: " + str(roll2) + "\n")
    Select.waitPrint("")

    rolls = [roll1, roll2]
    rollNum, groups = 0, [[], []]
    
    for roll in rolls:
        budget = budgets[rollNum]
        members = []
        match biome:
            case "Wildlands Pass": members = Avarice.passEncounters(roll, budget)
            case "Wildlands Bay": members = Avarice.bayEncounters(roll, budget)
            case "Ice Fjord": members = Avarice.fjordEncounter(roll, budget)
            case "Ice Glacier": members = Avarice.glacierEncounters(roll, budget)
            case "Dreamwood Periphery": members = Avarice.peripheryEncounters(roll, budget)
            case "Dreamwood Depths": members = Avarice.depthsEncounters(roll, budget)
            case "Flame Peninsula": members = Avarice.peninsulaEncounters(roll, budget)
            case "Flame Volcano": members = Avarice.volcanoEncounters(roll, budget)

            case "Kingdom Fort": members = Kingdom.strongholdEncounters(roll, rollNum, "Fort", budget)
            case "Kingdom Road": members = Kingdom.outlierEncounters(roll, rollNum, "Road", budget)
            case "Marshland": members = Kingdom.marshEncounters(roll, budget)
            case "Outlaw Camp": members = Kingdom.strongholdEncounters(roll, rollNum, "Camp", budget)
            case "Outlaw Range": members = Kingdom.outlierEncounters(roll, rollNum, "Range", budget)
            case "Unsettled": members = Kingdom.unsettledEncounters(roll, budget)

            case "Dream Sea-Cave": members = Benediction.seaCaveEncounters(roll, budget)
            case "Holy Scrubland": members = Benediction.scrublandEncounters(roll, budget)
            case "Holy Desert": members = Benediction.desertEncounters(roll, budget)
            case "Rot Encroachment": members = Benediction.encroachmentEncounter(roll, budget)
            case "Rot Locus": members = Benediction.locusEncounter(roll, budget)
            case "Shoreline Dunes": members = Benediction.duneEncounters(roll, budget)

            case "Flame Lowland": members = Infestation.lowlandEncounters(roll, budget)
            case "Ice Highland": members = Infestation.highlandEncounters(roll, budget)
            # case "Ice Peak": members = Infestation.peakEncounters(roll, budget)
            case "Marsh Depths": members = Infestation.depthsEncounters(roll, budget)
            case "Shoreline Nest": members = Infestation.nestEncounters(roll, budget)
            
        memberIndex = 1
        for member in members:
            member.props["name"] += "[" + str(rollNum) + str(memberIndex) + "]"
            member.props["initials"] = str(rollNum) + str(memberIndex)
            memberIndex += 1

        for member in members:
            if "echo" in member.inv:
                echo = member.inv["echo"]
                if (echo != "None"):
                    echo.props["name"] += "[" + str(rollNum) + str(memberIndex) + "]"
                    echo.props["initials"] = str(rollNum) + str(memberIndex)
                    memberIndex += 1

        groups[rollNum] = members
        rollNum += 1

    return groups