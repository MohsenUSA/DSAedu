import pygame
import random
import time
from abc import ABC, abstractmethod

# Colors
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

class BaseLevel(ABC):
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.start_time = time.time()
        self.score = 0
        self.completed = False
        self.failed = False
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
    
    def get_remaining_time(self):
        elapsed = time.time() - self.start_time
        return max(0, self.time_limit - elapsed)
    
    def is_time_up(self):
        return self.get_remaining_time() <= 0
    
    def get_score(self):
        # Bonus points for remaining time
        time_bonus = int(self.get_remaining_time() * 10)
        return self.score + time_bonus
    
    def draw_hud(self, screen):
        """Draw enhanced heads-up display with time and score (left side only)"""
        # HUD background (smaller to not conflict with persistent scoreboard)
        hud_rect = pygame.Rect(10, 10, 280, 100)
        pygame.draw.rect(screen, (0, 0, 50), hud_rect)
        pygame.draw.rect(screen, CYAN, hud_rect, 2)
        
        # Time display with progress bar
        remaining_time = self.get_remaining_time()
        time_text = f"Time: {int(remaining_time)}s"
        time_surface = self.font_medium.render(time_text, True, YELLOW)
        screen.blit(time_surface, (20, 20))
        
        # Time progress bar
        bar_width = 180
        bar_height = 10
        bar_x, bar_y = 20, 45
        
        # Background bar
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Progress bar
        progress = remaining_time / self.time_limit
        progress_width = int(bar_width * progress)
        
        if progress > 0.5:
            bar_color = GREEN
        elif progress > 0.25:
            bar_color = YELLOW
        else:
            bar_color = RED
            
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, progress_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Level score display (not total score - that's in persistent scoreboard)
        level_score_text = f"Level Score: {self.score:,}"
        score_surface = self.font_medium.render(level_score_text, True, WHITE)
        screen.blit(score_surface, (20, 70))
        
        # Time warning with pulsing effect
        if remaining_time < 10:
            current_time = pygame.time.get_ticks()
            alpha = int(128 + 127 * pygame.math.Vector2(1, 0).rotate(current_time / 100).x)
            warning_color = (255, alpha // 2, alpha // 2)
            warning = self.font_medium.render("TIME RUNNING OUT!", True, warning_color)
            screen.blit(warning, (320, 20))
    
    @abstractmethod
    def handle_event(self, event):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass

class ArrayLevel(BaseLevel):
    """Level 1: Array Basics - Find elements in array"""
    def __init__(self):
        super().__init__(60)  # 60 seconds
        self.array = [random.randint(1, 50) for _ in range(10)]
        self.target = random.choice(self.array)
        self.selected_index = 0
        self.attempts = 0
        self.max_attempts = 3
        self.generate_new_target()
    
    def generate_new_target(self):
        self.target = random.choice(self.array)
        self.attempts = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.selected_index > 0:
                self.selected_index -= 1
            elif event.key == pygame.K_RIGHT and self.selected_index < len(self.array) - 1:
                self.selected_index += 1
            elif event.key == pygame.K_SPACE:
                self.check_selection()
    
    def check_selection(self):
        self.attempts += 1
        if self.array[self.selected_index] == self.target:
            self.score += 100
            self.generate_new_target()
            # Shuffle array to make it harder
            random.shuffle(self.array)
        else:
            self.score = max(0, self.score - 20)
            
        if self.attempts >= self.max_attempts:
            self.generate_new_target()
    
    def update(self):
        if self.is_time_up():
            return "failed"
        if self.score >= 500:  # Win condition
            return "completed"
        return "playing"
    
    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_hud(screen)
        
        # Animated background grid
        current_time = pygame.time.get_ticks()
        for i in range(0, 1024, 50):
            alpha = int(30 + 20 * pygame.math.Vector2(1, 0).rotate(current_time / 1000 + i / 100).x)
            color = (0, alpha, alpha // 2)
            pygame.draw.line(screen, color, (i, 120), (i, 768), 1)
        
        # Enhanced instructions with background
        inst_rect = pygame.Rect(40, 140, 944, 60)
        pygame.draw.rect(screen, (0, 30, 0), inst_rect)
        pygame.draw.rect(screen, GREEN, inst_rect, 2)
        
        inst_text = f"Find {self.target} in the array! Use LEFT/RIGHT arrows and SPACE to select"
        inst_surface = self.font_medium.render(inst_text, True, WHITE)
        screen.blit(inst_surface, (60, 160))
        
        # Target highlight
        target_text = f"TARGET: {self.target}"
        target_surface = self.font_large.render(target_text, True, YELLOW)
        target_rect = pygame.Rect(60, 220, 200, 50)
        pygame.draw.rect(screen, (50, 50, 0), target_rect)
        pygame.draw.rect(screen, YELLOW, target_rect, 3)
        screen.blit(target_surface, (70, 235))
        
        # Enhanced array visualization
        start_x = 100
        start_y = 300
        cell_width = 70
        cell_height = 50
        
        for i, value in enumerate(self.array):
            x = start_x + i * (cell_width + 15)
            y = start_y
            
            # 3D cell effect
            # Shadow
            shadow_rect = pygame.Rect(x + 3, y + 3, cell_width, cell_height)
            pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
            
            # Main cell
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)
            
            # Color based on selection and value
            if i == self.selected_index:
                # Animated selection
                glow = int(100 + 50 * pygame.math.Vector2(1, 0).rotate(current_time / 200).x)
                cell_color = (glow, glow, 0)
                border_color = YELLOW
                pygame.draw.rect(screen, cell_color, cell_rect)
            elif value == self.target:
                cell_color = (0, 50, 0)
                border_color = GREEN
                pygame.draw.rect(screen, cell_color, cell_rect)
            else:
                cell_color = (30, 30, 50)
                border_color = WHITE
                pygame.draw.rect(screen, cell_color, cell_rect)
            
            pygame.draw.rect(screen, border_color, cell_rect, 3)
            
            # Highlight effect
            highlight_rect = pygame.Rect(x + 2, y + 2, cell_width - 4, cell_height // 3)
            pygame.draw.rect(screen, (255, 255, 255, 30), highlight_rect)
            
            # Value text with shadow
            text_shadow = self.font_medium.render(str(value), True, BLACK)
            screen.blit(text_shadow, (x + cell_width//2 - 8, y + cell_height//2 - 8))
            
            text = self.font_medium.render(str(value), True, WHITE)
            text_rect = text.get_rect(center=(x + cell_width//2, y + cell_height//2))
            screen.blit(text, text_rect)
            
            # Index label
            index_text = self.font_small.render(str(i), True, GRAY)
            index_rect = index_text.get_rect(center=(x + cell_width//2, y - 15))
            screen.blit(index_text, index_rect)
        
        # Enhanced attempts display
        attempts_rect = pygame.Rect(50, 400, 300, 80)
        pygame.draw.rect(screen, (50, 0, 0), attempts_rect)
        pygame.draw.rect(screen, RED, attempts_rect, 2)
        
        attempts_text = f"Attempts: {self.attempts}/{self.max_attempts}"
        attempts_surface = self.font_medium.render(attempts_text, True, WHITE)
        screen.blit(attempts_surface, (70, 420))
        
        # Visual attempt indicators
        for i in range(self.max_attempts):
            circle_x = 70 + i * 30
            circle_y = 450
            if i < self.attempts:
                pygame.draw.circle(screen, RED, (circle_x, circle_y), 8)
            else:
                pygame.draw.circle(screen, GRAY, (circle_x, circle_y), 8, 2)
        
        # Progress indicator
        progress_text = f"Score needed: 500 | Current: {self.score}"
        progress_surface = self.font_small.render(progress_text, True, WHITE)
        screen.blit(progress_surface, (400, 450))

class StackLevel(BaseLevel):
    """Level 2: Stack Operations - Push and Pop correctly"""
    def __init__(self):
        super().__init__(45)  # 45 seconds
        self.stack = []
        self.target_sequence = [random.randint(1, 9) for _ in range(5)]
        self.current_target_index = 0
        self.operations = []
        self.sequence_matches = []  # Track which targets have been matched
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                number = event.key - pygame.K_0
                self.push(number)
            elif event.key == pygame.K_SPACE:
                self.pop()
    
    def push(self, value):
        self.stack.append(value)
        self.operations.append(f"PUSH {value}")
        self.check_progress()
    
    def pop(self):
        if self.stack:
            value = self.stack.pop()
            self.operations.append(f"POP {value}")
            # Reset progress when popping - need to rebuild sequence
            self.reset_progress()
    
    def reset_progress(self):
        """Reset progress when stack is modified by popping"""
        self.current_target_index = 0
        self.sequence_matches = []
        self.check_progress()
    
    def check_progress(self):
        """Check if current stack matches the target sequence from bottom to top"""
        # Reset progress tracking
        self.current_target_index = 0
        self.sequence_matches = []
        
        # Check if stack contains the target sequence in order from bottom
        if len(self.stack) >= len(self.target_sequence):
            # Check if the last N elements match the target sequence
            stack_suffix = self.stack[-len(self.target_sequence):]
            if stack_suffix == self.target_sequence:
                self.sequence_matches = list(range(len(self.target_sequence)))
                self.current_target_index = len(self.target_sequence)
                # Award points for complete sequence
                if len(self.sequence_matches) == len(self.target_sequence):
                    self.score += 100  # Bonus for completing sequence
    
    def update(self):
        if self.is_time_up():
            return "failed"
        # Only complete when ALL targets in sequence are matched consecutively
        if (self.current_target_index >= len(self.target_sequence) and 
            len(self.sequence_matches) == len(self.target_sequence)):
            return "completed"
        return "playing"
    
    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_hud(screen)
        
        # Animated background
        current_time = pygame.time.get_ticks()
        for i in range(5):
            y = 150 + i * 100 + 20 * pygame.math.Vector2(1, 0).rotate(current_time / 1000 + i).y
            pygame.draw.line(screen, (20, 20, 40), (0, int(y)), (1024, int(y)), 1)
        
        # Enhanced instructions
        inst_rect = pygame.Rect(40, 110, 944, 80)
        pygame.draw.rect(screen, (30, 0, 30), inst_rect)
        pygame.draw.rect(screen, PURPLE, inst_rect, 2)
        
        inst_text = "Create the target sequence using stack operations!"
        inst_surface = self.font_medium.render(inst_text, True, WHITE)
        screen.blit(inst_surface, (60, 130))
        
        inst_text2 = "Build the sequence on your stack from LEFT to RIGHT (bottom to top)"
        inst_surface2 = self.font_medium.render(inst_text2, True, YELLOW)
        screen.blit(inst_surface2, (60, 155))
        
        controls_text = "Press 1-9 to PUSH numbers, SPACE to POP from top"
        controls_surface = self.font_small.render(controls_text, True, CYAN)
        screen.blit(controls_surface, (60, 175))
        
        # Enhanced target sequence display
        target_rect = pygame.Rect(50, 210, 500, 60)
        pygame.draw.rect(screen, (0, 50, 0), target_rect)
        pygame.draw.rect(screen, GREEN, target_rect, 3)
        
        target_label = self.font_medium.render("TARGET SEQUENCE:", True, GREEN)
        screen.blit(target_label, (70, 220))
        
        # Draw target sequence with progress
        for i, num in enumerate(self.target_sequence):
            x = 70 + i * 60
            y = 240
            
            # Check if this position is matched in current stack
            is_matched = False
            if len(self.stack) >= len(self.target_sequence):
                stack_suffix = self.stack[-len(self.target_sequence):]
                if i < len(stack_suffix) and stack_suffix[i] == num:
                    is_matched = True
            
            # Highlight based on match status
            if is_matched:
                color = GREEN
                bg_color = (0, 100, 0)
            else:
                color = WHITE
                bg_color = (30, 30, 30)
            
            # Draw target number
            num_rect = pygame.Rect(x, y, 40, 30)
            pygame.draw.rect(screen, bg_color, num_rect)
            pygame.draw.rect(screen, color, num_rect, 2)
            
            num_text = self.font_medium.render(str(num), True, color)
            num_text_rect = num_text.get_rect(center=num_rect.center)
            screen.blit(num_text, num_text_rect)
            
            # Arrow between numbers
            if i < len(self.target_sequence) - 1:
                arrow_x = x + 45
                arrow_y = y + 15
                pygame.draw.polygon(screen, WHITE, [
                    (arrow_x, arrow_y - 5),
                    (arrow_x, arrow_y + 5),
                    (arrow_x + 10, arrow_y)
                ])
        
        # Enhanced stack visualization
        stack_x = 600
        stack_y = 500
        cell_width = 80
        cell_height = 40
        
        # Stack base
        base_rect = pygame.Rect(stack_x - 10, stack_y + 10, cell_width + 20, 20)
        pygame.draw.rect(screen, GRAY, base_rect)
        
        # Stack elements with 3D effect
        for i, value in enumerate(reversed(self.stack)):
            y = stack_y - i * (cell_height + 5)
            
            # Shadow
            shadow_rect = pygame.Rect(stack_x + 3, y + 3, cell_width, cell_height)
            pygame.draw.rect(screen, (20, 20, 20), shadow_rect)
            
            # Main element
            element_rect = pygame.Rect(stack_x, y, cell_width, cell_height)
            
            # Color based on position
            if i == len(self.stack) - 1:  # Top element
                bg_color = (50, 50, 100)
                border_color = CYAN
            else:
                bg_color = (30, 30, 60)
                border_color = WHITE
            
            pygame.draw.rect(screen, bg_color, element_rect)
            pygame.draw.rect(screen, border_color, element_rect, 2)
            
            # Highlight
            highlight_rect = pygame.Rect(stack_x + 2, y + 2, cell_width - 4, cell_height // 3)
            pygame.draw.rect(screen, (255, 255, 255, 50), highlight_rect)
            
            # Value
            text = self.font_medium.render(str(value), True, WHITE)
            text_rect = text.get_rect(center=element_rect.center)
            screen.blit(text, text_rect)
            
            # Stack level indicator
            level_text = self.font_small.render(f"[{len(self.stack) - i - 1}]", True, GRAY)
            screen.blit(level_text, (stack_x - 30, y + cell_height // 2 - 8))
        
        # Stack label with animation
        stack_label_y = stack_y + 50 + 5 * pygame.math.Vector2(1, 0).rotate(current_time / 800).y
        stack_label = self.font_large.render("STACK", True, PURPLE)
        label_rect = stack_label.get_rect(center=(stack_x + cell_width // 2, int(stack_label_y)))
        screen.blit(stack_label, label_rect)
        
        # LIFO indicator
        lifo_text = self.font_small.render("(Last In, First Out)", True, GRAY)
        lifo_rect = lifo_text.get_rect(center=(stack_x + cell_width // 2, int(stack_label_y) + 25))
        screen.blit(lifo_text, lifo_rect)
        
        # Enhanced operations history
        ops_rect = pygame.Rect(50, 320, 400, 150)
        pygame.draw.rect(screen, (0, 0, 30), ops_rect)
        pygame.draw.rect(screen, BLUE, ops_rect, 2)
        
        ops_title = self.font_medium.render("RECENT OPERATIONS:", True, BLUE)
        screen.blit(ops_title, (70, 330))
        
        for i, op in enumerate(self.operations[-6:]):
            op_color = YELLOW if "PUSH" in op else ORANGE
            op_surface = self.font_small.render(f"• {op}", True, op_color)
            screen.blit(op_surface, (70, 355 + i * 20))
        
        # Progress indicator
        progress = (len(self.sequence_matches) / len(self.target_sequence)) * 100
        progress_text = f"Progress: {progress:.0f}% ({len(self.sequence_matches)}/{len(self.target_sequence)} targets matched)"
        progress_surface = self.font_small.render(progress_text, True, WHITE)
        screen.blit(progress_surface, (600, 300))
        
        # Show completion requirement
        if len(self.sequence_matches) < len(self.target_sequence):
            req_text = "Complete the ENTIRE sequence to win!"
            req_surface = self.font_small.render(req_text, True, YELLOW)
            screen.blit(req_surface, (600, 320))

class QueueLevel(BaseLevel):
    """Level 3: Queue Management - Process customers in order"""
    def __init__(self):
        super().__init__(45)  # 45 seconds
        self.queue = []
        self.processed = []
        self.customer_id = 1
        self.target_processed = 10
        self.spawn_timer = pygame.time.get_ticks()  # Initialize with current time
        self.spawn_interval = 2000  # milliseconds
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.process_customer()
            elif event.key == pygame.K_a:
                self.add_customer()
    
    def add_customer(self):
        if len(self.queue) < 15:  # Limit queue size to prevent overflow
            self.queue.append(self.customer_id)
            self.customer_id += 1
    
    def process_customer(self):
        if self.queue:
            customer = self.queue.pop(0)  # FIFO
            self.processed.append(customer)
            self.score += 25
    
    def update(self):
        try:
            # Auto-spawn customers
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_timer > self.spawn_interval:
                self.add_customer()
                self.spawn_timer = current_time
            
            if self.is_time_up():
                return "failed"
            if len(self.processed) >= self.target_processed:
                return "completed"
            return "playing"
        except Exception as e:
            print(f"QueueLevel update error: {e}")
            return "failed"
    
    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_hud(screen)
        
        # Animated background
        current_time = pygame.time.get_ticks()
        
        # Moving queue lines
        for i in range(10):
            y = 200 + i * 50
            x_offset = (current_time // 20 + i * 10) % 100
            pygame.draw.line(screen, (20, 40, 20), (x_offset, y), (x_offset + 50, y), 1)
        
        # Enhanced instructions
        inst_rect = pygame.Rect(40, 110, 944, 80)
        pygame.draw.rect(screen, (0, 40, 40), inst_rect)
        pygame.draw.rect(screen, CYAN, inst_rect, 2)
        
        inst_text = f"Process {self.target_processed} customers using FIFO (First In, First Out)!"
        inst_surface = self.font_medium.render(inst_text, True, WHITE)
        screen.blit(inst_surface, (60, 130))
        
        inst_text2 = "Press A to add customer, SPACE to process next customer"
        inst_surface2 = self.font_medium.render(inst_text2, True, YELLOW)
        screen.blit(inst_surface2, (60, 155))
        
        # Queue visualization with 3D effect
        queue_y = 250
        queue_start_x = 100
        
        # Queue background track
        track_rect = pygame.Rect(queue_start_x - 20, queue_y - 10, 800, 70)
        pygame.draw.rect(screen, (20, 20, 40), track_rect)
        pygame.draw.rect(screen, BLUE, track_rect, 2)
        
        # Queue direction arrow
        arrow_points = [
            (queue_start_x - 15, queue_y + 25),
            (queue_start_x + 750, queue_y + 25),
            (queue_start_x + 740, queue_y + 15),
            (queue_start_x + 750, queue_y + 25),
            (queue_start_x + 740, queue_y + 35)
        ]
        pygame.draw.lines(screen, YELLOW, False, arrow_points, 2)
        
        # Draw queue elements
        for i, customer in enumerate(self.queue):
            x = queue_start_x + i * 80
            
            # Customer shadow
            shadow_rect = pygame.Rect(x + 3, queue_y + 3, 70, 50)
            pygame.draw.rect(screen, (20, 20, 20), shadow_rect)
            
            # Customer box
            customer_rect = pygame.Rect(x, queue_y, 70, 50)
            
            # Color based on position
            if i == 0:  # Next to be processed
                bg_color = (0, 100, 0)
                border_color = GREEN
                # Pulsing effect
                pulse = int(20 + 30 * pygame.math.Vector2(1, 0).rotate(current_time / 200).x)
                bg_color = (pulse, 100 + pulse, pulse)
            else:
                bg_color = (0, 50, 100)
                border_color = BLUE
            
            pygame.draw.rect(screen, bg_color, customer_rect)
            pygame.draw.rect(screen, border_color, customer_rect, 3)
            
            # Highlight
            highlight_rect = pygame.Rect(x + 2, queue_y + 2, 66, 15)
            pygame.draw.rect(screen, (255, 255, 255, 30), highlight_rect)
            
            # Customer ID
            text = self.font_medium.render(str(customer), True, WHITE)
            text_rect = text.get_rect(center=customer_rect.center)
            screen.blit(text, text_rect)
            
            # Position indicator
            pos_text = self.font_small.render(f"#{i+1}", True, GRAY)
            screen.blit(pos_text, (x + 5, queue_y - 20))
        
        # Queue labels
        queue_label = self.font_large.render("QUEUE (FIFO)", True, BLUE)
        screen.blit(queue_label, (queue_start_x, 200))
        
        fifo_desc = self.font_small.render("First In, First Out", True, GRAY)
        screen.blit(fifo_desc, (queue_start_x + 200, 205))
        
        # Processing area
        process_rect = pygame.Rect(50, 350, 400, 120)
        pygame.draw.rect(screen, (0, 50, 0), process_rect)
        pygame.draw.rect(screen, GREEN, process_rect, 3)
        
        process_title = self.font_medium.render("PROCESSING STATUS", True, GREEN)
        screen.blit(process_title, (70, 365))
        
        processed_text = f"Processed: {len(self.processed)}/{self.target_processed}"
        processed_surface = self.font_medium.render(processed_text, True, WHITE)
        screen.blit(processed_surface, (70, 395))
        
        # Progress bar
        progress = len(self.processed) / self.target_processed
        bar_width = 300
        bar_height = 20
        bar_x, bar_y = 70, 420
        
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * progress), bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Recently processed customers
        recent_rect = pygame.Rect(500, 350, 450, 120)
        pygame.draw.rect(screen, (30, 30, 0), recent_rect)
        pygame.draw.rect(screen, YELLOW, recent_rect, 2)
        
        recent_title = self.font_medium.render("RECENTLY PROCESSED", True, YELLOW)
        screen.blit(recent_title, (520, 365))
        
        # Show last processed customers
        for i, customer in enumerate(self.processed[-8:]):
            x = 520 + (i % 4) * 100
            y = 395 + (i // 4) * 35
            
            # Processed customer indicator
            pygame.draw.circle(screen, GREEN, (x + 20, y + 15), 15)
            pygame.draw.circle(screen, WHITE, (x + 20, y + 15), 15, 2)
            
            text = self.font_small.render(str(customer), True, BLACK)
            text_rect = text.get_rect(center=(x + 20, y + 15))
            screen.blit(text, text_rect)
        
        # Queue statistics
        stats_text = f"Queue Length: {len(self.queue)} | Next Customer ID: {self.customer_id}"
        stats_surface = self.font_small.render(stats_text, True, WHITE)
        screen.blit(stats_surface, (100, 500))

class BinarySearchLevel(BaseLevel):
    """Level 4: Binary Search - Find target efficiently"""
    def __init__(self):
        super().__init__(30)  # 30 seconds
        self.array = sorted([random.randint(1, 100) for _ in range(15)])
        self.target = random.choice(self.array)
        self.left = 0
        self.right = len(self.array) - 1
        self.mid = (self.left + self.right) // 2
        self.comparisons = 0
        self.max_comparisons = 4  # log2(15) ≈ 4
        self.found = False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Target is smaller
                self.search_left()
            elif event.key == pygame.K_RIGHT:  # Target is larger
                self.search_right()
            elif event.key == pygame.K_SPACE:  # Found it
                self.check_found()
    
    def search_left(self):
        if not self.found and self.left <= self.right:
            self.comparisons += 1
            if self.array[self.mid] > self.target:
                self.right = self.mid - 1
                self.score += 20
            else:
                self.score = max(0, self.score - 10)
            self.update_mid()
    
    def search_right(self):
        if not self.found and self.left <= self.right:
            self.comparisons += 1
            if self.array[self.mid] < self.target:
                self.left = self.mid + 1
                self.score += 20
            else:
                self.score = max(0, self.score - 10)
            self.update_mid()
    
    def check_found(self):
        if self.array[self.mid] == self.target:
            self.found = True
            self.score += 100
        else:
            self.score = max(0, self.score - 20)
    
    def update_mid(self):
        if self.left <= self.right:
            self.mid = (self.left + self.right) // 2
    
    def update(self):
        if self.is_time_up() or self.comparisons >= self.max_comparisons:
            return "failed" if not self.found else "completed"
        if self.found:
            return "completed"
        return "playing"
    
    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_hud(screen)
        
        # Animated background
        current_time = pygame.time.get_ticks()
        
        # Binary tree-like background pattern
        for level in range(4):
            y = 150 + level * 100
            nodes = 2 ** level
            for i in range(nodes):
                x = SCREEN_WIDTH // 2 + (i - nodes // 2) * (200 // (level + 1))
                alpha = int(30 + 20 * pygame.math.Vector2(1, 0).rotate(current_time / 1000 + level + i).x)
                color = (alpha, alpha // 2, 0)
                pygame.draw.circle(screen, color, (x, y), 3)
        
        # Enhanced instructions
        inst_rect = pygame.Rect(40, 110, 944, 80)
        pygame.draw.rect(screen, (50, 25, 0), inst_rect)
        pygame.draw.rect(screen, ORANGE, inst_rect, 2)
        
        inst_text = f"Find {self.target} using binary search! Divide and conquer!"
        inst_surface = self.font_medium.render(inst_text, True, WHITE)
        screen.blit(inst_surface, (60, 130))
        
        inst_text2 = "LEFT: target smaller | RIGHT: target larger | SPACE: found it!"
        inst_surface2 = self.font_medium.render(inst_text2, True, YELLOW)
        screen.blit(inst_surface2, (60, 155))
        
        # Target display with animation
        target_rect = pygame.Rect(50, 210, 200, 60)
        glow = int(50 + 30 * pygame.math.Vector2(1, 0).rotate(current_time / 400).x)
        target_bg = (glow, glow // 2, 0)
        pygame.draw.rect(screen, target_bg, target_rect)
        pygame.draw.rect(screen, ORANGE, target_rect, 3)
        
        target_label = self.font_small.render("TARGET:", True, ORANGE)
        screen.blit(target_label, (70, 225))
        
        target_value = self.font_large.render(str(self.target), True, WHITE)
        target_value_rect = target_value.get_rect(center=(150, 250))
        screen.blit(target_value, target_value_rect)
        
        # Enhanced array visualization
        start_x = 50
        start_y = 300
        cell_width = 55
        cell_height = 50
        
        # Array background
        array_bg = pygame.Rect(start_x - 10, start_y - 10, 
                              len(self.array) * (cell_width + 5) + 15, cell_height + 20)
        pygame.draw.rect(screen, (20, 20, 30), array_bg)
        pygame.draw.rect(screen, WHITE, array_bg, 2)
        
        for i, value in enumerate(self.array):
            x = start_x + i * (cell_width + 5)
            y = start_y
            
            # Cell shadow
            shadow_rect = pygame.Rect(x + 2, y + 2, cell_width, cell_height)
            pygame.draw.rect(screen, (20, 20, 20), shadow_rect)
            
            # Main cell
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)
            
            # Color coding with enhanced effects
            if i < self.left or i > self.right:
                # Out of search range
                bg_color = (30, 30, 30)
                border_color = GRAY
                text_color = GRAY
            elif i == self.mid:
                # Current middle with pulsing effect
                pulse = int(100 + 50 * pygame.math.Vector2(1, 0).rotate(current_time / 200).x)
                bg_color = (pulse, pulse, 0)
                border_color = YELLOW
                text_color = BLACK
                
                # Add glow effect around middle
                for glow_size in range(5, 0, -1):
                    glow_rect = pygame.Rect(x - glow_size, y - glow_size, 
                                          cell_width + 2*glow_size, cell_height + 2*glow_size)
                    glow_alpha = 50 - glow_size * 10
                    glow_color = (glow_alpha, glow_alpha, 0)
                    pygame.draw.rect(screen, glow_color, glow_rect, 1)
            else:
                # In search range
                bg_color = (0, 50, 100)
                border_color = BLUE
                text_color = WHITE
            
            pygame.draw.rect(screen, bg_color, cell_rect)
            pygame.draw.rect(screen, border_color, cell_rect, 3)
            
            # Highlight effect
            if i >= self.left and i <= self.right:
                highlight_rect = pygame.Rect(x + 2, y + 2, cell_width - 4, cell_height // 3)
                pygame.draw.rect(screen, (255, 255, 255, 40), highlight_rect)
            
            # Value with shadow
            if text_color != BLACK:
                text_shadow = self.font_medium.render(str(value), True, BLACK)
                screen.blit(text_shadow, (x + cell_width//2 - 8, y + cell_height//2 - 6))
            
            text = self.font_medium.render(str(value), True, text_color)
            text_rect = text.get_rect(center=(x + cell_width//2, y + cell_height//2))
            screen.blit(text, text_rect)
            
            # Index label
            index_color = YELLOW if i == self.mid else WHITE if self.left <= i <= self.right else GRAY
            index_text = self.font_small.render(str(i), True, index_color)
            index_rect = index_text.get_rect(center=(x + cell_width//2, y - 15))
            screen.blit(index_text, index_rect)
        
        # Search range indicators
        if self.left <= self.right:
            # Left boundary
            left_x = start_x + self.left * (cell_width + 5) - 5
            pygame.draw.line(screen, GREEN, (left_x, start_y - 30), (left_x, start_y + cell_height + 10), 3)
            left_label = self.font_small.render("LEFT", True, GREEN)
            screen.blit(left_label, (left_x - 15, start_y - 45))
            
            # Right boundary
            right_x = start_x + self.right * (cell_width + 5) + cell_width + 5
            pygame.draw.line(screen, RED, (right_x, start_y - 30), (right_x, start_y + cell_height + 10), 3)
            right_label = self.font_small.render("RIGHT", True, RED)
            screen.blit(right_label, (right_x - 20, start_y - 45))
            
            # Middle indicator
            mid_x = start_x + self.mid * (cell_width + 5) + cell_width // 2
            pygame.draw.polygon(screen, YELLOW, [
                (mid_x - 10, start_y + cell_height + 15),
                (mid_x + 10, start_y + cell_height + 15),
                (mid_x, start_y + cell_height + 5)
            ])
            mid_label = self.font_small.render("MID", True, YELLOW)
            mid_rect = mid_label.get_rect(center=(mid_x, start_y + cell_height + 30))
            screen.blit(mid_label, mid_rect)
        
        # Enhanced search info panel
        info_rect = pygame.Rect(50, 400, 600, 120)
        pygame.draw.rect(screen, (0, 30, 30), info_rect)
        pygame.draw.rect(screen, CYAN, info_rect, 2)
        
        info_title = self.font_medium.render("BINARY SEARCH STATUS", True, CYAN)
        screen.blit(info_title, (70, 415))
        
        if self.left <= self.right:
            search_info = f"Search Range: [{self.left}, {self.right}] | Middle Index: {self.mid} | Middle Value: {self.array[self.mid]}"
            search_surface = self.font_small.render(search_info, True, WHITE)
            screen.blit(search_surface, (70, 445))
            
            # Comparison hint
            if self.array[self.mid] < self.target:
                hint = f"{self.array[self.mid]} < {self.target} → Search RIGHT half"
                hint_color = GREEN
            elif self.array[self.mid] > self.target:
                hint = f"{self.array[self.mid]} > {self.target} → Search LEFT half"
                hint_color = RED
            else:
                hint = f"{self.array[self.mid]} = {self.target} → FOUND IT!"
                hint_color = YELLOW
            
            hint_surface = self.font_small.render(hint, True, hint_color)
            screen.blit(hint_surface, (70, 470))
        
        # Comparisons counter with visual indicator
        comp_rect = pygame.Rect(700, 400, 250, 120)
        pygame.draw.rect(screen, (30, 0, 30), comp_rect)
        pygame.draw.rect(screen, PURPLE, comp_rect, 2)
        
        comp_title = self.font_medium.render("EFFICIENCY", True, PURPLE)
        screen.blit(comp_title, (720, 415))
        
        comparisons_text = f"Comparisons: {self.comparisons}/{self.max_comparisons}"
        comp_surface = self.font_small.render(comparisons_text, True, WHITE)
        screen.blit(comp_surface, (720, 445))
        
        # Efficiency bar
        efficiency = 1 - (self.comparisons / self.max_comparisons)
        bar_width = 200
        bar_height = 15
        bar_x, bar_y = 720, 470
        
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        if efficiency > 0.7:
            bar_color = GREEN
        elif efficiency > 0.4:
            bar_color = YELLOW
        else:
            bar_color = RED
            
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, int(bar_width * efficiency), bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        efficiency_text = f"Efficiency: {efficiency*100:.0f}%"
        eff_surface = self.font_small.render(efficiency_text, True, WHITE)
        screen.blit(eff_surface, (720, 495))

def get_level_instance(level_num):
    """Factory function to create level instances"""
    if level_num == 1:
        return ArrayLevel()
    elif level_num == 2:
        return StackLevel()
    elif level_num == 3:
        return QueueLevel()
    elif level_num == 4:
        return BinarySearchLevel()
    else:
        raise ValueError(f"Level {level_num} not implemented yet!")
