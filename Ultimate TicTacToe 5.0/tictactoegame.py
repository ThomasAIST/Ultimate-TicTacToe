# 27/12/2024 - 
from board import GameBoard
import copy
from helpers import DPStation
from player import Man, Bot
import pygame
from pygame.transform import scale
import time


BACKGROUND_COLOR = (169, 169, 169)


class TicTacToeGame:
    def __init__(self) -> None:
        # self.players = [Man('Player 1', 'X'), Bot('Player 2', 'O', 5)]# testing
        self.players = []
        self.page = 'start'#testing
        self.turn = 0
        self.last_pos = (-1, -1)    # Placeholder
        self.free_move = True
        self.status = 'Preparing'# testing
        self.next_moves = [(x, y) for x in range(9) for y in range(9)] #testing
        self.copy = None
        self.dp_station = DPStation()
        self.step = 0

    def __deepcopy__(self, memo) -> None:
        """Create a deepcopy of this class"""
        new_copy = TicTacToeGame()
        new_copy.gameboard = GameBoard(self.gameboard.x, self.gameboard.y, self.gameboard.width, self.gameboard.height, self.gameboard.thickness)
        new_copy.gameboard.cells = copy.deepcopy(self.gameboard.cells)
        new_copy.gameboard.sub_boards = copy.deepcopy(self.gameboard.sub_boards)
        new_copy.last_pos = self.last_pos
        new_copy.free_move = self.free_move
        new_copy.dp_station = self.dp_station
        new_copy.step = self.step
        return new_copy
    
    # def __deepcopy__(self, memo):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     memo[id(self)] = result
    #     for k, v in self.__dict__.items():
    #         setattr(result, k, copy.deepcopy(v, memo))
    #     return result

    def start_game(self) -> None:
        """Setup the window and start the main loop"""
        # pygame setup
        pygame.init()

        # Calculate window size for all resolutions
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        desired = 16/9
        ratio = width/height
        scaleratio = 0.9
        widthratio = 1 if width/height < desired else desired/ratio
        heightratio = ratio*9/16 if width/height < desired else 1

        self.screen_width = int(width*widthratio*scaleratio)
        self.screen_height = int(height*heightratio*scaleratio)

        self.objectratio = self.screen_width/1920*scaleratio
        self.cellwidth = int(self.objectratio*100)
        print(self.screen_width, self.screen_height, self.cellwidth)

        # Create the window & Set the name and icon
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Ultimate TicTacToe 5.0')
        
        board_width = (self.cellwidth//200*2+1)*2 + self.cellwidth*3
        thickness = board_width // 200 * 2 + 1
        gameboard_width, gameboard_height = 3*board_width+2*thickness, 3*board_width+2*thickness

        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.events = pygame.event.get()
            # print(type(events[0]))
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(BACKGROUND_COLOR)
            match self.page:
                case 'start':
                    self.draw_start_page()
                    for event in self.events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.one_player_button.collidepoint(event.pos):
                                print('single')
                                self.players = [Man('Player 1', 'X'),Bot('Player 2', 'O', 10)]
                                # self.players = [Bot('Player 2', 'O', 10),Man('Player 1', 'X')]
                            elif self.two_player_button.collidepoint(event.pos):
                                print('multi')
                                self.players = [Man('Player 1', 'X'), Man('Player 2', 'O')]
                            if len(self.players) == 2:
                                self.gameboard = GameBoard((self.screen_width-gameboard_width)//2, (self.screen_height-gameboard_height)//2, gameboard_width, gameboard_height, thickness)
                                self.page = 'game'
                                self.status = 'C'
                                self.next_moves = self.find_legal_moves()
                                # self.copy = copy.deepcopy(self)

                case 'game':
                    self.draw_game_page()
                    if self.status == 'C':
                        game = self if isinstance(self.players[self.turn], Man) else self.copy
                        # if :
                        # start = time.time()
                        pos = self.players[self.turn].make_move(game)
                        # end = time.time()
                        # print('makemove time', end-start)
                        # else:
                        #     pos = self.players[self.turn].make_move(copy.deepcopy(self))
                        # print('first', pos)
                        if pos is not None:
                            print(f'last: {self.last_pos}')
                            print(pos)
                            # if self.gameboard.cells[pos[0]] == ' ' and (pos[0] == self.last_pos[1] or self.last_pos == (-1, -1)):
                            #     if self.gameboard.sub_boards[pos[0]].cells[pos[1]] == ' ':
                            if pos in self.next_moves:  
                                self.gameboard.sub_boards[pos[0]].cells[pos[1]] = self.players[self.turn].mark
                                # self.gameboard.sub_boards[pos[0]].draw_marks(self.screen)
                                self.gameboard.draw_cell_shade(self.screen, pos)
                                self.conclude_turn(pos)
                    else:
                        for event in self.events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.play_again_button.collidepoint(event.pos):
                                    self.page = 'start'
                                    self.status = 'Preparing'
                                    self.last_pos = (-1, -1)



            # flip() the display to put your work on self.screen
            pygame.display.flip()
            clock.tick(60)  # limits FPS to 60

        # Wait all the threads to end
        # for i in range(len(self.players)):
        #     if isinstance(self.players[i], Bot):
        #         self.players[i].thread.join()
        pygame.quit()

    def draw_start_page(self) -> None:
        """Draw the start page of the game"""
        welcome_text = pygame.font.Font('freesansbold.ttf', 128).render('Ultimate TicTacToe 5.0', True, (0, 0, 0))
        welcome_text = self.rescale(welcome_text)
        self.screen.blit(welcome_text, ((self.screen_width-welcome_text.get_width())//2, (self.screen_height//2-welcome_text.get_height())//2))
        one_player_text = pygame.font.Font('freesansbold.ttf', 64).render('1 Player Game', True, (0, 0, 0))
        one_player_text = self.rescale(one_player_text)
        self.one_player_button = pygame.Rect((self.screen_width//2-one_player_text.get_width())//2, (3*self.screen_height//2-one_player_text.get_height())//2, one_player_text.get_width(), one_player_text.get_height())
        self.screen.blit(one_player_text, self.one_player_button)
        two_player_text = pygame.font.Font('freesansbold.ttf', 64).render('2 Player Game', True, (0, 0, 0))
        two_player_text = self.rescale(two_player_text)
        self.two_player_button = pygame.Rect((3*self.screen_width//2-two_player_text.get_width())//2, (3*self.screen_height//2-two_player_text.get_height())//2, two_player_text.get_width(), two_player_text.get_height())
        self.screen.blit(two_player_text, self.two_player_button)
    
    def draw_game_page(self) -> None:
        """Draw the game page of the game"""
        for x in self.gameboard.sub_boards:
            x.draw_grid(self.screen)
            x.create_rect()
            x.draw_marks(self.screen)
        self.gameboard.draw_grid(self.screen)
        self.gameboard.draw_shade(self.screen, self.last_pos, self.free_move)
        self.gameboard.draw_cell_shade(self.screen, self.last_pos)
        # if self.last_pos != (-1, -1):
        #     for i in range(9):
        #         if i != self.last_pos[1]:
        #             self.gameboard.sub_boards[i].draw_shade(self.screen)
        if self.status != 'C':
            text = f'{self.status} wins!' if self.status != 'T' else 'This game is a tie!'
            result_text = pygame.font.Font('freesansbold.ttf', 64).render(text, True, (0, 0, 0))
            result_text = self.rescale(result_text)
            self.screen.blit(result_text, (self.screen_width//2-result_text.get_width()//2, self.gameboard.y//2-result_text.get_height()//2))

            play_again_text = pygame.font.Font('freesansbold.ttf', 64).render('Play Again', True, (0, 0, 0))
            play_again_text = self.rescale(play_again_text)
            self.play_again_button = pygame.Rect(self.screen_width//2-play_again_text.get_width()//2, self.screen_height//2+(self.gameboard.y+self.gameboard.height)//2-play_again_text.get_height()//2, play_again_text.get_width(), play_again_text.get_height())
            self.screen.blit(play_again_text, self.play_again_button)
        pygame.display.update()

    def find_legal_moves(self) -> list[tuple]:
        """Find all the legal moves"""
        legal_moves = []
        # if self.last_pos == (-1, -1):
        if self.free_move:
            for i in range(9):
                if self.gameboard.cells[i] == ' ':
                    for j in range(9):
                        if self.gameboard.sub_boards[i].cells[j] == ' ':
                            legal_moves.append((i, j))
        else:
            for i in range(9):
                if self.gameboard.sub_boards[self.last_pos[1]].cells[i] == ' ':
                    legal_moves.append((self.last_pos[1], i))
        # print(legal_moves)
        return legal_moves

    def conclude_turn(self, pos: tuple[int, int]) -> None:
        """Conclude the turn and prepare switching to the next player"""
        status = self.gameboard.sub_boards[pos[0]].check_board_status(self.dp_station.status_dp)
        if status != 'C':
            self.gameboard.cells[pos[0]] = status
        self.status = self.gameboard.check_board_status(self.dp_station.status_dp)
        # if self.status != 'C':
        #     pass
        # self.gameboard.sub_boards[pos[0]].status = status
        
        # self.last_pos = pos if self.gameboard.cells[pos[1]] == ' ' else (-1, -1)
        self.last_pos = pos
        if self.status == 'C':
            self.free_move = (self.gameboard.cells[pos[1]] != ' ')
            self.next_moves = self.find_legal_moves()
            print('nextmove',self.next_moves)
            self.turn = not self.turn
            self.step += 1
            # print('minimax dp', self.dp_station.minimax_dp)
            print('status', self.dp_station.status_dp)
            print('heur', self.dp_station.heuristic_dp)
            print('obser', self.dp_station.observe_dp)
            if isinstance(self.players[self.turn], Bot):
                import time
                start = time.time()
                self.copy = copy.deepcopy(self)
                # for x in self.copy.gameboard:
                print('unsub', self.gameboard.cells)
                for x in self.copy.gameboard.sub_boards:
                    print('sub',x.cells)
                print(self.copy.find_legal_moves())
                end = time.time()
                print('copytime', end-start)
        else:
            self.free_move = True   # Unshade sub-boards that have not ended

    def rescale(self, object: pygame.Surface) -> pygame.Surface:
        """Rescale objects"""
        return scale(object, (int(object.get_width()*self.objectratio), int(object.get_height()*self.objectratio)))