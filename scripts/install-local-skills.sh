#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT_DIR="${REPO_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd -P)}"
DEST_DIR="${BELONG_SKILLS_DEST:-}"
HOST=""
SCOPE="repo"
UPDATE_EXISTING=1
BACKUP_EXISTING=1
DRY_RUN=0
LIST_ONLY=0

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

usage() {
  printf '%s\n' "Usage: $0 [--repo-root PATH] [--host codex|cursor|claude-code|other-ai|custom] [--scope repo|user] [--dest PATH] [--skip-existing] [--no-backup] [--dry-run] [--list]"
  printf '%s\n' ""
  printf '%s\n' "Installs or updates this repo's Belong skills into a host-native SKILL.md directory."
  printf '%s\n' "Known hosts have safe defaults: Codex/Cursor -> .agents/skills; Claude Code -> .claude/skills for repo scope."
  printf '%s\n' "Known hosts have user defaults: Codex/Cursor -> \$HOME/.agents/skills; Claude Code -> \$HOME/.claude/skills."
  printf '%s\n' "Other AI hosts are welcome; use the host's documented skills/custom-instructions directory with --dest PATH or BELONG_SKILLS_DEST."
  printf '%s\n' "Existing skill folders are backed up before replacement unless --no-backup is used."
}

resolve_default_dest() {
  case "$HOST:$SCOPE" in
    codex:repo|cursor:repo)
      DEST_DIR="$ROOT_DIR/.agents/skills"
      ;;
    claude-code:repo)
      DEST_DIR="$ROOT_DIR/.claude/skills"
      ;;
    codex:user|cursor:user)
      DEST_DIR="$HOME/.agents/skills"
      ;;
    claude-code:user)
      DEST_DIR="$HOME/.claude/skills"
      ;;
    other-ai:*|custom:*)
      ;;
    *)
      printf 'Unsupported host/scope combination: host=%s scope=%s\n' "$HOST" "$SCOPE" >&2
      exit 2
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      ROOT_DIR="$(cd "${2:?Missing path after --repo-root}" && pwd -P)"
      shift 2
      ;;
    --host)
      HOST="${2:?Missing value after --host}"
      shift 2
      ;;
    --scope)
      SCOPE="${2:?Missing value after --scope}"
      shift 2
      ;;
    --dest)
      DEST_DIR="${2:?Missing path after --dest}"
      shift 2
      ;;
    --skip-existing)
      UPDATE_EXISTING=0
      shift
      ;;
    --force)
      UPDATE_EXISTING=1
      shift
      ;;
    --no-backup)
      BACKUP_EXISTING=0
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --list)
      LIST_ONLY=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "$LIST_ONLY" == "1" ]]; then
  printf '%s\n' "${SKILL_PATHS[@]}"
  exit 0
fi

case "$SCOPE" in
  repo|user) ;;
  *)
    printf 'Unsupported scope: %s\n' "$SCOPE" >&2
    usage >&2
    exit 2
    ;;
esac

if [[ -n "$HOST" ]]; then
  case "$HOST" in
    codex|cursor|claude-code|other-ai|custom) ;;
    *)
      printf 'Unsupported host: %s\n' "$HOST" >&2
      usage >&2
      exit 2
      ;;
  esac
fi

if [[ -z "$DEST_DIR" && -n "$HOST" ]]; then
  resolve_default_dest
fi

if [[ -z "$DEST_DIR" ]]; then
  printf '%s\n' "Missing skill destination." >&2
  printf '%s\n' "Pass --host codex|cursor|claude-code with --scope repo|user, or pass --dest PATH / BELONG_SKILLS_DEST for Other AI Hosts." >&2
  printf '%s\n' "Other AI hosts are welcome, but their documented skills/custom-instructions directory must be explicit." >&2
  printf '%s\n' "No Codex, Claude Code, or other behavior-changing directory is selected implicitly." >&2
  exit 2
fi

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

printf 'Installing/updating Belong skills into %s\n' "$DEST_DIR"

if [[ "$DRY_RUN" != "1" ]]; then
  mkdir -p "$DEST_DIR"
fi

installed=0
updated=0
skipped=0
backed_up=0
backup_root="$DEST_DIR/.belong-skill-backups/$(date -u '+%Y%m%dT%H%M%SZ')"

for skill_path in "${SKILL_PATHS[@]}"; do
  src="$ROOT_DIR/$skill_path"
  name="$(basename "$skill_path")"
  dest="$DEST_DIR/$name"

  if [[ -e "$dest" && "$UPDATE_EXISTING" != "1" ]]; then
    printf 'skip    %s already exists\n' "$name"
    skipped=$((skipped + 1))
    continue
  fi

  if [[ "$DRY_RUN" == "1" ]]; then
    if [[ -e "$dest" ]]; then
      printf 'update  %s -> %s\n' "$skill_path" "$dest"
      updated=$((updated + 1))
    else
      printf 'install %s -> %s\n' "$skill_path" "$dest"
      installed=$((installed + 1))
    fi
    continue
  fi

  if [[ -e "$dest" ]]; then
    if [[ "$BACKUP_EXISTING" == "1" ]]; then
      mkdir -p "$backup_root"
      cp -R "$dest" "$backup_root/$name"
      backed_up=$((backed_up + 1))
    fi
    rm -rf "$dest"
    mkdir -p "$dest"
    cp -R "$src"/. "$dest"/
    printf 'update  %s\n' "$name"
    updated=$((updated + 1))
  else
    mkdir -p "$dest"
    cp -R "$src"/. "$dest"/
    printf 'install %s\n' "$name"
    installed=$((installed + 1))
  fi
done

printf '\nInstalled: %s, updated: %s, skipped: %s\n' "$installed" "$updated" "$skipped"
if [[ "$DRY_RUN" != "1" && "$backed_up" -gt 0 ]]; then
  printf 'Backed up replaced skills to %s\n' "$backup_root"
fi
printf 'Restart the host agent application if needed, then invoke the guide skill: Codex/Cursor use $belong-marketplace-guide; Claude Code uses /belong-marketplace-guide; Other AI Hosts open or invoke belong-marketplace-guide through their own skill mechanism\n'
