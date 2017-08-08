from EnemyAI import EnemyAI


class GameLogic:

    # total turn of the game, %2 = player, %2+1 = computer
    turn = 0

    def __init__(self, player_board, enemy_board):
        self.player_board = player_board
        self.enemy_board = enemy_board
        self.enemy_AI = EnemyAI(self.enemy_board, 0)

    def make_move(self, x, y):
        if self.turn % 2 == 0:
            #player turn
            self.enemy_board.pin_point_hit(x, y)

        elif self.turn % 2 == 1:
            # enemy turn
            point = self.enemy_AI.return_point()
            self.player_board.pin_point_hit(point.get_x(), point.get_y())

        self.turn += 1


