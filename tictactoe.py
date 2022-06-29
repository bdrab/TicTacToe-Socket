class TicTacToe:
    def __init__(self, game_id):
        self.board = []
        self.game_id = game_id
        self.ready = False
        self.create_board()
        self.player1_move = True
        self.player2_move = False
        self.game_finished = False
        self.winner = -1

    def check_move(self, player):
        if player == 0:
            return self.player1_move
        else:
            return self.player2_move

    def connected(self):
        return self.ready

    def create_board(self):
        for column in range(3):
            self.board.append([])
            for row in range(3):
                self.board[column].append(" ")

    def play(self, player, data):
        data = data.split("|")
        self.board[int(data[0])][int(data[1])] = data[2]

        if player == 0:
            self.player1_move = False
            self.player2_move = True
        elif player == 1:
            self.player1_move = True
            self.player2_move = False
        if self.check_win():
            self.winner = player
            self.game_finished = True

    def check_win(self):
        if (self.board[0][0] == self.board[0][1] == self.board[0][2]) and self.board[0][2] != " ":
            return True

        elif (self.board[1][0] == self.board[1][1] == self.board[1][2]) and self.board[1][2] != " ":
            return True

        elif (self.board[2][0] == self.board[2][1] == self.board[2][2]) and self.board[2][2] != " ":
            return True

        elif (self.board[0][0] == self.board[1][0] == self.board[2][0]) and self.board[2][0] != " ":
            return True

        elif (self.board[0][1] == self.board[1][1] == self.board[2][1]) and self.board[2][1] != " ":
            return True

        elif (self.board[0][2] == self.board[1][2] == self.board[2][2]) and self.board[2][2] != " ":
            return True

        elif (self.board[0][0] == self.board[1][1] == self.board[2][2]) and self.board[2][2] != " ":
            return True

        elif (self.board[0][2] == self.board[1][1] == self.board[2][0]) and self.board[2][0] != " ":
            return True

        values = []
        for row in self.board:
            for cell in row:
                values.append(cell)
        if " " not in values:
            self.winner = 2
            self.game_finished = True

        return False

    def reset(self):
        for row in range(3):
            for column in range(3):
                self.board[row][column] = " "
        self.player1_move = True
        self.player2_move = False
        self.game_finished = False
        self.winner = -1
