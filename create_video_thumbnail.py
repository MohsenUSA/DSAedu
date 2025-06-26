#!/usr/bin/env python3
"""
Create a video thumbnail with play button overlay
This creates a more video-like preview that users can click
"""

import pygame
import sys
import os

def create_video_thumbnail():
    """Create a video thumbnail that looks like a video player"""
    
    # Initialize pygame
    pygame.init()
    
    # Create a surface for the thumbnail
    width, height = 800, 450  # 16:9 aspect ratio like videos
    surface = pygame.Surface((width, height))
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 100, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 100, 100)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    
    # Fonts
    try:
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        font_tiny = pygame.font.Font(None, 18)
    except:
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        font_tiny = pygame.font.Font(None, 18)
    
    # Fill background with dark color (like video player)
    surface.fill(BLACK)
    
    # Add a subtle border to make it look like a video player
    pygame.draw.rect(surface, DARK_GRAY, (0, 0, width, height), 3)
    
    # Title at top
    title = font_large.render("DSA Learning Adventure", True, GREEN)
    title_rect = title.get_rect(center=(width//2, 60))
    surface.blit(title, title_rect)
    
    # Subtitle
    subtitle = font_medium.render("🎮 Interactive Gameplay Demo", True, WHITE)
    subtitle_rect = subtitle.get_rect(center=(width//2, 100))
    surface.blit(subtitle, subtitle_rect)
    
    # Create a large play button in the center
    play_button_center = (width//2, height//2)
    play_button_radius = 60
    
    # Play button background (semi-transparent circle)
    play_circle = pygame.Surface((play_button_radius*2, play_button_radius*2))
    play_circle.set_alpha(200)
    play_circle.fill(BLACK)
    pygame.draw.circle(play_circle, WHITE, (play_button_radius, play_button_radius), play_button_radius)
    pygame.draw.circle(play_circle, BLACK, (play_button_radius, play_button_radius), play_button_radius, 3)
    
    # Play triangle
    triangle_points = [
        (play_button_radius - 15, play_button_radius - 20),
        (play_button_radius - 15, play_button_radius + 20),
        (play_button_radius + 20, play_button_radius)
    ]
    pygame.draw.polygon(play_circle, BLACK, triangle_points)
    
    # Blit play button to main surface
    play_rect = play_circle.get_rect(center=play_button_center)
    surface.blit(play_circle, play_rect)
    
    # Game features around the play button
    features = [
        ("🔢 Array Search", 150, 180),
        ("📚 Stack Operations", 650, 180),
        ("🚶 Queue Processing", 150, 320),
        ("🔍 Binary Search", 650, 320)
    ]
    
    for feature_text, x, y in features:
        # Feature background
        feature_surface = font_small.render(feature_text, True, YELLOW)
        feature_rect = feature_surface.get_rect(center=(x, y))
        
        # Background box
        bg_rect = pygame.Rect(feature_rect.x - 10, feature_rect.y - 5, 
                             feature_rect.width + 20, feature_rect.height + 10)
        pygame.draw.rect(surface, DARK_GRAY, bg_rect)
        pygame.draw.rect(surface, YELLOW, bg_rect, 1)
        
        surface.blit(feature_surface, feature_rect)
    
    # Video info at bottom
    duration_text = font_small.render("📹 Full Demo Video • 81MB • All 4 Levels", True, WHITE)
    duration_rect = duration_text.get_rect(center=(width//2, height - 60))
    surface.blit(duration_text, duration_rect)
    
    # Click instruction
    click_text = font_small.render("👆 Click to download and watch full gameplay demo", True, GRAY)
    click_rect = click_text.get_rect(center=(width//2, height - 35))
    surface.blit(click_text, click_rect)
    
    # Amazon Q attribution
    attribution_text = font_tiny.render("Built using Amazon Q Developer CLI for AWS Games Challenge June 2025", True, GRAY)
    attribution_rect = attribution_text.get_rect(center=(width//2, height - 15))
    surface.blit(attribution_text, attribution_rect)
    
    # Save the thumbnail
    output_file = "video-thumbnail.png"
    pygame.image.save(surface, output_file)
    
    print(f"✅ Video thumbnail created: {output_file}")
    print(f"📊 Image size: {width}x{height} pixels")
    
    # Get file size
    if os.path.exists(output_file):
        size = os.path.getsize(output_file)
        size_kb = size // 1024
        print(f"📁 File size: {size_kb}KB")
    
    pygame.quit()
    return output_file

def create_clickable_video_section():
    """Create markdown for a clickable video section"""
    
    markdown = '''## 🎬 **Game Demo Video**

[![DSA Learning Adventure Gameplay Demo](video-thumbnail.png)](ScreenRecording2025-06-26.mov)

> **🎮 Click the thumbnail above to download the full gameplay demo (81MB)**
> 
> *Shows complete walkthrough of all 4 DSA levels with educational explanations*

### 📹 **What's in the Video:**
- **🏠 Main Menu**: Retro interface with high scores and Amazon Q attribution
- **🎯 Level Selection**: Interactive DSA challenge selection
- **🔢 Array Level**: Visual linear search demonstration
- **📚 Stack Level**: LIFO operations and sequence building
- **🚶 Queue Level**: FIFO customer processing simulation  
- **🔍 Binary Search**: Divide-and-conquer algorithm visualization
- **🏆 Scoring System**: Points, bonuses, and persistent high scores
- **🎨 Visual Effects**: Retro styling and smooth animations

### 🎮 **Alternative Ways to Experience:**
1. **📥 Download Demo**: Click thumbnail above for full video
2. **🎮 Play Interactive**: Run `./run_game.sh` to play yourself
3. **🌐 GitHub Releases**: Professional presentation with release notes

---'''
    
    return markdown

if __name__ == "__main__":
    try:
        # Create video thumbnail
        thumbnail_file = create_video_thumbnail()
        
        # Generate markdown
        video_markdown = create_clickable_video_section()
        
        print(f"\n🎯 Video thumbnail created successfully!")
        print(f"\n📋 Add this to your README.md:")
        print("=" * 50)
        print(video_markdown)
        print("=" * 50)
        
        print(f"\n✅ The thumbnail shows a play button and looks like a real video!")
        print(f"👆 Users can click it to download the actual video file")
        
    except Exception as e:
        print(f"❌ Error creating video thumbnail: {e}")
        sys.exit(1)
