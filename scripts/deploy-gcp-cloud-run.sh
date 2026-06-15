#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
PROJECT_ID="${PROJECT_ID:-belong-aaas-v1}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-belong-a2a-landing}"
ACCOUNT="${GCLOUD_ACCOUNT:-}"

GCLOUD_ARGS=(--project "$PROJECT_ID")
if [[ -n "$ACCOUNT" ]]; then
  GCLOUD_ARGS+=(--account "$ACCOUNT")
fi

printf 'Deploying %s to Cloud Run project=%s region=%s\n' "$SERVICE_NAME" "$PROJECT_ID" "$REGION"

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  "${GCLOUD_ARGS[@]}" \
  --quiet

gcloud run deploy "$SERVICE_NAME" \
  --source "$ROOT_DIR" \
  --region "$REGION" \
  --no-invoker-iam-check \
  "${GCLOUD_ARGS[@]}" \
  --quiet

url="$(gcloud run services describe "$SERVICE_NAME" \
  --region "$REGION" \
  "${GCLOUD_ARGS[@]}" \
  --format='value(status.url)')"

printf 'Deployed: %s\n' "$url"
