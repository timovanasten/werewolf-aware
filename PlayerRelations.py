import csv
import numpy as np


class PlayerRelations:
    def __init__(self, role_csv="Roles.csv"):
        self.role_csv = role_csv
        self.role_matrices = self.__generate_matrix()

    # Generates a pair with the relation of player1 to player2
    # e.g. ["w","v"] if player 1 is a wolf an player 2 is a villager
    def generate_label_2player(self, game_id, player_id_1, player_id_2):
        role_matrix = self.__generate_matrix()[game_id - 1]
        return role_matrix[player_id_1 - 1, player_id_2 - 1]

    # Retrieves the role of a certain player during the game. Returns 'w' for wolf and 'v' for villager
    def generate_label_1player(self, game_id, player_id):
        role_matrix = self.__generate_matrix()[game_id - 1]
        return role_matrix[player_id - 1, 0][0]

    def __generate_matrix(self):
        role_matrices = []
        # Initialize 10 player matrices for games 1 to 8
        for game in range(8):
            role_matrices.append(np.empty((10, 10, 2), dtype=str))
        # Initialize 12 player matrices for games 9 to 15
        for game in range(8, 15):
            role_matrices.append(np.empty((12, 12, 2), dtype=str))
        # Retrieve the list with wolves
        wolves = self.__retrieve_wolves()
        # Fill the matrices for each game with relations
        for game in range(15):
            role_matrix = role_matrices[game]
            shape = role_matrix.shape
            for p1 in range(shape[0]):
                for p2 in range(shape[1]):
                    p1_role = "w" if p1 + 1 in wolves[game] else "v"
                    p2_role = "w" if p2 + 1 in wolves[game] else "v"
                    role_matrix[p1, p2, 0] = p1_role
                    role_matrix[p1, p2, 1] = p2_role
        return role_matrices

    # Retrieve the wolves for each game from the CSV
    def __retrieve_wolves(self):
        wolves = [None] * 15
        csv_file = csv.reader(open(self.role_csv, "rt"), delimiter=",")
        for row in csv_file:
            # if current rows 2nd value is equal to input, print that row
            for game in range(1, 16):
                if str(game) == row[1] and wolves[game - 1] is None:
                    wolves[game - 1] = (int(row[7]), int(row[8]))
                    continue
        return wolves
