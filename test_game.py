"""
3D Gomoku Game - Test Suite
3D 오목 게임 - 테스트 스위트

이 파일은 게임의 핵심 기능들을 테스트합니다.
바둑판 로직, 승리 판정, AI 동작 등을 검증합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

import unittest
from board import Board
from ai import AI

class TestBoard(unittest.TestCase):
    """
    바둑판 테스트 클래스
    
    바둑판의 기본 기능들을 테스트합니다:
    - 돌 놓기
    - 유효한 수 확인
    - 승리 판정
    """
    
    def setUp(self):
        """
        테스트 설정
        
        각 테스트 메서드 실행 전에 새로운 바둑판을 생성합니다.
        """
        self.board = Board()
    
    def test_board_initialization(self):
        """
        바둑판 초기화 테스트
        
        바둑판이 올바르게 초기화되는지 확인합니다.
        """
        # 바둑판 크기 확인
        self.assertEqual(self.board.size, 15)
        
        # 모든 칸이 빈 상태인지 확인
        for y in range(self.board.size):
            for x in range(self.board.size):
                self.assertEqual(self.board.board[y][x], 0)
    
    def test_valid_move(self):
        """
        유효한 수 테스트
        
        유효한 수와 무효한 수를 올바르게 판별하는지 확인합니다.
        """
        # 중앙에 돌 놓기 (유효한 수)
        self.assertTrue(self.board.is_valid_move(7, 7))
        
        # 범위 밖 좌표 (무효한 수)
        self.assertFalse(self.board.is_valid_move(-1, 0))
        self.assertFalse(self.board.is_valid_move(15, 0))
        self.assertFalse(self.board.is_valid_move(0, -1))
        self.assertFalse(self.board.is_valid_move(0, 15))
    
    def test_place_stone(self):
        """
        돌 놓기 테스트
        
        돌을 올바르게 놓을 수 있는지 확인합니다.
        """
        # 돌 놓기
        self.assertTrue(self.board.place_stone(7, 7, 1))
        
        # 해당 위치에 돌이 놓였는지 확인
        self.assertEqual(self.board.board[7][7], 1)
        
        # 이미 돌이 있는 위치에 다시 놓기 (실패해야 함)
        self.assertFalse(self.board.place_stone(7, 7, 2))
    
    def test_horizontal_win(self):
        """
        가로 승리 테스트
        
        가로로 5개 연속이 되었을 때 승리 판정이 올바르게 되는지 확인합니다.
        """
        # 가로로 5개 연속 놓기
        for i in range(5):
            self.board.place_stone(i, 7, 1)
        
        # 마지막 돌에서 승리 확인
        self.assertTrue(self.board.check_win(4, 7, 1))
    
    def test_vertical_win(self):
        """
        세로 승리 테스트
        
        세로로 5개 연속이 되었을 때 승리 판정이 올바르게 되는지 확인합니다.
        """
        # 세로로 5개 연속 놓기
        for i in range(5):
            self.board.place_stone(7, i, 1)
        
        # 마지막 돌에서 승리 확인
        self.assertTrue(self.board.check_win(7, 4, 1))
    
    def test_diagonal_win(self):
        """
        대각선 승리 테스트
        
        대각선으로 5개 연속이 되었을 때 승리 판정이 올바르게 되는지 확인합니다.
        """
        # 우하향 대각선으로 5개 연속 놓기
        for i in range(5):
            self.board.place_stone(i, i, 1)
        
        # 마지막 돌에서 승리 확인
        self.assertTrue(self.board.check_win(4, 4, 1))
    
    def test_no_win(self):
        """
        승리하지 않은 상황 테스트
        
        승리 조건을 만족하지 않았을 때 승리 판정이 False를 반환하는지 확인합니다.
        """
        # 4개만 연속으로 놓기
        for i in range(4):
            self.board.place_stone(i, 7, 1)
        
        # 승리하지 않았는지 확인
        self.assertFalse(self.board.check_win(3, 7, 1))

class TestAI(unittest.TestCase):
    """
    AI 테스트 클래스
    
    AI의 기본 기능들을 테스트합니다:
    - 수 계산
    - 평가 함수
    """
    
    def setUp(self):
        """
        테스트 설정
        
        각 테스트 메서드 실행 전에 새로운 AI와 바둑판을 생성합니다.
        """
        self.ai = AI()
        self.board = Board()
    
    def test_ai_initialization(self):
        """
        AI 초기화 테스트
        
        AI가 올바르게 초기화되는지 확인합니다.
        """
        self.assertEqual(self.ai.player, 2)  # AI는 백돌
        self.assertEqual(self.ai.opponent, 1)  # 상대는 흑돌
        self.assertEqual(self.ai.depth, 3)  # 기본 탐색 깊이
    
    def test_first_move(self):
        """
        첫 수 테스트
        
        AI가 첫 수를 중앙에 놓는지 확인합니다.
        """
        move = self.ai.get_best_move(self.board)
        center = self.board.size // 2
        self.assertEqual(move, (center, center))
    
    def test_random_move(self):
        """
        랜덤 수 테스트
        
        랜덤 수 계산이 올바르게 작동하는지 확인합니다.
        """
        # 몇 개의 돌을 놓은 후
        self.board.place_stone(7, 7, 1)
        self.board.place_stone(8, 8, 2)
        
        # 랜덤 수 계산
        move = self.ai.get_random_move(self.board)
        
        # 유효한 수인지 확인
        self.assertIsNotNone(move)
        self.assertTrue(self.board.is_valid_move(move[0], move[1]))

def run_tests():
    """
    테스트 실행 함수
    
    모든 테스트를 실행하고 결과를 출력합니다.
    """
    print("Running 3D Gomoku Game Tests...")
    print("=" * 50)
    
    # 테스트 스위트 생성
    test_suite = unittest.TestSuite()
    
    # 테스트 클래스들 추가
    test_suite.addTest(unittest.makeSuite(TestBoard))
    test_suite.addTest(unittest.makeSuite(TestAI))
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 결과 요약
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    """
    스크립트가 직접 실행될 때 테스트를 실행합니다.
    """
    run_tests() 