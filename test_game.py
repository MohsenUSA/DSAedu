#!/usr/bin/env python3
"""
Quick test script to verify the game launches without crashing
"""
import pygame
import sys
import time

def test_game_launch():
    """Test that the game can launch and initialize properly"""
    try:
        # Initialize pygame
        pygame.init()
        print("✅ Pygame initialized")
        
        # Import game modules
        import dsa_game
        import levels
        print("✅ Game modules imported")
        
        # Create game instance
        game = dsa_game.DSAGame()
        print("✅ Game instance created")
        
        # Test level creation
        for i in range(1, 5):
            level = levels.get_level_instance(i)
            print(f"✅ Level {i} created: {level.__class__.__name__}")
        
        # Test game states
        print(f"✅ Initial game state: {game.state}")
        print(f"✅ High scores loaded: {len(game.high_scores)} entries")
        
        # Quick render test (create screen but don't show)
        screen = pygame.display.set_mode((100, 100))
        game.screen = screen
        
        # Test drawing functions without actually displaying
        print("✅ Testing draw functions...")
        
        # This would normally crash if there are issues
        game.draw_animated_background()
        print("✅ Animated background works")
        
        pygame.quit()
        print("🎉 All tests passed! Game is ready to run.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_game_launch()
    sys.exit(0 if success else 1)
