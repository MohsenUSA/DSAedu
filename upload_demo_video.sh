#!/bin/bash

# Upload demo video to GitHub Releases
# This script helps upload the large video file as a release asset

echo "🎬 GitHub Release Video Upload Helper"
echo "===================================="

VIDEO_FILE="ScreenRecording2025-06-26.mov"
REPO_NAME="DSAedu"  # Change this to your repository name
USERNAME=""  # Will be prompted

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Check if video file exists
if [ ! -f "$VIDEO_FILE" ]; then
    print_error "Video file $VIDEO_FILE not found!"
    exit 1
fi

# Get file size
FILE_SIZE=$(stat -f%z "$VIDEO_FILE" 2>/dev/null || stat -c%s "$VIDEO_FILE" 2>/dev/null)
FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))
print_info "Video file size: ${FILE_SIZE_MB}MB"

# Get GitHub username
if [ -z "$USERNAME" ]; then
    read -p "Enter your GitHub username: " USERNAME
fi

if [ -z "$USERNAME" ]; then
    print_error "GitHub username is required"
    exit 1
fi

echo ""
print_info "Setting up GitHub Release for video upload..."
echo ""

# Instructions for manual upload
echo "📋 Manual Upload Instructions:"
echo ""
echo "1. 🚀 Create a GitHub Release:"
echo "   - Go to: https://github.com/$USERNAME/$REPO_NAME/releases/new"
echo "   - Tag version: v1.0.0"
echo "   - Release title: DSA Learning Adventure v1.0.0 - Initial Release"
echo ""
echo "2. 📝 Release Description:"
cat << 'EOF'
# 🎮 DSA Learning Adventure v1.0.0

## 🎯 Initial Release Features
- **4 Interactive DSA Levels**: Array, Stack, Queue, Binary Search
- **Retro-Style Graphics**: Classic arcade aesthetic with animations  
- **Educational Focus**: Learn through hands-on gameplay
- **Comprehensive Documentation**: 57KB+ of guides and references
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎬 Demo Video
The attached demo video shows complete gameplay including:
- Menu navigation and interface
- All 4 levels with educational explanations
- Scoring system and high score tracking
- Visual effects and retro styling

## 🚀 Quick Start
```bash
git clone https://github.com/YOUR_USERNAME/DSAedu.git
cd DSAedu
python3 -m venv dsa_game_env
source dsa_game_env/bin/activate
pip install pygame
./run_game.sh
```

## 🏆 AWS Games Challenge June 2025
Built using Amazon Q Developer CLI for AWS Games Challenge June 2025.

## 📚 Documentation
- [Complete Documentation](DOCUMENTATION.md)
- [API Reference](API_REFERENCE.md)  
- [Contributing Guide](CONTRIBUTING.md)
EOF

echo ""
echo "3. 📎 Upload Video File:"
echo "   - Drag and drop: $VIDEO_FILE"
echo "   - Or click 'Attach binaries' and select the file"
echo ""
echo "4. ✅ Publish Release:"
echo "   - Check 'Set as the latest release'"
echo "   - Click 'Publish release'"
echo ""

# Check if GitHub CLI is available for automated upload
if command -v gh &> /dev/null; then
    echo ""
    print_info "GitHub CLI detected! You can also use automated upload:"
    echo ""
    echo "🤖 Automated Upload Command:"
    echo "gh release create v1.0.0 $VIDEO_FILE \\"
    echo "  --title 'DSA Learning Adventure v1.0.0 - Initial Release' \\"
    echo "  --notes-file release_notes.md \\"
    echo "  --repo $USERNAME/$REPO_NAME"
    echo ""
    
    # Create release notes file
    cat > release_notes.md << 'EOF'
# 🎮 DSA Learning Adventure v1.0.0

## 🎯 Initial Release Features
- **4 Interactive DSA Levels**: Array, Stack, Queue, Binary Search
- **Retro-Style Graphics**: Classic arcade aesthetic with animations
- **Educational Focus**: Learn through hands-on gameplay
- **Comprehensive Documentation**: 57KB+ of guides and references
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎬 Demo Video
The attached demo video shows complete gameplay including menu navigation, all 4 levels with educational explanations, scoring system, and visual effects.

## 🚀 Quick Start
```bash
git clone https://github.com/YOUR_USERNAME/DSAedu.git
cd DSAedu
python3 -m venv dsa_game_env
source dsa_game_env/bin/activate
pip install pygame
./run_game.sh
```

## 🏆 AWS Games Challenge June 2025
Built using Amazon Q Developer CLI for AWS Games Challenge June 2025.
EOF
    
    print_status "Created release_notes.md for automated upload"
    
    read -p "Would you like to create the release automatically? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Creating GitHub release..."
        gh release create v1.0.0 "$VIDEO_FILE" \
          --title "DSA Learning Adventure v1.0.0 - Initial Release" \
          --notes-file release_notes.md \
          --repo "$USERNAME/$REPO_NAME"
        
        if [ $? -eq 0 ]; then
            print_status "Release created successfully!"
            print_info "Video is now available at:"
            echo "https://github.com/$USERNAME/$REPO_NAME/releases/download/v1.0.0/$VIDEO_FILE"
        else
            print_error "Failed to create release. Try manual upload instead."
        fi
    fi
else
    print_warning "GitHub CLI not found. Using manual upload instructions."
    print_info "Install GitHub CLI: https://cli.github.com/"
fi

echo ""
print_info "After uploading, update your README.md with the correct release URL:"
echo "https://github.com/$USERNAME/$REPO_NAME/releases/download/v1.0.0/$VIDEO_FILE"

echo ""
print_status "Upload helper completed!"
