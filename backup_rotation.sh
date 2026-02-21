#!/usr/bin/env bash
set -euo pipefail

display_usage() {
  echo "Usage: $0 <source_dir> <backup_dir> [keep_count]"
  echo "Example: $0 ./logs ./backup 5"
  exit 1
}

# args
if [[ $# -lt 2 ]]; then
  display_usage
fi

source_dir="$1"
backup_dir="$2"
keep_count="${3:-5}"

# Validate source_dir
if [[ ! -d "$source_dir" ]]; then
  echo "ERROR: source_dir does not exist or is not a directory: $source_dir" >&2
  exit 2
fi

# Ensure zip exists (macOS usually has it)
if ! command -v zip >/dev/null 2>&1; then
  echo "ERROR: 'zip' command not found. Install it or use tar instead." >&2
  exit 3
fi

# Create backup dir
mkdir -p "$backup_dir"

# Convert backup_dir to absolute path (prevents path issues)
backup_dir_abs="$(cd "$backup_dir" && pwd)"

timestamp="$(date '+%Y-%m-%d-%H-%M-%S')"
backup_file="${backup_dir_abs}/backup_${timestamp}.zip"

create_backup() {
  echo "Creating backup: $backup_file"

  # Zip CONTENTS of source_dir into backup_dir
  (cd "$source_dir" && zip -rq "$backup_file" .)

  echo "Backup generated successfully: $backup_file"
}

perform_rotation() {
  backups=$(ls -1t "${backup_dir_abs}/backup_"*.zip 2>/dev/null || true)

  echo "$keep_count"
  count=0
  for file in $backups; do
    count=$((count + 1))
    if (( count > keep_count )); then
      echo "Deleting old backup: $file"
      rm -f "$file"
    fi
  done

  echo "Rotation complete. Kept latest ${keep_count} backups in: $backup_dir_abs"
}

create_backup
perform_rotation