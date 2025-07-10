"""
3D Gomoku Game - Utility Functions
3D 오목 게임 - 유틸리티 함수

이 파일은 게임에서 사용되는 유틸리티 함수들을 제공합니다.
색상 정의, 좌표 변환, 텍스트 렌더링 등의 헬퍼 함수들을 포함합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

import pygame
import numpy as np

COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GRAY': (128, 128, 128),
    'DARK_GRAY': (64, 64, 64),
    'LIGHT_GRAY': (192, 192, 192),
    'BROWN': (139, 69, 19),
    'LIGHT_BROWN': (160, 82, 45),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'GOLD': (255, 215, 0),
    'ORANGE': (255, 165, 0),
    'PURPLE': (128, 0, 128),
    'DARK_GREEN': (0, 100, 0),
    'DARK_ORANGE': (255, 140, 0),
    'DARK_BLUE': (0, 0, 139),
    'DARK_PURPLE': (75, 0, 130)
}

def get_stone_color(player: int):
    if player == 1:
        return COLORS['BLACK']
    elif player == 2:
        return COLORS['WHITE']
    return COLORS['GRAY']

def board_to_screen_pos(row, col, board_rect, board_size):
    cell = board_rect.width / (board_size + 1)
    x = board_rect.x + (col + 1) * cell
    y = board_rect.y + (row + 1) * cell
    return int(x), int(y)

def screen_to_board_pos(screen_x, screen_y, board_rect, board_size):
    if not board_rect.collidepoint(screen_x, screen_y):
        return -1, -1
    cell = board_rect.width / (board_size + 1)
    col = round((screen_x - board_rect.x - cell) / cell)
    row = round((screen_y - board_rect.y - cell) / cell)
    if 0 <= row < board_size and 0 <= col < board_size:
        return row, col
    return -1, -1

def draw_text(surface, text, font, color, pos, align='center'):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == 'center':
        text_rect.center = pos
    elif align == 'left':
        text_rect.midleft = pos
    elif align == 'right':
        text_rect.midright = pos
    surface.blit(text_surface, text_rect)
    return text_rect 