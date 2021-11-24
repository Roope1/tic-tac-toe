from random import randint

def displayBoard(status):
    print("#########")
    print("# "+status[6],status[7],status[8]+" #")
    print("# "+status[3],status[4],status[5]+" #")
    print("# "+status[0],status[1],status[2]+" #")
    print("#########")
    return None


def getUserPlay(boardstatus):
    print("\nYour turn!")
    print("Pick your spot with a number between 1 - 9")
    print("7,8,9\n4,5,6\n1,2,3")
    while(True):
        userInput = input("Where do you wan't to place your mark?: ")
        displayBoard(boardstatus)
        try:
            index = int(userInput) - 1
            if index < 0:
                print("Choose between numbers 1 - 9.")
            elif boardstatus[index] == "-":
                boardstatus[index] = "X"
                break
            else:
                print("That spot is already taken, please pick another one.\n")
        except ValueError:
            print("Please give your choice as an integer!\n")
        except IndexError:
            print("Choose between numbers 1 - 9.\n")
    return boardstatus
    


def checkForWin(boardstatus):
    # windexes = winning indexes
    # indexes that have to be the same mark for either one to win the game
    windexes = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for win in windexes:
        if boardstatus[win[0]] == boardstatus[win[1]] and boardstatus[win[1]] == boardstatus[win[2]]:
            winner = boardstatus[win[0]]
            if winner != "-":
                return winner
            else:
                continue
    for marks in boardstatus:
        if marks == "-":
            return "?"
    return "-"


# Minimax algorithm consideres all the possible ways a game can go and chooses a move based on that
def minimax(status, depth, isMax):
    # Check for win with the temporary move, if the move wins => make it
    winCheck = checkForWin(status)
    if winCheck == "-":
        # No more moves left, a tie game.
        score = 0
        return score
    elif winCheck == "X":
        # X wins, not good for the AI thus negative score
        score = -10
        return score
    elif winCheck == "O":
        # Best possible outcome, AI wins with the temporary move
        score = 10
        return score

    # Calculates where the next AI move should go
    if isMax:
        best = -100000
        for i in range(9):
            if status[i] == "-":
                # makes that move
                status[i] = "O"
                # recursively calls it self to check game till the end
                best = max(best, minimax(status, depth + 1, not isMax))
                #reverts it
                status[i] = "-"
        return best
    # Calculates where the best possible human move would be
    # Does exactly the same as above but this time with human moves
    else:
        best = 100000
        for i in range(9):
            if status[i] == "-":
                status[i] = "X"
                best = min(best, minimax(status, depth + 1, not isMax))
                status[i] = "-"
        return best



def findBestMove(status):
    bestValue = -100000
    bestMove = -1
    # look through all empty spots on the gameboard
    for i in range(len(status)):
        if status[i] == "-":
            # Make a move and check how good it is
            status[i] = "O"
            moveValue = minimax(status, 0, False)
            # Restore the move back to original
            status[i] = "-"

            if moveValue > bestValue:
                bestMove = i
                bestValue = moveValue
                
    return bestMove

def aiTurn(boardstatus):
    print("Ai turn! \n")
    bestMove = findBestMove(boardstatus)
    boardstatus[bestMove] = "O"
    return boardstatus



def main():
    # Initialize the gameboard
    boardstatus = ["-","-","-","-","-","-","-","-","-"]
    winner = "?"
    displayBoard(boardstatus)

    # Randomize who starts
    if(randint(0, 1) == 0):
        userTurn = True
    else:
        userTurn = False
    
    gameOn = True
    while(gameOn):
        if(userTurn):
            boardstatus = getUserPlay(boardstatus)
            userTurn = False
        else:
            boardstatus = aiTurn(boardstatus)
            displayBoard(boardstatus)
            userTurn = True
        winner = checkForWin(boardstatus)
        if winner == "-":
            gameOn = False
            print("Tie game!")
        elif winner != "?":
            gameOn = False
            displayBoard(boardstatus)
            print(f"{winner} wins the game!")
        

if __name__ == "__main__":
    main()