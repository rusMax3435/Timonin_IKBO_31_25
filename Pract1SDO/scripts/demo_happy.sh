#!/usr/bin/env bash
# Happy-path: запуск с обоими CLI-параметрами (--vfs, --start-script).
# На этапе 2 VFS не парсится — используется любой существующий файл.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT"

echo "=== Demo 1: main.py as VFS placeholder + startup_basic.txt ==="
echo exit | python3 main.py \
    --vfs main.py \
    --start-script scripts/startup_basic.txt
echo ""

echo "=== Demo 2: --help ==="
python3 main.py --help