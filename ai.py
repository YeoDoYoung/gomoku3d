"""
3D Gomoku Game - AI Player
3D 오목 게임 - AI 플레이어

이 파일은 AI 플레이어의 로직을 구현합니다.
Minimax 알고리즘과 알파-베타 가지치기를 사용하여 최적의 수를 계산합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

import random
import numpy as np

class AI:
    """
    AI 플레이어 클래스 - 게임 AI 로직
    
    AI가 게임에서 최적의 수를 계산하는 로직을 구현합니다:
    - Minimax 알고리즘
    - 알파-베타 가지치기
    - 위치 평가 함수
    """
    
    def __init__(self, depth=2, difficulty='Normal'):
        """
        AI 초기화
        
        Args:
            depth (int): 탐색 깊이 (기본값: 3)
            
        AI의 탐색 깊이와 평가 함수를 초기화합니다.
        """
        self.depth = depth
        self.difficulty = difficulty  # 'Easy', 'Normal', 'Hard'
        self.player = 2  # AI는 백돌 (플레이어 2)
        self.opponent = 1  # 상대는 흑돌 (플레이어 1)
    
    def get_best_move(self, board):
        """
        최적의 수 계산
        
        Args:
            board: Board 클래스 인스턴스
            
        Returns:
            tuple: 최적의 수 좌표 (x, y) 또는 None
            
        Minimax 알고리즘을 사용하여 최적의 수를 계산합니다.
        """
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            return None
        
        # Easy 모드: 즉시 승리/즉시 패배(막기) 우선, 그 외엔 랜덤
        if self.difficulty == 'Easy':
            # 1. AI가 이길 수 있는 수
            for x, y in valid_moves:
                board.place_stone(x, y, self.player)
                if board.check_win(x, y, self.player):
                    board.board[y][x] = 0
                    return (x, y)
                board.board[y][x] = 0
            # 2. 상대가 이길 수 있는 수 막기
            for x, y in valid_moves:
                board.place_stone(x, y, self.opponent)
                if board.check_win(x, y, self.opponent):
                    board.board[y][x] = 0
                    return (x, y)
                board.board[y][x] = 0
            # 3. 랜덤
            return random.choice(valid_moves)
        # Normal 모드: depth=1
        if self.difficulty == 'Normal':
            return self._minimax_move(board, depth=1)
        # Hard 모드: depth=3
        if self.difficulty == 'Hard':
            return self._minimax_move(board, depth=3)
        # 기본값: Normal
        return self._minimax_move(board, depth=2)

    def _minimax_move(self, board, depth):
        """
        Minimax 알고리즘 (알파-베타 가지치기 포함)
        
        Args:
            board: Board 클래스 인스턴스
            depth (int): 남은 탐색 깊이
            is_maximizing (bool): 최대화 플레이어인지 여부
            alpha (float): 알파 값
            beta (float): 베타 값
            
        Returns:
            float: 평가 점수
            
        Minimax 알고리즘으로 게임 트리를 탐색하고 최적의 수를 찾습니다.
        """
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            return None
        
        best_score = float('-inf')
        best_move = None
        
        # 모든 유효한 수에 대해 평가
        for move in valid_moves:
            x, y = move
            # 임시로 수를 놓아보기
            board.place_stone(x, y, self.player)
            
            # Minimax로 점수 계산
            score = self.minimax(board, depth - 1, False, float('-inf'), float('inf'))
            
            # 수 되돌리기
            board.board[y][x] = 0
            
            # 최고 점수 업데이트
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        """
        Minimax 알고리즘 (알파-베타 가지치기 포함)
        
        Args:
            board: Board 클래스 인스턴스
            depth (int): 남은 탐색 깊이
            is_maximizing (bool): 최대화 플레이어인지 여부
            alpha (float): 알파 값
            beta (float): 베타 값
            
        Returns:
            float: 평가 점수
            
        Minimax 알고리즘으로 게임 트리를 탐색하고 최적의 수를 찾습니다.
        """
        # 종료 조건: 깊이 도달 또는 게임 종료
        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board)
        
        valid_moves = board.get_valid_moves()
        
        if is_maximizing:
            # 최대화 플레이어 (AI)
            max_score = float('-inf')
            for move in valid_moves:
                x, y = move
                board.place_stone(x, y, self.player)
                score = self.minimax(board, depth - 1, False, alpha, beta)
                board.board[y][x] = 0  # 수 되돌리기
                
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                
                # 알파-베타 가지치기
                if beta <= alpha:
                    break
            return max_score
        else:
            # 최소화 플레이어 (상대)
            min_score = float('inf')
            for move in valid_moves:
                x, y = move
                board.place_stone(x, y, self.opponent)
                score = self.minimax(board, depth - 1, True, alpha, beta)
                board.board[y][x] = 0  # 수 되돌리기
                
                min_score = min(min_score, score)
                beta = min(beta, score)
                
                # 알파-베타 가지치기
                if beta <= alpha:
                    break
            return min_score
    
    def is_game_over(self, board):
        """
        게임 종료 여부 확인
        
        Args:
            board: Board 클래스 인스턴스
            
        Returns:
            bool: 게임이 종료되었는지 여부
            
        승리 조건 달성 또는 바둑판 가득 참을 확인합니다.
        """
        # 바둑판이 가득 찬 경우
        if board.is_full():
            return True
        
        # 승리 조건 확인
        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] != 0:
                    if board.check_win(x, y, board.board[y][x]):
                        return True
        
        return False
    
    def evaluate_board(self, board):
        """
        바둑판 상태 평가
        
        Args:
            board: Board 클래스 인스턴스
            
        Returns:
            float: 평가 점수 (양수: AI 유리, 음수: 상대 유리)
            
        현재 바둑판 상태를 평가하여 점수를 계산합니다.
        """
        score = 0
        
        # 각 위치의 돌을 평가
        for y in range(board.size):
            for x in range(board.size):
                if board.board[y][x] != 0:
                    player = board.board[y][x]
                    position_score = self.evaluate_position(board, x, y, player)
                    
                    # AI 돌이면 양수, 상대 돌이면 음수
                    if player == self.player:
                        score += position_score
                    else:
                        score -= position_score
        
        return score
    
    def evaluate_position(self, board, x, y, player):
        """
        특정 위치의 돌 평가
        
        Args:
            board: Board 클래스 인스턴스
            x (int): x 좌표
            y (int): y 좌표
            player (int): 플레이어 (1 또는 2)
            
        Returns:
            float: 위치 점수
            
        특정 위치의 돌이 얼마나 유용한지 평가합니다.
        연속된 돌의 개수와 막힌 끝의 개수를 고려합니다.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선
        total_score = 0
        
        for dx, dy in directions:
            # 양방향으로 연속된 돌 개수 확인
            count = 1  # 현재 돌 포함
            blocked = 0  # 막힌 끝의 개수
            
            # 정방향 확인
            nx, ny = x + dx, y + dy
            while 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[ny][nx] == player:
                    count += 1
                elif board.board[ny][nx] != 0:
                    blocked += 1
                    break
                else:
                    break
                nx += dx
                ny += dy
            
            # 역방향 확인
            nx, ny = x - dx, y - dy
            while 0 <= nx < board.size and 0 <= ny < board.size:
                if board.board[ny][nx] == player:
                    count += 1
                elif board.board[ny][nx] != 0:
                    blocked += 1
                    break
                else:
                    break
                nx -= dx
                ny -= dy
            
            # 점수 계산
            score = self.calculate_line_score(count, blocked)
            total_score += score
        
        return total_score
    
    def calculate_line_score(self, count, blocked):
        """
        연속된 돌의 점수 계산
        
        Args:
            count (int): 연속된 돌의 개수
            blocked (int): 막힌 끝의 개수
            
        Returns:
            float: 점수
            
        연속된 돌의 개수와 막힌 끝의 개수에 따라 점수를 계산합니다.
        """
        # 승리 조건 (5개 연속)
        if count >= 5:
            return 100000
        
        # 막힌 끝이 2개면 점수 없음
        if blocked == 2:
            return 0
        
        # 점수 계산 (연속된 돌 개수에 따라 지수적으로 증가)
        base_score = 10 ** (count - 1)
        
        # 막힌 끝이 1개면 점수 절반
        if blocked == 1:
            base_score //= 2
        
        return base_score
    
    def get_random_move(self, board):
        """
        랜덤 수 계산 (간단한 AI)
        
        Args:
            board: Board 클래스 인스턴스
            
        Returns:
            tuple: 랜덤한 수 좌표 (x, y) 또는 None
            
        유효한 수 중에서 랜덤하게 선택합니다.
        """
        valid_moves = board.get_valid_moves()
        if valid_moves:
            return random.choice(valid_moves)
        return None 