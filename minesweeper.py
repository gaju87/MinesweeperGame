import random
import re
# lets create a board object to represent the minesweeper game
# this is so that we can just say "create a new board object.or
#"dig here" or "render this game for this project"
class Board:
    def __init__(self,dim_size, num_bombs):
        #let's track the parameter they will helpful later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #lets create the board
        #helper function
        self.board=self.make_new_board() # plant bombs
        self.assign_values_to_board()
        # initilize a set to keep track of which location we have uncovered

        # we will save(row,col) tuples into this set

        self.dug=set() # if we digat 0,0 then self.dug={(0,0)}

    def make_new_board(self):

        #construct the new board on dim size and num bombs
        #we should construct the list of lists here(or whatever representation ypu prefer, but since we have 2D board, list of list is most natural
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # this create an array like this:
        # [None, None,None, None]
        # [None, None,None, None]
        # [None, None,None, None]
        # [None, None,None, None]
        # we can see how this represent board!

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)  # return a random integer N such that a<=N <=b
            row = loc // self.dim_size  # we want the number of times dim_size goes into loc to
            col = loc % self.dim_size  # we want want remainder to tell us what index in that row to

            if board[row][col] == '*':
                # this means we have actually planted a bomb there already keep going
                continue

            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        #now that we have  the bombs planted , let assign the number 0-8 for all the empty spaces which
        # represent how many neighbouring bombs there are. we can precompute these and it'll save us some
        # effort checking what's around the board later on :)
        for r in range (self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c]=='*':
                    #if this is already a bomb we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r,c)

    def get_num_neighbouring_bombs(self, row, col):
        # let's iterate through each of neighbouring position and sum number of bombs
        #lop left:[row-1,col-1]
        #top middle:[row-1,col]
        #top right:(row-1,col+1)
        #left:(row,col-1)
        #right:(row,col+1)
        #bottom left:(row+1,col-1)
        #bottom middle:(row+1,col)
        #bottom right:(row+1,col+1)

        #make sure to not go out of bounds!

        num_neighbouring_bombs=0
        for r in range(max(0, row-1),min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    #our original location Don't check
                    continue

                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs
        # generate new board


    def dig(self, row, col):

        # dig at that location!
        #return True if successful dig, False if bomb dig
        #few scenarios:
        # hit a bomb ->game over
        # dig at location with neighbouring bombs-> finsih dig
        # dig at location with no neighboring boms-> recursively dig neighbors!

        self.dug.add((row,col)) # keep teack that we actually dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True


        self.board[row][col] == 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0,col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r,c) in self.dug:
                    continue
                self.dig(r, c)

        return True


    def __str__(self):

        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if(row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] ='  '



        string_rep ='  '

        widths = []

        for idx in range(self.dim_size):
            columns=map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )
        indices = [i for i in range(self.dim_size)]
        indices_row = '  '
        cells = []
        for idx, col in enumerate(indices):
            format =' %- ' + str(widths[idx]) + "s"
            cells.append(format%[col])
        indices_row += ' '.join(cells)
        indices_row += ' \n'

        for i in range(len(visible_board)):
            row=visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(indices):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % [col])
            string_rep += ' '.join(cells)
            string_rep += ' \n'

        str_len = int(len(string_rep)/self.dim_size)
        string_rep = indices_row+'-'* str_len + '\n' +string_rep +'-'* str_len

        return string_rep


# play the game
def play(dim_size=10, num_bombs=10):
    #step1: create the board and plant bombs
    board = Board(dim_size, num_bombs)
    #step2: show the user board and ask foe where they want to dig
    #step3a:if location is bomb, show game over message
    #step3b :if location is not a bomb, dig recursively until reach square is at least next to a bomb
    #step 4: repeat step 2 and 3a/b until there are no more places to dig-> victory
    safe = True

    while len(board.dug) < board.dim_size**2-num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("where would you like to dig? Input row and col"))
        row,col=int(user_input[0]),int(user_input[-1])
        if row<0 or row>= board.dim_size or col < 0 or col >= dim_size:
            print("invalid location try again")
            continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("congratulation you win")
    else:
        print("game over")

        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]

if __name__== "__main__":
    play()