from Systems import PlayerSelect as Select
import random

club, heart, diamond, spade = "\u2663", "\u2665", "\u2666", "\u2660"


def setBody(value, suit) -> list:
    top, sides, bottom = [" _________ "], ["|         |"], ["|_________|"]
    card = top + sides + sides + sides + sides + sides + bottom
    card[3] = "|    " + value + "    |"
    card[1], card[5]= "| " + suit + "       |", "|       " + suit + " |"

    return card

def setFronts(type) -> list:
    deck = []

    for suit in [club, heart, diamond, spade]:
        match type:
            case "Aces":
                deck += [setBody("A", suit)]
            case "Numbers":
                deck += setBody("0", suit)
                for number in range(2, 10):
                    deck += [setBody(str(number), suit)]

                random.shuffle(deck)
                deck = deck[:12]

    return deck

def setBacks(length) -> list:
    backs, cardBack = [], setBody(" ", "?")
    for i in range(length): backs += [cardBack]

    return backs


def showEnvironment(environment):
    Select.waitPrint("\nCurrent Environment:")
    Select.waitPrint("| Density |   | Weather |   | Mana    |   | Threat  |")

    clubFace = setBody(environment["Clubs"][0], club)
    heartFace = setBody(environment["Hearts"][0], heart)
    diamondFace = setBody(environment["Diamonds"][0], diamond)
    spadeFace = setBody(environment["Spades"][0], spade)

    deck = [clubFace, heartFace, diamondFace, spadeFace]
    printDeck(deck)


def printDeck(deck):
    row, rowCount = 0, int(len(deck) / 4)
    excess = (len(deck) % 4)

    while row <= rowCount:
        cardNum, rowOffset = 4, 4 * row
        if row == rowCount: cardNum = excess

        if cardNum > 0:
            for line in range(7):
                for cardIndex in range(cardNum):
                    print(deck[cardIndex + rowOffset][line], end="   ")
                print()
            print()
        
        row += 1


def pickCard(hand) -> list:
    Select.waitPrint("\nChoose a card(1-" + str(len(hand)) + "):")

    backs = setBacks(len(hand))
    printDeck(backs)
    answer = int(Select.takeInput(1, len(hand))) - 1
    backs[answer] = hand[answer]
    printDeck(backs)

    return answer

def findSuit(line) -> str:
    if club in line: return "Clubs"
    elif diamond in line: return "Diamonds"
    elif heart in line: return "Hearts"
    elif spade in line: return "Spades"