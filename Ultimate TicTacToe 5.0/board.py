# 28/12/2024 - 
from helpers import DPStation
from math import pi, sqrt
import pygame


GRID_COLOR = pygame.Color('#000000')
CIRCLE_COLOR = pygame.Color('#DC143C')
CROSS_COLOR = pygame.Color('#00008B')


class Board:
    def __init__(self, x: int, y: int, width: int, height: int, thickness: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = thickness
        self.sub_width = (self.width-2*thickness) // 3
        self.sub_height = (self.height-2*thickness) // 3
        # print(x, y)
        # print(self.sub_width, self.sub_height, thickness)
        self.cells = [' ' for x in range(9)]
        # self.status_dp = {}
        # self.board_map = [1, 10, 1, 10, 25, 10, 1, 10, 1]
        # self.status = self.check_board_status()

    def check_board_status(self, dp: dict = None) -> str:
        """Determine whether the game is won, tied, or ongoing"""
        # DP for performance
        if dp is not None:
            # board_id = DPStation.board_hashing([self.cells[x*3:(x+1)*3] for x in range(3)])
            board_id = DPStation.board_hashing(self.cells)
            # cell_value = []
            # for x in self.cells:
            #     if x == 'O':
            #         cell_value.append(1)
            #     elif x == 'X':
            #         cell_value.append(100)
            #     else:
            #         cell_value.append(0)
            # board_id = sum(map(lambda x, y: x*y, cell_value, self.board_map))
            if board_id in dp:
                return dp[board_id]
            # for i in range(len(board_id)):
            #     if board_id[i] in dp:
            #         return dp[board_id[i]]
        
        for x in {'X', 'O'}:
            for i in range(3):
                if all(self.cells[i*3+j] == x for j in range(3)) or all(self.cells[j*3+i] == x for j in range(3)):
                    if dp is not None:
                        dp[board_id] = x
                    # self.status_dp[board_id] = x
                    return x
            if all(self.cells[i*4] == x for i in range(3)) or all(self.cells[(i+1)*2] == x for i in range(3)):
                if dp is not None:
                    dp[board_id] = x
                # self.status_dp[board_id] = x
                return x
            
        status = 'C' if any(x == ' ' for x in self.cells) else 'T'
        if dp is not None:
            dp[board_id] = status
        # self.status_dp[board_id] = status
        return status

    def draw_grid(self, screen: pygame.Surface) -> None:
        """Draw the 3x3 grid"""
        pygame.draw.line(screen, GRID_COLOR, (self.x, self.y+self.sub_height+self.thickness//2), (self.x+self.width-1, self.y+self.sub_height+self.thickness//2), self.thickness)
        pygame.draw.line(screen, GRID_COLOR, (self.x, self.y+2*self.sub_height+3*self.thickness//2), (self.x+self.width-1, self.y+2*self.sub_height+3*self.thickness//2), self.thickness)
        pygame.draw.line(screen, GRID_COLOR, (self.x+self.sub_width+self.thickness//2, self.y), (self.x+self.sub_width+self.thickness//2, self.y+self.height-1), self.thickness)
        pygame.draw.line(screen, GRID_COLOR, (self.x+2*self.sub_width+3*self.thickness//2, self.y), (self.x+2*self.sub_width+3*self.thickness//2, self.y+self.height-1), self.thickness)

    def create_rect(self) -> None:
        """Create Rect objects of the playing cells"""
        self.rects = [pygame.Rect(self.x+j*(self.sub_width+self.thickness), self.y+i*(self.sub_height+self.thickness), self.sub_width-1, self.sub_height-1) for i in range(3) for j in range(3)]
    
    def draw_marks(self, screen: pygame.Surface) -> None:
        """Draw the marks on the board"""
        for i in range(3):
            for j in range(3):
                if self.cells[i*3+j] == 'X':
                    self.draw_cross(screen, self.x+j*(self.sub_width+self.thickness), self.y+i*(self.sub_height+self.thickness))
                elif self.cells[i*3+j] == 'O':
                    self.draw_circle(screen, self.x+j*(self.sub_width+self.thickness), self.y+i*(self.sub_height+self.thickness))

    def draw_circle(self, screen: pygame.Surface, x: int, y: int) -> None:
        """Draw a circle on the board"""
        # square_width = sqrt(2)*self.sub_width//2
        # pygame.draw.arc(screen, CIRCLE_COLOR, [x+(self.sub_width-square_width)//2, y+(self.sub_height-square_width)//2, square_width, square_width], 0, 2*pi, self.thickness*2+1)
        radius = sqrt(2)*self.sub_width//4
        pygame.draw.circle(screen, CIRCLE_COLOR, (x+self.sub_width//2, y+self.sub_height//2), radius, self.thickness*2+1)

    def draw_cross(self, screen: pygame.Surface, x: int, y: int) -> None:
        """Draw a cross on the board"""
        pygame.draw.line(screen, CROSS_COLOR, (x+self.sub_width//4, y+self.sub_height//4), (x+3*self.sub_width//4, y+3*self.sub_height//4), self.thickness*2+1)
        pygame.draw.line(screen, CROSS_COLOR, (x+3*self.sub_width//4, y+self.sub_height//4), (x+self.sub_width//4, y+3*self.sub_height//4), self.thickness*2+1)
    
    
class GameBoard(Board):
    def __init__(self, x: int, y: int, width: int, height: int, thickness: int) -> None:
        super().__init__(x, y, width, height, thickness)
        self.sub_boards = [Board(self.x+j*(self.sub_width+self.thickness), self.y+i*(self.sub_height+self.thickness), self.sub_width, self.sub_height, self.sub_width//600*2+1) for i in range(3) for j in range(3)]
    
    def draw_shade(self, screen: pygame.Surface, last_pos: tuple[int, int], free_move: bool) -> None:
        """Draw shades to cover sub-boards"""
        for i in range(9):
            if self.cells[i] != ' ' or (not free_move and i != last_pos[1]):
                shade = pygame.Surface((self.sub_width, self.sub_height), pygame.SRCALPHA)
                colour = (0, 0, 0, 64)
                if self.cells[i] == 'X':
                    colour = (0, 0, 139, 64)
                elif self.cells[i] == 'O':
                    colour = (220, 20, 60, 64)
                elif self.cells[i] == 'T':
                    colour = (128, 0, 128, 64)
                shade.fill(colour)
                    # shade.fill((0, 0, 0, 64))
                screen.blit(shade, (self.sub_boards[i].x, self.sub_boards[i].y))

    def draw_cell_shade(self, screen: pygame.Surface, last_pos: tuple[int, int]) -> None:
        """Draw a shade to cover the last move played"""
        if last_pos != (-1, -1):
            shade = pygame.Surface((self.sub_boards[last_pos[0]].sub_width, self.sub_boards[last_pos[0]].sub_height), pygame.SRCALPHA)
            shade.fill((34, 139, 34, 64))
            screen.blit(shade, (self.sub_boards[last_pos[0]].rects[last_pos[1]]))