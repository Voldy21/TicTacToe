from random import Random
from sys import maxsize
# from player import HumanPlayer, RandomComputerPlayer
import time


class Player:
    def __init__(self, letter):
        #letter is x or o
        self.letter = letter

    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        depth = len(game.available_moves())
        if depth == 9:
            return random.choice(game.available_moves())
        tempGame = TicTacToe(game.board)
        move = self.minimax(tempGame, depth, self.letter)[0]
        if move not in game.available_moves():
            raise Exception("failed move")
        return move

    
    def minimax(self, game, depth, player):
        """
        AI function that choice the best move
        :param game: current game of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        switch = {
            "X": "O",
            "O": "X"
        }
        if player == self.letter:
            best = [-1, -2000]
        else:
            best = [-1, +2000]

        if depth == 0 or game.current_winner:
            score = self.evaluate(game)
            return [-1, score]

        for square in game.available_moves():
            game.make_move(square, player)
            temp = switch[player]
            score = self.minimax(game, depth-1, temp)
            game.make_move(square, " ")
            score[0] = square

            if player == self.letter:
                if score[1] > best[1]:
                    best = score
            else:
                if score[1] < best[1]:
                    best = score
        return best


    def evaluate(self, game):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if game.current_winner:
            if game.current_winner == self.letter:
                score = 1
            else:
                score = -1
            game.toggle()
        else:
            score = 0

        return score

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            #we're going to check that this is a correct value by trying to cast
            #it to an integer and if it's not, then we can say it's invalid
            #if that spot is not availble on the board, we also say it's invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True # if these are successful, then yay
            except ValueError:
                print('Invalid square. Try again.')
        return val





class TicTacToe:
    def __init__(self, board=False):
        self.board = [' ' for _ in range(9)] # we will use a single list to rep 3x3 board
        if board:
            self.board = board
        self.current_winner = None # keep track of winner!

    def print_board(self):
        #this is just getting the rows
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print(' | ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what numbers corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1) * 3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        #return []
        moves = []
        for (i, spot) in enumerate(self.board):
            #['x', 'x', 'o'] --> [(0, 'x'), (1, 'x'), (2, 'o')]
            if spot == " ":
                moves.append(i)
        return moves
    
    def toggle(self):
        self.current_winner = None

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(" ")

    def make_move(self, square, letter):
        #if valid move, then make the move (assign square to letter)
        #then return true. if invalid, return false

        if self.board[square] == ' ' or letter == " ":
            self.board[square] = letter
            if letter != " " and self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        #winner if 3 in a row anywhere.. we have to check all of these!
        #first let's check the row
        row_ind = square // 3
        row = self.board[row_ind * 3: (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        
        # check column
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        #check diagonals
        #but only if the square is an even number (0, 2, 4, 6, 8)
        # these are the only moves to win a diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]] #left to right diagonal
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2,4,6]] #right to left diagonal
            if all([spot == letter for spot in diagonal2]):
                return True
        
        #if all fails
        return False


def play(game, x_player, o_player, print_game=True):
    #returns the winner of the game(the letter)! or None for a tie
    if print_game:
        game.print_board_nums()

    letter = "X" #starting letter
    #iterate while the game has empty squares
    #(we don't have to worry about winner because we'll just return that)
    #which breaks the loop

    while game.empty_squares():
        #get the move from the appropriate player
        if letter == "O":
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        #let's define a function to make a move!
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('') #just empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            #after we made our move, we need to alternate letters
            letter = 'O' if letter == 'X' else 'X' #switches player
        
        #tiny break to make things easier to read
        time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')



if __name__ == "__main__":
    x_player = HumanPlayer("X")
    o_player = RandomComputerPlayer("O")
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)