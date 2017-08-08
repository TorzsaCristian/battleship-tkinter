from tkinter import *
from Board import *
from GameLogic import GameLogic


class GUI:

    player_board = 0
    enemy_board = 0

    #always add +1 and get the direction rotation by modulo %4
    total_positions = 0

    def __init__(self, player_board, enemy_board):
        self.player_board = player_board
        self.enemy_board = enemy_board
        self.root = Tk()


    def initialize(self):
        self.player_frame = Frame(self.root)
        self.player_frame.pack(side=LEFT)

        self.enemy_frame = Frame(self.root)
        self.enemy_frame.pack(side=LEFT)

        self. menu_frame = Frame(self.root)
        self.menu_frame.pack(side=LEFT)



        # initialize GUI for player board
        divider = Label(self.player_frame, text='  \n  \n \n  \n  \n  \n  \n  \n  \n  \n')
        divider.pack(side=TOP)


        self.enemy_buttons_2d_array = [[0 for x in range(self.player_board.get_board_size() + 1)] for y in
                                       range(self.player_board.get_board_size() + 1)]

        # initialize GUI for enemy board
        for i in range(0, self.enemy_board.get_board_size()):
            for j in range(0, self.enemy_board.get_board_size()):
                b = Button(self.enemy_frame, text=' ', command=lambda x=j, y=i: self.button_click_at_pos(x, y), background="yellow")
                b.grid(row=i, column=j)
                self.enemy_buttons_2d_array[j][i] = b

        self.player_info_label = Label(self.menu_frame, text='You still have ships: ')
        self.player_info_label.pack(side=TOP)

        self.enemy_info_label = Label(self.menu_frame, text='Enemy still have ships: ')
        self.enemy_info_label.pack(side=TOP)

        greenbutton = Button(self.menu_frame, text="Restart game", command=lambda: self.restart_game(), fg="brown")
        greenbutton.pack(side=LEFT)


        self.game_logic = GameLogic(self.player_board, self.enemy_board)

    def player_setup(self):

        self.setup_frame = Frame(self.root)
        self.setup_frame.pack(side=LEFT)

        self.setup_frame.grid_rowconfigure(1, weight=1)
        self.setup_frame.grid_columnconfigure(1, weight=1)

        self.setup_help_frame = Frame(self.root)
        self.setup_help_frame.pack(side=LEFT)

        title_label = Label(self.setup_help_frame, text="Welcome to Battleship!")
        title_label.pack(side=TOP)

        help_label = Label(self.setup_help_frame, text="Click to position ship!\nClick again to delete ship and rotate!")
        help_label.pack(side=TOP)

        start_button = Button(self.setup_help_frame, text="Start!", command=lambda: self.start_button())
        start_button.pack(side=BOTTOM)

        random_button = Button(self.setup_help_frame, text="Place random!", command=lambda: self.random_button())
        random_button.pack(side=BOTTOM)

        self.player_setup_buttons_2d_array = [[0 for x in range(self.player_board.get_board_size() + 1)] for y in
                                       range(self.player_board.get_board_size() + 1)]

        # initialize GUI for player board
        for i in range(0, self.player_board.get_board_size()):
            for j in range(0, self.player_board.get_board_size()):
                    b = Button(self.setup_frame, text=' ', command=lambda x=j, y=i: self.player_setup_button_click_at_pos(x, y))
                    b.grid(row=i, column=j)
                    self.player_setup_buttons_2d_array[j][i] = b



        self.root.mainloop()


    def start_button(self):
        if len(self.player_board.get_remaining_ships()) > 0:
            msg = str("You still have to place ship with size: " + str(self.player_board.get_remaining_ships()))
            self.popup_message(msg)
        else:
            self.player_board.clear_bounds()

            self.initialize()

            self.setup_help_frame.pack_forget()
            self.setup_help_frame.destroy()

            self.set_setup_buttons_disabled()



    def random_button(self):
        del self.player_board
        self.player_board = 0
        self.player_board = Board()
        self.player_board.set_blank_board()

        self.player_board.initialize()
        self.refresh_player_setup_frame()

    def set_setup_buttons_disabled(self):
        for i in range(0, self.player_board.get_board_size()):
            for j in range(0, self.player_board.get_board_size()):
                self.player_setup_buttons_2d_array[j][i]["state"] = DISABLED

    def popup_message(self, msg):
        popup = Tk()
        popup.wm_title("Place all the ships!")
        label = Label(popup, text=msg,)
        label.pack(side="top")
        b1 = Button(popup, text="Okay", command=popup.destroy)
        b1.pack()
        popup.mainloop()

    def player_setup_button_click_at_pos(self, x, y):
        if self.player_board.get_board_info_at_pos(x, y) != 0 and self.player_board.get_board_info_at_pos(x, y) != 7:
            self.player_board.delete_ship(x, y)
            self.refresh_player_setup_frame()
        else:
            self.player_board.place_ship_at_pos(x, y, self.total_positions % 2)
            self.total_positions += 1
            self.refresh_player_setup_frame()
            self.player_board.print_board()

    def refresh_player_setup_frame(self):
        # initialize GUI for player board
        self.player_board.print_board()
        for i in range(0, self.player_board.get_board_size()):
            for j in range(0, self.player_board.get_board_size()):
                self.player_setup_buttons_2d_array[j][i]["state"] = ACTIVE
                if self.player_board.get_board_info_at_pos(j, i) == 0:
                    self.player_setup_buttons_2d_array[j][i]["text"] = " "
                elif self.player_board.get_board_info_at_pos(j, i) == 7:
                    self.player_setup_buttons_2d_array[j][i]["state"] = DISABLED
                else:
                    self.player_setup_buttons_2d_array[j][i]["text"] = "x"

    def button_click_at_pos(self, x, y):

        # player move
        self.game_logic.make_move(x, y)
        print("ENEMY BOARD =----")
        self.enemy_board.print_board()
        # AI Move
        self.game_logic.make_move(-1, -1)

        self.refresh_boards()
        self.refresh_info()

    def refresh_info(self):
        # refresh remaining ships info
        player_ships_sizes = []
        enemy_ships_sizes = []

        for i, obj in enumerate(self.player_board.get_remaining_alive_ships()):
            player_ships_sizes.append(obj.get_size())

        for i, obj in enumerate(self.enemy_board.get_remaining_alive_ships()):
            enemy_ships_sizes.append(obj.get_size())

        self.player_info_label["text"] = "You: " + str(player_ships_sizes)
        self.enemy_info_label["text"] = "Enemy: " + str(enemy_ships_sizes)

    def refresh_boards(self):
        # refresh player board
        for i in range(0, self.player_board.get_board_size()):
            for j in range(0, self.player_board.get_board_size()):
                if self.player_board.get_board_info_at_pos(j, i) == 9:
                    self.player_setup_buttons_2d_array[j][i]["text"] = 'hit'

                if self.player_board.get_board_info_at_pos(j, i) == 8:
                    self.player_setup_buttons_2d_array[j][i]["state"] = DISABLED
                    self.player_setup_buttons_2d_array[j][i]["text"] = 'o'

        # refresh enemy board
        for i in range(0, self.enemy_board.get_board_size()):
            for j in range(0, self.enemy_board.get_board_size()):
                if self.enemy_board.get_board_info_at_pos(j, i) == 9:
                    self.enemy_buttons_2d_array[j][i]["state"] = DISABLED
                    self.enemy_buttons_2d_array[j][i]["text"] = 'x'

                if self.enemy_board.get_board_info_at_pos(j, i) == 8:
                    self.enemy_buttons_2d_array[j][i]["state"] = DISABLED
                    self.enemy_buttons_2d_array[j][i]["text"] = 'o'

    def restart_game(self):
        self.setup_frame.destroy()
        self.enemy_frame.destroy()
        self.menu_frame.destroy()

        del self.player_board
        self.player_board = 0
        self.player_board = Board()
        self.player_board.set_blank_board()

        del self.enemy_buttons_2d_array
        del self.player_setup_buttons_2d_array

        del self.enemy_board
        self.enemy_board = 0
        self.enemy_board = Board()

        self.enemy_board.initialize()
        self.player_setup()
