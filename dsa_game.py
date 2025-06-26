import pygame
import sys
import time
import random
from enum import Enum
from typing import List, Dict, Any

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors (Retro palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

class GameState(Enum):
    MENU = 1
    LEVEL_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4
    SCOREBOARD = 5

class DSAGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("DSA Learning Adventure")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.state = GameState.MENU
        self.current_level = None
        self.score = 0
        self.high_scores = self.load_high_scores()
        
        # Level definitions
        self.levels = {
            1: {"name": "Array Basics", "time_limit": 60, "difficulty": "Easy"},
            2: {"name": "Stack Operations", "time_limit": 45, "difficulty": "Easy"},
            3: {"name": "Queue Management", "time_limit": 45, "difficulty": "Easy"},
            4: {"name": "Binary Search", "time_limit": 30, "difficulty": "Medium"},
            # Placeholders for future levels
            5: {"name": "Linked Lists", "time_limit": 40, "difficulty": "Medium", "locked": True},
            6: {"name": "Binary Trees", "time_limit": 50, "difficulty": "Medium", "locked": True},
            7: {"name": "Hash Tables", "time_limit": 35, "difficulty": "Medium", "locked": True},
            8: {"name": "Graph Traversal", "time_limit": 60, "difficulty": "Hard", "locked": True},
            9: {"name": "Dynamic Programming", "time_limit": 90, "difficulty": "Hard", "locked": True},
            10: {"name": "Sorting Algorithms", "time_limit": 45, "difficulty": "Medium", "locked": True},
        }
        
        self.running = True
        
    def load_high_scores(self):
        """Load high scores from file or return default"""
        try:
            with open('high_scores.txt', 'r') as f:
                scores = []
                for line in f:
                    name, score = line.strip().split(',')
                    scores.append((name, int(score)))
                return sorted(scores, key=lambda x: x[1], reverse=True)[:10]
        except FileNotFoundError:
            return [("CPU", 1000), ("PLAYER", 800), ("RETRO", 600)]
    
    def save_high_scores(self):
        """Save high scores to file"""
        with open('high_scores.txt', 'w') as f:
            for name, score in self.high_scores:
                f.write(f"{name},{score}\n")
    
    def add_high_score(self, name, score):
        """Add a new high score"""
        self.high_scores.append((name, score))
        self.high_scores = sorted(self.high_scores, key=lambda x: x[1], reverse=True)[:10]
        self.save_high_scores()
    
    def draw_animated_background(self):
        """Draw animated retro background"""
        current_time = pygame.time.get_ticks()
        
        # Moving grid pattern
        grid_size = 50
        offset = (current_time // 50) % grid_size
        
        for x in range(-grid_size, SCREEN_WIDTH + grid_size, grid_size):
            for y in range(-grid_size, SCREEN_HEIGHT + grid_size, grid_size):
                pygame.draw.circle(self.screen, (0, 20, 40), 
                                 (x + offset, y + offset), 2)
        
        # Floating particles
        for i in range(20):
            x = (current_time // 10 + i * 50) % SCREEN_WIDTH
            y = 100 + 50 * (i % 4) + 20 * pygame.math.Vector2(1, 0).rotate(current_time / 20 + i).y
            color_intensity = int(128 + 127 * pygame.math.Vector2(1, 0).rotate(current_time / 30 + i).x)
            color = (color_intensity // 4, color_intensity // 2, color_intensity)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 3)
    
    def draw_retro_button(self, text, x, y, width, height, color=WHITE, bg_color=None):
        """Draw a retro-style button with 3D effect"""
        # Shadow
        shadow_rect = pygame.Rect(x + 3, y + 3, width, height)
        pygame.draw.rect(self.screen, (50, 50, 50), shadow_rect)
        
        # Main button
        button_rect = pygame.Rect(x, y, width, height)
        if bg_color:
            pygame.draw.rect(self.screen, bg_color, button_rect)
        pygame.draw.rect(self.screen, color, button_rect, 3)
        
        # Text (render first to ensure visibility)
        text_surface = self.font_medium.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
        self.screen.blit(text_surface, text_rect)
        
        # Subtle highlight (reduced opacity and size to not cover text)
        highlight_rect = pygame.Rect(x + 2, y + 2, width - 4, height // 6)
        highlight_surface = pygame.Surface((width - 4, height // 6))
        highlight_surface.set_alpha(30)
        highlight_surface.fill((255, 255, 255))
        self.screen.blit(highlight_surface, (x + 2, y + 2))
        
        return button_rect
    
    def draw_persistent_scoreboard(self, screen):
        """Draw persistent scoreboard in top right corner"""
        # Scoreboard background
        score_rect = pygame.Rect(SCREEN_WIDTH - 250, 10, 240, 80)
        pygame.draw.rect(screen, (0, 0, 50), score_rect)
        pygame.draw.rect(screen, CYAN, score_rect, 2)
        
        # Current score
        score_text = f"Total Score: {self.score:,}"
        score_surface = self.font_medium.render(score_text, True, WHITE)
        screen.blit(score_surface, (SCREEN_WIDTH - 240, 25))
        
        # High score for comparison
        if self.high_scores:
            high_score = self.high_scores[0][1]
            high_text = f"High Score: {high_score:,}"
            high_surface = self.font_small.render(high_text, True, YELLOW)
            screen.blit(high_surface, (SCREEN_WIDTH - 240, 50))
            
            # Progress indicator
            if self.score > 0:
                progress = min(1.0, self.score / high_score)
                bar_width = 200
                bar_height = 8
                bar_x = SCREEN_WIDTH - 240
                bar_y = 70
                
                pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * progress), bar_height))
                pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
    
    def draw_text_centered(self, text, font, color, y_pos):
        """Draw centered text"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def handle_menu_events(self, event):
        """Handle menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Reset score when starting new game
                self.score = 0
                self.state = GameState.LEVEL_SELECT
            elif event.key == pygame.K_s:
                self.state = GameState.SCOREBOARD
            elif event.key == pygame.K_q:
                self.running = False
    
    def handle_level_select_events(self, event):
        """Handle level selection events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
            elif pygame.K_1 <= event.key <= pygame.K_4:
                level_num = event.key - pygame.K_0
                self.current_level = level_num
                self.start_level(level_num)
    
    def handle_game_over_events(self, event):
        """Handle game over events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Reset score when returning to main menu
                self.score = 0
                self.state = GameState.MENU
            elif event.key == pygame.K_r:
                # Restart current level (keep accumulated score)
                if hasattr(self, 'current_level') and self.current_level:
                    self.start_level(self.current_level)
            elif event.key == pygame.K_SPACE:
                # Go to level select (keep accumulated score)
                self.state = GameState.LEVEL_SELECT
    
    def start_level(self, level_num):
        """Start a specific level"""
        from levels import get_level_instance
        self.current_level_instance = get_level_instance(level_num)
        self.level_start_time = time.time()
        self.state = GameState.PLAYING
    
    def run(self):
        """Main game loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == GameState.MENU:
                    self.handle_menu_events(event)
                elif self.state == GameState.LEVEL_SELECT:
                    self.handle_level_select_events(event)
                elif self.state == GameState.PLAYING:
                    if hasattr(self, 'current_level_instance'):
                        self.current_level_instance.handle_event(event)
                elif self.state == GameState.SCOREBOARD:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.GAME_OVER:
                    self.handle_game_over_events(event)
            
            # Update game state
            if self.state == GameState.PLAYING and hasattr(self, 'current_level_instance'):
                result = self.current_level_instance.update()
                if result == "completed":
                    level_score = self.current_level_instance.get_score()
                    self.score += level_score
                    # Check if it's a new high score
                    if self.high_scores and self.score > self.high_scores[-1][1]:
                        self.add_high_score("PLAYER", self.score)
                    self.state = GameState.LEVEL_SELECT
                elif result == "failed":
                    self.state = GameState.GAME_OVER
            
            # Draw everything
            self.screen.fill(BLACK)
            
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.LEVEL_SELECT:
                self.draw_level_select()
            elif self.state == GameState.PLAYING:
                if hasattr(self, 'current_level_instance'):
                    self.current_level_instance.draw(self.screen)
                    # Add persistent scoreboard to all levels
                    self.draw_persistent_scoreboard(self.screen)
            elif self.state == GameState.SCOREBOARD:
                self.draw_scoreboard()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def draw_menu(self):
        """Draw main menu with enhanced graphics"""
        self.draw_animated_background()
        
        # Animated title with glow effect
        current_time = pygame.time.get_ticks()
        glow_intensity = int(50 + 30 * pygame.math.Vector2(1, 0).rotate(current_time / 500).x)
        
        # Title glow (reduced intensity to not overwhelm text)
        for offset in range(3, 0, -1):
            glow_color = (0, max(20, glow_intensity - offset * 15), max(10, glow_intensity - offset * 10))
            title_surface = self.font_large.render("DSA LEARNING ADVENTURE", True, glow_color)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2 + offset, 150 + offset))
            self.screen.blit(title_surface, title_rect)
        
        # Main title (ensure it's clearly visible)
        main_title = self.font_large.render("DSA LEARNING ADVENTURE", True, GREEN)
        title_rect = main_title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(main_title, title_rect)
        
        # Animated subtitle box
        subtitle_y = 200 + 10 * pygame.math.Vector2(1, 0).rotate(current_time / 1000).y
        title_rect = pygame.Rect(150, int(subtitle_y), 724, 80)
        
        # Gradient effect simulation (reduced intensity)
        for i in range(3):
            color_val = 20 + i * 15
            inner_rect = pygame.Rect(title_rect.x + i, title_rect.y + i, 
                                   title_rect.width - 2*i, title_rect.height - 2*i)
            pygame.draw.rect(self.screen, (0, color_val, color_val), inner_rect, 2)
        
        subtitle_text = self.font_medium.render("Master Data Structures & Algorithms", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, int(subtitle_y) + 40))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Enhanced menu buttons with better text visibility
        button_y = 320
        self.draw_retro_button("PRESS SPACE TO START", 300, button_y, 424, 50, YELLOW, (40, 40, 0))
        self.draw_retro_button("PRESS S FOR SCOREBOARD", 300, button_y + 70, 424, 50, WHITE, (20, 20, 20))
        self.draw_retro_button("PRESS Q TO QUIT", 300, button_y + 140, 424, 50, RED, (40, 0, 0))
        
        # High Scores Preview on Main Menu
        self.draw_main_menu_scoreboard()
        
        # Amazon Q Developer Attribution
        attribution_y = SCREEN_HEIGHT - 40
        attribution_rect = pygame.Rect(50, attribution_y - 10, SCREEN_WIDTH - 100, 35)
        pygame.draw.rect(self.screen, (20, 20, 50), attribution_rect)
        pygame.draw.rect(self.screen, CYAN, attribution_rect, 1)
        
        attribution_text = "Built using Amazon Q Developer CLI for AWS Games Challenge June 2025"
        attribution_surface = self.font_small.render(attribution_text, True, CYAN)
        attribution_text_rect = attribution_surface.get_rect(center=(SCREEN_WIDTH // 2, attribution_y + 7))
        self.screen.blit(attribution_surface, attribution_text_rect)
        
        # Animated decorative elements (reduced intensity)
        for i in range(10):
            angle = current_time / 1500 + i * 0.6
            x = SCREEN_WIDTH // 2 + 250 * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x
            y = SCREEN_HEIGHT // 2 + 150 * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y
            size = 2 + 1 * pygame.math.Vector2(1, 0).rotate(angle * 2 * 57.3).x
            color_intensity = int(100 + 50 * pygame.math.Vector2(1, 0).rotate(angle * 3 * 57.3).x)
            color = (color_intensity, 0, color_intensity // 2)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), max(1, int(size)))
    
    def draw_main_menu_scoreboard(self):
        """Draw a compact scoreboard on the main menu"""
        # Scoreboard background
        score_rect = pygame.Rect(50, 320, 200, 200)
        pygame.draw.rect(self.screen, (0, 0, 30), score_rect)
        pygame.draw.rect(self.screen, YELLOW, score_rect, 2)
        
        # Title
        title_text = self.font_medium.render("HIGH SCORES", True, YELLOW)
        title_rect = title_text.get_rect(center=(150, 340))
        self.screen.blit(title_text, title_rect)
        
        # Top 5 scores
        y_start = 365
        for i, (name, score) in enumerate(self.high_scores[:5]):
            y_pos = y_start + i * 25
            
            # Rank color
            if i == 0:
                color = YELLOW
            elif i == 1:
                color = (192, 192, 192)  # Silver
            elif i == 2:
                color = (205, 127, 50)   # Bronze
            else:
                color = WHITE
            
            # Score text
            score_text = f"{i+1}. {name[:6]} {score:,}"
            score_surface = self.font_small.render(score_text, True, color)
            self.screen.blit(score_surface, (65, y_pos))
        
        # Current session score if any
        if self.score > 0:
            current_rect = pygame.Rect(60, 490, 180, 25)
            pygame.draw.rect(self.screen, (0, 50, 0), current_rect)
            pygame.draw.rect(self.screen, GREEN, current_rect, 1)
            
            current_text = f"Current: {self.score:,}"
            current_surface = self.font_small.render(current_text, True, GREEN)
            current_text_rect = current_surface.get_rect(center=(150, 502))
            self.screen.blit(current_surface, current_text_rect)
    
    def draw_level_select(self):
        """Draw level selection screen with enhanced graphics"""
        self.draw_animated_background()
        
        # Animated header
        current_time = pygame.time.get_ticks()
        header_y = 80 + 5 * pygame.math.Vector2(1, 0).rotate(current_time / 800).y
        self.draw_text_centered("SELECT LEVEL", self.font_large, GREEN, int(header_y))
        
        # Level cards
        y_start = 180
        card_width = 900
        card_height = 45
        
        for level_num, level_info in self.levels.items():
            y_pos = y_start + (level_num - 1) * 55
            card_x = (SCREEN_WIDTH - card_width) // 2
            
            # Determine colors and status
            if level_info.get("locked", False):
                bg_color = (30, 30, 30)
                border_color = GRAY
                text_color = GRAY
                status = " [LOCKED]"
            else:
                if level_num <= 4:
                    bg_color = (0, 40, 0) if level_num <= 2 else (40, 40, 0) if level_num <= 4 else (40, 0, 0)
                    border_color = GREEN if level_num <= 2 else YELLOW if level_num <= 4 else RED
                    text_color = WHITE
                else:
                    bg_color = (20, 20, 20)
                    border_color = GRAY
                    text_color = GRAY
                
                difficulty_colors = {"Easy": GREEN, "Medium": YELLOW, "Hard": RED}
                diff_color = difficulty_colors.get(level_info['difficulty'], WHITE)
                status = f" - {level_info['difficulty']} ({level_info['time_limit']}s)"
            
            # Draw level card
            card_rect = pygame.Rect(card_x, y_pos, card_width, card_height)
            
            # Card background with gradient effect
            for i in range(3):
                inner_rect = pygame.Rect(card_x + i, y_pos + i, card_width - 2*i, card_height - 2*i)
                shade = max(0, bg_color[0] + i * 10), max(0, bg_color[1] + i * 10), max(0, bg_color[2] + i * 10)
                pygame.draw.rect(self.screen, shade, inner_rect)
            
            pygame.draw.rect(self.screen, border_color, card_rect, 3)
            
            # Level number circle
            circle_x = card_x + 30
            circle_y = y_pos + card_height // 2
            pygame.draw.circle(self.screen, border_color, (circle_x, circle_y), 18, 3)
            num_text = self.font_medium.render(str(level_num), True, text_color)
            num_rect = num_text.get_rect(center=(circle_x, circle_y))
            self.screen.blit(num_text, num_rect)
            
            # Level info
            info_text = f"{level_info['name']}{status}"
            info_surface = self.font_medium.render(info_text, True, text_color)
            self.screen.blit(info_surface, (card_x + 70, y_pos + 12))
            
            # Difficulty indicator
            if not level_info.get("locked", False):
                diff_rect = pygame.Rect(card_x + card_width - 100, y_pos + 10, 80, 25)
                diff_bg = difficulty_colors.get(level_info['difficulty'], GRAY)
                pygame.draw.rect(self.screen, diff_bg, diff_rect)
                diff_text = self.font_small.render(level_info['difficulty'], True, BLACK)
                diff_text_rect = diff_text.get_rect(center=diff_rect.center)
                self.screen.blit(diff_text, diff_text_rect)
        
        # Instructions with animated background
        inst_y = 720
        inst_rect = pygame.Rect(50, inst_y - 10, SCREEN_WIDTH - 100, 60)
        pygame.draw.rect(self.screen, (0, 0, 50), inst_rect)
        pygame.draw.rect(self.screen, CYAN, inst_rect, 2)
        
        self.draw_text_centered("Press 1-4 to select available levels", self.font_small, YELLOW, inst_y + 5)
        self.draw_text_centered("Press ESC to return to menu", self.font_small, WHITE, inst_y + 25)
    
    def draw_scoreboard(self):
        """Draw high scores with enhanced graphics"""
        self.draw_animated_background()
        
        # Animated title
        current_time = pygame.time.get_ticks()
        title_glow = int(100 + 50 * pygame.math.Vector2(1, 0).rotate(current_time / 600).x)
        
        # Title with glow
        for offset in range(3, 0, -1):
            glow_color = (0, title_glow - offset * 20, 0)
            title_surface = self.font_large.render("HIGH SCORES", True, glow_color)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2 + offset, 100 + offset))
            self.screen.blit(title_surface, title_rect)
        
        self.draw_text_centered("HIGH SCORES", self.font_large, GREEN, 100)
        
        # Scoreboard background
        board_rect = pygame.Rect(200, 180, 624, 400)
        pygame.draw.rect(self.screen, (0, 0, 30), board_rect)
        pygame.draw.rect(self.screen, CYAN, board_rect, 3)
        
        # Header
        header_rect = pygame.Rect(220, 200, 584, 40)
        pygame.draw.rect(self.screen, (0, 50, 50), header_rect)
        rank_text = self.font_medium.render("RANK", True, WHITE)
        name_text = self.font_medium.render("NAME", True, WHITE)
        score_text = self.font_medium.render("SCORE", True, WHITE)
        
        self.screen.blit(rank_text, (240, 210))
        self.screen.blit(name_text, (350, 210))
        self.screen.blit(score_text, (650, 210))
        
        # Scores with alternating backgrounds
        y_start = 250
        for i, (name, score) in enumerate(self.high_scores):
            y_pos = y_start + i * 35
            
            # Alternating row colors
            row_rect = pygame.Rect(220, y_pos - 5, 584, 30)
            row_color = (20, 20, 40) if i % 2 == 0 else (10, 10, 20)
            pygame.draw.rect(self.screen, row_color, row_rect)
            
            # Rank medal for top 3
            rank_color = YELLOW if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50) if i == 2 else WHITE
            
            # Draw rank with medal effect for top 3
            if i < 3:
                medal_x, medal_y = 250, y_pos + 10
                pygame.draw.circle(self.screen, rank_color, (medal_x, medal_y), 12)
                pygame.draw.circle(self.screen, BLACK, (medal_x, medal_y), 12, 2)
                rank_surface = self.font_small.render(str(i+1), True, BLACK)
                rank_rect = rank_surface.get_rect(center=(medal_x, medal_y))
                self.screen.blit(rank_surface, rank_rect)
            else:
                rank_surface = self.font_medium.render(f"{i+1:2d}.", True, rank_color)
                self.screen.blit(rank_surface, (240, y_pos))
            
            # Name and score
            name_surface = self.font_medium.render(name, True, WHITE)
            score_surface = self.font_medium.render(f"{score:,}", True, rank_color)
            
            self.screen.blit(name_surface, (350, y_pos))
            score_rect = score_surface.get_rect(right=750)
            score_rect.y = y_pos
            self.screen.blit(score_surface, score_rect)
        
        # Instructions
        self.draw_text_centered("Press ESC to return to menu", self.font_small, WHITE, 650)
    
    def draw_game_over(self):
        """Draw game over screen with enhanced graphics"""
        self.draw_animated_background()
        
        # Animated "GAME OVER" with dramatic effect
        current_time = pygame.time.get_ticks()
        
        # Pulsing red glow (reduced intensity)
        glow_intensity = int(100 + 50 * pygame.math.Vector2(1, 0).rotate(current_time / 300).x)
        
        # Multiple glow layers (reduced)
        for offset in range(4, 0, -1):
            glow_color = (max(50, glow_intensity - offset * 20), 0, 0)
            title_surface = self.font_large.render("GAME OVER", True, glow_color)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2 + offset, 250 + offset))
            self.screen.blit(title_surface, title_rect)
        
        # Main title
        main_title = self.font_large.render("GAME OVER", True, RED)
        title_rect = main_title.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(main_title, title_rect)
        
        # Score display with background
        score_rect = pygame.Rect(300, 350, 424, 80)
        pygame.draw.rect(self.screen, (40, 0, 0), score_rect)
        pygame.draw.rect(self.screen, RED, score_rect, 3)
        
        score_text = self.font_medium.render(f"Final Score: {self.score:,}", True, WHITE)
        score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 390))
        self.screen.blit(score_text, score_text_rect)
        
        # Check if it's a high score
        if self.high_scores and self.score > self.high_scores[-1][1]:
            high_score_text = self.font_medium.render("NEW HIGH SCORE!", True, YELLOW)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            self.screen.blit(high_score_text, high_score_rect)
        
        # Enhanced control options with better text visibility
        button_y = 480
        self.draw_retro_button("PRESS R TO RETRY", 250, button_y, 524, 50, YELLOW, (40, 40, 0))
        self.draw_retro_button("PRESS SPACE FOR LEVEL SELECT", 250, button_y + 70, 524, 50, WHITE, (20, 20, 20))
        self.draw_retro_button("PRESS ESC FOR MAIN MENU", 250, button_y + 140, 524, 50, CYAN, (0, 20, 20))
        
        # Animated failure particles (reduced intensity)
        for i in range(8):
            angle = current_time / 800 + i * 0.8
            x = SCREEN_WIDTH // 2 + 150 * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x
            y = 400 + 80 * pygame.math.Vector2(1, 0).rotate(angle * 2 * 57.3).y
            size = 1 + 2 * abs(pygame.math.Vector2(1, 0).rotate(angle * 3 * 57.3).x)
            color_intensity = int(150 + 50 * pygame.math.Vector2(1, 0).rotate(angle * 4 * 57.3).x)
            color = (color_intensity, 0, 0)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), max(1, int(size)))

if __name__ == "__main__":
    game = DSAGame()
    game.run()
