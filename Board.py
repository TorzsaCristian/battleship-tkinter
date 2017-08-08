from random import randint
from Ship import *


class Board:

    # Legend
    # 1-5 = ship size/index, 7 = bounds, 8 = pin and miss,  9 = pin and hit

    # map sizes
    width, heigth = 10, 10

    # initialize map array with 0
    map = []

    # ship_sizes = [5, 4, 3, 2, 1]

    # ships = []

    # 4 directions, up, right, down left
    direction = [0, 0, 1, 1]

    # assign every ship to a unique number
    current_ship_size = 5

    # ships bounds area placeholder
    bounds_placeholder = 5

    # temporary ship for user placement
    temp_ship = 0

    def __init__(self):
        self.ships = []
        self.ship_sizes = [5, 4, 3, 2, 1]
        self.current_ship_size_remaining = [5, 4, 3, 2, 1]
        self.placed_and_deleted_ships_size = []

    def set_blank_board(self):
        self.map = [[0 for x in range(self.width + 1)] for y in range(self.heigth + 1)]
        self.ship_sizes = [5, 4, 3, 2, 1]
        self.current_ship_size_remaining = [5, 4, 3, 2, 1]
        self.placed_and_deleted_ships_size = []

    def initialize(self):
        self.map = [[0 for x in range(self.width + 1)] for y in range(self.heigth + 1)]
        self.create_random_positioned_ships()
        self.placed_and_deleted_ships_size = []
        self.current_ship_size_remaining = []

    def place_ship_at_pos(self, x, y, direction):

        self.print_all_placed_ships()

        if len(self.placed_and_deleted_ships_size) + len(self.current_ship_size_remaining) == 0:
            return

        if self.check_point_available(x, y):
            if len(self.placed_and_deleted_ships_size) > 0:
                temp_size = self.placed_and_deleted_ships_size.pop()
                if self.check_if_valid_position(x, y, temp_size, direction):
                    ship = Ship(x, y, temp_size, direction)
                    self.ships.append(ship)
                    self.place_ship_on_map(ship)
                    self.assign_ship_bounds(ship)
                else:
                    self.current_ship_size_remaining.append(temp_size)
            else:
                temp_size = self.current_ship_size_remaining.pop()
                if self.check_if_valid_position(x, y, temp_size, direction):
                    ship = Ship(x, y, temp_size, direction)
                    self.ships.append(ship)
                    self.place_ship_on_map(ship)
                    self.assign_ship_bounds(ship)
                else:
                    self.current_ship_size_remaining.append(temp_size)

    def check_if_valid_position(self, x, y, size, direction):
        is_possible = True
        if self.check_point_available(x, y):
            if direction == 0:
                # up
                if y - size + 1 < 0:
                    is_possible = False
                for k in range(size-1):
                    if not self.check_point_available(x, y - k - 1):
                        is_possible = False
            elif direction == 1:
                # right
                if x + size > self.width:
                    is_possible = False
                for k in range(size-1):
                    if not self.check_point_available(x + k, y):
                        is_possible = False
        return is_possible

    def place_ship_on_map(self, ship):
        ship_x = ship.get_x()
        ship_y = ship.get_y()
        # self.map[ship_x][ship_y] = self.current_ship_size
        if ship.get_dir() == 0:
            for i in range(ship.get_size()):
                self.map[ship_x][ship_y - i] = ship.get_size()
        elif ship.get_dir() == 1:
            for i in range(ship.get_size()):
                self.map[ship_x + i][ship_y] = ship.get_size()
        elif ship.get_dir() == 2:
            for i in range(ship.get_size()):
                self.map[ship_x][ship_y + i] = ship.get_size()
        elif ship.get_dir() == 3:
            for i in range(ship.get_size()):
                self.map[ship_x - i][ship_y] = ship.get_size()

    def delete_ship(self, x, y):
        self.clear_bounds()
        for i, shp in enumerate(self.ships):
            if self.get_board_info_at_pos(x, y, ) == shp.get_size():
                print("SIZE: ", shp.get_size())
                print("SHP X Y", shp.get_x(), shp.get_y())
                for k in range(self.ships[i].get_size()):
                    if self.ships[i].get_dir() == 0:
                        self.map[self.ships[i].get_x()][self.ships[i].get_y() - k] = 0
                    elif self.ships[i].get_dir() == 1:
                        self.map[shp.get_x() + k][shp.get_y()] = 0
                self.placed_and_deleted_ships_size.append(shp.get_size())
                for j, o in enumerate(self.ships):
                    if o.get_size() == shp.get_size():
                        del self.ships[j]
                        print("CACACAACACACACACA =======", j)
                        break

        for i in range(len(self.ships)):
            self.assign_ship_bounds(self.ships[i])
        self.print_all_placed_ships()

    def create_random_positioned_ships(self):
        for i in range(len(self.ship_sizes)):
            ship_placed = 0

            print("NEW SHIP")
            while not ship_placed:
                ship_placed = 0
                is_possible = True
                temp_x = randint(0, 9)
                temp_y = randint(0, 9)

                print("TEMP_X  TEMP_Y ", temp_x, temp_y)

                if not self.check_point_available(temp_x, temp_y):
                    continue

                self.shuffle_directions()
                for j in range(len(self.direction)):
                    direction = self.direction[j]
                    print("DIRECTION" + str(direction))
                    if direction == 0:
                        # up
                        if temp_y - self.ship_sizes[i] >= 0:
                            for k in range(self.ship_sizes[i]):
                                if not self.check_point_available(temp_x, temp_y - k - 1):
                                    is_possible = False
                            if is_possible:
                                ship = Ship(temp_x, temp_y, self.ship_sizes[i], direction)
                                self.ships.append(ship)
                                self.place_ship_on_map(ship)
                                self.assign_ship_bounds(ship)
                                ship_placed = 1
                                print("X  Y ", temp_x, temp_y)
                                break
                    elif direction == 1:
                        # right
                        if self.ship_sizes[i] + temp_x < self.width:
                            for k in range(self.ship_sizes[i]):
                                if not self.check_point_available(temp_x + k + 1, temp_y):
                                    is_possible = False
                            if is_possible:
                                ship = Ship(temp_x, temp_y, self.ship_sizes[i], direction)
                                self.ships.append(ship)
                                self.place_ship_on_map(ship)
                                self.assign_ship_bounds(ship)
                                ship_placed = 1
                                print("X  Y ", temp_x, temp_y)
                                break
                    elif direction == 2:
                        # down
                        if self.ship_sizes[i] + temp_y < self.heigth:
                            for k in range(self.ship_sizes[i]):
                                if not self.check_point_available(temp_x, temp_y + k + 1):
                                    is_possible = False
                            if is_possible:
                                ship = Ship(temp_x, temp_y, self.ship_sizes[i], direction)
                                self.ships.append(ship)
                                self.place_ship_on_map(ship)
                                ship_placed = 1
                                print("X Y", temp_x, temp_y)
                                break
                    elif direction == 3:
                        # left
                        if temp_x - self.ship_sizes[i] >= 0:
                            for k in range(self.ship_sizes[i]):
                                if not self.check_point_available(temp_x - k - 1, temp_y):
                                    is_possible = False
                            if is_possible:
                                ship = Ship(temp_x, temp_y, self.ship_sizes[i], direction)
                                self.ships.append(ship)
                                self.place_ship_on_map(ship)
                                ship_placed = 1
                                print("X  Y ", temp_x, temp_y)
                                break
        self.clear_bounds()

    def assign_ship_bounds(self, ship):
        ship_x = ship.get_x()
        ship_y = ship.get_y()

        if ship.get_size() == 1:
            self.map[ship_x + 1][ship_y] = 7
            self.map[ship_x - 1][ship_y] = 7
            self.map[ship_x + 1][ship_y + 1] = 7
            self.map[ship_x - 1][ship_y + 1] = 7
            self.map[ship_x][ship_y + 1] = 7
            self.map[ship_x + 1][ship_y - 1] = 7
            self.map[ship_x - 1][ship_y - 1] = 7
            self.map[ship_x][ship_y - 1] = 7

        else:
            if ship.get_dir() == 0:
                for i in range(ship.get_size()):
                    if i == 0:
                        self.map[ship_x - 1][ship_y] = 7
                        self.map[ship_x + 1][ship_y] = 7
                        self.map[ship_x][ship_y + 1] = 7
                        self.map[ship_x - 1][ship_y + 1] = 7
                        self.map[ship_x + 1][ship_y + 1] = 7

                    elif i == ship.get_size() - 1:
                        self.map[ship_x - 1][ship_y - i - 1] = 7
                        self.map[ship_x + 1][ship_y - i - 1] = 7
                        self.map[ship_x][ship_y - i - 1] = 7
                        self.map[ship_x - 1][ship_y - i] = 7
                        self.map[ship_x + 1][ship_y - i] = 7
                    else:
                        self.map[ship_x - 1][ship_y - i] = 7
                        self.map[ship_x + 1][ship_y - i] = 7
            elif ship.get_dir() == 1:
                for i in range(ship.get_size()):
                    if i == 0:
                        self.map[ship_x][ship_y + 1] = 7
                        self.map[ship_x][ship_y - 1] = 7
                        self.map[ship_x - 1][ship_y + 1] = 7
                        self.map[ship_x - 1][ship_y] = 7
                        self.map[ship_x - 1][ship_y - 1] = 7

                    elif i == ship.get_size() - 1 and ship_x + i + 1 < self.width:
                        self.map[ship_x + i + 1][ship_y + 1] = 7
                        self.map[ship_x + i + 1][ship_y - 1] = 7
                        self.map[ship_x + i + 1][ship_y] = 7
                        self.map[ship_x + i][ship_y - 1] = 7
                        self.map[ship_x + i][ship_y + 1] = 7
                    else:
                        self.map[ship_x + i][ship_y + 1] = 7
                        self.map[ship_x + i][ship_y - 1] = 7
            elif ship.get_dir() == 2:
                for i in range(ship.get_size()):
                    pass
            elif ship.get_dir() == 3:
                for i in range(ship.get_size()):
                    pass

    def print_all_placed_ships(self):
        for i, shp in enumerate(self.ships):
            print("------- SHIP INDEX: ", i)
            print("SHIP SIZE: ", shp.get_size())
            print("SHIP X Y ", shp.get_x(), shp.get_y())
            print("SHIP DIR: ", shp.get_dir())

    # Fisher-Yates shuffle
    def shuffle_directions(self):
        # self.direction = [0, 1, 2, 3]

        for i in range(len(self.direction) - 1, -1, -1):
            j = randint(0, i)
            temp = self.direction[j]
            self.direction[j] = self.direction[i]
            self.direction[i] = temp

    def clear_bounds(self):
        for i in range(self.heigth):
            for j in range(self.width):
                if self.map[j][i] == 7:
                    self.map[j][i] = 0

    def check_point_available(self, x, y):
        if self.map[x][y] == 0:
            return True
        else:
            return False

    def get_remaining_ships(self):
        lst = self.current_ship_size_remaining + self.placed_and_deleted_ships_size
        return lst

    def pin_point_hit(self, x, y):
        # return code legend
        # HIT, DEAD, MISS

        ship_index_size = self.get_board_info_at_pos(x, y,)
        # if it hit something
        if ship_index_size != 0:
            # mark ship part as hit
            self.map[x][y] = 9
            # check if the ship with index is destroyed
            if self.check_if_ship_is_destroyed(ship_index_size):
                return "DEAD"
            return "HIT"

        self.map[x][y] = 8
        return "MISS"

    def check_if_ship_is_destroyed(self, ship_size):
        # check if the ship with ship size is destroyed
        for i in range(self.heigth):
            for j in range(self.width):
                if self.map[j][i] == ship_size:
                    # if one spot with the same  size index is found
                    # this mens that the ship is not destroyed
                    return False

        # the ship is dead
        # remove ship from active ships list
        for i, obj in enumerate(self.ships):
            if obj.get_size() == ship_size:
                del self.ships[i]
                break
        # return True, the ship is destroyed
        return True

    def print_board(self):
        # print current board for console debugging
        for i in range(self.heigth):
            for j in range(self.width):
                print(self.map[j][i], end=" ")
            print()

    def get_remaining_alive_ships(self):
        # return remaining alive ships
        return self.ships

    def get_board_size(self):
        return self.width

    def get_board_info_at_pos(self, pos_x, pos_y):
        # get the info number item at the given position
        return self.map[pos_x][pos_y]

    def check_game_over(self):
        # check if is game over
        # if a board has no more active ships
        # the game is over
        if len(self.ships) > 0:
            return False
        return True

    def get_board(self):
        return map
