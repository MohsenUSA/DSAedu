#!/bin/bash

# Convert demo video to GIF for GitHub README display
# This script converts the MOV file to an optimized GIF

echo "🎬 Converting demo video to GIF for GitHub display..."

INPUT_VIDEO="ScreenRecording2025-06-26.mov"
OUTPUT_GIF="demo.gif"
OUTPUT_GIF_OPTIMIZED="demo-optimized.gif"

# Check if input video exists
if [ ! -f "$INPUT_VIDEO" ]; then
    echo "❌ Error: $INPUT_VIDEO not found!"
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg is required but not installed."
    echo "Install with:"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu: sudo apt install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/"
    exit 1
fi

echo "✅ Converting video to GIF..."

# Convert to GIF with optimization for GitHub
# - Scale to reasonable size (width 800px)
# - Reduce frame rate to 10fps for smaller file size
# - Optimize palette for better quality
ffmpeg -i "$INPUT_VIDEO" \
    -vf "fps=10,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    -loop 0 \
    "$OUTPUT_GIF" \
    -y

if [ $? -eq 0 ]; then
    echo "✅ GIF created: $OUTPUT_GIF"
    
    # Get file size
    if command -v stat &> /dev/null; then
        SIZE=$(stat -f%z "$OUTPUT_GIF" 2>/dev/null || stat -c%s "$OUTPUT_GIF" 2>/dev/null)
        SIZE_MB=$((SIZE / 1024 / 1024))
        echo "📊 GIF size: ${SIZE_MB}MB"
        
        # GitHub has a 10MB limit for files in repositories
        if [ $SIZE_MB -gt 10 ]; then
            echo "⚠️  GIF is larger than 10MB. Creating optimized version..."
            
            # Create a more compressed version
            ffmpeg -i "$INPUT_VIDEO" \
                -vf "fps=8,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
                -loop 0 \
                "$OUTPUT_GIF_OPTIMIZED" \
                -y
            
            if [ -f "$OUTPUT_GIF_OPTIMIZED" ]; then
                SIZE_OPT=$(stat -f%z "$OUTPUT_GIF_OPTIMIZED" 2>/dev/null || stat -c%s "$OUTPUT_GIF_OPTIMIZED" 2>/dev/null)
                SIZE_OPT_MB=$((SIZE_OPT / 1024 / 1024))
                echo "✅ Optimized GIF created: $OUTPUT_GIF_OPTIMIZED (${SIZE_OPT_MB}MB)"
                
                if [ $SIZE_OPT_MB -le 10 ]; then
                    echo "✅ Optimized GIF is under 10MB and ready for GitHub!"
                else
                    echo "⚠️  Still too large. Consider using external hosting."
                fi
            fi
        else
            echo "✅ GIF size is acceptable for GitHub!"
        fi
    fi
    
    echo ""
    echo "🎯 Next steps:"
    echo "1. Add the GIF to your repository:"
    echo "   git add $OUTPUT_GIF"
    if [ -f "$OUTPUT_GIF_OPTIMIZED" ]; then
        echo "   git add $OUTPUT_GIF_OPTIMIZED"
    fi
    echo "   git commit -m 'Add demo GIF for README display'"
    echo ""
    echo "2. Update README.md to use:"
    echo "   ![Demo GIF]($OUTPUT_GIF)"
    echo ""
    
else
    echo "❌ Error converting video to GIF"
    exit 1
fi
