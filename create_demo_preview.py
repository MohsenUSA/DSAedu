#!/usr/bin/env python3
"""
Create a demo preview image from the video using Python
This script creates a preview image that can be used in the README
"""

import pygame
import sys
import os

def create_demo_preview():
    """Create a demo preview image showing game features"""
    
    # Initialize pygame
    pygame.init()
    
    # Create a surface for the preview
    width, height = 800, 600
    surface = pygame.Surface((width, height))
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 100, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 100, 100)
    
    # Fonts
    try:
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
    except:
        print("Using default font")
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
    
    # Fill background
    surface.fill(BLACK)
    
    # Title
    title = font_large.render("DSA Learning Adventure", True, GREEN)
    title_rect = title.get_rect(center=(width//2, 60))
    surface.blit(title, title_rect)
    
    # Subtitle
    subtitle = font_medium.render("Interactive Data Structures & Algorithms Game", True, WHITE)
    subtitle_rect = subtitle.get_rect(center=(width//2, 100))
    surface.blit(subtitle, subtitle_rect)
    
    # Game features preview
    features = [
        ("🔢 Array Level", "Linear search with visual navigation", GREEN),
        ("📚 Stack Level", "LIFO operations and sequence building", BLUE),
        ("🚶 Queue Level", "FIFO customer processing simulation", YELLOW),
        ("🔍 Binary Search", "Efficient divide-and-conquer algorithm", RED)
    ]
    
    y_start = 160
    for i, (title_text, desc_text, color) in enumerate(features):
        y = y_start + i * 80
        
        # Feature box
        box_rect = pygame.Rect(50, y, width-100, 70)
        pygame.draw.rect(surface, (20, 20, 40), box_rect)
        pygame.draw.rect(surface, color, box_rect, 2)
        
        # Feature title
        feature_title = font_medium.render(title_text, True, color)
        surface.blit(feature_title, (70, y + 10))
        
        # Feature description
        feature_desc = font_small.render(desc_text, True, WHITE)
        surface.blit(feature_desc, (70, y + 40))
    
    # Bottom info
    bottom_text = font_small.render("Built using Amazon Q Developer CLI for AWS Games Challenge June 2025", True, WHITE)
    bottom_rect = bottom_text.get_rect(center=(width//2, height-30))
    surface.blit(bottom_text, bottom_rect)
    
    # Demo video notice
    demo_text = font_medium.render("📹 Full Demo Video Available in GitHub Releases", True, YELLOW)
    demo_rect = demo_text.get_rect(center=(width//2, height-80))
    surface.blit(demo_text, demo_rect)
    
    # Save the preview image
    output_file = "demo-preview.png"
    pygame.image.save(surface, output_file)
    
    print(f"✅ Demo preview created: {output_file}")
    print(f"📊 Image size: {width}x{height} pixels")
    
    # Get file size
    if os.path.exists(output_file):
        size = os.path.getsize(output_file)
        size_kb = size // 1024
        print(f"📁 File size: {size_kb}KB")
    
    pygame.quit()
    return output_file

if __name__ == "__main__":
    try:
        preview_file = create_demo_preview()
        print(f"\n🎯 Usage in README.md:")
        print(f"![DSA Learning Adventure Demo]({preview_file})")
        print(f"\n✅ Preview image ready for GitHub!")
    except Exception as e:
        print(f"❌ Error creating preview: {e}")
        sys.exit(1)
