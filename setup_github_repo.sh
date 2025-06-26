#!/bin/bash

# DSA Learning Adventure - GitHub Repository Setup Script
# This script helps set up the project as a GitHub repository

set -e  # Exit on any error

echo "🎮 DSA Learning Adventure - GitHub Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "dsa_game.py" ] || [ ! -f "levels.py" ]; then
    print_error "This script must be run from the DSAedu project directory"
    exit 1
fi

print_info "Setting up DSA Learning Adventure for GitHub..."

# Step 1: Check Git installation
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi
print_status "Git is installed"

# Step 2: Initialize Git repository if not already done
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
else
    print_status "Git repository already exists"
fi

# Step 3: Check for large files and suggest Git LFS
VIDEO_FILE="ScreenRecording2025-06-26.mov"
if [ -f "$VIDEO_FILE" ]; then
    FILE_SIZE=$(stat -f%z "$VIDEO_FILE" 2>/dev/null || stat -c%s "$VIDEO_FILE" 2>/dev/null)
    FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))
    
    if [ $FILE_SIZE_MB -gt 50 ]; then
        print_warning "Video file is ${FILE_SIZE_MB}MB (larger than GitHub's 50MB limit)"
        
        # Check if Git LFS is available
        if command -v git-lfs &> /dev/null; then
            print_info "Setting up Git LFS for large files..."
            git lfs install
            git lfs track "*.mov"
            git lfs track "$VIDEO_FILE"
            print_status "Git LFS configured for video files"
        else
            print_warning "Git LFS not found. Consider installing it for large file support:"
            print_info "  macOS: brew install git-lfs"
            print_info "  Ubuntu: sudo apt install git-lfs"
            print_info "  Windows: Download from https://git-lfs.github.io/"
        fi
    fi
fi

# Step 4: Clean up any unwanted files
print_info "Cleaning up temporary files..."
rm -rf __pycache__
rm -f .DS_Store
print_status "Cleanup completed"

# Step 5: Add all files to Git
print_info "Adding files to Git..."
git add .

# Step 6: Check if there are changes to commit
if git diff --staged --quiet; then
    print_info "No changes to commit"
else
    # Step 7: Create initial commit
    print_info "Creating initial commit..."
    git commit -m "Initial commit: DSA Learning Adventure v1.0.0

🎮 Complete educational game with 4 DSA levels
📚 Comprehensive documentation suite (57KB+)
🎨 Retro-style graphics and animations
🏆 Built using Amazon Q Developer CLI for AWS Games Challenge June 2025

Features:
- Level 1: Array Basics (Linear search)
- Level 2: Stack Operations (LIFO mechanics)
- Level 3: Queue Management (FIFO processing)
- Level 4: Binary Search (Divide and conquer)
- Persistent scoring system
- Cross-platform compatibility
- Complete API documentation"
    
    print_status "Initial commit created"
fi

# Step 8: Set up main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_info "Renaming branch to 'main'..."
    git branch -M main
    print_status "Branch renamed to 'main'"
fi

# Step 9: Provide GitHub setup instructions
echo ""
print_info "🚀 Next Steps - GitHub Repository Setup:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: DSAedu (or dsa-learning-adventure)"
echo "   - Description: 🎮 Educational game teaching Data Structures & Algorithms through retro-style interactive gameplay"
echo "   - Make it PUBLIC (for AWS Games Challenge)"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "2. Connect your local repository to GitHub:"
echo "   Replace YOUR_USERNAME with your GitHub username:"
echo ""
echo -e "${BLUE}   git remote add origin https://github.com/YOUR_USERNAME/DSAedu.git${NC}"
echo -e "${BLUE}   git push -u origin main${NC}"
echo ""
echo "3. Configure repository settings:"
echo "   - Add topics: education, game, python, pygame, data-structures, algorithms"
echo "   - Enable Issues and Discussions"
echo "   - Set up branch protection (optional)"
echo ""
echo "4. Create a release:"
echo "   - Go to Releases tab"
echo "   - Create new release with tag v1.0.0"
echo "   - Upload demo video as release asset"
echo ""

# Step 10: Provide file size information
echo ""
print_info "📊 Repository Statistics:"
echo "   - Python Code: $(find . -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}') lines"
echo "   - Documentation: $(find . -name "*.md" -exec wc -l {} + | tail -1 | awk '{print $1}') lines"
echo "   - Total Files: $(find . -type f | wc -l | tr -d ' ') files"

if [ -f "$VIDEO_FILE" ]; then
    echo "   - Demo Video: ${FILE_SIZE_MB}MB"
fi

echo ""
print_status "GitHub setup preparation complete!"
print_info "Your DSA Learning Adventure is ready for GitHub! 🎉"

# Step 11: Offer to open GitHub
echo ""
read -p "Would you like to open GitHub in your browser to create the repository? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        open "https://github.com/new"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "https://github.com/new"
    else
        print_info "Please open https://github.com/new in your browser"
    fi
fi

echo ""
print_status "Setup script completed successfully!"
echo ""
echo "🏆 AWS Games Challenge June 2025"
echo "Built using Amazon Q Developer CLI"
