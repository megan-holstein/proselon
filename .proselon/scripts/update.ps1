# Update the Proselon framework in the current project to the latest version.
#
# Windows-native counterpart of update.sh. Run from inside your Proselon
# project folder, in PowerShell:
#   powershell -ExecutionPolicy Bypass -File .proselon\scripts\update.ps1
#
# It pulls the latest framework from the public repo and refreshes the Proselon
# files in place. It is git-agnostic and never modifies your writing (Plot\,
# Manuscripts\, Worldbuilding\, ...), your Obsidian setup (.obsidian\), or your
# version history (.git\).

$ErrorActionPreference = "Stop"

$RepoOwner = "megan-holstein"
$RepoName  = "proselon"
$Branch    = "main"
$ZipUrl    = "https://github.com/$RepoOwner/$RepoName/archive/refs/heads/$Branch.zip"

$Target = (Get-Location).Path

# Guard: make sure we're in a Proselon project, not a random directory.
# A generic AGENTS.md alone is not enough -- this script overwrites
# AGENTS.md/README.md/LICENSE.md. Require a Proselon-specific marker.
function Test-ProselonProject {
    if (Test-Path (Join-Path $Target ".proselon\VERSION")) { return $true }
    if (Test-Path (Join-Path $Target ".proselon\workflow")) { return $true }
    if (Test-Path (Join-Path $Target ".workflow")) { return $true }  # pre-release flat layout
    $agents = Join-Path $Target "AGENTS.md"
    if ((Test-Path $agents) -and (Select-String -Path $agents -Pattern "proselon" -Quiet)) { return $true }
    if ((Test-Path (Join-Path $Target "Plot")) -and (Test-Path (Join-Path $Target "Manuscripts"))) { return $true }
    return $false
}
if (-not (Test-ProselonProject)) {
    Write-Error "This doesn't look like a Proselon project folder.`ncd into your project (the folder with AGENTS.md) and run this again."
    exit 1
}

# Remember the installed version before touching anything, so we can tell
# afterwards whether this update crossed a version boundary (and the content
# migrations in .proselon\MIGRATIONS.md may apply).
$OldVersionFile = Join-Path $Target ".proselon\VERSION"
$OldVersion = if (Test-Path $OldVersionFile) { (Get-Content $OldVersionFile -Raw).Trim() } else { "unknown" }

$Tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("proselon-update-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $Tmp | Out-Null

try {
    Write-Host "Downloading the latest Proselon framework..."
    $ZipPath = Join-Path $Tmp "proselon.zip"
    Invoke-WebRequest -Uri $ZipUrl -OutFile $ZipPath -UseBasicParsing
    Expand-Archive -Path $ZipPath -DestinationPath $Tmp

    $Src = Join-Path $Tmp "$RepoName-$Branch"
    if (-not (Test-Path $Src)) {
        Write-Error "Downloaded framework not found where expected."
        exit 1
    }

    # One-time migration from the old flat layout (.workflow/.scripts at the
    # project root). Any old launcher state is dropped; the launcher re-detects
    # what's installed on the next run.
    if ((Test-Path (Join-Path $Target ".workflow")) -or (Test-Path (Join-Path $Target ".scripts"))) {
        Write-Host "Migrating to the new .proselon\ layout..."
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $Target ".workflow")
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $Target ".scripts")
        $OldProselon = Join-Path $Target ".proselon"
        if ((Test-Path $OldProselon) -and -not (Test-Path (Join-Path $OldProselon "workflow"))) {
            Remove-Item -Recurse -Force $OldProselon
        }
    }

    # Refresh the framework. .proselon\ is pure framework, so it's safe to
    # replace wholesale. Copy first, then swap, so a failed copy can't leave
    # the project without a framework.
    $New = Join-Path $Target ".proselon.new"
    if (Test-Path $New) { Remove-Item -Recurse -Force $New }
    Copy-Item -Recurse (Join-Path $Src ".proselon") $New
    $Old = Join-Path $Target ".proselon"
    if (Test-Path $Old) { Remove-Item -Recurse -Force $Old }
    Move-Item $New $Old

    # Root framework files (Proselon-owned, not your writing).
    foreach ($f in @("AGENTS.md", "README.md", "LICENSE.md",
                     "Start Proselon - Mac.command", "Start Proselon - Windows.bat")) {
        $SrcFile = Join-Path $Src $f
        if (Test-Path $SrcFile) {
            Copy-Item -Force $SrcFile (Join-Path $Target $f)
        }
    }

    # CLAUDE.md ships as a symlink in the repo; write a portable regular file here.
    Set-Content -Path (Join-Path $Target "CLAUDE.md") -Value "@AGENTS.md" -NoNewline
    Add-Content -Path (Join-Path $Target "CLAUDE.md") -Value ""

    $VersionFile = Join-Path $Target ".proselon\VERSION"
    $Version = if (Test-Path $VersionFile) { (Get-Content $VersionFile -Raw).Trim() } else { "latest" }
    Write-Host "Proselon updated to $Version."

    # The refresh above replaced framework files only -- author content is
    # never touched. But an update can change the *shape* the framework
    # expects (where the workflow looks for project files). Those moves need
    # judgment, so they are done by the agent, not this script: hand it the
    # migration ledger and the version boundary it just crossed.
    if (($OldVersion -ne $Version) -and (Test-Path (Join-Path $Target ".proselon\MIGRATIONS.md"))) {
        Write-Host ""
        Write-Host "== CONTENT MIGRATION =="
        Write-Host "This project was on version: $OldVersion (now: $Version)."
        Write-Host "If you are the AI assistant running this update: read .proselon\MIGRATIONS.md"
        Write-Host "now and apply every migration entry newer than $OldVersion. Move the author"
        Write-Host "files those entries name from their old locations to the new canonical ones --"
        Write-Host "moves only, never edit a document's contents -- then report what moved. If no"
        Write-Host "entry applies, say so and move on."
        Write-Host "If you are a human running this by hand: open your Proselon session and say"
        Write-Host "'finish the Proselon update' so your assistant completes this step."
    }
}
finally {
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $Tmp
}
