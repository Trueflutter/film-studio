#!/usr/bin/env bash
# One-shot setup for the AI video studio (macOS). Safe to run again: every step checks first.
#
#   bash setup/install.sh [--dry-run] [--studio ~/Documents/my-studio]
#
# Installs: ffmpeg-full (cuts, mixes, captions), Node 22+ (graphics in code), the film-studio
# and HyperFrames Claude Code plugins with auto-update on, and the student's studio folder.
# Claude runs this for the student (see SETUP.md). It never asks for or prints API keys.

set -u
DRY=0
STUDIO="$HOME/Documents/my-studio"
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --studio) shift; STUDIO="$1" ;;
  esac
  shift
done
KIT_REPO="Trueflutter/film-studio"
HERE="$(cd "$(dirname "$0")/.." && pwd)"   # the kit checkout this script came from
FAILED=0
NODE_SHADOW=0

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
todo() { printf '  \033[33m→\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; FAILED=1; }
run()  { if [ $DRY = 1 ]; then echo "    [dry-run] $*"; else "$@"; fi; }

echo "AI video studio setup$([ $DRY = 1 ] && echo ' (dry run)')"

if [ "$(uname)" != "Darwin" ]; then
  bad "This installer is for macOS. On Windows: winget install Gyan.FFmpeg OpenJS.NodeJS Python.Python.3.12, then follow SETUP.md from step 3."
  exit 1
fi

# 1. Homebrew (needs the student's password once, so Claude can't do it for them)
if command -v brew >/dev/null 2>&1; then
  ok "Homebrew"
else
  bad "Homebrew is missing. Open the Terminal app, paste this, press Return and type your Mac password when asked:"
  echo '      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  echo "    Then ask Claude to run the setup again."
  exit 1
fi
BREW_BIN="$(brew --prefix)/bin"

# 2. ffmpeg with libass (captions need it; plain Homebrew ffmpeg lacks it)
if [ -x "$(brew --prefix)/opt/ffmpeg-full/bin/ffmpeg" ]; then
  ok "ffmpeg-full"
else
  todo "installing ffmpeg-full (a few minutes)"
  run brew install ffmpeg-full && ok "ffmpeg-full" || bad "ffmpeg-full did not install"
fi

# 3. Node 22 or newer (HyperFrames renders graphics with it)
node_major() { "$1" -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0; }
NODE_NOW="$(command -v node || true)"
if [ -n "$NODE_NOW" ] && [ "$(node_major "$NODE_NOW")" -ge 22 ]; then
  ok "Node $("$NODE_NOW" --version)"
else
  todo "installing Node (current release)"
  run brew install node || bad "Node did not install"
  if [ $DRY = 0 ] && [ -n "$NODE_NOW" ] && [ "$NODE_NOW" != "$BREW_BIN/node" ]; then
    todo "an older Node ($NODE_NOW) comes first on your PATH; your studio notes tell Claude to use $BREW_BIN/node"
    NODE_SHADOW=1
  fi
fi

# 4. Python 3.9+ (the film command)
if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
  ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
else
  todo "installing Python"
  run brew install python && ok "Python" || bad "Python did not install"
fi

# 5. The Claude Code plugins: film-studio and HyperFrames, auto-updating
find_claude() {
  if command -v claude >/dev/null 2>&1; then command -v claude; return; fi
  # The desktop app ships its own binary; take the newest.
  ls -t "$HOME/Library/Application Support/Claude/claude-code/"*/*/claude.app/Contents/MacOS/claude 2>/dev/null | head -1
}
CLAUDE_BIN="$(find_claude)"
if [ -z "$CLAUDE_BIN" ]; then
  bad "Claude Code not found. Install the Claude desktop app (claude.ai/download), open the Code tab once, then run the setup again."
else
  have_mkt() { "$CLAUDE_BIN" plugin marketplace list 2>/dev/null | grep -q "$1"; }
  have_plugin() { "$CLAUDE_BIN" plugin list 2>/dev/null | grep -q "$1"; }
  for pair in "saqr-film|$KIT_REPO|film-studio@saqr-film" "hyperframes|heygen-com/hyperframes|hyperframes@hyperframes"; do
    IFS='|' read -r MKT SRC PLUGIN <<EOF
$pair
EOF
    if have_mkt "$MKT"; then
      run "$CLAUDE_BIN" plugin marketplace update "$MKT" >/dev/null 2>&1
    else
      run "$CLAUDE_BIN" plugin marketplace add "$SRC" >/dev/null 2>&1 || bad "could not add the $MKT marketplace ($SRC)"
    fi
    if have_plugin "$PLUGIN"; then
      run "$CLAUDE_BIN" plugin update "$PLUGIN" >/dev/null 2>&1; ok "$PLUGIN (up to date)"
    else
      run "$CLAUDE_BIN" plugin install "$PLUGIN" >/dev/null 2>&1 && ok "$PLUGIN installed" || bad "$PLUGIN did not install"
    fi
  done
  # Auto-update both marketplaces, so fixes during the week arrive without anyone doing anything.
  SETTINGS="$HOME/.claude/settings.json"
  if [ $DRY = 1 ]; then
    echo "    [dry-run] set autoUpdate on saqr-film and hyperframes in $SETTINGS"
  elif [ -f "$SETTINGS" ]; then
    python3 - "$SETTINGS" <<'PY' && ok "auto-update on" || bad "could not turn on auto-update (the studio still works)"
import json, shutil, sys
p = sys.argv[1]
d = json.load(open(p))
shutil.copy(p, p + ".before-film-studio")
known = d.setdefault("extraKnownMarketplaces", {})
srcs = {"saqr-film": "Trueflutter/film-studio", "hyperframes": "heygen-com/hyperframes"}
for name, repo in srcs.items():
    entry = known.setdefault(name, {"source": {"source": "github", "repo": repo}})
    entry["autoUpdate"] = True
json.dump(d, open(p, "w"), indent=2)
PY
  fi
fi

# 6. The studio folder: where every production lives
if [ -d "$STUDIO" ]; then
  ok "studio folder $STUDIO"
else
  run mkdir -p "$STUDIO"
  run cp -R "$HERE/starter/." "$STUDIO/"
  ok "studio folder created at $STUDIO"
fi
if [ -f "$STUDIO/.env" ]; then
  ok ".env exists (keys are filled in by Claude, never printed)"
else
  run cp "$HERE/starter/.env.example" "$STUDIO/.env"
  todo ".env created: Claude asks for your EvoLink and ElevenLabs keys next"
fi

if [ $NODE_SHADOW = 1 ] && [ $DRY = 0 ] && ! grep -q "HyperFrames needs Node 22" "$STUDIO/CLAUDE.md" 2>/dev/null; then
  printf '\n- HyperFrames needs Node 22+: an older Node comes first on PATH here, so run graphics commands with PATH="%s:$PATH".\n' "$BREW_BIN" >> "$STUDIO/CLAUDE.md"
  ok "studio notes: graphics use $BREW_BIN/node"
fi

# 7. Warm the graphics renderer so the first render in class is fast
if [ $DRY = 0 ]; then
  NPX="$(command -v npx)"; [ "$(node_major "$(command -v node)")" -lt 22 ] && NPX="$BREW_BIN/npx"
  "$NPX" -y hyperframes --version >/dev/null 2>&1 && ok "HyperFrames renderer ready" || todo "HyperFrames will download on first use"
fi

# 8. The check
FILM="$HERE/film-studio/bin/film"
if [ $DRY = 0 ] && [ -x "$FILM" ]; then
  echo; (cd "$STUDIO" && "$FILM" doctor) || true
fi

echo
if [ $FAILED = 0 ]; then
  echo "Done. Start a new Claude session in $STUDIO (or type /reload-plugins) so the studio skills load."
else
  echo "Finished with problems: fix the ✗ lines above, then run the setup again."
fi
exit $FAILED
