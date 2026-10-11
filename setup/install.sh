#!/usr/bin/env bash
# One-shot setup for the AI video studio, on a Mac (Homebrew) or a Windows PC (winget, run from
# the Git Bash that Claude Code uses on Windows). Safe to run again: every step checks first.
#
#   bash setup/install.sh [--dry-run] [--studio ~/Documents/my-studio]
#
# Installs: ffmpeg with libass (cuts, mixes, captions), Node 22+ (graphics in code), Python 3.9+,
# the film-studio plugin (auto-updating), the HyperFrames plugin, and the student's studio folder.
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

case "$(uname -s)" in
  Darwin) OS=mac ;;
  MINGW*|MSYS*|CYGWIN*) OS=win ;;
  *) echo "This installer supports macOS and Windows (Git Bash). Follow SETUP.md by hand on Linux."; exit 1 ;;
esac
echo "AI video studio setup, $([ $OS = mac ] && echo macOS || echo Windows)$([ $DRY = 1 ] && echo ' (dry run)')"

# Windows: winget puts new tools where this shell can't see them until a new session; look there too.
if [ $OS = win ]; then
  LAD="$(cygpath -u "${LOCALAPPDATA:-$HOME/AppData/Local}")"
  export PATH="$LAD/Microsoft/WinGet/Links:/c/Program Files/nodejs:$LAD/Programs/Python/Python312:$LAD/Programs/Python/Python312/Scripts:$PATH"
  WINGET="winget.exe"
  wg() { run "$WINGET" install -e --id "$1" --silent --accept-source-agreements --accept-package-agreements; }
  command -v "$WINGET" >/dev/null 2>&1 || { bad "winget is missing: install 'App Installer' from the Microsoft Store, then run the setup again."; exit 1; }
  ok "winget"
fi

# 1. Homebrew (Mac only; needs the student's password once, so Claude can't do it for them)
if [ $OS = mac ]; then
  if command -v brew >/dev/null 2>&1; then
    ok "Homebrew"
  else
    bad "Homebrew is missing. Open the Terminal app, paste this, press Return and type your Mac password when asked:"
    echo '      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo "    Then ask Claude to run the setup again."
    exit 1
  fi
  BREW_BIN="$(brew --prefix)/bin"
fi

# 2. ffmpeg with libass (captions need it; Homebrew's plain ffmpeg lacks it, Gyan's Windows build has it)
if [ $OS = mac ]; then
  if [ -x "$(brew --prefix)/opt/ffmpeg-full/bin/ffmpeg" ]; then ok "ffmpeg-full"
  else todo "installing ffmpeg-full (a few minutes)"; run brew install ffmpeg-full && ok "ffmpeg-full" || bad "ffmpeg-full did not install"; fi
else
  if command -v ffmpeg >/dev/null 2>&1; then ok "ffmpeg"
  else todo "installing ffmpeg (a few minutes)"; wg Gyan.FFmpeg && ok "ffmpeg" || bad "ffmpeg did not install"; fi
fi

# 3. Node 22 or newer (HyperFrames renders graphics with it)
node_major() { "$1" -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0; }
NODE_NOW="$(command -v node || true)"
if [ -n "$NODE_NOW" ] && [ "$(node_major "$NODE_NOW")" -ge 22 ]; then
  ok "Node $("$NODE_NOW" --version)"
else
  todo "installing Node (current release; on Windows, click Yes if asked)"
  if [ $OS = mac ]; then run brew install node || bad "Node did not install"
  else wg OpenJS.NodeJS || bad "Node did not install"; fi
  if [ $OS = mac ] && [ $DRY = 0 ] && [ -n "$NODE_NOW" ] && [ "$NODE_NOW" != "$BREW_BIN/node" ]; then
    todo "an older Node ($NODE_NOW) comes first on your PATH; your studio notes tell Claude to use $BREW_BIN/node"
    NODE_SHADOW=1
  fi
fi

# 4. Python 3.9+ (the film command). On Windows `python3` may be a Store placeholder, so test each name.
find_python() {
  for c in python3 python py; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
      echo "$c"; return
    fi
  done
}
PY="$(find_python)"
if [ -n "$PY" ]; then
  ok "Python $("$PY" -c 'import platform; print(platform.python_version())')"
else
  todo "installing Python"
  if [ $OS = mac ]; then run brew install python; else wg Python.Python.3.12; fi
  PY="$(find_python)"
  if [ -n "$PY" ]; then ok "Python"; elif [ $DRY = 1 ]; then PY=python3; else bad "Python did not install"; fi
fi

# 5. The Claude Code plugins: film-studio (auto-updating) and HyperFrames
find_claude() {
  if command -v claude >/dev/null 2>&1; then command -v claude; return; fi
  if [ $OS = mac ]; then  # the desktop app ships its own binary; take the newest
    ls -t "$HOME/Library/Application Support/Claude/claude-code/"*/*/claude.app/Contents/MacOS/claude 2>/dev/null | head -1
  else
    find "$LAD" "$(cygpath -u "${APPDATA:-$HOME/AppData/Roaming}")" -maxdepth 7 -iname claude.exe 2>/dev/null | grep -i claude-code | head -1
  fi
}
CLAUDE_BIN="$(find_claude)"
if [ -z "$CLAUDE_BIN" ]; then
  todo "Claude can't add plugins from here. Ask the student to type these four lines in Claude Code, one at a time:"
  echo "      /plugin marketplace add $KIT_REPO"
  echo "      /plugin install film-studio@saqr-film"
  echo "      /plugin marketplace add heygen-com/hyperframes"
  echo "      /plugin install hyperframes@hyperframes"
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
fi

# Auto-update only the course's own marketplace, so our fixes arrive by themselves. HyperFrames is
# third-party: it stays at the version installed today unless someone updates it on purpose.
SETTINGS="$HOME/.claude/settings.json"
if [ $DRY = 1 ]; then
  echo "    [dry-run] set autoUpdate on saqr-film in $SETTINGS"
elif [ -n "$PY" ]; then
  if [ $OS = win ]; then SETTINGS_ARG="$(cygpath -w "$SETTINGS")"; else SETTINGS_ARG="$SETTINGS"; fi
  "$PY" - "$SETTINGS_ARG" <<'PY' && ok "auto-update on for the course kit" || bad "could not turn on auto-update (the studio still works)"
import json, os, shutil, sys
p = sys.argv[1]
d = {}
if os.path.exists(p):
    d = json.load(open(p, encoding="utf-8"))
    shutil.copy(p, p + ".before-film-studio")
else:
    os.makedirs(os.path.dirname(p), exist_ok=True)
known = d.setdefault("extraKnownMarketplaces", {})
entry = known.setdefault("saqr-film", {"source": {"source": "github", "repo": "Trueflutter/film-studio"}})
entry["autoUpdate"] = True
json.dump(d, open(p, "w", encoding="utf-8"), indent=2)
PY
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
if [ $OS = win ] && [ $DRY = 0 ] && ! grep -q "Windows PC" "$STUDIO/CLAUDE.md" 2>/dev/null; then
  printf '\n- This is a Windows PC: commands run in Git Bash. If a tool installed today is "not found", start a new Claude session (new tools join the PATH then).\n' >> "$STUDIO/CLAUDE.md"
fi

# 7. The check
if [ $DRY = 0 ] && [ -n "$PY" ]; then
  echo; (cd "$STUDIO" && sh "$HERE/film-studio/bin/film" doctor) || true
fi

echo
if [ $FAILED = 0 ]; then
  echo "Done. Start a new Claude session in $STUDIO (or type /reload-plugins) so the studio skills load."
else
  echo "Finished with problems: fix the ✗ lines above, then run the setup again."
fi
exit $FAILED
