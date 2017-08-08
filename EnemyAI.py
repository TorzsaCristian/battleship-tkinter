import random

from Point import Point


class EnemyAI:

    difficulty = 0

    points_history = []

    def __init__(self, board, difficulty):
        self.board = board
        self.difficulty = difficulty

    def return_point(self):
        # return unique point
        same_point = True

        while same_point:
            same_point = False
            temp_x = random.randint(0, self.board.get_board_size()-1)
            temp_y = random.randint(0, self.board.get_board_size()-1)
            point = Point(temp_x, temp_y)
            for i, o in enumerate(self.points_history):
                if o.get_x() == temp_x and o.get_y() == temp_y:
                    same_point = True
                    break
        self.points_history.append(point)
        return point





