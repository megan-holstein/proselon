#!/bin/bash
cd "$(dirname "$0")"

# Locate the writing engines.
find_claude() {
    if command -v claude >/dev/null 2>&1; then command -v claude; return 0; fi
    if [ -x "$HOME/.local/bin/claude" ]; then echo "$HOME/.local/bin/claude"; return 0; fi
    return 1
}
have_claude() { find_claude >/dev/null 2>&1; }
have_codex()  { command -v codex >/dev/null 2>&1; }

# Pick the engine from what's installed. Only ask when it's ambiguous: both
# installed (which one this time?) or neither (which subscription to set up?).
ENGINE=""
if have_claude && have_codex; then
    echo "Welcome to Proselon."
    echo ""
    echo "You have both Claude and ChatGPT set up. Which should I write with today?"
    echo ""
    echo "  1) Claude"
    echo "  2) ChatGPT"
    echo ""
    read -p "Type 1 or 2 and press Enter: " CHOICE
    case "$CHOICE" in
        2) ENGINE="chatgpt" ;;
        *) ENGINE="claude" ;;
    esac
elif have_claude; then
    ENGINE="claude"
elif have_codex; then
    ENGINE="chatgpt"
else
    echo "Welcome to Proselon."
    echo ""
    echo "Proselon writes using an AI subscription you already have. Which one do you use?"
    echo ""
    echo "  1) Claude    (any paid plan)"
    echo "  2) ChatGPT   (Plus or Pro)"
    echo ""
    read -p "Type 1 or 2 and press Enter: " CHOICE
    case "$CHOICE" in
        1) ENGINE="claude" ;;
        2) ENGINE="chatgpt" ;;
        *)
            echo ""
            echo "Proselon currently works with a Claude or a ChatGPT subscription. Once you"
            echo "have one, double-click this launcher again."
            read -p "Press Enter to close."
            exit 0
            ;;
    esac
fi

# Detect git without triggering Apple's developer-tools popup
git_available() {
    if xcode-select -p >/dev/null 2>&1; then return 0; fi
    GIT_PATH="$(command -v git 2>/dev/null)"
    if [ -n "$GIT_PATH" ] && [ "$GIT_PATH" != "/usr/bin/git" ]; then return 0; fi
    return 1
}

if ! git_available; then
    echo "Your project is always saved right here on your computer, exactly where you left it."
    echo ""
    echo "One optional extra: Proselon can also keep a history of past versions, so you"
    echo "can go back in time to earlier drafts. That part needs a free one-time download"
    echo "from Apple."
    echo ""
    read -p "Install it now? Type y for yes, or just press Enter to skip: " REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        xcode-select --install >/dev/null 2>&1
        echo ""
        echo "Click \"Install\" in the window that just popped up. When it finishes,"
        echo "double-click this launcher again."
        read -p "Press Enter to close."
        exit 0
    fi
    echo ""
fi

# Obsidian is the optional window for reading and editing your book. If it's
# installed, open this folder in it; otherwise stay quiet (see README.md).
if open -Ra Obsidian >/dev/null 2>&1; then
    open "obsidian://open?path=${PWD// /%20}" 2>/dev/null || open -a Obsidian
fi

if [ "$ENGINE" = "claude" ]; then

    CLAUDE_BIN="$(find_claude)" || {
        echo "Proselon writes with Claude Code, which isn't installed yet."
        echo "It's free to install and uses the Claude subscription you already have."
        echo ""
        read -p "Press Enter to install Claude Code now (or close this window to cancel)..."
        echo ""
        curl -fsSL https://claude.ai/install.sh | bash
        CLAUDE_BIN="$(find_claude)" || {
            echo ""
            echo "The install didn't finish. See \"README.md\" in this folder for help."
            read -p "Press Enter to close."
            exit 1
        }
    }

    echo ""
    echo "Starting Proselon..."
    echo "If you're asked to log in, choose \"Claude account\" and use your normal Claude login."
    echo ""
    exec "$CLAUDE_BIN"

else

    if ! command -v codex >/dev/null 2>&1; then
        echo "Proselon writes with Codex -- the part of ChatGPT that can work with the"
        echo "files on your computer. It isn't installed yet. It's free, and it runs on"
        echo "the ChatGPT subscription you already have."
        echo ""
        if command -v brew >/dev/null 2>&1; then
            read -p "Press Enter to install it now (or close this window to cancel)..."
            echo ""
            brew install codex
        elif command -v npm >/dev/null 2>&1; then
            read -p "Press Enter to install it now (or close this window to cancel)..."
            echo ""
            npm install -g @openai/codex
        else
            echo "First install Node.js from https://nodejs.org (choose the LTS version),"
            echo "then double-click this launcher again."
            read -p "Press Enter to close."
            exit 1
        fi
        if ! command -v codex >/dev/null 2>&1; then
            echo ""
            echo "The install didn't finish. See \"README.md\" in this folder for help."
            read -p "Press Enter to close."
            exit 1
        fi
    fi

    echo ""
    echo "Starting Proselon..."
    echo "If you're asked to log in, choose \"Sign in with ChatGPT\" and use your normal ChatGPT login."
    echo ""
    exec codex

fi
