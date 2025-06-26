# 🎬 Video Demo Setup Guide

This guide explains how to properly display your demo video on GitHub, since the current link shows a 404 error.

## 🚨 **Current Issue**
The README link `[ScreenRecording2025-06-26.mov](ScreenRecording2025-06-26.mov)` shows "404 - page not found" because:
1. The file isn't pushed to GitHub yet
2. Even if pushed, GitHub doesn't display videos inline in README files
3. The 81MB file exceeds GitHub's display limits

## ✅ **Solutions (Choose One)**

### **Option 1: Animated GIF Preview (Recommended)**
Create a GIF that displays directly in the README:

```bash
# Convert video to GIF
./convert_video_to_gif.sh

# Add to repository
git add demo.gif
git commit -m "Add demo GIF for README display"
git push origin main
```

**Pros**: 
- ✅ Displays directly in README
- ✅ No external dependencies
- ✅ Works on all platforms

**Cons**: 
- ❌ Larger file size than video
- ❌ Lower quality than original video

### **Option 2: GitHub Releases (Best for Full Video)**
Upload the full video as a release asset:

```bash
# Use the upload helper
./upload_demo_video.sh

# Or manually:
# 1. Go to GitHub → Releases → Create new release
# 2. Upload ScreenRecording2025-06-26.mov as asset
# 3. Update README with release download link
```

**Pros**: 
- ✅ Full quality video
- ✅ No file size limits
- ✅ Professional presentation

**Cons**: 
- ❌ Requires manual download
- ❌ Doesn't display inline

### **Option 3: External Video Hosting**
Upload to YouTube, Vimeo, or similar:

```markdown
## 🎬 Game Demo

[![DSA Learning Adventure Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

*Click to watch the full demo on YouTube*
```

**Pros**: 
- ✅ Professional video player
- ✅ No file size limits
- ✅ Better streaming experience

**Cons**: 
- ❌ Requires external account
- ❌ May not be suitable for all audiences

### **Option 4: Git LFS (For Repository Storage)**
Use Git Large File Storage for the video:

```bash
# Install and configure Git LFS
git lfs install
git lfs track "*.mov"
git add .gitattributes
git add ScreenRecording2025-06-26.mov
git commit -m "Add demo video with Git LFS"
git push origin main
```

**Pros**: 
- ✅ Video stored in repository
- ✅ Version controlled
- ✅ Direct download link

**Cons**: 
- ❌ Still doesn't display inline
- ❌ Requires Git LFS setup

## 🎯 **Recommended Approach: Combination**

Use **both** GIF preview and GitHub Release:

1. **Create GIF for README preview**:
```bash
./convert_video_to_gif.sh
```

2. **Upload full video to GitHub Releases**:
```bash
./upload_demo_video.sh
```

3. **Update README with both**:
```markdown
## 🎬 Game Demo

### 📹 Live Preview
![DSA Learning Adventure Demo](demo.gif)

### 🎥 Full Quality Video
**[📹 Download Full Demo (81MB)](https://github.com/YOUR_USERNAME/DSAedu/releases/download/v1.0.0/ScreenRecording2025-06-26.mov)**

*Complete gameplay demonstration with all features*
```

## 🛠️ **Step-by-Step Implementation**

### Step 1: Create GIF Preview
```bash
cd /Users/mason/GitHub/DSAedu

# Convert video to GIF (requires ffmpeg)
./convert_video_to_gif.sh

# Check the result
ls -la demo*.gif
```

### Step 2: Upload to GitHub Releases
```bash
# First, push your code to GitHub
git add .
git commit -m "Prepare for release with video demo"
git push origin main

# Then upload video to releases
./upload_demo_video.sh
```

### Step 3: Update README
The README is already updated with the new video section. Just replace `YOUR_USERNAME` with your actual GitHub username.

### Step 4: Test the Links
After uploading:
1. Check that the GIF displays in README
2. Verify the release download link works
3. Test on different devices/browsers

## 🔧 **Troubleshooting**

### GIF Creation Issues
```bash
# Install ffmpeg if missing
# macOS:
brew install ffmpeg

# Ubuntu:
sudo apt install ffmpeg

# Windows:
# Download from https://ffmpeg.org/
```

### GitHub Upload Issues
```bash
# Install GitHub CLI for automated uploads
# macOS:
brew install gh

# Ubuntu:
sudo apt install gh

# Login to GitHub CLI
gh auth login
```

### File Size Issues
If GIF is too large (>10MB):
```bash
# Create smaller version
ffmpeg -i ScreenRecording2025-06-26.mov \
  -vf "fps=5,scale=400:-1:flags=lanczos" \
  -t 30 \
  demo-small.gif
```

## 📊 **File Size Comparison**

| Format | Size | Quality | GitHub Display |
|--------|------|---------|----------------|
| Original MOV | 81MB | Excellent | ❌ No |
| Optimized GIF | ~15MB | Good | ✅ Yes |
| Small GIF | ~5MB | Fair | ✅ Yes |
| YouTube | 0MB | Excellent | ✅ Embedded |

## 🎯 **Final Recommendation**

For the **AWS Games Challenge**, use this approach:

1. **✅ Create optimized GIF** for immediate visual impact
2. **✅ Upload full video to GitHub Releases** for complete demonstration
3. **✅ Update README** with both options
4. **✅ Mention video in submission** as key feature demonstration

This provides:
- **Immediate visual engagement** (GIF in README)
- **Complete demonstration** (full video download)
- **Professional presentation** (proper GitHub integration)
- **Accessibility** (works for all users)

---

**Built using Amazon Q Developer CLI for AWS Games Challenge June 2025**
