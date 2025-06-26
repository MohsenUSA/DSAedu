#!/usr/bin/env python3
"""
Create an animated GIF from the demo video using Python
This will show actual gameplay footage in the README
"""

import subprocess
import os
import sys

def create_animated_gif():
    """Create an animated GIF from the demo video"""
    
    input_video = "ScreenRecording2025-06-26.mov"
    output_gif = "gameplay-demo.gif"
    
    print("🎬 Creating animated GIF from demo video...")
    
    # Check if input video exists
    if not os.path.exists(input_video):
        print(f"❌ Error: {input_video} not found!")
        return False
    
    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ ffmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ffmpeg not found. Installing...")
        
        # Try to install ffmpeg
        try:
            # macOS with Homebrew
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
            print("✅ ffmpeg installed via Homebrew")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Could not install ffmpeg automatically.")
            print("Please install ffmpeg manually:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu: sudo apt install ffmpeg")
            print("  Windows: Download from https://ffmpeg.org/")
            return False
    
    # Create optimized GIF for GitHub
    print("🎨 Converting video to animated GIF...")
    
    try:
        # FFmpeg command to create optimized GIF
        # - Take first 30 seconds of video
        # - Scale to 600px width (good for GitHub)
        # - 8 fps for reasonable file size
        # - Optimize palette for better quality
        cmd = [
            "ffmpeg",
            "-i", input_video,
            "-t", "30",  # First 30 seconds
            "-vf", "fps=8,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop", "0",
            output_gif,
            "-y"  # Overwrite if exists
        ]
        
        subprocess.run(cmd, check=True)
        
        # Check file size
        if os.path.exists(output_gif):
            size = os.path.getsize(output_gif)
            size_mb = size / (1024 * 1024)
            print(f"✅ GIF created: {output_gif}")
            print(f"📊 File size: {size_mb:.1f}MB")
            
            if size_mb > 10:
                print("⚠️  GIF is larger than 10MB (GitHub limit)")
                print("🔄 Creating smaller version...")
                
                # Create smaller version
                cmd_small = [
                    "ffmpeg",
                    "-i", input_video,
                    "-t", "20",  # First 20 seconds
                    "-vf", "fps=6,scale=400:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
                    "-loop", "0",
                    "gameplay-demo-small.gif",
                    "-y"
                ]
                
                subprocess.run(cmd_small, check=True)
                
                if os.path.exists("gameplay-demo-small.gif"):
                    small_size = os.path.getsize("gameplay-demo-small.gif")
                    small_size_mb = small_size / (1024 * 1024)
                    print(f"✅ Small GIF created: gameplay-demo-small.gif")
                    print(f"📊 Small file size: {small_size_mb:.1f}MB")
                    
                    if small_size_mb <= 10:
                        print("✅ Small GIF is suitable for GitHub!")
                        return "gameplay-demo-small.gif"
            
            return output_gif
        else:
            print("❌ Failed to create GIF")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating GIF: {e}")
        return False

def update_readme_with_gif(gif_file):
    """Update README with the animated GIF"""
    
    readme_file = "README.md"
    
    if not os.path.exists(readme_file):
        print("❌ README.md not found")
        return False
    
    # Read current README
    with open(readme_file, 'r') as f:
        content = f.read()
    
    # Replace the static preview with animated GIF
    old_line = "![DSA Learning Adventure Demo](demo-preview.png)"
    new_line = f"![DSA Learning Adventure Gameplay]({gif_file})"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Add a note about the animated demo
        gif_description = f"""
*🎮 Live gameplay footage showing all 4 DSA levels in action*

> **Note**: This is an animated GIF showing actual gameplay. For the full HD video experience, download the complete demo video below.
"""
        
        # Insert description after the GIF
        content = content.replace(new_line, new_line + "\n" + gif_description)
        
        # Write updated README
        with open(readme_file, 'w') as f:
            f.write(content)
        
        print(f"✅ README.md updated with animated GIF: {gif_file}")
        return True
    else:
        print("⚠️  Could not find preview image line in README")
        print("Please manually add this line to your README:")
        print(f"![DSA Learning Adventure Gameplay]({gif_file})")
        return False

if __name__ == "__main__":
    print("🎬 DSA Learning Adventure - Video to GIF Converter")
    print("=" * 50)
    
    # Create animated GIF
    gif_file = create_animated_gif()
    
    if gif_file:
        print(f"\n🎯 Success! Created: {gif_file}")
        
        # Update README
        if update_readme_with_gif(gif_file):
            print("\n✅ All done! Your README now shows animated gameplay!")
            print("\n📋 Next steps:")
            print("1. git add .")
            print("2. git commit -m 'Add animated gameplay GIF'")
            print("3. git push origin main")
            print("\n🎮 Your GitHub README will now show actual gameplay footage!")
        else:
            print(f"\n📝 Manual step needed:")
            print(f"Add this line to your README.md:")
            print(f"![DSA Learning Adventure Gameplay]({gif_file})")
    else:
        print("\n❌ Failed to create animated GIF")
        print("You can still use the static preview image or upload to external video hosting.")
