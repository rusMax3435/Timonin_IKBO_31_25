#!/usr/bin/env bash
# Error-path: отсутствующий VFS, отсутствующий start-script, скрипт со ошибкой.
set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT"

echo "=== Demo 1: missing VFS (fatal, exit=1) ==="
echo exit | python3 main.py \
    --vfs does/not/exist.txt \
    --start-script scripts/startup_basic.txt
echo "exit code: $?"
echo ""

echo "=== Demo 2: missing start-script (warning, interactive continues) ==="
echo exit | python3 main.py \
    --vfs main.py \
    --start-script scripts/missing.txt
echo "exit code: $?"
echo ""

echo "=== Demo 3: start script stops on first error ==="
echo exit | python3 main.py \
    --vfs main.py \
    --start-script scripts/startup_errors.txt
echo "exit code: $?"