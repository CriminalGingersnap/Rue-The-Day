from Systems import PlayerSelect as Select
import random

club, heart, diamond, spade = "\u2663", "\u2665", "\u2666", "\u2660"


def drawNumbers(quantity) -> int:
    numberValues = [[], []]
    numbers = setFronts("Numbers")
    numberChoices = pickCard(numbers, quantity)
    drawNumbers = numberChoices[0]

    for card in drawNumbers: numberValues[0] += [findValue(numbers[card])]
    numberValues[1] = numberChoices[1]

    return numberValues


def setBody(value, suit) -> list:
    top, sides, bottom = [" _________ "], ["|         |"], ["|_________|"]
    card = top + sides + sides + sides + sides + sides + bottom
    card[3] = "|    " + value + "    |"
    card[1], card[5]= "| " + suit + "       |", "|       " + suit + " |"

    return card

def setFronts(type) -> list:
    deck = []

    match type:
        case "Aces":
            for suit in [club, heart, diamond, spade]: deck += [setBody("A", suit)]
        case "Numbers":
            for suit in [club, heart, diamond, spade]:
                for number in range(2, 10): deck += [setBody(str(number), suit)]
                random.shuffle(deck)
                deck = deck[:6]

    return deck

def setBacks(length) -> list:
    backs, cardBack = [], setBody(" ", "?")
    for i in range(length): backs += [cardBack]

    return backs


def printDeck(deck):
    row, rowCount = 0, int(len(deck) / 3)
    excess = (len(deck) % 3)

    while row <= rowCount:
        cardNum, rowOffset = 3, 3 * row
        if row == rowCount: cardNum = excess

        if cardNum > 0:
            for line in range(7):
                for cardIndex in range(cardNum):
                    print(deck[cardIndex + rowOffset][line], end="   ")
                print()
            print()
        
        row += 1


def pickCard(hand, picks) -> list:
    drawn, down, backs = [], [], setBacks(len(hand))
    # printDeck(backs)

    # autoSelect = Select.yesNo("Forgo selection and take cards in order?")
    autoSelect = True

    if autoSelect:
        Select.clearPrint("Auto-select enabled. Flipping first five cards.")
        for cardNum in range(picks):
            backs[cardNum] = hand[cardNum]
            drawn += [cardNum]
        printDeck(backs)
    
    else:
        for pick in range(picks):
            Select.clearPrint("Choose a card(1-" + str(len(hand)) + "):")
            
            while True:
                answer = int(Select.takeInput(1, len(hand))) - 1

                if answer not in drawn:
                    backs[answer] = hand[answer]
                    drawn += [answer]
                    printDeck(backs)
                    break

                else: Select.waitPrint("Please select a new card.")

    for recount in range(len(hand)):
        if "?" in backs[recount][1]: down += hand[recount]

    Select.waitPrint("")
    return [drawn, down]


def findSuit(card) -> str:
    line = card[1]
    if club in line: return "Clubs"
    elif diamond in line: return "Diamonds"
    elif heart in line: return "Hearts"
    elif spade in line: return "Spades"

def findValue(card) -> str:
    line = card[3]
    if "2" in line: return 2
    elif "3" in line: return 3
    elif "4" in line: return 4
    elif "5" in line: return 5
    elif "6" in line: return 6
    elif "7" in line: return 7
    elif "8" in line: return 8
    elif "9" in line: return 9