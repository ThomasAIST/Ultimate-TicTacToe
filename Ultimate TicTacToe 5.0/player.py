# 27/12/2024 - 
from abc import abstractmethod
from board import Board, GameBoard
from helpers import DPStation
import math
import pygame
import random
from threading import Thread
import time
import timeit
import sys


class Player:
    def __init__(self, name: str, mark: str) -> None:
        self.name = name
        self.mark = mark

    @abstractmethod
    def make_move(self, game: 'TicTacToeGame') -> tuple[int, int]:
        """Return the coordinates of the selected cell"""
        pass


class Man(Player):
    def make_move(self, game: 'TicTacToeGame') -> tuple[int, int] | None:
        """Select a cell to make a move"""
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(9):
                    for j in range(9):
                        if game.gameboard.sub_boards[i].rects[j].collidepoint(event.pos):
                            return (i, j)
        return None


class Bot(Player):
    def __init__(self, name: str, mark: str, difficulty: int) -> None:
        super().__init__(name, mark)
        self.difficulty = difficulty
        self.thread = None
        self.processing = False
        self.next_move = None
        # self.heuristic_dp = {}
        # self.observe_dp = {}
        # self.board_map = [1, 10, 1, 10, 25, 10, 1, 10, 1]

    def make_move(self, game: 'TicTacToeGame') -> tuple[int, int]:
        """Calculate the best cell to make a move"""
        
        # pass
        # Find legal moves
        # legal_moves = game.find_legal_moves()
        # opponent_mark = 'X' if self.mark == 'O' else 'O'
        # # scores = []

        # for x in legal_moves:
        #     game.gameboard.sub_boards[x[0]].cells[x[1]] = self.mark
        #     status = game.gameboard.sub_boards[x[0]].check_board_status()
        #     if status != 'C':
        #         game.gameboard.cells[x[0]] = status
        #     game.last_pos = x if game.gameboard.cells[x[1]] == ' ' else (-1, -1)
        #     tem = minimax(game.gameboard, False)
        #     # scores.append()
        #     game.gameboard.sub_boards[x[0]].cells[x[1]] = ' '
        #     game.gameboard.cells[x[0]] = ' '
        #     if tem == 10:
        #         return x

        # next_move = (-1, -1)
        dp = {}
        iteration = 0
        alphaing = [0]*10
        opponent_mark = 'X' if self.mark == 'O' else 'O'
        # last_pos = game.last_pos
        def minimax(depth: int, maximum: bool, alpha: float, beta: float, state_id: int = 0) -> int:
            """Return the best score of the given gameboard"""
            nonlocal iteration
            iteration += 1
            if depth == 0:
                start = time.time()
            # print(depth)
            # else:
            
            # board_id = DPStation.board_hashing([[game.gameboard.sub_boards[x//3+y].cells[y*3+z] for y in range(3) for z in range(3)]for x in range(9)])
            # print([y for x in game.gameboard.sub_boards for y in x.cells])
            # board_id = DPStation.board_hashing([y for x in game.gameboard.sub_boards for y in x.cells])
            
            # if state_id in dp and depth != 0:
            #     return dp[state_id]
            # # assert(board_id is not None)
            # if board_id in game.dp_station.minimax_dp[game.step+depth] and depth != 0:
            #     return game.dp_station.minimax_dp[game.step+depth][board_id]

            # board_id.sort()
            # for i in range(len(board_id)):
            #     # print(i)
            #     if board_id[i] in game.dp_station.minimax_dp:
            #         # print('done')
            #         if depth != 0:
            #             return game.dp_station.minimax_dp[board_id[i]]
            # if depth != 0 and board_id[0] in game.dp_station.minimax_dp:
            #     return game.dp_station.minimax_dp[board_id[0]]
                    
            # status = gameboard.check_board_status()
            # if status == self.mark:
            #     return 10
            # elif status == 'T':
            #     return 0
            # elif status == opponent_mark:
            #     return -10
            if game.gameboard.check_board_status(game.dp_station.status_dp) != 'C' or depth == self.difficulty:
                # test1 = time.time()

                tem = self.heuristic(game.gameboard, self.mark, game.dp_station.status_dp, game.dp_station.heuristic_dp, game.dp_station.analyse_dp)
                # print('timeit', timeit.timeit(lambda: Bot.heuristic(game.gameboard, self.mark), number=10000))
                # test2 = time.time()
                # print('heuristics time:', test2-test1)
                # game.dp_station.minimax_dp[board_id[0]] = tem
                # game.dp_station.minimax_dp[game.step+depth][board_id] = tem
                dp[state_id] = tem
                return tem

            # Find legal moves
            legal_moves = game.find_legal_moves()
            # if game.last_pos == (-1, -1):
            #     for i in range(9):
            #         if game.gameboard.cells[i] == ' ':
            #             for j in range(9):
            #                 if game.gameboard.sub_boards[i].cells[j] == ' ':
            #                     legal_moves.append((i, j))
            # else:
            #     for i in range(9):
            #         if game.gameboard.sub_boards[game.last_pos[1]].cells[i] == ' ':
            #             legal_moves.append((game.last_pos[1], i))
            # test1= time.time()
            scores = []
            # best_score = float('-inf') if maximum else float('inf')
            # if depth<3:
            #     print('legal moves',legal_moves)
            mark = self.mark if maximum else opponent_mark
            mark_num = 0 if mark == 'X' else 1
            if depth == 0:
                print(legal_moves)
            best_score = float('-inf') if maximum else float('inf')
            for x in legal_moves:
                
                game.gameboard.sub_boards[x[0]].cells[x[1]] = mark
                # if maximum:
                #     gameboard.sub_boards[x[0]].cells[x[1]] = self.mark
                # else:
                #     gameboard.sub_boards[x[0]].cells[x[1]] = opponent_mark
                status = game.gameboard.sub_boards[x[0]].check_board_status(game.dp_station.status_dp)
                if status != 'C':
                    game.gameboard.cells[x[0]] = status
                pos, free_move = game.last_pos, game.free_move
                game.last_pos = x
                game.free_move = (game.gameboard.cells[x[1]] != ' ')
                new_state_id = DPStation.state_hashing(state_id, x[0], x[1], mark_num)
                scores.append(minimax(depth+1, not maximum, alpha, beta, new_state_id))
                # if scores[-1] > -14:
                #     print(depth, x, legal_moves)
                #     print(pos, free_move)
                #     if scores[-1] > 0:
                        
                #         sys.exit()
                if depth == 0 and x == (4, 1):
                    # print()
                    print('haha')
                # if depth == 0 and x == (4, 2):
                #     # print()
                #     sys.exit()
                    

                game.gameboard.sub_boards[x[0]].cells[x[1]] = ' '
                game.gameboard.cells[x[0]] = ' '
                game.last_pos, game.free_move = pos, free_move
                # if len(scores) == 1:
                #     best_score = scores[-1]
                if maximum:
                    best_score = max(best_score, scores[-1])
                else:
                    best_score = min(best_score, scores[-1])
                if maximum:
                    if best_score > beta:
                        # nonlocal alphaing
                        alphaing[depth]+=1
                        break
                    alpha = max(alpha, best_score)
                    # alpha = max(alpha, scores[-1])
                else:
                    if best_score < alpha:
                        # nonlocal alphaing
                        alphaing[depth]+=1
                        break
                    beta = min(beta, best_score)
                    # beta = min(beta, scores[-1]) 
                # if alpha > beta:
                #     # print('alphaing',depth, x)
                #     nonlocal alphaing
                #     alphaing[depth]+=1
                #     break    
                # if depth != 0 and ((maximum and scores[-1] == 100) or (not maximum and scores[-1] == -100)):
                #     best_score = scores[-1]
                #     break
            # test2 = time.time()
            # if depth<3:
            #     print('forloop',depth, test2-test1)
                # print(legal_moves)
            # else:
            #     best_score = max(scores) if maximum else min(scores)
            
            
            # best_score = alpha if maximum else beta
            # nonlocal best_score
            # best_score = max(scores) if maximum else min(scores)
            # if depth == 1 and (24.413 in scores or 26.225 == best_score):
            #     print(best_score, 'clickclick', scores)

            # if depth == 2 and (24.413 == best_score or 26.225 == best_score):
            #     print(2, best_score, 'clickclick', scores, legal_moves)
            # if depth == 2:
            #     print('cccccccccccccccccccclick', best_score, scores)
            # if depth == 3:
            #     print(best_score, 'click', scores)
            # if depth == 4:
            #     print(scores, best_score)
            if depth == 0:
                # nonlocal next_move
                self.next_move = random.choice([legal_moves[i] for i in range(len(scores)) if scores[i] == best_score])
                print('caled next move', self.next_move, best_score, scores)
                end = time.time()
                print('minimax time', end-start)
                print('iteration', iteration)
                print('dp', len(dp), alphaing)
                # print('heuristic dp', self.heuristic_dp)
                # print('observe dp', self.observe_dp)
            # for i in range(len(scores)):
            #     if scores[i] == best_score:
            #         nonlocal next_move
            #         next_move = legal_moves[i]
            # game.dp_station.minimax_dp[board_id[0]] = best_score
            # game.dp_station.minimax_dp[game.step+depth][board_id] = best_score
            dp[state_id] = best_score
            return best_score
        if not self.processing:
            self.processing = True
            self.thread = Thread(target=minimax, args=[0, True, float('-inf'), float('inf')])
            self.thread.daemon = True
            self.thread.start()
            # thread.join()
        next_move = self.next_move
        if self.next_move is not None:
            self.processing = False
            self.next_move = None
        return next_move
        # print('minimax result', minimax(0, True))
        # return next_move
    
    def heuristic(self, gameboard: GameBoard, mark: str, status_dp: dict = None, heuristic_dp: dict = None, analyse_dp: dict = None) -> int:
        """Calculate the heuristic value of a gameboard"""
        # DP for performance
        if heuristic_dp is not None:
            # board_id = DPStation.board_hashing([gameboard.cells[x*3:(x+1)*3] for x in range(3)])
            # board_id = DPStation.board_hashing(gameboard.cells)
            # board_id = DPStation.board_hashing([[gameboard.sub_boards[x//3+y].cells[y*3+z] for y in range(3) for z in range(3)]for x in range(9)])
            board_id = DPStation.board_hashing([y for x in gameboard.sub_boards for y in x.cells])
            # cell_value = []
            # for x in gameboard.cells:
            #     if x == 'O':
            #         cell_value.append(1)
            #     elif x == 'X':
            #         cell_value.append(100)
            #     else:
            #         cell_value.append(0)
            # board_id = sum(map(lambda x, y: x*y, cell_value, self.board_map))
            if board_id in heuristic_dp:
                return heuristic_dp[board_id]
            # for i in range(len(board_id)):
            #     if board_id[i] in heuristic_dp:
            #         return heuristic_dp[board_id[i]]
        
        opponent_mark = 'X' if mark == 'O' else 'O'

        # Return value if the board is ended
        status = gameboard.check_board_status(status_dp)
        if status == mark:
            if heuristic_dp is not None:
                heuristic_dp[board_id] = 1000
            # self.heuristic_dp[board_id] = 100
            return 1000
        elif status == opponent_mark:
            if heuristic_dp is not None:
                heuristic_dp[board_id] = -1000
            # self.heuristic_dp[board_id] = -100
            return -1000
        elif status == 'T':
            if heuristic_dp is not None:
                heuristic_dp[board_id] = 0
            # self.heuristic_dp[board_id] = 0
            return 0
        
        # Analyse
        get_sub_board_prob = [self.analyse(x, analyse_dp) for x in gameboard.sub_boards]
        get_line_prob = [[], []]
        def calculate_prob(prob: list) -> None:
            """Calcute 'get_line_prob' values"""
            get_line_prob[0].append(math.prod(x['X'] for x in prob))
            get_line_prob[1].append(math.prod(x['O'] for x in prob))
        
        for i in range(3):
            calculate_prob(get_sub_board_prob[3*i:3*i+3])
        for i in range(3):
            calculate_prob(get_sub_board_prob[i::3])
        calculate_prob(get_sub_board_prob[::4])
        calculate_prob(get_sub_board_prob[2:7:2])
        assert(len(get_line_prob[0]) == len(get_line_prob[1]) == 8)

        not_win_prob = math.prod(1-y for x in get_line_prob for y in x)
        win_related_prob = get_line_prob[0] if mark == 'X' else get_line_prob[1]
        lose_related_prob = get_line_prob[1] if mark == 'X' else get_line_prob[0]
        win_prob = sum(not_win_prob * x / (1-x) for x in win_related_prob)
        lose_prob = sum(not_win_prob * x / (1-x) for x in lose_related_prob)
        assert(0<=win_prob<=1 and 0<=lose_prob<=1)
        value = 1000 * win_prob + (-1000) * lose_prob
        value = round(value, 3)
        assert(-1000<value<1000)

        if heuristic_dp is not None:
            heuristic_dp[board_id] = value
        # self.heuristic_dp[board_id] = value
        # if value > -14:
        #     print(value, gameboard.cells)
        #     tem = [[gameboard.sub_boards[x//3*3+y].cells[x%3*3+z] for y in range(3) for z in range(3)]for x in range(9)]
        #     for x in tem:
        #         print(x)
            # return None
        if [x.cells for x in gameboard.sub_boards] == [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
    [' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' '],
    ['X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'O', ' ', 'X', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
]:
            print(value, 'hahahahah')
        # if value == 24.413:
        #     print('wtf')
        return value

    # def observe(self, gameboard: GameBoard, mark: str, dp: dict = None) -> int:
    #     """Calculate the number of ways to win if another mark is placed"""
    #     # DP for performance
    #     if dp is not None:
    #         # board_id = DPStation.board_hashing([gameboard.cells[x*3:(x+1)*3] for x in range(3)])
    #         board_id = DPStation.board_hashing(gameboard.cells)
    #         # cell_value = []
    #         # for x in gameboard.cells:
    #         #     if x == 'O':
    #         #         cell_value.append(1)
    #         #     elif x == 'X':
    #         #         cell_value.append(100)
    #         #     else:
    #         #         cell_value.append(0)
    #         # board_id = sum(map(lambda x, y: x*y, cell_value, self.board_map))
    #         if board_id in dp:
    #             return dp[board_id]
    #         # for i in range(len(board_id)):
    #         #     if board_id[i] in dp:
    #         #         return dp[board_id[i]]

    #     num = 0
    #     for i in range(9):
    #         if gameboard.cells[i] == ' ':
    #             gameboard.cells[i] = mark
    #             tem = i // 3 * 3

    #             # if all(gameboard.cells[tem+j] == mark for j in range(3)):
    #             #     num += 1
    #             # if all(gameboard.cells[i%3+j*3] == mark for j in range(3)):
    #             #     num += 1



    #             if all(x == mark for x in gameboard.cells[tem:tem+3]):
    #                 num += 1
    #             if all(x == mark for x in gameboard.cells[i%3::3]):
    #                 num += 1
    #             # for j in range(3):
    #             #     if gameboard.cells[i*3:(i+1)*3].count(mark) == 2:
    #             #         num += 1
    #             #     if gameboard.cells[i::3].count(mark) == 2:
    #             #         num += 1
    #             if all(gameboard.cells[i*4] == mark for i in range(3)):
    #                 num += 1
    #             if all(gameboard.cells[(i+1)*2] == mark for i in range(3)):
    #                 num += 1
    #             # if gameboard.cells[::4].count(mark) == 2:
    #             #     num += 1
    #             # if gameboard.cells[2:7:2].count(mark) == 2:
    #                 # num += 1
    #         # if gameboard.check_board_status() == mark:
    #             #     ans += 1



    #             gameboard.cells[i] = ' '
    #     assert(0 <= num < 8)
    #     if dp is not None:
    #         dp[board_id] = num
    #     # self.observe_dp[board_id] = num
    #     return num
    
    def analyse(self, board: Board, dp: dict = None) -> dict:
        """Analyse the probality of winning a sub board of each player"""
        # DP for performance
        if dp is not None:
            board_id = DPStation.board_hashing(board.cells)
            if board_id in dp:
                return dp[board_id]
        
        # Find the largest number of effective winning mark
        num = [0, 0]
        def count_effective_mark(line: list) -> None:
            """Count the number of effective mark in the line"""
            if 'O' not in line:
                num[0] = max(num[0], line.count('X'))
            if 'X' not in line:
                num[1] = max(num[1], line.count('O'))
        
        for i in range(3):
            count_effective_mark(board.cells[3*i:3*i+3])
        for i in range(3):
            count_effective_mark(board.cells[i::3])
        count_effective_mark(board.cells[::4])
        count_effective_mark(board.cells[2:7:2])

        adjustment = (num[0] - num[1]) * 0.5 / 3
        probability = {'X': 0.5+adjustment, 'O': 0.5-adjustment}
        assert(0<=probability['X']<=1 and 0<=probability['O']<=1)
        dp[board_id] = probability
        return probability