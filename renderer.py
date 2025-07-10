"""
3D Gomoku Game - 3D Renderer
3D 오목 게임 - 3D 렌더러

이 파일은 3D 바둑판을 렌더링하고, 우측 1/4에 메뉴 패널을 표시합니다.
좌측 3/4는 바둑판, 우측 1/4는 설정/정보/버튼 UI를 담당합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

import pygame
import numpy as np
from utils import COLORS, board_to_screen_pos, draw_text, get_stone_color

class Renderer:
    def __init__(self, screen_width: int = 1400, screen_height: int = 900):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_size = 15
        self.update_layout()
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 28)
        self.info_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 16)

    def update_layout(self):
        # 좌측 3/4 바둑판, 우측 1/4 메뉴
        self.board_area_width = int(self.screen_width * 0.75)
        self.menu_area_width = self.screen_width - self.board_area_width
        self.board_width = min(self.board_area_width - 60, self.screen_height - 120)
        self.board_height = self.board_width
        self.board_x = (self.board_area_width - self.board_width) // 2
        self.board_y = (self.screen_height - self.board_height) // 2
        self.cell_size = self.board_width // (self.board_size + 1)
        self.menu_x = self.board_area_width
        self.menu_y = 0
        self.menu_width = self.menu_area_width
        self.menu_height = self.screen_height

    def set_screen_size(self, width: int, height: int):
        self.screen_width = width
        self.screen_height = height
        self.update_layout()

    def render_board(self, surface: pygame.Surface, board_state: np.ndarray, last_move=None):
        # 바둑판 배경
        board_rect = pygame.Rect(self.board_x, self.board_y, self.board_width, self.board_height)
        pygame.draw.rect(surface, COLORS['LIGHT_BROWN'], board_rect)
        # 격자
        self._draw_grid(surface)
        # 돌
        self._draw_stones(surface, board_state, last_move)

    def _draw_grid(self, surface: pygame.Surface):
        start_x = self.board_x + self.cell_size
        end_x = self.board_x + self.board_width - self.cell_size
        start_y = self.board_y + self.cell_size
        end_y = self.board_y + self.board_height - self.cell_size
        for i in range(self.board_size):
            y = self.board_y + (i + 1) * self.cell_size
            pygame.draw.line(surface, COLORS['BROWN'], (start_x, y), (end_x, y), 2)
        for j in range(self.board_size):
            x = self.board_x + (j + 1) * self.cell_size
            pygame.draw.line(surface, COLORS['BROWN'], (x, start_y), (x, end_y), 2)
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.board_x + (col + 1) * self.cell_size
                y = self.board_y + (row + 1) * self.cell_size
                pygame.draw.circle(surface, COLORS['BROWN'], (x, y), 3)

    def _draw_stones(self, surface: pygame.Surface, board_state: np.ndarray, last_move=None):
        stone_radius = int(self.cell_size * 0.4)
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board_state[row, col] != 0:
                    x, y = board_to_screen_pos(row, col, pygame.Rect(self.board_x, self.board_y, self.board_width, self.board_height), self.board_size)
                    stone_color = get_stone_color(board_state[row, col])
                    is_last_move = last_move and (row, col) == last_move
                    shadow_offset = 3
                    pygame.draw.circle(surface, COLORS['GRAY'], (x + shadow_offset, y + shadow_offset), stone_radius)
                    pygame.draw.circle(surface, stone_color, (x, y), stone_radius)
                    if board_state[row, col] == 2:
                        pygame.draw.circle(surface, COLORS['BLACK'], (x, y), stone_radius, 2)
                    if is_last_move:
                        pygame.draw.circle(surface, COLORS['RED'], (x, y), stone_radius + 4, 3)

    def render_main_menu(self, surface, buttons):
        surface.fill((192, 192, 192))
        draw_text(surface, "3D Gomoku", self.title_font, COLORS['BLACK'], (self.screen_width // 2, 100))
        button_w = 300
        button_h = 60
        button_gap = 40  # 간격 넓힘
        start_y = 220
        center_x = self.screen_width // 2
        btn_2p = pygame.Rect(center_x - button_w//2, start_y, button_w, button_h)
        pygame.draw.rect(surface, COLORS['GREEN'], btn_2p)
        draw_text(surface, "2 Player Mode", self.button_font, COLORS['WHITE'], btn_2p.center)
        buttons['2player'] = btn_2p
        btn_easy = pygame.Rect(center_x - button_w//2, start_y + (button_h + button_gap), button_w, button_h)
        pygame.draw.rect(surface, COLORS['BLUE'], btn_easy)
        draw_text(surface, "AI Mode (Easy)", self.button_font, COLORS['WHITE'], btn_easy.center)
        buttons['ai_easy'] = btn_easy
        btn_normal = pygame.Rect(center_x - button_w//2, start_y + 2*(button_h + button_gap), button_w, button_h)
        pygame.draw.rect(surface, COLORS['ORANGE'], btn_normal)
        draw_text(surface, "AI Mode (Normal)", self.button_font, COLORS['WHITE'], btn_normal.center)
        buttons['ai_normal'] = btn_normal
        btn_hard = pygame.Rect(center_x - button_w//2, start_y + 3*(button_h + button_gap), button_w, button_h)
        pygame.draw.rect(surface, COLORS['RED'], btn_hard)
        draw_text(surface, "AI Mode (Hard)", self.button_font, COLORS['WHITE'], btn_hard.center)
        buttons['ai_hard'] = btn_hard

    def render_settings_panel(self, surface, buttons):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0,0,0,120))
        surface.blit(overlay, (0,0))
        panel_w, panel_h = 400, 480  # 패널 높이를 늘림
        panel_x = (self.screen_width - panel_w)//2
        panel_y = (self.screen_height - panel_h)//2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(surface, COLORS['WHITE'], panel_rect)
        pygame.draw.rect(surface, COLORS['BLACK'], panel_rect, 3)
        draw_text(surface, "Settings", self.title_font, COLORS['BLACK'], (panel_x+panel_w//2, panel_y+50))
        button_w = 300
        button_h = 50
        button_gap = 32  # 간격 넓힘
        start_y = panel_y + 110
        center_x = panel_x + panel_w//2
        btn_2p = pygame.Rect(center_x - button_w//2, start_y, button_w, button_h)
        pygame.draw.rect(surface, COLORS['GREEN'], btn_2p)
        draw_text(surface, "2 Player Mode", self.button_font, COLORS['WHITE'], btn_2p.center)
        buttons['set_2player'] = btn_2p
        btn_easy = pygame.Rect(center_x - button_w//2, start_y + (button_h + button_gap), button_w, button_h)
        pygame.draw.rect(surface, COLORS['BLUE'], btn_easy)
        draw_text(surface, "AI Mode (Easy)", self.button_font, COLORS['WHITE'], btn_easy.center)
        buttons['set_ai_easy'] = btn_easy
        btn_normal = pygame.Rect(center_x - button_w//2, start_y + 2*(button_h + button_gap), button_w, button_h)
        pygame.draw.rect(surface, COLORS['ORANGE'], btn_normal)
        draw_text(surface, "AI Mode (Normal)", self.button_font, COLORS['WHITE'], btn_normal.center)
        buttons['set_ai_normal'] = btn_normal
        btn_hard = pygame.Rect(center_x - button_w//2, start_y + 3*(button_h + button_gap), button_w, button_h)
        pygame.draw.rect(surface, COLORS['RED'], btn_hard)
        draw_text(surface, "AI Mode (Hard)", self.button_font, COLORS['WHITE'], btn_hard.center)
        buttons['set_ai_hard'] = btn_hard
        btn_close = pygame.Rect(center_x - 60, panel_y + panel_h - 80, 120, 40)  # Close 버튼을 더 아래로 이동
        pygame.draw.rect(surface, COLORS['GRAY'], btn_close)
        draw_text(surface, "Close", self.button_font, COLORS['WHITE'], btn_close.center)
        buttons['close_settings'] = btn_close

    def render_menu_panel(self, surface: pygame.Surface, current_player, game_mode, ai_difficulty, game_over, winner, buttons, show_settings_btn=True):
        # 메뉴 패널 배경
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(surface, COLORS['LIGHT_GRAY'], menu_rect)
        # 타이틀
        draw_text(surface, "3D Gomoku", self.title_font, COLORS['BLACK'], (self.menu_x + self.menu_width // 2, 40))
        # 플레이어 정보
        draw_text(surface, f"Player: {'Black' if current_player == 1 else 'White'}", self.info_font, COLORS['BLACK'], (self.menu_x + self.menu_width // 2, 100))
        # 모드 정보
        draw_text(surface, f"Mode: {game_mode} ({ai_difficulty})", self.info_font, COLORS['BLACK'], (self.menu_x + self.menu_width // 2, 140))
        # 버튼들
        button_w = self.menu_width - 60
        button_h = 50
        button_y = 200
        button_gap = 20
        # New Game
        btn_new = pygame.Rect(self.menu_x + 30, button_y, button_w, button_h)
        pygame.draw.rect(surface, COLORS['GREEN'], btn_new)
        draw_text(surface, "New Game", self.button_font, COLORS['WHITE'], btn_new.center)
        buttons['new_game'] = btn_new
        # Restart
        btn_restart = pygame.Rect(self.menu_x + 30, button_y + button_h + button_gap, button_w, button_h)
        pygame.draw.rect(surface, COLORS['ORANGE'], btn_restart)
        draw_text(surface, "Restart", self.button_font, COLORS['WHITE'], btn_restart.center)
        buttons['restart'] = btn_restart
        # 승리 메시지
        if game_over and winner:
            btn_win = pygame.Rect(self.menu_x + 30, button_y + 2 * (button_h + button_gap), button_w, button_h)
            pygame.draw.rect(surface, COLORS['GOLD'], btn_win)
            draw_text(surface, f"{'Black' if winner == 1 else 'White'} Wins!", self.button_font, COLORS['BLACK'], btn_win.center)
            buttons['winner'] = btn_win
        # 우측 하단 설정(톱니바퀴) 버튼
        if show_settings_btn:
            size = 48
            margin = 20
            btn_settings = pygame.Rect(self.menu_x + self.menu_width - size - margin, self.menu_height - size - margin, size, size)
            pygame.draw.circle(surface, COLORS['DARK_GRAY'], btn_settings.center, size//2)
            pygame.draw.circle(surface, COLORS['BLACK'], btn_settings.center, size//2, 3)
            # 간단한 톱니바퀴 아이콘
            cx, cy = btn_settings.center
            for i in range(8):
                import math
                angle = i * 45
                x = cx + int((size//2-8) * math.cos(math.radians(angle)))
                y = cy + int((size//2-8) * math.sin(math.radians(angle)))
                pygame.draw.circle(surface, COLORS['BLACK'], (x, y), 4)
            buttons['settings'] = btn_settings

    def get_board_rect(self):
        """
        바둑판 영역 반환
        Returns:
            pygame.Rect: 바둑판의 화면상 영역
        """
        return pygame.Rect(self.board_x, self.board_y, self.board_width, self.board_height) 