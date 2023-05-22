import pygame

BLOCK_SIZE = 30
MATRIX_SIZE = (10, 20)
MATRIX_CORNER_POS = (450, 200)
SCREEN_SIZE = (1200, 900)
NEXT_POS = (14, 3)

MENU_BG_ALPHA = 150
MENU_OPT_FONT = "couriernew"
MENU_OPT_FONTSIZE = 40
MENU_OPT_SEPARATION = 80
CURSOR_SEPARATION = 20
SELECTION_DELAY = 100

NEXT_FONT = MENU_OPT_FONT
NEXT_FONTSIZE = 30

BLOCK_FALL_DELAY = 1 #500
BLOCK_FALL_TIME = 1000
BLOCK_FALL_FAST_TIME = int(BLOCK_FALL_TIME/20)
AUTO_REPEAT_DELAY = 300
AUTO_REPEAT_TIME = int(500/MATRIX_SIZE[0])
LINE_CLEAR_DELAY = 300
LOSE_DELAY = 500

CW_KEYS = (pygame.K_x, pygame.K_UP)
CCW_KEYS = (pygame.K_z,)