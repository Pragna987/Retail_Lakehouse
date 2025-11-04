# GitHub Upload Guide - Step-by-Step

This guide walks you through uploading your complete lakehouse project to GitHub.

---

## Prerequisites

- ✅ Git installed: `git --version`
- ✅ GitHub account created
- ✅ Repository created on GitHub: `Pragna987/Retail_Lakehouse`

---

## Option 1: Using VS Code (Recommended)

### Step 1: Open Source Control Panel

1. Click the **Source Control** icon in VS Code sidebar (3rd icon, looks like branches)
2. Or press `Ctrl+Shift+G`

### Step 2: Initialize Repository (If Not Already Done)

If you see "Initialize Repository" button:
1. Click **Initialize Repository**
2. VS Code creates `.git` folder

If already initialized, skip to Step 3.

### Step 3: Stage All Files

1. In Source Control panel, you'll see all changed files
2. Click the **+** icon next to "Changes" to stage all files
3. Or hover over individual files and click **+** to stage specific files

### Step 4: Commit Changes

1. Type commit message in the text box at top:
   ```
   Complete lakehouse implementation with Steps 5-16
   ```
2. Click the **✓** checkmark icon (Commit)
3. If prompted about no staged changes, click "Yes" to stage all and commit

### Step 5: Add Remote Repository

1. Click **...** (three dots) in Source Control panel
2. Select **Remote** → **Add Remote**
3. Enter repository URL:
   ```
   https://github.com/Pragna987/Retail_Lakehouse.git
   ```
4. Name it: `origin`

### Step 6: Push to GitHub

1. Click **...** → **Push**
2. Select branch: `main` (or create if needed)
3. If prompted for credentials:
   - Username: Your GitHub username
   - Password: Use **Personal Access Token** (not your GitHub password)

### Step 7: Verify Upload

1. Open browser: https://github.com/Pragna987/Retail_Lakehouse
2. Verify all files are visible
3. Check that README.md displays correctly

---

## Option 2: Using Command Line (PowerShell)

### Step 1: Navigate to Project Directory

```powershell
cd C:\Users\Sri\Retail_Lakehouse\Retail_Lakehouse\retail-lakehouse-project
```

### Step 2: Initialize Git (If Not Already Done)

```powershell
git init
```

### Step 3: Add Remote Repository

```powershell
git remote add origin https://github.com/Pragna987/Retail_Lakehouse.git
```

Verify remote:
```powershell
git remote -v
```

### Step 4: Stage All Files

```powershell
git add .
```

Check what will be committed:
```powershell
git status
```

### Step 5: Commit Changes

```powershell
git commit -m "Complete lakehouse implementation with Steps 5-16"
```

### Step 6: Set Main Branch and Push

```powershell
git branch -M main
git push -u origin main
```

If prompted for credentials:
- Username: Your GitHub username
- Password: **Personal Access Token** (see below)

### Step 7: Verify Upload

```powershell
# Open GitHub in browser
Start-Process https://github.com/Pragna987/Retail_Lakehouse
```

---

## Creating GitHub Personal Access Token (PAT)

If you need a Personal Access Token for authentication:

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Name it: `Retail_Lakehouse`
4. Select scopes:
   - ✅ `repo` (full control of private repositories)
5. Click **Generate token**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing to GitHub

---

## Handling Large Files

The `.gitignore` file should already exclude large files:

```gitignore
# Large data files
data/bronze/
data/silver/
data/gold/
raw_data/*.csv

# Virtual environment
.venv/
venv/

# Python cache
__pycache__/
*.pyc
```

### If You Want to Upload Data (Not Recommended)

**Option A: Use Git LFS (Large File Storage)**

```powershell
# Install Git LFS
git lfs install

# Track large CSV files
git lfs track "raw_data/*.csv"
git lfs track "data/**/*.parquet"

# Commit and push
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

**Option B: Upload to Cloud Storage**
- Upload large files to Google Drive, Dropbox, or DBFS
- Include download link in README.md

---

## Common Issues and Solutions

### Issue 1: "fatal: remote origin already exists"

**Solution**: Remove and re-add remote

```powershell
git remote remove origin
git remote add origin https://github.com/Pragna987/Retail_Lakehouse.git
```

### Issue 2: "failed to push some refs"

**Solution**: Pull changes first

```powershell
git pull origin main --rebase
git push -u origin main
```

### Issue 3: "Authentication failed"

**Solution**: Use Personal Access Token instead of password

1. Generate PAT (see above)
2. When prompted for password, paste the PAT

### Issue 4: "The requested URL returned error: 403"

**Solution**: Check repository URL and permissions

```powershell
git remote set-url origin https://github.com/Pragna987/Retail_Lakehouse.git
```

### Issue 5: "Changes not staged for commit"

**Solution**: Stage all changes

```powershell
git add .
git commit -m "Your message"
```

---

## Best Practices

### ✅ DO:
- Write descriptive commit messages
- Review changes before committing (`git status`, `git diff`)
- Commit frequently (small, logical changes)
- Use `.gitignore` to exclude large files
- Test code locally before pushing

### ❌ DON'T:
- Commit sensitive data (passwords, API keys)
- Upload large datasets to GitHub (use Git LFS or cloud storage)
- Force push (`git push -f`) unless absolutely necessary
- Commit temporary files (`.pyc`, `__pycache__`)

---

## Updating Repository After Changes

### Make Changes Locally

1. Edit files in VS Code
2. Save changes

### Commit and Push Updates

**VS Code**:
1. Open Source Control panel
2. Stage changes (click **+**)
3. Enter commit message
4. Click **✓** to commit
5. Click **...** → **Push**

**Command Line**:
```powershell
git add .
git commit -m "Add ML models and dashboards"
git push
```

---

## Verifying GitHub Upload

### Check Repository Contents

1. Go to: https://github.com/Pragna987/Retail_Lakehouse
2. Verify folder structure:
   ```
   ├── retail-lakehouse-project/
   │   ├── scripts/
   │   ├── databricks/
   │   ├── examples/
   │   ├── setup_storage.py
   │   ├── generate_retail_data.py
   │   ├── run_all.py
   │   ├── README.md
   │   └── ...
   ├── README.md
   └── test_pyspark.py
   ```

### Check README Display

1. Scroll down on repository page
2. Verify README.md renders correctly
3. Check that all formatting (headings, code blocks) displays properly

### Verify File Count

Should see approximately:
- 20+ files in `retail-lakehouse-project/`
- 10+ Python scripts
- 5+ Markdown documentation files

---

## Next Steps After Upload

1. **Share repository**:
   ```
   https://github.com/Pragna987/Retail_Lakehouse
   ```

2. **Add repository description** on GitHub:
   - Click ⚙️ Settings on repository page
   - Add description: "Retail Data Lakehouse with Apache Spark and Delta Lake"
   - Add topics: `data-engineering`, `apache-spark`, `delta-lake`, `python`, `medallion-architecture`

3. **Create README badges** (optional):
   - Python version badge
   - License badge
   - Build status badge

4. **Enable GitHub Pages** (optional):
   - Settings → Pages
   - Publish documentation

---

## Collaboration Features

### Invite Collaborators

1. Repository → Settings → Collaborators
2. Click "Add people"
3. Enter GitHub username

### Create Issues

Track bugs or enhancements:
- Repository → Issues → New Issue
- Add labels (bug, enhancement, documentation)

### Pull Requests

For collaborative development:
1. Create new branch: `git checkout -b feature-name`
2. Make changes and commit
3. Push branch: `git push origin feature-name`
4. Create Pull Request on GitHub

---

## Quick Reference Commands

```powershell
# Check status
git status

# View changes
git diff

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename

# Update from remote
git pull origin main

# View remote URLs
git remote -v
```

---

**You're all set! Your lakehouse project is now on GitHub.** 🎉

Share the link: **https://github.com/Pragna987/Retail_Lakehouse**
