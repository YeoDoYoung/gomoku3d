"""
3D Gomoku Game - Board Management
3D 오목 게임 - 바둑판 관리

이 파일은 바둑판의 상태를 관리하고 승리 판정을 처리합니다.
바둑판의 크기, 돌 배치, 승리 조건 확인 등을 담당합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

import numpy as np

class Board:
    """
    바둑판 클래스 - 게임 상태 관리
    
    바둑판의 상태를 관리하고 게임 규칙을 처리합니다:
    - 바둑판 초기화
    - 돌 놓기
    - 승리 조건 확인
    - 유효한 수 확인
    """
    
    def __init__(self, size=15):
        """
        바둑판 초기화
        
        Args:
            size (int): 바둑판 크기 (기본값: 15x15)
        
        바둑판을 빈 상태로 초기화합니다.
        0: 빈 칸, 1: 흑돌, 2: 백돌
        """
        self.size = size
        # 바둑판을 2D 배열로 초기화 (0: 빈 칸)
        self.board = np.zeros((size, size), dtype=int)
        
        # 승리 조건: 5개 연속
        self.win_length = 5
    
    def is_valid_move(self, x, y):
        """
        유효한 수인지 확인
        
        Args:
            x (int): x 좌표
            y (int): y 좌표
            
        Returns:
            bool: 유효한 수인지 여부
            
        바둑판 범위 내이고 빈 칸인지 확인합니다.
        """
        # 바둑판 범위 확인
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        
        # 빈 칸인지 확인
        return self.board[y][x] == 0
    
    def place_stone(self, x, y, player):
        """
        돌 놓기
        
        Args:
            x (int): x 좌표
            y (int): y 좌표
            player (int): 플레이어 (1: 흑, 2: 백)
            
        Returns:
            bool: 돌을 놓았는지 여부
            
        지정된 위치에 돌을 놓습니다.
        """
        if self.is_valid_move(x, y):
            self.board[y][x] = player
            return True
        return False
    
    def check_win(self, x, y, player):
        """
        승리 조건 확인
        
        Args:
            x (int): 마지막으로 놓은 돌의 x 좌표
            y (int): 마지막으로 놓은 돌의 y 좌표
            player (int): 플레이어 (1: 흑, 2: 백)
            
        Returns:
            bool: 승리했는지 여부
            
        마지막으로 놓은 돌을 기준으로 8방향을 확인하여
        5개 연속이 있는지 확인합니다.
        """
        # 확인할 8방향 (가로, 세로, 대각선)
        directions = [
            (1, 0),   # 가로
            (0, 1),   # 세로
            (1, 1),   # 우하향 대각선
            (1, -1)   # 우상향 대각선
        ]
        
        for dx, dy in directions:
            # 양방향으로 연속된 돌 개수 확인
            count = 1  # 현재 돌 포함
            
            # 정방향 확인
            count += self.count_direction(x, y, dx, dy, player)
            # 역방향 확인
            count += self.count_direction(x, y, -dx, -dy, player)
            
            # 5개 이상 연속이면 승리
            if count >= self.win_length:
                return True
        
        return False
    
    def count_direction(self, x, y, dx, dy, player):
        """
        특정 방향으로 연속된 돌 개수 세기
        
        Args:
            x (int): 시작 x 좌표
            y (int): 시작 y 좌표
            dx (int): x 방향
            dy (int): y 방향
            player (int): 플레이어
            
        Returns:
            int: 연속된 돌 개수
            
        지정된 방향으로 같은 플레이어의 돌이 연속으로 몇 개 있는지 셉니다.
        """
        count = 0
        nx, ny = x + dx, y + dy
        
        # 바둑판 범위 내에서 같은 플레이어의 돌이 연속되는 동안 카운트
        while (0 <= nx < self.size and 0 <= ny < self.size and 
               self.board[ny][nx] == player):
            count += 1
            nx += dx
            ny += dy
        
        return count
    
    def get_board_state(self):
        """
        현재 바둑판 상태 반환
        
        Returns:
            numpy.ndarray: 현재 바둑판 상태
            
        바둑판의 현재 상태를 2D 배열로 반환합니다.
        """
        return self.board.copy()
    
    def get_valid_moves(self):
        """
        유효한 수 목록 반환
        
        Returns:
            list: 유효한 수들의 좌표 리스트 [(x, y), ...]
            
        현재 바둑판에서 놓을 수 있는 모든 위치를 반환합니다.
        """
        valid_moves = []
        for y in range(self.size):
            for x in range(self.size):
                if self.is_valid_move(x, y):
                    valid_moves.append((x, y))
        return valid_moves
    
    def is_full(self):
        """
        바둑판이 가득 찼는지 확인
        
        Returns:
            bool: 바둑판이 가득 찼는지 여부
            
        모든 칸에 돌이 놓여졌는지 확인합니다.
        """
        return np.all(self.board != 0)
    
    def reset(self):
        """
        바둑판 초기화
        
        바둑판을 빈 상태로 초기화합니다.
        """
        self.board = np.zeros((self.size, self.size), dtype=int)
    
    def print_board(self):
        """
        바둑판 출력 (디버깅용)
        
        현재 바둑판 상태를 콘솔에 출력합니다.
        0: 빈 칸, 1: 흑돌, 2: 백돌
        """
        print("  " + " ".join([f"{i:2}" for i in range(self.size)]))
        for y in range(self.size):
            row = f"{y:2} "
            for x in range(self.size):
                if self.board[y][x] == 0:
                    row += " ."
                elif self.board[y][x] == 1:
                    row += " ●"  # 흑돌
                else:
                    row += " ○"  # 백돌
            print(row) 