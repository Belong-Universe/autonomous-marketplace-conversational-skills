#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT_DIR="${REPO_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd -P)}"

SKILL_PATHS=(
  "skills/marketplace/belong-marketplace-runtime"
  "skills/human/shared/belong-marketplace-guide"
  "skills/human/shared/belong-setup-account"
  "skills/human/shared/belong-inbox"
  "skills/human/shared/belong-check-active-services"
  "skills/human/shared/belong-check-payments"
  "skills/human/shared/belong-check-reputation"
  "skills/human/buyer/belong-train-buying-agent"
  "skills/human/buyer/belong-start-buying-request"
  "skills/human/buyer/belong-check-buying-requests"
  "skills/human/buyer/belong-steer-buying-agent"
  "skills/human/seller/belong-train-selling-agent"
  "skills/human/seller/belong-check-selling-pipeline"
  "skills/human/seller/belong-steer-selling-agent"
  "skills/autonomous/belong-internal-buying-workflow"
  "skills/autonomous/belong-internal-selling-workflow"
  "skills/autonomous/belong-internal-active-service-actions"
  "skills/autonomous/belong-internal-disputes"
)

MIRROR_ROOTS=(
  ".agents/skills"
  ".claude/skills"
)

missing=0
for skill_path in "${SKILL_PATHS[@]}"; do
  if [[ ! -f "$ROOT_DIR/$skill_path/SKILL.md" ]]; then
    printf 'Missing skill folder: %s\n' "$skill_path" >&2
    missing=1
  fi
done

if [[ "$missing" == "1" ]]; then
  exit 1
fi

for mirror_root in "${MIRROR_ROOTS[@]}"; do
  mirror_dir="$ROOT_DIR/$mirror_root"
  rm -rf "$mirror_dir"
  mkdir -p "$mirror_dir"

  for skill_path in "${SKILL_PATHS[@]}"; do
    name="$(basename "$skill_path")"
    mkdir -p "$mirror_dir/$name"
    cp -R "$ROOT_DIR/$skill_path"/. "$mirror_dir/$name"/
  done

  printf 'Synced %s skills into %s\n' "${#SKILL_PATHS[@]}" "$mirror_root"
done
