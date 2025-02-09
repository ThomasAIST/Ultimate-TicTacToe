# 31/12/2024 - 
import copy
import math
import random


# ZOBRIST_HASHING_TABLE = [[random.randint(0, math.pow(2, 64)) for j in range(3)] for i in range(81)]


class DPStation:
    ZOBRIST_HASHING_TABLE = [[random.randint(0, 2**64) for j in range(3)] for i in range(81)]

    def __init__(self) -> None:
        # self.minimax_dp = [{} for x in range(81)]
        self.status_dp = {}
        self.heuristic_dp = {}
        self.observe_dp = {}

    @classmethod
    def board_hashing(cls, board_cells: list[str]) -> int:
        """Calculate the hash value of the board"""
        return ''.join(board_cells)
        # if isinstance(board_cells[0], str):
            # board_map = [1, 10, 1, 10, 25, 10, 1, 10, 1]
            # cell_value = []
            # for x in board_cells:
            #     if x == 'O':
            #         cell_value.append(1)
            #     elif x == 'X':
            #         cell_value.append(100)
            #     elif x == 'T':
            #         cell_value.append(100000)
            #     else:
            #         cell_value.append(0)

            # adjacent_link, hollow_link = 0, 0
            # for i in range(3):
            #     tem = cell_value[i*3:(i+1)*3]
            #     adjacent_link += tem[0] * tem[1]
            #     adjacent_link += tem[1] * tem[2]
            #     hollow_link += tem[0] * tem[2]
            # for i in range(3):
            #     tem = cell_value[i::3]
            #     adjacent_link += tem[0] * tem[1]
            #     adjacent_link += tem[1] * tem[2]
            #     hollow_link += tem[0] * tem[2]

            # hash_key = {'pos': sum(map(lambda x, y: x*y, cell_value, board_map)), 'adj': adjacent_link, 'hol': hollow_link}
            # return frozenset(hash_key.items())
        value = 0
        for i in range(len(board_cells)):
            # for j in range(3):
            if board_cells[i] == 'X':
                tem = 0
            elif board_cells[i] == 'O':
                tem = 1
            else:
                tem = 2
            # tem = (board_cells[i] == 'X')
            value ^= cls.ZOBRIST_HASHING_TABLE[i][tem]
        return value
        
        # cell_value = []
        # for x in board_cells:
        #     tem = []
        #     for y in x:
        #         if y == 'O':
        #             tem.append(1)
        #         elif y == 'X':
        #             tem.append(1000)
        #         else:
        #             tem.append(0)
        #     cell_value.append(tem)
        
        # hash_key = {x:0 for x in range(1, 9)}
        # for i in range(9):
        #     for j in range(9):
        #         x = i if i < 4 else 8-i
        #         y = i if j < 4 else 8-j
        #         x, y = str(x), str(y)
        #         if x+y in hash_key:
        #             hash_key[x+y] += cell_value[i][j]
        #         elif y+x in hash_key:
        #             hash_key[y+x] += cell_value[i][j]
        #         else:
        #             hash_key[x+y] = cell_value[i][j]

        # for i in range(9):
        #     for j in range(9):
        #         for k in range(j+1, 9):
        #             hash_key[k-j] += cell_value[i][j]*cell_value[i][k]
        #             # tem = cell_value[i*3:(i+1)*3]
        #             # adjacent_link += tem[0] * tem[1]
        #             # adjacent_link += tem[1] * tem[2]
        #             # hollow_link += tem[0] * tem[2]
        
        # for i in range(9):
        #     for j in range(9):
        #         for k in range(j+1, 9):
        #             hash_key[k-j] += cell_value[j][i]*cell_value[k][i]   

        # return frozenset(hash_key.items())

        # def rotate(cells: list[list]) -> list[list]:
        #     # row, rotated = [], []
        #     # for i in range(len(cells)):
        #     #     for j in range(len(cells)-1, -1):
        #     #         row.append(cells[j][i])
        #     #     rotated.append(copy.deepcopy(row))
        #     return [[cells[y][x] for y in range(len(cells)-1, -1, -1)] for x in range(len(cells))]
        
        # def flip(cells: list[list]) -> list[list]:
        #     return [[cells[y][x] for y in range(len(cells))] for x in range(len(cells))]
        
        # def hashing(cells: list[list]) -> str:
        #     return ''.join([''.join(cells[x]) for x in range(len(cells))])

        # hash_key, tem = [board_cells, flip(board_cells)], board_cells
        # for i in range(3):
        #     tem = rotate(tem)
        #     hash_key.append(tem)
        #     tem = flip(tem)
        #     hash_key.append(tem)
        # # print(hash_key)
        
        # tem = [hashing(x) for x in hash_key]
        # # for i in range(len(tem)-1, 0, -1):
        # #     if tem[i] < tem[i-1]:
        # #         tem[i-1], tem[i] = tem[i], tem[i-1]
        # # for x in tem:
        # #     print(x)
        # # print(tem)
        # # tem.sort()
        # return min(tem)

        def rotate(cells: list[list]) -> list[list]:
            return [[cells[y][x] for y in range(len(cells)-1, -1, -1)] for x in range(len(cells))]
        
        def flip(cells: list[list]) -> list[list]:
            return [[cells[y][x] for y in range(len(cells))] for x in range(len(cells))]

        def hashing(cells: list[list]) -> str:
            value = 0
            for i in range(9):
                for j in range(9):
                    # if cells[i][j] == 'X':
                    #     tem = 0
                    # elif cells[i][j] == 'O':
                    #     tem = 1
                    # else:
                    #     tem = 2
                    tem = (cells[i][j] == 'X')
                    value ^= cls.ZOBRIST_HASHING_TABLE[i*9+j][tem]
            return value

        # hash_key, tem = [board_cells, flip(board_cells)], board_cells
        # for i in range(3):
        #     tem = rotate(tem)
        #     hash_key.append(tem)
        #     tem = flip(tem)
        #     hash_key.append(tem)
        # # print(hash_key)
        
        # tem = [hashing(x) for x in hash_key]
        # tem.sort()
        # return tem[0]
        return hashing(board_cells)

    @classmethod
    def state_hashing(cls, value: int, x: int, y: int, mark: int) -> int:
        """Calculate the hash value of the game state"""
        # if value == -1:
        #     value = sum(x[2] for x in cls.ZOBRIST_HASHING_TABLE)
        tem = x * 9 + y
        # value ^= cls.ZOBRIST_HASHING_TABLE[tem][2]
        value ^= cls.ZOBRIST_HASHING_TABLE[tem][mark]
        return value