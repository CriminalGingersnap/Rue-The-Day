from Campaigns.Benediction import Journal as B_Journal
from Campaigns.Avarice import Journal as A_Journal
import time

longWait, quickWait = .3, .07

# make a fast print option for large blocks of text. let the player choose before it starts.
def slowPrint(text):
    for i in text:
        quickPrint(i, '')
        time.sleep(quickWait)
    time.sleep(longWait)
    quickPrint('', '')


def readScene(title, campaign) -> None:
    if yesNo("\nRead '" + title + "' journal entry?"):
        phraseList = ""
        match campaign:
            case "Avarice": phraseList = A_Journal.scenes[title]
            case "Benediction": phraseList = B_Journal.scenes[title]

        time.sleep(longWait)
        for phrase in phraseList:
            quickPrint(phrase[0], '')
            conversationPrint(phrase[1])

        input("Press Enter to continue.")

def conversationPrint(text):
    for i in text:
        quickPrint(i, '')
        if i in [".", ",", "?", "!"]: time.sleep(longWait)
    quickPrint("\n")


def quickPrint(text, ending: str | None = "\n"):
    time.sleep(quickWait)
    print(text, end=ending)

def waitPrint(text):
    time.sleep(longWait)
    quickPrint(text, "\n")
    time.sleep(longWait)


def targetSelect(targets) -> int:
    targetNames = []
    for target in targets: targetNames += [target.props["name"]]
    
    name = pickOption(targetNames, "target")

    for target in targets:
        if target.props["name"] == name: return target


def pickOption(options, category):    
    if len(options) > 1:
        waitPrint("\nSelect " + category + ":")
        return makeSelection(options)
    else: return options[0]

def makeSelection(options):
    for option in options:
        quickPrint(str(options.index(option)+1) + ": " + str(option))

    selection = takeInput(1, len(options))
    print()
    return options[selection - 1]


def yesNo(prompt) -> bool:
    waitPrint(prompt)
    answer = makeSelection(["Yes", "No"])
    if answer == "Yes": return True
    else: return False
    

def takeInput(floor, ceiling):
    if floor == ceiling:
        quickPrint("Value defaults to " + str(floor) + ".")
        print()
        return floor
    else:
        while True:
            try:
                answer = int(input("-> "))
                if floor <= answer <= ceiling:
                    print()
                    return answer
                else: raise ValueError
            except ValueError:
                if ceiling == (floor + 1): print("Enter either " + str(floor) + " or " + str(ceiling) + ".")
                else: print("Enter a number between " + str(floor) + " and ", str(ceiling) + ".")


def listSelection(options, cap, prompt):
    ceiling, selection = len(options), []
    waitPrint(prompt)

    if cap <= 0: waitPrint("Action skipped. Limit reached.")
    elif ceiling == 0: waitPrint("Action skipped. No options in category.")
    else:
        quickPrint("Enter a comma separated list without spaces (Ex: 1,4,9).")
        if cap > 2: quickPrint("The list may include dashed sections (Ex: 1-4,9).")
        
        for option in options:
            quickPrint(str(options.index(option)+1) + ": " + str(option))

        while True:
            try:
                answerList = input("-> ").split(",")
                for answer in answerList:
                    if "-" in answer:
                        answerList.remove(answer)
                        start, end = int(answer.split("-")[0]), int(answer.split("-")[1])
                        for inclusion in range(start, end):
                            answerList += [inclusion]

                if len(answerList) > cap: raise SyntaxError
                elif not all((1 <= answer <= ceiling) for answer in answerList): raise ValueError
                else:
                    for answer in answerList: selection += [options[answer - 1]]
            
            except SyntaxError:
                print("Quantity of selected values cannot exceed " + str(cap) + ".")
            except ValueError:
                print("All values must be numbers between 1 and ", str(ceiling) + ".")
            except TypeError:
                print("All values must be numeric.")
    
    return selection