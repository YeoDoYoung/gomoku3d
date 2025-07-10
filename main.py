#!/usr/bin/env python3
"""
3D Gomoku Game - Main Entry Point
3D 오목 게임 - 메인 진입점

이 파일은 3D 오목 게임의 시작점입니다.
게임을 초기화하고 실행하는 역할을 담당합니다.

Author: 3D Gomoku Development Team
Version: 1.0
"""

from game import Game

def main():
    """
    메인 함수 - 게임 실행의 시작점
    
    게임을 초기화하고 실행하는 메인 루프를 시작합니다.
    사용자에게 기본 조작법을 안내하고 게임 인스턴스를 생성합니다.
    """
    # 게임 시작 메시지 출력
    print("Starting 3D Gomoku Game...")
    print("Controls:")
    print("- Left click: Place stone")
    print("- ESC: Quit")
    print("- R: Reset game")
    print("- M: Toggle AI/2 Player mode")
    print()
    
    # 게임 인스턴스 생성 및 실행
    game = Game()  # Game 클래스 인스턴스 생성
    game.run()     # 게임 메인 루프 시작

if __name__ == "__main__":
    """
    스크립트가 직접 실행될 때만 main() 함수를 호출합니다.
    이 파일이 다른 모듈에서 import될 때는 실행되지 않습니다.
    """
    main() 