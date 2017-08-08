from GUI import *

def main():

    player_board = Board()
    player_board.set_blank_board()

    enemy_board = Board()
    enemy_board.initialize()

    gui = GUI(player_board, enemy_board)
    gui.player_setup()

main()
