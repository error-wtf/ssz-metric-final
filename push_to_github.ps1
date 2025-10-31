# SSZ Metric - Interactive GitHub Push Helper
# © 2025 Carmen Wrede & Lino Casu

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  SSZ Metric v1.0.0 - GitHub Push" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check git status
Write-Host "[1/5] Checking git status..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "ERROR: You have uncommitted changes!" -ForegroundColor Red
    git status --short
    exit 1
}
Write-Host "OK: Working tree is clean" -ForegroundColor Green

# Count commits
$commitCount = git rev-list --count HEAD
Write-Host "OK: $commitCount commits ready to push" -ForegroundColor Green

# Check for existing remote
Write-Host "`n[2/5] Checking for GitHub remote..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "OK: Remote already configured:" -ForegroundColor Green
    Write-Host "    $remoteExists" -ForegroundColor White
    
    $continue = Read-Host "`nRemote exists. Continue with push? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted by user." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "INFO: No remote configured yet" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "BEFORE CONTINUING:" -ForegroundColor Cyan
    Write-Host "1. Open: https://github.com/new" -ForegroundColor White
    Write-Host "2. Create repo named: ssz-full-metric" -ForegroundColor White
    Write-Host "3. Make it Public (or Private)" -ForegroundColor White
    Write-Host "4. DO NOT add README, .gitignore, or License!" -ForegroundColor Red
    Write-Host ""
    
    $created = Read-Host "Have you created the GitHub repo? (y/n)"
    if ($created -ne "y") {
        Write-Host "`nPlease create the repo first, then run this script again." -ForegroundColor Yellow
        Write-Host "Press any key to open GitHub in browser..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        Start-Process "https://github.com/new"
        exit 0
    }
    
    Write-Host "`n[3/5] Adding GitHub remote..." -ForegroundColor Yellow
    $username = Read-Host "Enter your GitHub username"
    
    if (-not $username) {
        Write-Host "ERROR: Username required!" -ForegroundColor Red
        exit 1
    }
    
    $repoUrl = "https://github.com/$username/ssz-full-metric.git"
    Write-Host "Adding remote: $repoUrl" -ForegroundColor White
    
    git remote add origin $repoUrl
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to add remote!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "OK: Remote added successfully" -ForegroundColor Green
}

# Verify remote
Write-Host "`n[4/5] Verifying remote..." -ForegroundColor Yellow
git remote -v
Write-Host ""

# Ask for confirmation
Write-Host "READY TO PUSH:" -ForegroundColor Cyan
Write-Host "  Commits: $commitCount" -ForegroundColor White
Write-Host "  Remote:  $(git remote get-url origin)" -ForegroundColor White
Write-Host "  Branch:  master" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Push to GitHub now? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Aborted by user." -ForegroundColor Yellow
    exit 0
}

# Push!
Write-Host "`n[5/5] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "This may take 1-3 minutes for the first push..." -ForegroundColor Gray
Write-Host ""

git push -u origin master

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Push failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Authentication failed:" -ForegroundColor White
    Write-Host "   - Use Personal Access Token, not password!" -ForegroundColor Gray
    Write-Host "   - Create at: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Remote rejected:" -ForegroundColor White
    Write-Host "   - Make sure repo exists and is empty" -ForegroundColor Gray
    Write-Host "   - Check you have write access" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host "`nOK: Push successful!" -ForegroundColor Green

# Create and push tag
Write-Host "`n[BONUS] Creating version tag..." -ForegroundColor Yellow
git tag -a v1.0.0 -m "SSZ Metric v1.0.0 - Production Release"
git push origin v1.0.0

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK: Tag v1.0.0 created and pushed" -ForegroundColor Green
}

# Success summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  PUSH COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your repository is now live at:" -ForegroundColor White
$repoUrl = git remote get-url origin
$webUrl = $repoUrl -replace '\.git$', '' -replace 'https://github.com/', 'https://github.com/'
Write-Host $webUrl -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit your repo and check that everything looks good" -ForegroundColor White
Write-Host "2. Check GitHub Actions (will start automatically)" -ForegroundColor White
Write-Host "3. Create a Release for v1.0.0 (optional)" -ForegroundColor White
Write-Host "4. Share with the world!" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to open your repo in browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Start-Process $webUrl
