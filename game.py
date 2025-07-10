"""
3D Gomoku Game - Core Game Logic
3D 오목 게임 - 핵심 게임 로직

이 파일은 게임의 핵심 로직을 담당합니다.
게임 상태 관리, 플레이어 턴 처리, 승패 판정, 메뉴 패널/버튼 UI를 처리합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

import pygame
from board import Board
from renderer import Renderer
from ai import AI

class Game:
    def __init__(self):
        pygame.init()
        self.width = 1400
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("3D Gomoku Game (15x15)")
        self.board = Board(size=15)
        self.renderer = Renderer(self.width, self.height)
        self.game_mode = "2 Player"
        self.ai_difficulty = "Normal"  # Easy, Normal, Hard
        self.ai_player = 2
        self.ai = AI(depth=2)
        self.buttons = {}
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.game_over = False
        self.winner = None
        self.current_player = 1
        self.show_main_menu = True
        self.show_settings = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.renderer.set_screen_size(self.width, self.height)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_settings:
                        self.show_settings = False
                    elif not self.show_main_menu:
                        self.show_main_menu = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        if self.show_main_menu:
            for name, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    if name == '2player':
                        self.set_mode('2 Player', None)
                        self.show_main_menu = False
                        self.reset_game()
                        return
                    elif name == 'ai_easy':
                        self.set_mode('AI Mode', 'Easy')
                        self.show_main_menu = False
                        self.reset_game()
                        return
                    elif name == 'ai_normal':
                        self.set_mode('AI Mode', 'Normal')
                        self.show_main_menu = False
                        self.reset_game()
                        return
                    elif name == 'ai_hard':
                        self.set_mode('AI Mode', 'Hard')
                        self.show_main_menu = False
                        self.reset_game()
                        return
            return
        if self.show_settings:
            for name, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    if name == 'set_2player':
                        self.set_mode('2 Player', None)
                        self.show_settings = False
                        self.reset_game()
                        return
                    elif name == 'set_ai_easy':
                        self.set_mode('AI Mode', 'Easy')
                        self.show_settings = False
                        self.reset_game()
                        return
                    elif name == 'set_ai_normal':
                        self.set_mode('AI Mode', 'Normal')
                        self.show_settings = False
                        self.reset_game()
                        return
                    elif name == 'set_ai_hard':
                        self.set_mode('AI Mode', 'Hard')
                        self.show_settings = False
                        self.reset_game()
                        return
                    elif name == 'close_settings':
                        self.show_settings = False
                        return
            return
        # 게임 화면
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if name == 'new_game' or name == 'restart' or name == 'winner':
                    self.reset_game()
                    return
                elif name == 'settings':
                    self.show_settings = True
                    return
        # 바둑판 클릭
        board_rect = self.renderer.get_board_rect()
        board_x, board_y = self.screen_to_board(pos, board_rect)
        if board_x is not None and board_y is not None and not self.game_over:
            if self.board.is_valid_move(board_x, board_y):
                self.board.place_stone(board_x, board_y, self.current_player)
                if self.board.check_win(board_x, board_y, self.current_player):
                    self.game_over = True
                    self.winner = self.current_player
                else:
                    self.current_player = 3 - self.current_player
                    if self.game_mode == "AI Mode" and self.current_player == self.ai_player:
                        self.make_ai_move()

    def set_mode(self, mode, difficulty):
        self.game_mode = mode
        if difficulty:
            self.ai_difficulty = difficulty
        if self.game_mode == "AI Mode":
            if self.ai_difficulty == "Easy":
                self.ai = AI(depth=1, difficulty='Easy')
            elif self.ai_difficulty == "Normal":
                self.ai = AI(depth=1, difficulty='Normal')
            elif self.ai_difficulty == "Hard":
                self.ai = AI(depth=3, difficulty='Hard')
            self.ai_player = 2
        else:
            self.ai_player = None

    def screen_to_board(self, pos, board_rect):
        if not board_rect.collidepoint(pos[0], pos[1]):
            return None, None
        cell_size = board_rect.width / (self.board.size + 1)
        col = round((pos[0] - board_rect.x - cell_size) / cell_size)
        row = round((pos[1] - board_rect.y - cell_size) / cell_size)
        if 0 <= row < self.board.size and 0 <= col < self.board.size:
            return col, row
        return None, None

    def make_ai_move(self):
        ai_move = self.ai.get_best_move(self.board)
        if ai_move:
            x, y = ai_move
            self.board.place_stone(x, y, self.current_player)
            if self.board.check_win(x, y, self.current_player):
                self.game_over = True
                self.winner = self.current_player
            else:
                self.current_player = 3 - self.current_player

    def reset_game(self):
        self.board = Board(size=15)
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def update(self):
        pass

    def render(self):
        self.screen.fill((128, 128, 128))
        self.buttons = {}
        if self.show_main_menu:
            self.renderer.render_main_menu(self.screen, self.buttons)
        elif self.show_settings:
            self.renderer.render_board(self.screen, self.board.get_board_state())
            self.renderer.render_menu_panel(
                self.screen,
                self.current_player,
                self.game_mode,
                self.ai_difficulty,
                self.game_over,
                self.winner,
                self.buttons,
                show_settings_btn=False
            )
            self.renderer.render_settings_panel(self.screen, self.buttons)
        else:
            self.renderer.render_board(self.screen, self.board.get_board_state())
            self.renderer.render_menu_panel(
                self.screen,
                self.current_player,
                self.game_mode,
                self.ai_difficulty,
                self.game_over,
                self.winner,
                self.buttons,
                show_settings_btn=True
            )
        pygame.display.flip() 