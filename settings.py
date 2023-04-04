import pygame

BLOCK_SIZE = 30
MATRIX_SIZE = (10, 20)
MATRIX_CORNER_POS = (450, 200)
SCREEN_SIZE = (1200, 900)

SH_O, SH_I, SH_T, SH_J, SH_L, SH_S, SH_Z = range(7)
COLORS = [pygame.Color("yellow2"),
          pygame.Color("cyan2"),
          pygame.Color("purple3"),
          pygame.Color("orange2"),
          pygame.Color("darkblue"),
          pygame.Color("green3"),
          pygame.Color("red2")]
SHAPES = [[(4, -2), (5, -2), (4, -1), (5, -1)],
          [(3, -1), (4, -1), (5, -1), (6, -1)],
          [(4, -2), (3, -1), (4, -1), (5, -1)],
          [(5, -2), (3, -1), (4, -1), (5, -1)],
          [(3, -2), (3, -1), (4, -1), (5, -1)],
          [(4, -2), (5, -2), (3, -1), (4, -1)],
          [(3, -2), (4, -2), (4, -1), (5, -1)]]

AUTO_REPEAT_TIME = 300
AUTO_REPEAT_SPEED = int(500/MATRIX_SIZE[0])