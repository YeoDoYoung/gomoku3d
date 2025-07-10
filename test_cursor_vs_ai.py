"""
3D Gomoku Game - AI vs AI Test
3D 오목 게임 - AI 대전 테스트

이 파일은 AI 간의 대전을 시뮬레이션하여 AI의 성능을 테스트합니다.
두 AI가 서로 대전하여 게임의 진행과 결과를 확인합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

import pygame
import time
from board import Board
from ai import AI

def test_ai_vs_ai():
    """
    AI vs AI 대전 테스트
    
    두 AI가 서로 대전하여 게임을 진행하고 결과를 출력합니다.
    게임의 진행 상황을 실시간으로 확인할 수 있습니다.
    """
    print("Starting AI vs AI Test...")
    print("=" * 50)
    
    # 게임 컴포넌트 초기화
    board = Board()
    ai1 = AI(depth=2)  # 흑돌 AI (플레이어 1)
    ai2 = AI(depth=3)  # 백돌 AI (플레이어 2)
    
    # AI 설정
    ai1.player = 1
    ai1.opponent = 2
    ai2.player = 2
    ai2.opponent = 1
    
    current_player = 1  # 흑돌부터 시작
    move_count = 0
    max_moves = 100  # 최대 수 제한 (무한 루프 방지)
    
    print("AI 1 (Black) vs AI 2 (White)")
    print("AI 1 depth: 2, AI 2 depth: 3")
    print()
    
    while move_count < max_moves:
        # 현재 플레이어 결정
        current_ai = ai1 if current_player == 1 else ai2
        player_name = "AI 1 (Black)" if current_player == 1 else "AI 2 (White)"
        
        print(f"Turn {move_count + 1}: {player_name}")
        
        # AI가 수 계산
        start_time = time.time()
        move = current_ai.get_best_move(board)
        calculation_time = time.time() - start_time
        
        if move is None:
            print("No valid moves available. Game ended.")
            break
        
        x, y = move
        
        # 수 실행
        board.place_stone(x, y, current_player)
        move_count += 1
        
        print(f"  Move: ({x}, {y}) - Calculation time: {calculation_time:.2f}s")
        
        # 승리 확인
        if board.check_win(x, y, current_player):
            print(f"\n🎉 {player_name} wins!")
            print(f"Total moves: {move_count}")
            return current_player
        
        # 플레이어 전환
        current_player = 3 - current_player
        
        # 바둑판 출력 (간단한 텍스트 형태)
        print("  Board state:")
        board.print_board()
        print()
        
        # 잠시 대기 (진행 상황 확인용)
        time.sleep(0.5)
    
    print("Game ended in draw (max moves reached)")
    return None

def test_ai_performance():
    """
    AI 성능 테스트
    
    다양한 깊이의 AI들이 서로 대전하여 성능을 비교합니다.
    """
    print("AI Performance Test")
    print("=" * 50)
    
    # 테스트할 AI 조합들
    test_cases = [
        ("AI Depth 1", "AI Depth 2", 1, 2),
        ("AI Depth 2", "AI Depth 3", 2, 3),
        ("AI Depth 1", "AI Depth 3", 1, 3),
    ]
    
    results = []
    
    for test_name, opponent_name, depth1, depth2 in test_cases:
        print(f"\n{test_name} vs {opponent_name}")
        print("-" * 30)
        
        # 게임 실행
        board = Board()
        ai1 = AI(depth=depth1)
        ai2 = AI(depth=depth2)
        
        ai1.player = 1
        ai1.opponent = 2
        ai2.player = 2
        ai2.opponent = 1
        
        current_player = 1
        move_count = 0
        max_moves = 50
        
        while move_count < max_moves:
            current_ai = ai1 if current_player == 1 else ai2
            
            move = current_ai.get_best_move(board)
            if move is None:
                break
            
            x, y = move
            board.place_stone(x, y, current_player)
            move_count += 1
            
            if board.check_win(x, y, current_player):
                winner = test_name if current_player == 1 else opponent_name
                print(f"Winner: {winner} (Moves: {move_count})")
                results.append((test_name, opponent_name, winner, move_count))
                break
            
            current_player = 3 - current_player
        
        if move_count >= max_moves:
            print(f"Draw (Moves: {move_count})")
            results.append((test_name, opponent_name, "Draw", move_count))
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("Performance Test Results:")
    print("=" * 50)
    
    for test_name, opponent_name, winner, moves in results:
        print(f"{test_name} vs {opponent_name}: {winner} ({moves} moves)")

if __name__ == "__main__":
    """
    스크립트가 직접 실행될 때 AI 대전 테스트를 실행합니다.
    """
    print("3D Gomoku - AI vs AI Test Suite")
    print("=" * 50)
    
    # 기본 AI 대전 테스트
    print("1. Basic AI vs AI Test")
    winner = test_ai_vs_ai()
    
    print("\n" + "=" * 50)
    
    # AI 성능 테스트
    print("2. AI Performance Test")
    test_ai_performance()
    
    print("\nTest completed!") 