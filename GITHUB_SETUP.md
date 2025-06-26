# GitHub Repository Setup Guide

This guide will help you set up the DSA Learning Adventure project as a GitHub repository with the demo video.

## 🎬 Video File Handling

The demo video `ScreenRecording2025-06-26.mov` (81MB) exceeds GitHub's recommended file size limit (50MB). Here are the recommended approaches:

### Option 1: Git LFS (Recommended)
Git Large File Storage (LFS) is perfect for large media files.

```bash
# Install Git LFS (if not already installed)
# macOS: brew install git-lfs
# Windows: Download from https://git-lfs.github.io/
# Linux: sudo apt install git-lfs

# Initialize Git LFS in your repository
cd /Users/mason/GitHub/DSAedu
git lfs install

# Track the video file with LFS
git lfs track "*.mov"
git lfs track "ScreenRecording2025-06-26.mov"

# Add the .gitattributes file created by LFS
git add .gitattributes

# Now add and commit the video file
git add ScreenRecording2025-06-26.mov
git commit -m "Add demo video with Git LFS"
```

### Option 2: GitHub Releases (Alternative)
Upload the video as a release asset:

1. Create a GitHub release
2. Upload the video file as a release asset
3. Link to it in the README

### Option 3: External Hosting (Backup)
Upload to YouTube, Vimeo, or cloud storage and embed/link in README.

## 🚀 Repository Setup Steps

### 1. Initialize Git Repository
```bash
cd /Users/mason/GitHub/DSAedu

# Initialize git (if not already done)
git init

# Add all files except those in .gitignore
git add .

# Initial commit
git commit -m "Initial commit: DSA Learning Adventure v1.0.0

- Complete educational game with 4 DSA levels
- Retro-style graphics and animations
- Comprehensive documentation suite
- Built using Amazon Q Developer CLI for AWS Games Challenge June 2025"
```

### 2. Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Repository name: `DSAedu` or `dsa-learning-adventure`
4. Description: "🎮 Educational game teaching Data Structures & Algorithms through retro-style interactive gameplay"
5. Make it **Public** (for AWS Games Challenge)
6. Don't initialize with README (we already have one)
7. Click "Create Repository"

### 3. Connect Local Repository to GitHub
```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/DSAedu.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Set Up Git LFS (If Using Option 1)
```bash
# After setting up LFS as described above
git push origin main

# Verify LFS files are tracked
git lfs ls-files
```

### 5. Update README with Correct Video Link
After uploading, update the README with the correct GitHub video URL:

```markdown
## 🎬 **Game Demo**

https://github.com/YOUR_USERNAME/DSAedu/raw/main/ScreenRecording2025-06-26.mov

> **📹 Full Demo Video**: Complete gameplay demonstration showing all 4 levels
```

## 📋 Repository Configuration

### Repository Settings
1. **About Section**:
   - Description: "🎮 Educational game teaching Data Structures & Algorithms through retro-style interactive gameplay"
   - Website: (Your demo URL if hosted elsewhere)
   - Topics: `education`, `game`, `python`, `pygame`, `data-structures`, `algorithms`, `retro`, `learning`

2. **README Features**:
   - Enable "Releases" 
   - Enable "Packages"
   - Enable "Environments" (for future CI/CD)

### Branch Protection (Optional)
For collaborative development:
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Require pull request reviews
4. Require status checks

## 🏷️ Release Creation

### Create v1.0.0 Release
1. Go to "Releases" tab
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `DSA Learning Adventure v1.0.0 - Initial Release`
5. Description:
```markdown
# 🎮 DSA Learning Adventure v1.0.0

## 🎯 Initial Release Features
- **4 Interactive DSA Levels**: Array, Stack, Queue, Binary Search
- **Retro-Style Graphics**: Classic arcade aesthetic with animations
- **Educational Focus**: Learn through hands-on gameplay
- **Comprehensive Documentation**: 57KB+ of guides and references
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎬 Demo Video
See the attached demo video for complete gameplay walkthrough.

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
```

6. Upload `ScreenRecording2025-06-26.mov` as release asset
7. Mark as "Latest Release"
8. Publish release

## 🎯 GitHub Features to Enable

### Issues Templates
Create `.github/ISSUE_TEMPLATE/` with:
- `bug_report.md`
- `feature_request.md`
- `level_suggestion.md`

### Pull Request Template
Create `.github/pull_request_template.md`

### GitHub Actions (Future)
Create `.github/workflows/` for:
- Automated testing
- Code quality checks
- Release automation

## 📊 Repository Analytics

### Insights to Monitor
- **Traffic**: Views and clones
- **Community**: Issues, PRs, discussions
- **Code Frequency**: Commit activity
- **Contributors**: Community growth

### Success Metrics
- ⭐ **Stars**: Community interest
- 🍴 **Forks**: Developer engagement  
- 👁️ **Watchers**: Ongoing interest
- 📥 **Downloads**: Usage metrics

## 🎮 AWS Games Challenge Submission

### Required Elements
- ✅ **Public Repository**: Accessible to judges
- ✅ **Clear README**: Project description and setup
- ✅ **Demo Video**: Gameplay demonstration
- ✅ **Amazon Q Attribution**: Properly credited
- ✅ **Open Source License**: MIT License included
- ✅ **Complete Documentation**: Comprehensive guides

### Submission Checklist
- [ ] Repository is public
- [ ] README includes demo video
- [ ] All code is committed and pushed
- [ ] Documentation is complete
- [ ] License is included
- [ ] Amazon Q Developer attribution is visible
- [ ] Demo video shows all features
- [ ] Installation instructions work
- [ ] Game runs without errors

## 🔗 Useful Commands

```bash
# Check repository status
git status
git log --oneline

# Check LFS status
git lfs ls-files
git lfs status

# Update remote repository
git add .
git commit -m "Update: description of changes"
git push origin main

# Create and switch to new branch
git checkout -b feature/new-feature
git push -u origin feature/new-feature

# Tag a release
git tag -a v1.0.1 -m "Version 1.0.1 - Bug fixes"
git push origin v1.0.1
```

## 🆘 Troubleshooting

### Large File Issues
If you get errors about large files:
```bash
# Remove file from git history
git rm --cached ScreenRecording2025-06-26.mov
git commit -m "Remove large file from git"

# Set up LFS and re-add
git lfs track "*.mov"
git add .gitattributes
git add ScreenRecording2025-06-26.mov
git commit -m "Add video with LFS"
```

### Authentication Issues
```bash
# Use personal access token instead of password
# Generate token at: GitHub Settings → Developer settings → Personal access tokens
```

---

**Built using Amazon Q Developer CLI for AWS Games Challenge June 2025**

This setup guide ensures your DSA Learning Adventure project is properly configured for GitHub with the demo video included.
