#!/usr/bin/env python3
"""Stateful mocked backend for the Belong Agent-to-Agent Marketplace Skill Pack."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_VERSION = "2026-06-08.5"
DEFAULT_PLATFORM_FEE_RATE = 0.08
STOPWORDS = {
    "and",
    "are",
    "can",
    "for",
    "from",
    "has",
    "have",
    "need",
    "needs",
    "the",
    "this",
    "that",
    "with",
    "within",
    "will",
    "what",
    "when",
    "where",
    "why",
    "how",
    "our",
    "your",
    "their",
    "service",
    "services",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def split_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r"[,;\n]", value) if item.strip()]


def terms(value: str | list[str] | None) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return {term for term in re.findall(r"[a-z0-9]+", value.lower()) if len(term) > 2 and term not in STOPWORDS}


def parse_percent(value: str | int | float | None) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group(0)) if match else 0.0


def canonical_payment_type(value: str | None) -> str:
    aliases = {
        "authorize": "authorization",
        "auth": "authorization",
    }
    normalized = (value or "charge").strip().lower().replace("-", "_")
    return aliases.get(normalized, normalized)


def slug(value: str) -> str:
    clean = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return clean or "item"


def default_state() -> dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "created_at": now(),
        "updated_at": now(),
        "counters": {},
        "accounts": {},
        "organizations": {},
        "agents": {},
        "services": {},
        "buying_requests": {},
        "engagement_feeds": {},
        "discovery_questionnaires": {},
        "proposals": {},
        "contracts": {},
        "active_services": {},
        "inbox": {},
        "payments": {},
        "disputes": {},
        "reputation_events": {},
        "audit": {},
        "training_recommendations": {},
        "steering_instructions": {},
        "notifications": {},
        "notification_events": {},
        "marketplace_signals": {
            "privacy_promise": "Private by default; private Playbooks, contracts, messages, evidence, and organization data are shared only through explicit marketplace actions.",
            "learning_boundary": "Aggregated/anonymized outcomes, reputation, pricing benchmarks, search/conversion patterns, and dispute statistics can improve marketplace ranking and recommendations.",
            "belong_monetization": {
                "model": "seller_side_transaction_fee",
                "platform_fee_rate": DEFAULT_PLATFORM_FEE_RATE,
            },
        },
    }


def find_workspace_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists() or (candidate / "WORKFLOW.md").exists():
            return candidate
    return current


def state_path(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    env_path = os.environ.get("BELONG_MOCK_STATE")
    if env_path:
        return Path(env_path).expanduser().resolve()
    root = find_workspace_root(Path.cwd())
    return root / ".belong" / "mock-marketplace" / "state.json"


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_state()
    with path.open("r", encoding="utf-8") as handle:
        state = json.load(handle)
    base = default_state()
    for key, value in base.items():
        state.setdefault(key, value)
    if "playbook_updates" in state:
        state.setdefault("training_recommendations", {})
        for update_id, update in state.pop("playbook_updates", {}).items():
            recommendation_id = update_id.replace("playbook_update", "training_rec")
            state["training_recommendations"].setdefault(
                recommendation_id,
                {
                    **update,
                    "id": recommendation_id,
                    "status": "pending_training_review"
                    if update.get("status") == "pending_human_approval"
                    else update.get("status", "pending_training_review"),
                    "migrated_from": update_id,
                },
            )
    return state


def save_state(path: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = now()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
    tmp.replace(path)


def next_id(state: dict[str, Any], prefix: str) -> str:
    state["counters"][prefix] = state["counters"].get(prefix, 0) + 1
    return f"{prefix}_{state['counters'][prefix]:04d}"


def find_by_name(collection: dict[str, dict[str, Any]], name: str) -> str | None:
    normalized = name.strip().lower()
    for object_id, item in collection.items():
        if str(item.get("name", "")).strip().lower() == normalized:
            return object_id
    return None


def find_service_for_org(state: dict[str, Any], org_id: str, service_name: str) -> str | None:
    normalized = service_name.strip().lower()
    for service_id, service in state["services"].items():
        if service.get("provider_organization_id") == org_id and service.get("name", "").strip().lower() == normalized:
            return service_id
    return None


def ensure_agent_can_act(agent: dict[str, Any], action: str) -> None:
    if agent.get("paused"):
        raise ValueError(
            f"{agent['id']} is paused. It cannot initiate {action}; urgent obligations, deadlines, notices, and disputes remain visible through the Marketplace Inbox."
        )
    if agent.get("status") != "production":
        raise ValueError(f"{agent['id']} is not in Production. Complete validation before {action}.")


def ensure_flow_agent_can_act(flow: dict[str, Any], action: str) -> None:
    ensure_flow_actor_can_act(flow, False, action)


def ensure_flow_actor_can_act(flow: dict[str, Any], as_human: bool, action: str) -> None:
    control_state = flow.get("control_state", "agent_controlled")
    if control_state == "paused":
        raise ValueError(
            f"Flow {flow.get('id')} is paused. No actor can {action} until it is resumed; obligations, deadlines, notices, and disputes remain visible through the Marketplace Inbox."
        )
    if control_state == "human_controlled" and not as_human:
        raise ValueError(
            f"Flow {flow.get('id')} is under human control. The Belong agent cannot {action}; the human drives this flow directly through the act-directly skills. Release control to return the flow to the agent."
        )
    if control_state == "agent_controlled" and as_human:
        raise ValueError(
            f"Flow {flow.get('id')} is agent-controlled. Take control first with flow-control --action take before the human can {action}."
        )


# Scenario B: standing Playbook rule reserving high-criticality action types for the human.
# These are the only action types a Playbook may mark as human-performed; operational actions
# (negotiate, discovery, meeting, message, fulfillment-task) are not eligible.
ELIGIBLE_HUMAN_CONTROLLED_ACTIONS = {
    "buyer": {"sign", "accept", "payment", "change-order", "dispute"},
    "seller": {"sign", "deliver", "accept-change-order", "payment", "dispute"},
}


def validate_human_controlled_actions(tokens: list[str], role: str) -> list[str]:
    eligible = ELIGIBLE_HUMAN_CONTROLLED_ACTIONS[role]
    invalid = [token for token in tokens if token not in eligible]
    if invalid:
        raise ValueError(
            f"Ineligible human-controlled action(s) for {role}: {', '.join(invalid)}. "
            f"Eligible {role} action types: {', '.join(sorted(eligible))}. "
            "Operational actions (negotiate, discovery, meeting, message, fulfillment-task) cannot be reserved for the human."
        )
    return tokens


def playbook_human_actions(playbook: dict[str, Any]) -> set[str]:
    return set(playbook.get("standing_authorization", {}).get("human_controlled_actions", []))


def active_action_human_token(action: str, role: str) -> str | None:
    if action == "deliver" and role == "seller":
        return "deliver"
    if action == "accept" and role == "buyer":
        return "accept"
    if action == "payment":
        return "payment"
    if action == "change-order":
        return "change-order" if role == "buyer" else "accept-change-order"
    if action == "dispute":
        return "dispute"
    return None


def route_action_to_human(
    state: dict[str, Any],
    role: str,
    action_token: str,
    link_type: str,
    link_id: str,
    playbook_version: Any,
) -> dict[str, Any]:
    skill = "belong-operate-buying-flow" if role == "buyer" else "belong-operate-selling-flow"
    summary = (
        f"The {role}'s Playbook reserves '{action_token}' as a human-performed action (Scenario B). "
        "The agent will not execute it and is not asking for approval; the human performs it directly."
    )
    inbox = add_inbox(
        state,
        role,
        "human_performed_action",
        f"Perform {action_token} yourself",
        summary,
        link_type,
        link_id,
        urgency="high",
        metadata={"reserved_action": action_token, "role": role},
    )
    audit(
        state,
        "Belong Agent",
        "authority.routed_to_human",
        link_type,
        link_id,
        summary,
        {"reserved_action": action_token, "role": role, "playbook_version": playbook_version},
    )
    return output(
        f"{action_token} was routed to the {role}-side human because the Playbook reserves it as a human-performed action.",
        {"inbox_item": inbox},
        [
            f"Use {skill} to take control of the flow and perform {action_token} with --as-human.",
            "This is a standing Playbook rule (Scenario B), not an approval request; the human performs the action, not the agent.",
        ],
    )


def audit(
    state: dict[str, Any],
    actor: str,
    event_type: str,
    object_type: str,
    object_id: str,
    summary: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event_id = next_id(state, "audit")
    event = {
        "id": event_id,
        "timestamp": now(),
        "actor": actor,
        "event_type": event_type,
        "object_type": object_type,
        "object_id": object_id,
        "summary": summary,
        "details": details or {},
    }
    state["audit"][event_id] = event
    return event


def add_inbox(
    state: dict[str, Any],
    owner_role: str,
    request_type: str,
    title: str,
    summary: str,
    linked_object_type: str,
    linked_object_id: str,
    urgency: str = "normal",
    assigned_to: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    for existing in state["inbox"].values():
        if (
            existing.get("status") == "pending"
            and existing.get("owner_role") == owner_role
            and existing.get("request_type") == request_type
            and existing.get("title") == title
            and existing.get("linked_object_type") == linked_object_type
            and existing.get("linked_object_id") == linked_object_id
        ):
            existing["summary"] = summary
            existing["updated_at"] = now()
            existing["urgency"] = urgency
            existing["assigned_to"] = assigned_to
            existing["metadata"] = {**existing.get("metadata", {}), **(metadata or {})}
            return existing
    item_id = next_id(state, "inbox")
    item = {
        "id": item_id,
        "status": "pending",
        "created_at": now(),
        "updated_at": now(),
        "owner_role": owner_role,
        "request_type": request_type,
        "title": title,
        "summary": summary,
        "linked_object_type": linked_object_type,
        "linked_object_id": linked_object_id,
        "urgency": urgency,
        "assigned_to": assigned_to,
        "metadata": metadata or {},
    }
    state["inbox"][item_id] = item
    record_notification_events(state, item)
    audit(state, "belong_marketplace", "inbox.created", "Marketplace Inbox", item_id, title, item)
    return item


def add_reputation_event(
    state: dict[str, Any],
    agent_id: str,
    delta: float,
    reason: str,
    linked_object_type: str,
    linked_object_id: str,
) -> dict[str, Any]:
    event_id = next_id(state, "rep_event")
    agent = state["agents"].get(agent_id)
    if not agent:
        raise ValueError(f"Unknown agent: {agent_id}")
    reputation = agent.setdefault("reputation", {"score": 100.0, "events": []})
    reputation["score"] = max(0, min(100, round(float(reputation.get("score", 100)) + delta, 2)))
    reputation["events"].append(event_id)
    event = {
        "id": event_id,
        "timestamp": now(),
        "agent_id": agent_id,
        "delta": delta,
        "score_after": reputation["score"],
        "reason": reason,
        "linked_object_type": linked_object_type,
        "linked_object_id": linked_object_id,
    }
    state["reputation_events"][event_id] = event
    audit(state, "belong_marketplace", "reputation.changed", "Belong Agent", agent_id, reason, event)
    return event


def resolve_matching_inbox(
    state: dict[str, Any],
    linked_object_type: str,
    linked_object_id: str,
    title: str | None,
    actor: str,
    notes: str,
) -> None:
    for item in state["inbox"].values():
        if item["status"] != "pending":
            continue
        if item["linked_object_type"] != linked_object_type or item["linked_object_id"] != linked_object_id:
            continue
        if title and item["title"] != title:
            continue
        item["status"] = "resolved"
        item["updated_at"] = now()
        item["resolution"] = {"decision": "completed", "notes": notes, "actor": actor, "timestamp": now()}
        audit(state, actor, "inbox.auto_resolved", "Marketplace Inbox", item["id"], notes, item)


def resolve_inbox_by_request_type(
    state: dict[str, Any],
    linked_object_type: str,
    linked_object_id: str,
    request_type: str,
    actor: str,
    notes: str,
) -> None:
    for item in state["inbox"].values():
        if item["status"] != "pending":
            continue
        if item["linked_object_type"] != linked_object_type or item["linked_object_id"] != linked_object_id:
            continue
        if item["request_type"] != request_type:
            continue
        item["status"] = "resolved"
        item["updated_at"] = now()
        item["resolution"] = {"decision": "completed", "notes": notes, "actor": actor, "timestamp": now()}
        audit(state, actor, "inbox.auto_resolved", "Marketplace Inbox", item["id"], notes, item)


def output(summary: str, objects: dict[str, Any] | None = None, next_steps: list[str] | None = None) -> dict[str, Any]:
    return {
        "summary": summary,
        "objects": objects or {},
        "next_steps": next_steps or [],
    }


def account_matches_owner_role(account: dict[str, Any], owner_role: str) -> bool:
    if owner_role in {"all", "both"}:
        return True
    return owner_role in set(account.get("roles", []))


def record_notification_events(state: dict[str, Any], inbox_item: dict[str, Any]) -> None:
    owner_role = inbox_item.get("owner_role", "all")
    for account in state["accounts"].values():
        if not account_matches_owner_role(account, owner_role):
            continue
        for channel in account.get("notifications", []) or ["email"]:
            event_id = next_id(state, "notification_event")
            state["notification_events"][event_id] = {
                "id": event_id,
                "account_id": account["id"],
                "owner_role": owner_role,
                "channel": channel,
                "status": "mocked_sent",
                "inbox_item_id": inbox_item["id"],
                "message": f"Go to your favorite agentic application and open your Belong Marketplace Inbox: {inbox_item['title']}",
                "created_at": now(),
            }


def ensure_org(state: dict[str, Any], name: str, kind: str = "company") -> str:
    existing = find_by_name(state["organizations"], name)
    if existing:
        return existing
    org_id = next_id(state, "org")
    state["organizations"][org_id] = {
        "id": org_id,
        "name": name,
        "kind": kind,
        "roles": ["Owner", "Admin", "Operator", "Approver"],
        "payment_setup": "mocked_ready",
        "legal_setup": "mocked_ready",
        "created_at": now(),
    }
    audit(state, "belong_account", "organization.created", "Organization Profile", org_id, f"Created Organization Profile {name}")
    return org_id


def ensure_account(state: dict[str, Any], human_name: str, role: str, org_id: str, notifications: list[str]) -> str:
    existing = find_by_name(state["accounts"], human_name)
    if existing:
        account = state["accounts"][existing]
        account.setdefault("roles", [])
        if role not in account["roles"]:
            account["roles"].append(role)
        if org_id not in account.setdefault("organizations", []):
            account["organizations"].append(org_id)
        account["notifications"] = sorted(set(account.get("notifications", []) + notifications))
        return existing
    account_id = next_id(state, "acct")
    state["accounts"][account_id] = {
        "id": account_id,
        "name": human_name,
        "roles": [role],
        "organizations": [org_id],
        "oauth_login": {
            "status": "mocked_authenticated",
            "provider": "Belong OAuth mock",
            "authenticated_at": now(),
        },
        "notifications": notifications,
        "created_at": now(),
    }
    audit(state, human_name, "account.oauth_login.mocked", "Belong Account", account_id, f"Mock OAuth completed for {human_name}")
    for channel in notifications:
        notification_id = next_id(state, "notification")
        state["notifications"][notification_id] = {
            "id": notification_id,
            "account_id": account_id,
            "channel": channel,
            "status": "mocked_ready",
            "message_pattern": "Go to your favorite agentic application and open your Belong Marketplace Inbox.",
        }
    return account_id


def require_account(state: dict[str, Any], human_name: str, role: str, org_id: str, notifications: list[str]) -> str:
    existing = find_by_name(state["accounts"], human_name)
    if not existing:
        raise ValueError(
            f"No Belong account found for '{human_name}'. Run belong-setup-account first to create the account, "
            "then return to training. Training cannot create an account."
        )
    account = state["accounts"][existing]
    account.setdefault("roles", [])
    if role not in account["roles"]:
        account["roles"].append(role)
    if org_id not in account.setdefault("organizations", []):
        account["organizations"].append(org_id)
    account["notifications"] = sorted(set(account.get("notifications", []) + notifications))
    return existing


INVITE_ROLES = {"owner", "admin", "developer", "finance", "support", "buyer", "approver"}


def parse_invites(raw_invites: list[str] | None) -> list[dict[str, str]]:
    members: list[dict[str, str]] = []
    seen_emails: set[str] = set()
    for raw in raw_invites or []:
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) != 3 or not all(parts):
            raise ValueError(f"Invalid --invite '{raw}'. Use 'Name|email|role'.")
        name, email, role = parts
        role = role.lower()
        if role not in INVITE_ROLES:
            raise ValueError(
                f"Invalid invite role '{role}'. Choose one of: {', '.join(sorted(INVITE_ROLES))}."
            )
        if email.lower() in seen_emails:
            continue
        seen_emails.add(email.lower())
        members.append({"name": name, "email": email, "role": role, "status": "invited", "invited_at": now()})
    return members


def command_setup_account(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    notifications = split_list(args.notifications) or ["email"]
    org_id = ensure_org(state, args.org_name, args.org_kind)
    account_id = ensure_account(state, args.human_name, args.role, org_id, notifications)
    invited = parse_invites(getattr(args, "invite", None))
    if invited:
        account = state["accounts"][account_id]
        account.setdefault("invited_members", []).extend(invited)
        for m in invited:
            audit(
                state,
                args.human_name,
                "account.member.invited",
                "Belong Account",
                account_id,
                f"Invitation email sent to {m['name']} <{m['email']}> as {m['role']}.",
                {"invited_member": m},
            )
    add_inbox(
        state,
        "both" if args.role == "both" else args.role,
        "instruction_execution",
        "Finish agent training",
        "OAuth, organization, payment, legal, and notifications are mocked as ready. Train a Buying Agent, Selling Agent, or both next.",
        "Belong Account",
        account_id,
    )
    return output(
        f"Mock OAuth and account setup are ready for {args.human_name}."
        + (f" Invitation emails sent to {len(invited)} teammate(s)." if invited else ""),
        {
            "account": state["accounts"][account_id],
            "organization": state["organizations"][org_id],
            "invited_members": invited,
        },
        [
            "Train a Buying Agent with belong-train-buying-agent if this human buys services.",
            "Train a Selling Agent with belong-train-selling-agent if this human provides a Service.",
            "Open the Marketplace Inbox with belong-inbox to see pending guided work.",
        ],
    )


def expand_account_roles(roles: list[str]) -> set[str]:
    caps: set[str] = set()
    for role in roles:
        if role == "both":
            caps.update({"buyer", "seller"})
        elif role in {"buyer", "seller"}:
            caps.add(role)
    return caps


def collapse_account_roles(caps: set[str]) -> list[str]:
    if {"buyer", "seller"}.issubset(caps):
        return ["both"]
    return sorted(caps)


def command_update_account(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    account_id = args.account_id
    if not account_id and args.human_name:
        account_id = find_by_name(state["accounts"], args.human_name)
    if not account_id or account_id not in state["accounts"]:
        raise ValueError(
            "No matching Belong Account. Provide an existing --account-id or --human-name, or run belong-setup-account first."
        )
    account = state["accounts"][account_id]

    if args.set_notifications is None and not args.rename_org and not args.remove_role:
        raise ValueError(
            "Nothing to update. Provide --set-notifications, --rename-org, or --remove-role."
        )

    changes: list[str] = []

    if args.set_notifications is not None:
        channels = sorted(set(split_list(args.set_notifications)))
        if not channels:
            raise ValueError(
                "An account cannot be left without a notification channel. Provide at least one channel to --set-notifications."
            )
        previous = list(account.get("notifications", []))
        for notification_id in [
            nid for nid, item in state["notifications"].items() if item.get("account_id") == account_id
        ]:
            del state["notifications"][notification_id]
        account["notifications"] = channels
        for channel in channels:
            notification_id = next_id(state, "notification")
            state["notifications"][notification_id] = {
                "id": notification_id,
                "account_id": account_id,
                "channel": channel,
                "status": "mocked_ready",
                "message_pattern": "Go to your favorite agentic application and open your Belong Marketplace Inbox.",
            }
        audit(
            state,
            account["name"],
            "account.notifications.updated",
            "Belong Account",
            account_id,
            f"Notification channels changed from {previous or ['email']} to {channels}.",
            {"previous": previous, "current": channels},
        )
        changes.append(f"notification channels set to {', '.join(channels)}")

    if args.rename_org:
        new_name = args.rename_org.strip()
        if not new_name:
            raise ValueError("Provide a non-empty organization name for --rename-org.")
        org_ids = account.get("organizations", [])
        org_id = args.org_id
        if not org_id:
            if len(org_ids) == 1:
                org_id = org_ids[0]
            else:
                raise ValueError(
                    f"This account has multiple organizations ({', '.join(org_ids)}). Specify which one with --org-id."
                )
        if org_id not in org_ids or org_id not in state["organizations"]:
            raise ValueError(f"Organization {org_id} is not linked to this account.")
        collision = find_by_name(state["organizations"], new_name)
        if collision and collision != org_id:
            raise ValueError(
                f"Another organization ({collision}) already uses the name '{new_name}'. Choose a different name."
            )
        previous_name = state["organizations"][org_id]["name"]
        state["organizations"][org_id]["name"] = new_name
        audit(
            state,
            account["name"],
            "organization.renamed",
            "Organization",
            org_id,
            f"Organization renamed from '{previous_name}' to '{new_name}'.",
            {"previous": previous_name, "current": new_name},
        )
        changes.append(f"organization {org_id} renamed to {new_name}")

    if args.remove_role:
        role = args.remove_role
        caps = expand_account_roles(account.get("roles", []))
        if role not in caps:
            raise ValueError(f"This account does not hold the {role} role; nothing to remove.")
        if role == "seller":
            backing = [
                aid
                for aid, agent in state["agents"].items()
                if agent.get("type") == "Selling Agent" and agent.get("account_id") == account_id
            ]
        else:
            backing = [
                aid
                for aid, agent in state["agents"].items()
                if agent.get("type") == "Buying Agent" and agent.get("account_id") == account_id
            ]
        if backing:
            raise ValueError(
                f"Cannot remove the {role} role while agents still back it: {', '.join(backing)}. "
                "Retire those agents before removing the role."
            )
        caps.discard(role)
        account["roles"] = collapse_account_roles(caps)
        audit(
            state,
            account["name"],
            "account.role.removed",
            "Belong Account",
            account_id,
            f"Removed {role} role; remaining roles {account['roles']}.",
            {"removed": role, "current": account["roles"]},
        )
        changes.append(f"{role} role removed")

    return output(
        f"Updated Belong Account for {account['name']}: {'; '.join(changes)}.",
        {
            "account": account,
            "organizations": {
                oid: state["organizations"][oid]
                for oid in account.get("organizations", [])
                if oid in state["organizations"]
            },
        },
        [
            "Open the Marketplace Inbox with belong-inbox to see pending guided work.",
            "Re-run belong-setup-account to add a role, organization, or notification channel.",
        ],
    )


def service_price(args: argparse.Namespace) -> dict[str, Any]:
    amount = float(args.starting_price or 5000)
    return {
        "pricing_model": args.pricing_model,
        "starting_price": amount,
        "currency": args.currency,
        "billing_cycle": args.billing_cycle,
        "collections": args.collections,
        "platform_fee_rate": DEFAULT_PLATFORM_FEE_RATE,
        "seller_receives_after_platform_fee": round(amount * (1 - DEFAULT_PLATFORM_FEE_RATE), 2),
    }


def has_meaningful_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(has_meaningful_value(item) for item in value)
    if isinstance(value, dict):
        return any(has_meaningful_value(item) for item in value.values())
    return True


def validation_status(required: list[str], values: dict[str, Any]) -> dict[str, Any]:
    missing = []
    for key in required:
        value = values.get(key)
        if not has_meaningful_value(value):
            missing.append(key)
    return {
        "status": "production" if not missing else "validation",
        "missing": missing,
    }


def command_train_selling(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    org_id = ensure_org(state, args.org_name, "company")
    account_id = require_account(state, args.human_name, "seller", org_id, split_list(args.notifications) or ["email"])
    playbook = {
        "service_description": args.description,
        "buyer_personas": split_list(args.buyer_personas),
        "use_cases": split_list(args.use_cases),
        "discovery_questions": split_list(args.discovery_questions)
        or [
            "What outcome do you need?",
            "What timeline, budget, and constraints should we respect?",
            "What acceptance evidence will prove the Service worked?",
        ],
        "pricing": service_price(args),
        "contract_terms": args.contract_terms,
        "negotiation_limits": {
            "discount_limit": args.discount_limit,
            "scope_limits": args.scope_limits,
            "commercial_notes": args.negotiation_limits,
        },
        "delivery_workflow": args.delivery_workflow,
        "deliverables": split_list(args.deliverables),
        "evidence_requirements": split_list(args.evidence_requirements),
        "billing_collections": {
            "billing_cycle": args.billing_cycle,
            "collections": args.collections,
        },
        "escalation_paths": split_list(args.escalation_paths),
        "meeting_rules": args.meeting_rules,
        "dispute_rules": args.dispute_rules,
        "reputation_rules": args.reputation_rules,
        "standing_authorization": {
            "discount_limit": args.discount_limit,
            "scope_limits": args.scope_limits,
            "contract_terms": args.contract_terms,
            "must_escalate": split_list(args.escalation_paths),
            "human_controlled_actions": validate_human_controlled_actions(
                split_list(getattr(args, "human_controlled_actions", "")), "seller"
            ),
        },
        "privacy_boundary": state["marketplace_signals"]["privacy_promise"],
    }
    required = [
        "service_description",
        "buyer_personas",
        "use_cases",
        "discovery_questions",
        "pricing",
        "contract_terms",
        "negotiation_limits",
        "delivery_workflow",
        "deliverables",
        "evidence_requirements",
        "billing_collections",
        "escalation_paths",
        "meeting_rules",
        "dispute_rules",
        "reputation_rules",
        "standing_authorization",
    ]
    validation = validation_status(required, playbook)
    status = "production" if args.activate and validation["status"] == "production" else validation["status"]
    existing_service_id = find_service_for_org(state, org_id, args.service_name)
    service_id = existing_service_id or next_id(state, "svc")
    existing_agent_id = state["services"].get(service_id, {}).get("selling_agent_id") if existing_service_id else None
    agent_id = existing_agent_id or next_id(state, "sell_agent")
    previous_agent = state["agents"].get(agent_id, {})
    paused = bool(previous_agent.get("paused", False))
    stored_status = "paused" if paused else status
    phase = previous_agent.get("phase") if paused else ("Production" if status == "production" else "Validation")
    state["agents"][agent_id] = {
        "id": agent_id,
        "type": "Selling Agent",
        "name": f"{args.service_name} Selling Agent",
        "status": stored_status,
        "phase": phase,
        "account_id": account_id,
        "organization_id": org_id,
        "service_id": service_id,
        "playbook_version": previous_agent.get("playbook_version", 0) + 1,
        "playbook": playbook,
        "paused": paused,
        "reputation": previous_agent.get("reputation", {"score": 95.0, "events": []}),
        "created_at": previous_agent.get("created_at", now()),
    }
    state["services"][service_id] = {
        "id": service_id,
        "name": args.service_name,
        "provider_organization_id": org_id,
        "selling_agent_id": agent_id,
        "description": args.description,
        "tags": split_list(args.tags),
        "availability": args.availability,
        "price_signal": playbook["pricing"],
        "supported_contract_terms": args.contract_terms,
        "status": "paused" if stored_status == "paused" else ("listed" if stored_status == "production" else "draft"),
        "created_at": state["services"].get(service_id, {}).get("created_at", now()),
    }
    audit(state, args.human_name, "selling_agent.trained", "Selling Agent", agent_id, f"Trained Selling Agent for {args.service_name}", {"validation": validation})
    resolve_matching_inbox(
        state,
        "Belong Account",
        account_id,
        "Finish agent training",
        args.human_name,
        "Selling Agent training completed for this account.",
    )
    if validation["missing"]:
        add_inbox(
            state,
            "seller",
            "information",
            "Complete Selling Agent Playbook",
            f"Missing: {', '.join(validation['missing'])}",
            "Selling Agent",
            agent_id,
            assigned_to=account_id,
        )
    else:
        resolve_matching_inbox(
            state,
            "Selling Agent",
            agent_id,
            "Complete Selling Agent Playbook",
            args.human_name,
            "Selling Agent validation is complete.",
        )
        if stored_status == "production":
            add_inbox(
                state,
                "seller",
                "instruction_execution",
                "Selling Agent ready for marketplace",
                "Review the Service listing and run a mocked discovery or proposal flow when a Buying Agent engages.",
                "Service",
                service_id,
                assigned_to=account_id,
            )
        else:
            resolve_matching_inbox(
                state,
                "Service",
                service_id,
                "Selling Agent ready for marketplace",
                args.human_name,
                "Selling Agent is trained but remains paused until the Service Provider human resumes it.",
            )
    return output(
        f"Created {stored_status} Selling Agent for Service {args.service_name}.",
        {
            "agent": state["agents"][agent_id],
            "service": state["services"][service_id],
            "validation": validation,
        },
        [
            "Use belong-check-active-services to inspect active seller obligations after buyer signature.",
            "Use belong-check-payments to inspect billing, collections, and transaction ledger state.",
            "Use belong-inbox to resolve any pending information or validation items.",
        ],
    )


def command_train_buying(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    org_id = ensure_org(state, args.org_name, args.org_kind)
    account_id = require_account(state, args.human_name, "buyer", org_id, split_list(args.notifications) or ["email"])
    playbook = {
        "buying_goals": split_list(args.goals),
        "needed_services": split_list(args.needed_services),
        "provider_preferences": split_list(args.provider_preferences),
        "blocked_providers": split_list(args.blocked_providers),
        "budget": float(args.budget or 10000),
        "timeline": args.timeline,
        "selection_rules": args.selection_rules,
        "rfp_rules": args.rfp_rules,
        "negotiation_limits": args.negotiation_limits,
        "proposal_comparison_rules": args.proposal_comparison_rules,
        "contract_authority": args.contract_authority,
        "payment_rules": args.payment_rules,
        "acceptance_criteria": split_list(args.acceptance_criteria),
        "escalation_rules": args.escalation_rules,
        "dispute_posture": args.dispute_posture,
        "rating_rules": args.rating_rules,
        "optimization_goals": args.optimization_goals,
        "standing_authorization": {
            "max_spend": float(args.max_spend or args.budget or 10000),
            "provider_requirements": split_list(args.provider_preferences),
            "contract_authority": args.contract_authority,
            "payment_rules": args.payment_rules,
            "must_escalate": args.escalation_rules,
            "human_controlled_actions": validate_human_controlled_actions(
                split_list(getattr(args, "human_controlled_actions", "")), "buyer"
            ),
        },
        "privacy_boundary": state["marketplace_signals"]["privacy_promise"],
    }
    required = [
        "buying_goals",
        "budget",
        "timeline",
        "selection_rules",
        "rfp_rules",
        "proposal_comparison_rules",
        "contract_authority",
        "payment_rules",
        "acceptance_criteria",
        "escalation_rules",
        "dispute_posture",
        "rating_rules",
        "optimization_goals",
    ]
    validation = validation_status(required, playbook)
    status = "production" if args.activate and validation["status"] == "production" else validation["status"]
    existing_agent = None
    for agent_id, agent in state["agents"].items():
        if agent.get("type") == "Buying Agent" and agent.get("account_id") == account_id:
            existing_agent = agent_id
            break
    agent_id = existing_agent or next_id(state, "buy_agent")
    previous_agent = state["agents"].get(agent_id, {})
    paused = bool(previous_agent.get("paused", False))
    stored_status = "paused" if paused else status
    phase = previous_agent.get("phase") if paused else ("Production" if status == "production" else "Validation")
    state["agents"][agent_id] = {
        "id": agent_id,
        "type": "Buying Agent",
        "name": f"{args.human_name} Buying Agent",
        "status": stored_status,
        "phase": phase,
        "account_id": account_id,
        "organization_id": org_id,
        "playbook_version": previous_agent.get("playbook_version", 0) + 1,
        "playbook": playbook,
        "paused": paused,
        "reputation": previous_agent.get("reputation", {"score": 95.0, "events": []}),
        "created_at": previous_agent.get("created_at", now()),
    }
    audit(state, args.human_name, "buying_agent.trained", "Buying Agent", agent_id, "Trained Buying Agent", {"validation": validation})
    resolve_matching_inbox(
        state,
        "Belong Account",
        account_id,
        "Finish agent training",
        args.human_name,
        "Buying Agent training completed for this account.",
    )
    if validation["missing"]:
        add_inbox(
            state,
            "buyer",
            "information",
            "Complete Buying Agent Playbook",
            f"Missing: {', '.join(validation['missing'])}",
            "Buying Agent",
            agent_id,
            assigned_to=account_id,
        )
    else:
        resolve_matching_inbox(
            state,
            "Buying Agent",
            agent_id,
            "Complete Buying Agent Playbook",
            args.human_name,
            "Buying Agent validation is complete.",
        )
        add_inbox(
            state,
            "buyer",
            "instruction_execution",
            "Buying Agent ready for first Buying Request",
            "Start a mocked Buying Request and choose direct engagement or a competitive feed.",
            "Buying Agent",
            agent_id,
            assigned_to=account_id,
        )
    return output(
        f"Created {stored_status} Buying Agent for {args.human_name}.",
        {"agent": state["agents"][agent_id], "validation": validation},
        [
            "The Buying Agent can now execute Buying Requests through internal agent capabilities.",
            "Use belong-inbox to resolve validation or authorization requests.",
            "Use belong-check-reputation to inspect authority, audit, and decision explanations.",
        ],
    )


def seed_marketplace_catalog(state: dict[str, Any]) -> None:
    catalog = [
        {
            "provider": "Northstar RevOps",
            "service": "RevOps Pipeline Rescue",
            "description": "Diagnose funnel leakage, rebuild CRM stages, and deliver a revenue operations playbook.",
            "tags": ["revops", "crm", "pipeline", "sales"],
            "price": 12000,
            "deliverables": ["CRM audit", "pipeline dashboard", "handoff workshop"],
        },
        {
            "provider": "Brightline Support",
            "service": "AI Support Desk Launch",
            "description": "Stand up a customer support operation with agent triage, macros, QA, and escalation design.",
            "tags": ["support", "customer-success", "ai-ops", "zendesk"],
            "price": 8500,
            "deliverables": ["support workflow", "macro library", "QA evidence pack"],
        },
        {
            "provider": "Meridian Security",
            "service": "SOC2 Readiness Sprint",
            "description": "Prepare a startup for SOC2 readiness with control mapping, evidence collection, and gap closure.",
            "tags": ["security", "soc2", "compliance", "evidence"],
            "price": 18000,
            "deliverables": ["control matrix", "evidence binder", "readiness report"],
        },
    ]
    for item in catalog:
        if find_by_name(state["services"], item["service"]):
            continue
        org_id = ensure_org(state, item["provider"], "company")
        account_id = ensure_account(state, f"{item['provider']} Human", "seller", org_id, ["email"])
        agent_id = next_id(state, "sell_agent")
        service_id = next_id(state, "svc")
        playbook = {
            "service_description": item["description"],
            "buyer_personas": ["ops leader", "founder", "department head"],
            "use_cases": item["tags"],
            "discovery_questions": [
                "What outcome do you need and by when?",
                "What systems, constraints, and budget should we account for?",
                "What evidence will prove the work is accepted?",
            ],
            "pricing": {
                "pricing_model": "fixed_fee",
                "starting_price": item["price"],
                "currency": "USD",
                "billing_cycle": "milestone",
                "collections": "50% at signature, 50% on acceptance",
                "platform_fee_rate": DEFAULT_PLATFORM_FEE_RATE,
                "seller_receives_after_platform_fee": round(item["price"] * (1 - DEFAULT_PLATFORM_FEE_RATE), 2),
            },
            "contract_terms": "Standard Belong facilitated Service Contract/SOW with milestone payment and revision window.",
            "negotiation_limits": {"discount_limit": "10%", "scope_limits": "No regulated legal advice", "commercial_notes": "Escalate non-standard indemnity."},
            "delivery_workflow": "Kickoff, discovery, draft delivery, evidence submission, acceptance review.",
            "deliverables": item["deliverables"],
            "evidence_requirements": ["files", "links", "completion notes", "acceptance criteria mapping"],
            "billing_collections": {"billing_cycle": "milestone", "collections": "50% at signature, 50% on acceptance"},
            "escalation_paths": ["contract exceptions", "scope expansion", "human workshop scheduling"],
            "meeting_rules": "Video meetings allowed for kickoff, dispute, or complex delivery.",
            "dispute_rules": "Attempt agent negotiation first, then Belong Judge.",
            "reputation_rules": "Accepted delivery and fast response improve score; missed obligations reduce score.",
            "standing_authorization": {"discount_limit": "10%", "scope_limits": "No regulated legal advice", "contract_terms": "standard", "must_escalate": ["non-standard legal terms"]},
        }
        state["agents"][agent_id] = {
            "id": agent_id,
            "type": "Selling Agent",
            "name": f"{item['service']} Selling Agent",
            "status": "production",
            "phase": "Production",
            "account_id": account_id,
            "organization_id": org_id,
            "service_id": service_id,
            "playbook_version": 1,
            "playbook": playbook,
            "paused": False,
            "reputation": {"score": 91.0 + len(state["services"]), "events": []},
            "created_at": now(),
        }
        state["services"][service_id] = {
            "id": service_id,
            "name": item["service"],
            "provider_organization_id": org_id,
            "selling_agent_id": agent_id,
            "description": item["description"],
            "tags": item["tags"],
            "availability": "24/7 agent response; human workshops during business hours",
            "price_signal": playbook["pricing"],
            "supported_contract_terms": playbook["contract_terms"],
            "status": "listed",
            "created_at": now(),
        }
        audit(state, "belong_marketplace", "catalog.seeded", "Service", service_id, f"Seeded marketplace Service {item['service']}")


def best_buying_agent(state: dict[str, Any], explicit_id: str | None = None) -> str:
    if explicit_id:
        if explicit_id not in state["agents"]:
            raise ValueError(f"Unknown Buying Agent: {explicit_id}")
        if state["agents"][explicit_id].get("type") != "Buying Agent":
            raise ValueError(f"{explicit_id} is not a Buying Agent.")
        return explicit_id
    for agent_id, agent in state["agents"].items():
        if agent.get("type") == "Buying Agent":
            return agent_id
    raise ValueError("No Buying Agent exists. Train one with belong-train-buying-agent first, or run the full demo scenario.")


def command_buying_request(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    buyer_agent_id = best_buying_agent(state, args.buyer_agent_id)
    agent = state["agents"][buyer_agent_id]
    ensure_agent_can_act(agent, "a new Buying Request")
    request_id = next_id(state, "buy_req")
    request = {
        "id": request_id,
        "buying_agent_id": buyer_agent_id,
        "need": args.need,
        "budget": float(args.budget or agent["playbook"].get("budget", 10000)),
        "timeline": args.timeline or agent["playbook"].get("timeline"),
        "constraints": split_list(args.constraints),
        "mode": args.mode,
        "is_composite": args.composite,
        "status": "search_ready",
        "control_state": "agent_controlled",
        "created_at": now(),
        "search_results": [],
        "engagement_feeds": [],
    }
    state["buying_requests"][request_id] = request
    audit(state, agent["name"], "buying_request.created", "Buying Request", request_id, args.need, request)
    resolve_matching_inbox(
        state,
        "Buying Agent",
        buyer_agent_id,
        "Buying Agent ready for first Buying Request",
        agent["name"],
        "Buying Request has been created.",
    )
    return output(
        f"Created Buying Request {request_id}: {args.need}",
        {"buying_request": request},
        [
            "Search semantically for Services.",
            "Open an Engagement Feed with one Selling Agent or a competitive set.",
            "Escalate to the buyer-side human if budget, provider, or contract limits are unclear.",
        ],
    )


def command_start_buying_request(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    buyer_agent_id = best_buying_agent(state, args.buyer_agent_id)
    request_result = command_buying_request(
        argparse.Namespace(
            buyer_agent_id=buyer_agent_id,
            need=args.need,
            budget=args.budget,
            timeline=args.timeline,
            constraints=args.constraints,
            mode=args.mode,
            composite=args.composite,
        ),
        state,
    )
    request = request_result["objects"]["buying_request"]
    search_result = command_search(
        argparse.Namespace(
            request_id=request["id"],
            query=args.search_query or args.need,
            tags=args.tags,
            limit=args.limit,
        ),
        state,
    )
    objects: dict[str, Any] = {
        "buying_request": request,
        "search_results": search_result["objects"]["search_results"],
    }
    if int(args.auto_engage_count or 0) > 0:
        engagement = command_engage(
            argparse.Namespace(
                request_id=request["id"],
                service_ids=None,
                count=int(args.auto_engage_count),
            ),
            state,
        )["objects"]["engagement_feed"]
        objects["engagement_feed"] = engagement
    audit(
        state,
        state["agents"][buyer_agent_id]["name"],
        "buying_request.started_by_human_intent",
        "Buying Request",
        request["id"],
        args.need,
        {
            "buying_request": request,
            "search_results_count": len(objects["search_results"]),
            "auto_engaged": "engagement_feed" in objects,
            "playbook_version": state["agents"][buyer_agent_id].get("playbook_version"),
            "playbook_rule": "Buyer-side human intent starts a Buying Request; the Buying Agent then runs the marketplace workflow inside its Buying Playbook.",
            "authority_check": {"result": "request_started_inside_current_playbook", "rule": "Buying Agent Standing Authorization checked before downstream commitments"},
        },
    )
    next_steps = [
        "The Buying Agent can continue with discovery, proposals, comparison, negotiation, and signature inside its Buying Playbook.",
        "Use belong-check-buying-requests to inspect the pre-contract pipeline.",
        "Use belong-inbox for escalations, belong-steer-buying-agent for temporary guidance, or belong-train-buying-agent for durable retraining.",
    ]
    return output(f"Started Buying Request {request['id']} from buyer intent.", objects, next_steps)


def score_service(request: dict[str, Any], service: dict[str, Any], agent: dict[str, Any], buyer_agent: dict[str, Any], query: str, tags: list[str]) -> dict[str, Any]:
    service_text = " ".join(
        [
            service.get("name", ""),
            service.get("description", ""),
            " ".join(service.get("tags", [])),
            " ".join(agent.get("playbook", {}).get("deliverables", [])),
            " ".join(agent.get("playbook", {}).get("use_cases", [])),
        ]
    ).lower()
    query_terms = terms(
        " ".join(
            [
                request.get("need", ""),
                query,
                " ".join(request.get("constraints", [])),
                " ".join(buyer_agent.get("playbook", {}).get("buying_goals", [])),
                " ".join(buyer_agent.get("playbook", {}).get("needed_services", [])),
            ]
        )
    )
    matched_terms = sorted(term for term in query_terms if term in service_text)
    overlap_ratio = len(matched_terms) / max(1, len(query_terms))
    service_tags = [tag.lower() for tag in service.get("tags", [])]
    matched_tags = sorted(tag for tag in tags if tag.lower() in service_tags)
    tag_bonus = len(matched_tags) * 6
    price = float(service.get("price_signal", {}).get("starting_price", 0))
    budget = float(request.get("budget") or 0)
    budget_fit = budget and price <= budget
    budget_score = 12 if budget_fit else -10
    reputation = float(agent.get("reputation", {}).get("score", 80))
    semantic_fit = round(min(100, 20 + overlap_ratio * 65 + tag_bonus), 2)
    score = max(0, min(100, round(semantic_fit * 0.58 + reputation * 0.24 + budget_score + len(matched_tags) * 2, 2)))
    return {
        "semantic_fit": semantic_fit,
        "matched_terms": matched_terms,
        "matched_tags": matched_tags,
        "budget_fit": bool(budget_fit) if budget else True,
        "reputation": reputation,
        "score": score,
    }


def command_search(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    request = state["buying_requests"].get(args.request_id)
    if not request:
        raise ValueError(f"Unknown Buying Request: {args.request_id}")
    buyer_agent = state["agents"][request["buying_agent_id"]]
    ensure_agent_can_act(buyer_agent, "marketplace search")
    ensure_flow_agent_can_act(request, "run marketplace search")
    if not any(service.get("status") == "listed" for service in state["services"].values()):
        seed_marketplace_catalog(state)
    tags = split_list(args.tags)
    results = []
    for service_id, service in state["services"].items():
        if service.get("status") != "listed":
            continue
        selling_agent = state["agents"][service["selling_agent_id"]]
        scoring = score_service(request, service, selling_agent, buyer_agent, args.query or request.get("need", ""), tags)
        results.append(
            {
                "service_id": service_id,
                "service_name": service["name"],
                "provider": state["organizations"][service["provider_organization_id"]]["name"],
                "selling_agent_id": service["selling_agent_id"],
                "price_signal": service["price_signal"],
                "availability": service["availability"],
                "supported_contract_terms": service["supported_contract_terms"],
                "tags": service["tags"],
                "ranking": scoring,
            }
        )
    results.sort(key=lambda item: item["ranking"]["score"], reverse=True)
    request["search_results"] = results[: int(args.limit)]
    request["status"] = "searched"
    audit(state, "Buying Agent", "search.completed", "Buying Request", args.request_id, f"Semantic search returned {len(request['search_results'])} Services")
    return output(
        f"Found {len(request['search_results'])} Service Search Results for {args.request_id}.",
        {"search_results": request["search_results"]},
        [
            "Engage one top result for direct buying or multiple results for a competitive feed.",
            "Use the ranking explanation to explain semantic fit, reputation, constraints, availability, and buyer preferences.",
            "Open the inbox if a provider, budget, or policy exception appears.",
        ],
    )


def selected_service_ids(state: dict[str, Any], request: dict[str, Any], raw_ids: str | None, count: int) -> list[str]:
    result_ids = [result["service_id"] for result in request.get("search_results", [])]
    if request.get("status") != "searched" or not result_ids:
        raise ValueError("Run semantic search before opening an Engagement Feed.")
    if raw_ids:
        ids = split_list(raw_ids)
    else:
        ids = result_ids[:count]
    if not ids:
        raise ValueError("No Service IDs selected. Run search first or pass --service-ids.")
    unknown = [service_id for service_id in ids if service_id not in state["services"]]
    if unknown:
        raise ValueError(f"Unknown Service IDs: {', '.join(unknown)}")
    outside_search = [service_id for service_id in ids if service_id not in set(result_ids)]
    if outside_search:
        raise ValueError(f"Service IDs must come from the Buying Request search results: {', '.join(outside_search)}")
    return ids


def command_engage(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    request = state["buying_requests"].get(args.request_id)
    if not request:
        raise ValueError(f"Unknown Buying Request: {args.request_id}")
    buyer_agent = state["agents"][request["buying_agent_id"]]
    ensure_agent_can_act(buyer_agent, "an Engagement Feed")
    ensure_flow_agent_can_act(request, "open an Engagement Feed")
    service_ids = selected_service_ids(state, request, args.service_ids, args.count)
    feed_id = next_id(state, "feed")
    feed = {
        "id": feed_id,
        "buying_request_id": args.request_id,
        "mode": "competitive" if len(service_ids) > 1 else "direct",
        "service_ids": service_ids,
        "selling_agent_ids": [state["services"][service_id]["selling_agent_id"] for service_id in service_ids],
        "status": "discovery",
        "messages": [],
        "proposal_ids": [],
        "created_at": now(),
    }
    state["engagement_feeds"][feed_id] = feed
    request.setdefault("engagement_feeds", []).append(feed_id)
    questionnaires = []
    for service_id in service_ids:
        service = state["services"][service_id]
        agent = state["agents"][service["selling_agent_id"]]
        ensure_agent_can_act(agent, "seller-led discovery")
        resolve_matching_inbox(
            state,
            "Service",
            service_id,
            "Selling Agent ready for marketplace",
            agent["name"],
            "Buying Agent opened an Engagement Feed for this Service.",
        )
        questionnaire_id = next_id(state, "questionnaire")
        questionnaire = {
            "id": questionnaire_id,
            "feed_id": feed_id,
            "service_id": service_id,
            "selling_agent_id": agent["id"],
            "questions": agent["playbook"].get("discovery_questions", []),
            "status": "pending_answer",
            "answers": None,
            "created_at": now(),
        }
        state["discovery_questionnaires"][questionnaire_id] = questionnaire
        questionnaires.append(questionnaire)
    add_inbox(
        state,
        "buyer",
        "information",
        "Answer seller-led Discovery Questionnaires",
        f"{len(questionnaires)} Selling Agent questionnaire(s) are waiting in Engagement Feed {feed_id}.",
        "Engagement Feed",
        feed_id,
    )
    add_inbox(
        state,
        "seller",
        "information",
        "Review Engagement Feed discovery",
        f"Buying Agent opened Engagement Feed {feed_id}. Review buyer need and wait for discovery answers before sending seller-signed Service Contract/SOW proposals.",
        "Engagement Feed",
        feed_id,
    )
    audit(state, "Buying Agent", "engagement_feed.opened", "Engagement Feed", feed_id, f"Opened {feed['mode']} Engagement Feed", {"service_ids": service_ids})
    return output(
        f"Opened {feed['mode']} Engagement Feed {feed_id}.",
        {"engagement_feed": feed, "discovery_questionnaires": questionnaires},
        [
            "Answer the seller-led Discovery Questionnaires.",
            "Ask Selling Agents to produce seller-signed Service Contract/SOW proposals.",
            "Escalate to the buyer-side human if a discovery answer is unknown or sensitive.",
        ],
    )


def command_answer_discovery(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    feed = state["engagement_feeds"].get(args.feed_id)
    if not feed:
        raise ValueError(f"Unknown Engagement Feed: {args.feed_id}")
    as_human = bool(getattr(args, "as_human", False))
    discovery_flow = state["buying_requests"].get(feed["buying_request_id"])
    if discovery_flow:
        ensure_flow_actor_can_act(discovery_flow, as_human, "answer seller-led discovery")
    updated = []
    for questionnaire in state["discovery_questionnaires"].values():
        if questionnaire.get("feed_id") == args.feed_id:
            questionnaire["answers"] = args.answers
            questionnaire["status"] = "answered"
            updated.append(questionnaire)
    feed["status"] = "ready_for_proposals"
    resolve_matching_inbox(
        state,
        "Engagement Feed",
        args.feed_id,
        "Answer seller-led Discovery Questionnaires",
        "Buying Agent",
        "Discovery answers submitted.",
    )
    add_inbox(
        state,
        "seller",
        "instruction_execution",
        "Send seller-signed Service Contract/SOW proposals",
        f"Discovery answers are ready in Engagement Feed {args.feed_id}. Selling Agents can create seller-signed Service Contract/SOW proposals.",
        "Engagement Feed",
        args.feed_id,
    )
    audit(state, "Buying Agent", "discovery.answered", "Engagement Feed", args.feed_id, "Answered seller-led discovery questionnaires", {"answers": args.answers})
    return output(
        f"Answered {len(updated)} Discovery Questionnaire(s) in {args.feed_id}.",
        {"discovery_questionnaires": updated},
        [
            "Create seller-signed Service Contract/SOW proposals.",
            "Compare proposals before signature.",
            "Use Decision Explanation if the Buying Agent chooses one provider over another.",
        ],
    )


def proposal_amount(service: dict[str, Any], request: dict[str, Any]) -> float:
    starting = float(service["price_signal"].get("starting_price", 5000))
    budget = float(request.get("budget") or starting)
    if starting > budget:
        return starting
    return starting


def payment_schedule(amount: float, payment_terms: str | None) -> dict[str, Any]:
    text = (payment_terms or "").lower()
    if "50%" in text:
        signature_due = round(amount * 0.5, 2)
        acceptance_due = round(amount - signature_due, 2)
    elif "subscription" in text:
        signature_due = round(amount, 2)
        acceptance_due = 0.0
    else:
        signature_due = round(amount, 2)
        acceptance_due = 0.0
    return {
        "signature_due": signature_due,
        "acceptance_due": acceptance_due,
        "total": round(amount, 2),
        "description": payment_terms or "Collected according to signed Service Contract/SOW",
    }


def update_contract_amount(contract: dict[str, Any], amount: float, reason: str) -> None:
    contract["versions"].append(deepcopy({k: v for k, v in contract.items() if k != "versions"}))
    contract["version"] += 1
    contract["commercial_terms"]["amount"] = round(amount, 2)
    contract["commercial_terms"]["belong_platform_fee"] = round(amount * DEFAULT_PLATFORM_FEE_RATE, 2)
    contract["commercial_terms"]["seller_net_after_platform_fee"] = round(amount * (1 - DEFAULT_PLATFORM_FEE_RATE), 2)
    contract["commercial_terms"]["payment_schedule"] = payment_schedule(amount, contract["commercial_terms"].get("payment_terms"))
    contract["last_amendment_reason"] = reason


def command_create_proposals(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    feed = state["engagement_feeds"].get(args.feed_id)
    if not feed:
        raise ValueError(f"Unknown Engagement Feed: {args.feed_id}")
    questionnaires = [q for q in state["discovery_questionnaires"].values() if q.get("feed_id") == args.feed_id]
    unanswered = [q["id"] for q in questionnaires if q.get("status") != "answered"]
    if unanswered:
        raise ValueError(f"Discovery must be answered before seller-signed proposals. Unanswered questionnaires: {', '.join(unanswered)}")
    as_human = bool(getattr(args, "as_human", False))
    request = state["buying_requests"][feed["buying_request_id"]]
    ensure_flow_actor_can_act(request, as_human, "create seller-signed proposals")
    if not as_human:
        for service_id in feed["service_ids"]:
            seller_agent = state["agents"][state["services"][service_id]["selling_agent_id"]]
            if "sign" in playbook_human_actions(seller_agent["playbook"]):
                return route_action_to_human(state, "seller", "sign", "Engagement Feed", args.feed_id, seller_agent.get("playbook_version"))
    proposals = []
    for service_id in feed["service_ids"]:
        service = state["services"][service_id]
        agent = state["agents"][service["selling_agent_id"]]
        if not as_human:
            ensure_agent_can_act(agent, "seller-signed proposal creation")
        existing = [
            state["proposals"][proposal_id]
            for proposal_id in feed.get("proposal_ids", [])
            if state["proposals"].get(proposal_id, {}).get("service_id") == service_id
            and state["proposals"].get(proposal_id, {}).get("status") in {"seller_signed_waiting_buyer_signature", "seller_signed_revised_waiting_buyer_signature"}
        ]
        if existing:
            proposal = existing[-1]
            proposals.append({"proposal": proposal, "contract": state["contracts"][proposal["contract_id"]], "reused": True})
            continue
        amount = proposal_amount(service, request)
        proposal_id = next_id(state, "proposal")
        contract_id = next_id(state, "contract")
        schedule = payment_schedule(amount, service["price_signal"].get("collections"))
        contract = {
            "id": contract_id,
            "proposal_id": proposal_id,
            "status": "seller_signed_waiting_buyer_signature",
            "signing_provider": "Mock Signing Provider (provider choice open for production)",
            "seller_signature": {"status": "signed", "timestamp": now(), "agent_id": agent["id"]},
            "buyer_signature": {"status": "pending"},
            "legal_parties": {
                "buyer_organization_id": state["agents"][request["buying_agent_id"]]["organization_id"],
                "service_provider_organization_id": service["provider_organization_id"],
                "belong_role": "workflow_facilitator_not_legal_party",
            },
            "sow": {
                "scope": agent["playbook"].get("service_description"),
                "deliverables": agent["playbook"].get("deliverables", []),
                "evidence_requirements": agent["playbook"].get("evidence_requirements", []),
                "acceptance_criteria": state["agents"][request["buying_agent_id"]]["playbook"].get("acceptance_criteria", []),
                "timeline": request.get("timeline"),
            },
            "commercial_terms": {
                "amount": amount,
                "currency": service["price_signal"].get("currency", "USD"),
                "payment_terms": service["price_signal"].get("collections"),
                "billing_cycle": service["price_signal"].get("billing_cycle"),
                "payment_schedule": schedule,
                "belong_platform_fee": round(amount * DEFAULT_PLATFORM_FEE_RATE, 2),
                "seller_net_after_platform_fee": round(amount * (1 - DEFAULT_PLATFORM_FEE_RATE), 2),
                "merchant_of_record": state["organizations"][service["provider_organization_id"]]["name"],
                "belong_role": "legal/payment workflow facilitator, not merchant of record",
            },
            "version": 1,
            "versions": [],
        }
        proposal = {
            "id": proposal_id,
            "feed_id": args.feed_id,
            "buying_request_id": request["id"],
            "service_id": service_id,
            "selling_agent_id": agent["id"],
            "contract_id": contract_id,
            "status": "seller_signed_waiting_buyer_signature",
            "summary": f"Seller-signed Service Contract/SOW for {service['name']}",
            "created_at": now(),
        }
        state["contracts"][contract_id] = contract
        state["proposals"][proposal_id] = proposal
        feed["proposal_ids"].append(proposal_id)
        proposals.append({"proposal": proposal, "contract": contract})
        audit(
            state,
            agent["name"],
            "proposal.seller_signed",
            "Proposal",
            proposal_id,
            proposal["summary"],
            {
                "contract_id": contract_id,
                "playbook_version": agent.get("playbook_version"),
                "playbook_rule": "Selling Agent may send seller-signed Service Contract/SOW proposals after seller-led discovery is answered.",
                "authority_check": {"result": "passed", "rule": "within standard Service Playbook proposal authority"},
                "contract": contract,
            },
        )
    feed["status"] = "proposals_received"
    resolve_matching_inbox(
        state,
        "Engagement Feed",
        args.feed_id,
        "Send seller-signed Service Contract/SOW proposals",
        "Selling Agent",
        "Seller-signed Service Contract/SOW proposals were sent.",
    )
    resolve_matching_inbox(
        state,
        "Engagement Feed",
        args.feed_id,
        "Review Engagement Feed discovery",
        "Selling Agent",
        "Discovery was reviewed and proposals were sent.",
    )
    add_inbox(
        state,
        "buyer",
        "authorization",
        "Review seller-signed Service Contract/SOW proposals",
        f"{len(proposals)} proposal(s) are ready for comparison, negotiation, or buyer signature.",
        "Engagement Feed",
        args.feed_id,
    )
    return output(
        f"Created {len(proposals)} seller-signed Service Contract/SOW Proposal(s).",
        {"proposals": proposals},
        [
            "Compare proposals by scope, price, terms, timing, reputation, and fit.",
            "Negotiate terms if the Buying Playbook suggests a better outcome.",
            "Sign a proposal only when it fits Standing Authorization or after human approval.",
        ],
    )


def sow_fit(contract: dict[str, Any], service: dict[str, Any], request: dict[str, Any], buyer_agent: dict[str, Any]) -> dict[str, Any]:
    required = terms(
        " ".join(
            [
                request.get("need", ""),
                " ".join(request.get("constraints", [])),
                " ".join(buyer_agent.get("playbook", {}).get("acceptance_criteria", [])),
                " ".join(buyer_agent.get("playbook", {}).get("needed_services", [])),
            ]
        )
    )
    offered_text = " ".join(
        [
            service.get("name", ""),
            service.get("description", ""),
            " ".join(service.get("tags", [])),
            " ".join(contract.get("sow", {}).get("deliverables", [])),
            " ".join(contract.get("sow", {}).get("evidence_requirements", [])),
            contract.get("sow", {}).get("scope", ""),
        ]
    ).lower()
    matched = sorted(term for term in required if term in offered_text)
    ratio = len(matched) / max(1, len(required))
    return {
        "required_terms": sorted(required),
        "matched_terms": matched,
        "coverage": round(ratio, 3),
        "score": round(min(100, 25 + ratio * 75), 2),
    }


def command_compare_proposals(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    request = state["buying_requests"].get(args.request_id)
    if not request:
        raise ValueError(f"Unknown Buying Request: {args.request_id}")
    proposals = [
        proposal
        for proposal in state["proposals"].values()
        if proposal.get("buying_request_id") == args.request_id
    ]
    buyer_agent = state["agents"][request["buying_agent_id"]]
    comparisons = []
    for proposal in proposals:
        contract = state["contracts"][proposal["contract_id"]]
        service = state["services"][proposal["service_id"]]
        agent = state["agents"][proposal["selling_agent_id"]]
        amount = contract["commercial_terms"]["amount"]
        fit = sow_fit(contract, service, request, buyer_agent)
        budget_fit = amount <= float(request.get("budget") or amount)
        recommendation = "shortlist"
        if fit["coverage"] < 0.35:
            recommendation = "do_not_shortlist_scope_mismatch"
        elif not budget_fit:
            recommendation = "escalate_budget_exception"
        comparisons.append(
            {
                "proposal_id": proposal["id"],
                "service": service["name"],
                "selling_agent_id": agent["id"],
                "reputation": agent["reputation"]["score"],
                "amount": amount,
                "budget_fit": budget_fit,
                "sow_fit": fit,
                "status": proposal["status"],
                "recommendation": recommendation,
            }
        )
    comparisons.sort(key=lambda item: (item["sow_fit"]["score"], item["budget_fit"], item["reputation"], -item["amount"]), reverse=True)
    audit(
        state,
        "Buying Agent",
        "proposal.compared",
        "Buying Request",
        args.request_id,
        f"Compared {len(comparisons)} proposals",
        {
            "comparisons": comparisons,
            "playbook_version": buyer_agent.get("playbook_version"),
            "playbook_rule": buyer_agent["playbook"].get("proposal_comparison_rules"),
            "authority_check": {"result": "comparison_only", "rule": "No signature executed during comparison"},
        },
    )
    return output(
        f"Compared {len(comparisons)} proposal(s) for {args.request_id}.",
        {"comparison": comparisons},
        [
            "Negotiate the preferred proposal if scope, price, or timeline can improve.",
            "Sign the best proposal if within Standing Authorization.",
            "Escalate to the buyer-side human if there are multiple close choices or any authority exception.",
        ],
    )


def command_negotiate(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    proposal = state["proposals"].get(args.proposal_id)
    if not proposal:
        raise ValueError(f"Unknown Proposal: {args.proposal_id}")
    if proposal.get("status") not in {"seller_signed_waiting_buyer_signature", "seller_signed_revised_waiting_buyer_signature"}:
        raise ValueError(f"Proposal {args.proposal_id} is not negotiable in status {proposal.get('status')}.")
    as_human = bool(getattr(args, "as_human", False))
    negotiate_flow = state["buying_requests"].get(proposal["buying_request_id"])
    if negotiate_flow:
        ensure_flow_actor_can_act(negotiate_flow, as_human, "negotiate the contract")
    contract = state["contracts"][proposal["contract_id"]]
    previous = deepcopy(contract)
    amount = float(contract["commercial_terms"]["amount"])
    previous_amount = amount
    if args.price_delta:
        amount += float(args.price_delta)
    elif "discount" in args.instruction.lower():
        amount = round(amount * 0.95, 2)
    selling_agent = state["agents"][proposal["selling_agent_id"]]
    if not as_human:
        ensure_agent_can_act(selling_agent, "contract negotiation")
    original_amount = float(contract.get("versions", [{}])[0].get("commercial_terms", {}).get("amount", previous_amount)) if contract.get("versions") else previous_amount
    discount_percent = max(0.0, round((original_amount - amount) / max(1, original_amount) * 100, 2))
    limit = parse_percent(selling_agent["playbook"].get("standing_authorization", {}).get("discount_limit"))
    authority_check = {
        "rule": "Selling Agent discount limit",
        "threshold": f"{limit}%",
        "actual": f"{discount_percent}%",
        "result": "passed" if discount_percent <= limit or args.seller_approved or as_human else "blocked_requires_seller_human_authorization",
    }
    if discount_percent > limit and not (args.seller_approved or as_human):
        inbox = add_inbox(
            state,
            "seller",
            "authorization",
            "Approve discount above Selling Agent Standing Authorization",
            f"Requested discount {discount_percent}% exceeds limit {limit}% for Proposal {args.proposal_id}.",
            "Proposal",
            args.proposal_id,
            urgency="high",
            metadata={"authority_check": authority_check},
        )
        audit(
            state,
            "Selling Agent",
            "contract.negotiation_blocked_authority",
            "Proposal",
            args.proposal_id,
            args.instruction,
            {
                "playbook_version": selling_agent.get("playbook_version"),
                "playbook_rule": "Selling Agent must escalate discounts above Standing Authorization.",
                "authority_check": authority_check,
                "previous_amount": previous_amount,
                "requested_amount": round(amount, 2),
            },
        )
        return output(
            "Negotiation was not applied because it exceeds Selling Agent Standing Authorization.",
            {"proposal": proposal, "contract": contract, "inbox_item": inbox},
            [
                "Resolve the seller authorization inbox item or negotiate within discount limits.",
                "Run negotiate again with seller approval if the Service Provider human approves the exception.",
            ],
        )
    contract["version"] += 1
    contract["versions"].append(previous)
    contract["commercial_terms"]["amount"] = round(amount, 2)
    contract["commercial_terms"]["belong_platform_fee"] = round(amount * DEFAULT_PLATFORM_FEE_RATE, 2)
    contract["commercial_terms"]["seller_net_after_platform_fee"] = round(amount * (1 - DEFAULT_PLATFORM_FEE_RATE), 2)
    contract["commercial_terms"]["payment_schedule"] = payment_schedule(amount, contract["commercial_terms"].get("payment_terms"))
    contract["status"] = "seller_signed_revised_waiting_buyer_signature"
    contract["seller_signature"] = {"status": "signed_revised", "timestamp": now(), "agent_id": proposal["selling_agent_id"]}
    proposal["status"] = contract["status"]
    audit(
        state,
        "Buying Agent and Selling Agent",
        "contract.negotiated",
        "Proposal",
        args.proposal_id,
        args.instruction,
        {
            "contract": contract,
            "playbook_version": selling_agent.get("playbook_version"),
            "playbook_rule": "Selling Agent may revise seller-signed Service Contract/SOW inside Standing Authorization.",
            "authority_check": authority_check,
            "previous_amount": previous_amount,
            "new_amount": round(amount, 2),
        },
    )
    return output(
        f"Negotiated Proposal {args.proposal_id}; contract is now version {contract['version']}.",
        {"proposal": proposal, "contract": contract},
        [
            "Compare revised proposals.",
            "Sign if the revised terms fit Standing Authorization.",
            "Open an authorization inbox item if terms exceed spend, scope, payment, or legal limits.",
        ],
    )


def buyer_agent_exposure(
    state: dict[str, Any],
    buyer_agent_id: str,
    exclude_change_order_id: str | None = None,
    exclude_composite_request_id: str | None = None,
    exclude_buying_request_id: str | None = None,
) -> float:
    total = 0.0
    for active in state["active_services"].values():
        if active.get("buyer_agent_id") != buyer_agent_id:
            continue
        if active.get("status") in {"canceled"}:
            continue
        contract = state["contracts"].get(active.get("contract_id"))
        if contract:
            total += float(contract["commercial_terms"].get("amount", 0))
        for change_order in active.get("change_orders", []):
            if change_order.get("id") == exclude_change_order_id:
                continue
            if change_order.get("status") in {"awaiting_signature", "awaiting_authorization"}:
                total += max(0.0, float(change_order.get("price_change", 0)))
    proposal_exposure_by_request: dict[str, float] = {}
    for proposal in state["proposals"].values():
        if proposal.get("status") not in {"seller_signed_waiting_buyer_signature", "seller_signed_revised_waiting_buyer_signature"}:
            continue
        request_id = proposal.get("buying_request_id")
        if request_id == exclude_buying_request_id:
            continue
        request = state["buying_requests"].get(request_id)
        if not request or request.get("buying_agent_id") != buyer_agent_id:
            continue
        contract = state["contracts"].get(proposal.get("contract_id"))
        if not contract:
            continue
        amount = float(contract["commercial_terms"].get("amount", 0))
        proposal_exposure_by_request[request_id] = max(proposal_exposure_by_request.get(request_id, 0.0), amount)
    total += sum(proposal_exposure_by_request.values())
    for request in state["buying_requests"].values():
        if request.get("id") == exclude_composite_request_id:
            continue
        if request.get("buying_agent_id") != buyer_agent_id or not request.get("is_composite"):
            continue
        if request.get("status") in {"canceled", "completed", "closed"}:
            continue
        total += max(0.0, float(request.get("budget") or 0))
    return round(total, 2)


def buyer_agent_spend(state: dict[str, Any], buyer_agent_id: str) -> float:
    return buyer_agent_exposure(state, buyer_agent_id)


def payment_ledger_for_contract(contract: dict[str, Any]) -> dict[str, Any]:
    amount = float(contract["commercial_terms"]["amount"])
    schedule = contract["commercial_terms"].get("payment_schedule") or payment_schedule(amount, contract["commercial_terms"].get("payment_terms"))
    return {
        "contract_amount": round(amount, 2),
        "currency": contract["commercial_terms"].get("currency", "USD"),
        "payment_schedule": schedule,
        "authorized": 0.0,
        "charged": 0.0,
        "held": 0.0,
        "released": 0.0,
        "refunded": 0.0,
        "collected": 0.0,
        "platform_fee_accrued": 0.0,
        "seller_net_accrued": 0.0,
        "merchant_of_record": contract["commercial_terms"].get("merchant_of_record", "Service Provider"),
        "belong_role": "workflow/payment facilitator, not merchant of record",
    }


def record_payment_event(
    state: dict[str, Any],
    active: dict[str, Any],
    payment_type: str,
    amount: float,
    notes: str,
    authority_check: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger = active.setdefault("payment_ledger", payment_ledger_for_contract(state["contracts"][active["contract_id"]]))
    amount = round(max(0.0, amount), 2)
    if payment_type == "authorization":
        ledger["authorized"] = round(max(ledger["authorized"], amount), 2)
    elif payment_type == "authorization_delta":
        ledger["authorized"] = round(min(ledger["contract_amount"], ledger["authorized"] + amount), 2)
    elif payment_type in {"charge", "collection"}:
        ledger["charged"] = round(min(ledger["contract_amount"], ledger["charged"] + amount), 2)
        ledger["collected"] = round(min(ledger["contract_amount"], ledger["collected"] + amount), 2)
    elif payment_type == "hold":
        ledger["held"] = round(min(ledger["contract_amount"], ledger["held"] + amount), 2)
    elif payment_type == "release":
        ledger["released"] = round(min(ledger["contract_amount"], ledger["released"] + amount), 2)
        ledger["collected"] = round(min(ledger["contract_amount"], ledger["collected"] + amount), 2)
    elif payment_type == "refund":
        ledger["refunded"] = round(min(ledger["collected"], ledger["refunded"] + amount), 2)
    ledger["platform_fee_accrued"] = round(max(0.0, (ledger["collected"] - ledger["refunded"]) * DEFAULT_PLATFORM_FEE_RATE), 2)
    ledger["seller_net_accrued"] = round(max(0.0, (ledger["collected"] - ledger["refunded"]) * (1 - DEFAULT_PLATFORM_FEE_RATE)), 2)
    payment_id = next_id(state, "payment")
    payment = {
        "id": payment_id,
        "active_service_id": active["id"],
        "type": payment_type,
        "status": f"mocked_{payment_type}",
        "amount": amount,
        "currency": ledger["currency"],
        "platform_fee": round(amount * DEFAULT_PLATFORM_FEE_RATE, 2),
        "seller_net": round(amount * (1 - DEFAULT_PLATFORM_FEE_RATE), 2),
        "provider": "Stripe Payment Stack mock",
        "merchant_of_record": ledger["merchant_of_record"],
        "belong_role": ledger["belong_role"],
        "payment_schedule": ledger["payment_schedule"],
        "ledger_after": deepcopy(ledger),
        "notes": notes,
        "created_at": now(),
    }
    state["payments"][payment_id] = payment
    audit(
        state,
        "Stripe Payment Stack mock",
        f"payment.{payment_type}",
        "Active Service",
        active["id"],
        f"Payment event {payment_type}",
        {
            "payment": payment,
            "payment_ledger": deepcopy(ledger),
            "playbook_rule": "Payments and collections follow the executed Service Contract/SOW.",
            "authority_check": authority_check or {"result": "mocked_provider_event", "rule": "Stripe Payment Stack mock"},
        },
    )
    return payment


def command_sign(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    proposal = state["proposals"].get(args.proposal_id)
    if not proposal:
        raise ValueError(f"Unknown Proposal: {args.proposal_id}")
    if proposal.get("status") not in {"seller_signed_waiting_buyer_signature", "seller_signed_revised_waiting_buyer_signature"}:
        raise ValueError(f"Proposal {args.proposal_id} cannot be signed in status {proposal.get('status')}.")
    existing_active = next((active for active in state["active_services"].values() if active.get("proposal_id") == args.proposal_id), None)
    if existing_active:
        raise ValueError(f"Proposal {args.proposal_id} is already executed as Active Service {existing_active['id']}.")
    contract = state["contracts"][proposal["contract_id"]]
    request = state["buying_requests"][proposal["buying_request_id"]]
    as_human = bool(getattr(args, "as_human", False))
    ensure_flow_actor_can_act(request, as_human, "sign the contract")
    buyer_agent_id = request["buying_agent_id"]
    buyer_agent = state["agents"][buyer_agent_id]
    if not as_human and "sign" in playbook_human_actions(buyer_agent["playbook"]):
        return route_action_to_human(state, "buyer", "sign", "Proposal", args.proposal_id, buyer_agent.get("playbook_version"))
    if not as_human:
        ensure_agent_can_act(buyer_agent, "buyer signature")
    amount = float(contract["commercial_terms"]["amount"])
    max_spend = float(buyer_agent["playbook"]["standing_authorization"].get("max_spend", 0))
    existing_spend = buyer_agent_exposure(state, buyer_agent_id, exclude_buying_request_id=request["id"])
    projected_spend = round(existing_spend + amount, 2)
    authority_check = {
        "rule": "Buying Agent cumulative spend limit",
        "threshold": max_spend,
        "current_spend": existing_spend,
        "proposal_amount": amount,
        "projected_spend": projected_spend,
        "result": "passed" if projected_spend <= max_spend or args.human_approved or as_human else "blocked_requires_buyer_human_authorization",
    }
    if projected_spend > max_spend and not (args.human_approved or as_human):
        inbox = add_inbox(
            state,
            "buyer",
            "authorization",
            "Approve spend above Buying Agent Standing Authorization",
            f"Projected spend {projected_spend} exceeds max spend {max_spend}. Current spend: {existing_spend}; proposal amount: {amount}.",
            "Proposal",
            args.proposal_id,
            urgency="high",
            metadata={"authority_check": authority_check},
        )
        audit(
            state,
            buyer_agent["name"],
            "signature.blocked_authority",
            "Proposal",
            args.proposal_id,
            "Signature requires human approval",
            {
                "playbook_version": buyer_agent.get("playbook_version"),
                "playbook_rule": buyer_agent["playbook"].get("contract_authority"),
                "authority_check": authority_check,
                "proposal": proposal,
                "contract": contract,
            },
        )
        return output(
            "Buyer signature was not executed because the proposal exceeds Standing Authorization.",
            {"proposal": proposal, "contract": contract, "inbox_item": inbox},
            [
                "Resolve the authorization inbox item as the buyer-side human.",
                "Run sign again with human approval after review.",
                "Negotiate the proposal below the authority threshold.",
            ],
        )
    service = state["services"][proposal["service_id"]]
    selling_agent_id = proposal["selling_agent_id"]
    active_service_id = next_id(state, "active")
    contract["status"] = "executed"
    contract["buyer_signature"] = {
        "status": "signed",
        "timestamp": now(),
        "agent_id": buyer_agent_id,
        "human_approved": bool(args.human_approved) or as_human,
        "signed_by_human": as_human,
    }
    proposal["status"] = "signed_executed"
    active_service = {
        "id": active_service_id,
        "status": "delivery",
        "control_state": "agent_controlled",
        "buying_request_id": request["id"],
        "proposal_id": proposal["id"],
        "contract_id": contract["id"],
        "buyer_agent_id": buyer_agent_id,
        "selling_agent_id": selling_agent_id,
        "service_id": service["id"],
        "delivery": {"tasks": [], "deliverables": [], "evidence_packages": [], "acceptance": []},
        "payment_ledger": payment_ledger_for_contract(contract),
        "messages": [],
        "meetings": [],
        "change_orders": [],
        "created_at": now(),
    }
    state["active_services"][active_service_id] = active_service
    auth_payment = record_payment_event(
        state,
        active_service,
        "authorization",
        amount,
        "Buyer signature authorized the contract amount.",
        {"result": "buyer_signature_authorized", "rule": buyer_agent["playbook"].get("payment_rules")},
    )
    signature_due = float(active_service["payment_ledger"]["payment_schedule"].get("signature_due", 0))
    signature_payment = None
    if signature_due:
        signature_payment = record_payment_event(
            state,
            active_service,
            "collection",
            signature_due,
            "Signature milestone collected according to Service Contract/SOW.",
            {"result": "contract_signature_milestone", "rule": contract["commercial_terms"].get("payment_terms")},
        )
    audit(
        state,
        buyer_agent["name"],
        "contract.buyer_signed",
        "Active Service",
        active_service_id,
        f"Buyer signed proposal {proposal['id']} and created Active Service",
        {
            "playbook_version": buyer_agent.get("playbook_version"),
            "playbook_rule": buyer_agent["playbook"].get("contract_authority"),
            "authority_check": authority_check,
            "proposal": proposal,
            "contract": contract,
            "payment_ledger": active_service["payment_ledger"],
        },
    )
    add_reputation_event(state, buyer_agent_id, 0.5, "Signed Service Contract/SOW within authority", "Active Service", active_service_id)
    add_reputation_event(state, selling_agent_id, 0.5, "Seller-signed proposal converted to Active Service", "Active Service", active_service_id)
    add_inbox(
        state,
        "seller",
        "fulfillment",
        "Start Active Service delivery",
        f"Active Service {active_service_id} is executed. Create provider tasks, prepare kickoff, and submit evidence.",
        "Active Service",
        active_service_id,
    )
    resolve_matching_inbox(
        state,
        "Engagement Feed",
        proposal["feed_id"],
        "Review seller-signed Service Contract/SOW proposals",
        buyer_agent["name"],
        "Buyer signature executed a seller-signed Service Contract/SOW.",
    )
    resolve_matching_inbox(
        state,
        "Proposal",
        args.proposal_id,
        "Approve spend above Buying Agent Standing Authorization",
        buyer_agent["name"],
        "Buyer-side human approval was applied to signature.",
    )
    return output(
        f"Executed Service Contract/SOW and created Active Service {active_service_id}.",
        {"active_service": active_service, "contract": contract, "payment": auth_payment, "signature_payment": signature_payment},
        [
            "Internal agent capabilities can now coordinate fulfillment tasks, meetings, evidence, Delivery Acceptance, payments, and Change Orders.",
            "Use belong-inbox to resolve provider fulfillment requests.",
            "Use belong-check-reputation to inspect the audit trail and reputation events.",
        ],
    )


def get_active(state: dict[str, Any], active_service_id: str) -> dict[str, Any]:
    active = state["active_services"].get(active_service_id)
    if not active:
        raise ValueError(f"Unknown Active Service: {active_service_id}")
    return active


def active_actor_roles(state: dict[str, Any], active: dict[str, Any], actor: str) -> set[str]:
    actor_lower = actor.lower()
    roles = set()
    if "buying" in actor_lower or "buyer" in actor_lower:
        roles.add("buyer")
    if "selling" in actor_lower or "seller" in actor_lower or "service provider" in actor_lower:
        roles.add("seller")
    buyer_agent = state["agents"][active["buyer_agent_id"]]
    seller_agent = state["agents"][active["selling_agent_id"]]
    buyer_account = state["accounts"].get(buyer_agent.get("account_id"), {})
    seller_account = state["accounts"].get(seller_agent.get("account_id"), {})
    buyer_org = state["organizations"].get(buyer_agent.get("organization_id"), {})
    seller_org = state["organizations"].get(seller_agent.get("organization_id"), {})
    buyer_names = [buyer_agent.get("name"), buyer_account.get("name"), buyer_org.get("name")]
    seller_names = [seller_agent.get("name"), seller_account.get("name"), seller_org.get("name")]
    if any(name and actor_lower == str(name).lower() for name in buyer_names):
        roles.add("buyer")
    if any(name and actor_lower == str(name).lower() for name in seller_names):
        roles.add("seller")
    return roles


def active_required_roles(action: str, payment_type: str | None = None) -> tuple[set[str], set[str]]:
    if action in {"fulfillment-task", "deliver"}:
        return {"seller"}, {"seller"}
    if action in {"accept", "reject", "revise"}:
        return {"buyer"}, {"buyer"}
    if action == "payment":
        payment_type = canonical_payment_type(payment_type)
        if payment_type in {"charge", "collection"}:
            return {"seller"}, {"seller"}
        return {"buyer"}, {"buyer"}
    if action == "change-order":
        return {"buyer", "seller"}, {"buyer", "seller"}
    if action in {"dispute", "meeting", "message"}:
        return {"buyer", "seller"}, {"buyer", "seller"}
    return {"buyer", "seller"}, set()


def ensure_active_actor_can_act(state: dict[str, Any], active: dict[str, Any], actor: str, action: str, payment_type: str | None = None, as_human: bool = False) -> None:
    ensure_flow_actor_can_act(active, as_human, f"perform Active Service action {action}")
    pause_roles, allowed_roles = active_required_roles(action, payment_type)
    if not as_human:
        if "buyer" in pause_roles:
            ensure_agent_can_act(state["agents"][active["buyer_agent_id"]], f"Active Service action {action}")
        if "seller" in pause_roles:
            ensure_agent_can_act(state["agents"][active["selling_agent_id"]], f"Active Service action {action}")
    actor_roles = active_actor_roles(state, active, actor)
    if allowed_roles and not (actor_roles & allowed_roles):
        role_names = " or ".join(sorted(allowed_roles))
        raise ValueError(f"Active Service action {action} requires {role_names} authority. Actor '{actor}' resolved to roles: {sorted(actor_roles) or ['unknown']}.")


def active_has_evidence(active: dict[str, Any]) -> bool:
    return bool(active.get("delivery", {}).get("evidence_packages"))


def active_has_buyer_acceptance(active: dict[str, Any]) -> bool:
    return active.get("status") == "accepted" or any(
        acceptance.get("decision") == "accept"
        for acceptance in active.get("delivery", {}).get("acceptance", [])
    )


def ensure_delivery_acceptance_ready(active: dict[str, Any], action: str) -> None:
    if action in {"accept", "reject", "revise"} and not active_has_evidence(active):
        raise ValueError(f"Delivery decision {action} requires a Deliverable Evidence Package first.")


def ensure_payment_lifecycle_ready(active: dict[str, Any], payment_type: str, human_approved: bool) -> None:
    if payment_type in {"charge", "collection", "release"}:
        if not active_has_evidence(active) and not human_approved:
            raise ValueError(f"Payment event {payment_type} requires deliverable evidence or explicit human-approved exception.")
        if not active_has_buyer_acceptance(active) and not human_approved:
            raise ValueError(f"Payment event {payment_type} requires buyer acceptance or explicit human-approved exception.")
    if payment_type == "refund" and not human_approved and active.get("status") not in {"disputed", "revision_requested", "rejected"}:
        raise ValueError("Refund requires dispute/revision context or explicit human-approved exception.")


def apply_signed_change_order(
    state: dict[str, Any],
    active: dict[str, Any],
    change_order: dict[str, Any],
    actor: str,
    human_approved: bool,
    source: str,
    as_human: bool = False,
) -> dict[str, Any]:
    ensure_active_actor_can_act(state, active, actor, "change-order", as_human=as_human)
    contract = state["contracts"][active["contract_id"]]
    buyer_agent = state["agents"][active["buyer_agent_id"]]
    old_amount = float(contract["commercial_terms"]["amount"])
    new_amount = round(old_amount + float(change_order.get("price_change", 0)), 2)
    max_spend = float(buyer_agent["playbook"]["standing_authorization"].get("max_spend", 0))
    current_spend = buyer_agent_exposure(state, active["buyer_agent_id"], exclude_change_order_id=change_order.get("id"))
    projected_spend = round(current_spend - old_amount + new_amount, 2)
    authority_check = {
        "rule": "Buying Agent cumulative spend limit for Change Order",
        "threshold": max_spend,
        "current_spend": current_spend,
        "current_contract_amount": old_amount,
        "change_order_delta": float(change_order.get("price_change", 0)),
        "projected_spend": projected_spend,
        "result": "passed" if projected_spend <= max_spend else ("human_approved_exception" if (human_approved or as_human) else "blocked_requires_buyer_human_authorization"),
    }
    if projected_spend > max_spend and not (human_approved or as_human):
        change_order["status"] = "awaiting_authorization"
        inbox = add_inbox(
            state,
            "buyer",
            "authorization",
            "Approve Change Order spend above Buying Agent Standing Authorization",
            f"Projected spend {projected_spend} exceeds max spend {max_spend} for Change Order {change_order['id']}.",
            "Active Service",
            active["id"],
            urgency="high",
            metadata={"change_order_id": change_order["id"], "authority_check": authority_check},
        )
        audit(
            state,
            actor,
            "change_order.blocked_authority",
            "Active Service",
            active["id"],
            change_order["summary"],
            {
                "change_order": change_order,
                "contract_before": contract,
                "payment_ledger": active.get("payment_ledger"),
                "playbook_version": buyer_agent.get("playbook_version"),
                "playbook_rule": buyer_agent["playbook"].get("contract_authority"),
                "authority_check": authority_check,
                "inbox_item_id": inbox["id"],
            },
        )
        return {"blocked": True, "inbox_item": inbox, "authority_check": authority_check}

    contract_before = deepcopy(contract)
    ledger = active.setdefault("payment_ledger", payment_ledger_for_contract(contract))
    ledger_before = deepcopy(ledger)
    update_contract_amount(contract, new_amount, f"{source} Change Order {change_order['id']}: {change_order['summary']}")
    change_order["status"] = "signed"
    change_order["signed_at"] = now()
    change_order["signed_by"] = actor
    change_order["contract_version_after"] = contract["version"]
    ledger["contract_amount"] = round(new_amount, 2)
    ledger["currency"] = contract["commercial_terms"].get("currency", "USD")
    ledger["payment_schedule"] = payment_schedule(new_amount, contract["commercial_terms"].get("payment_terms"))
    ledger["merchant_of_record"] = contract["commercial_terms"].get("merchant_of_record", ledger.get("merchant_of_record", "Service Provider"))
    ledger["belong_role"] = "workflow/payment facilitator, not merchant of record"
    auth_delta = max(0.0, round(new_amount - float(ledger.get("authorized", 0)), 2))
    signature_gap = max(0.0, round(float(ledger["payment_schedule"].get("signature_due", 0)) - float(ledger.get("collected", 0)), 2))
    payment_events = []
    if auth_delta:
        payment_events.append(record_payment_event(state, active, "authorization_delta", auth_delta, f"Change Order {change_order['id']} authorized contract amount delta."))
    if signature_gap:
        payment_events.append(record_payment_event(state, active, "collection", signature_gap, f"Change Order {change_order['id']} collected signature milestone delta."))
    ledger["platform_fee_accrued"] = round(max(0.0, (ledger["collected"] - ledger["refunded"]) * DEFAULT_PLATFORM_FEE_RATE), 2)
    ledger["seller_net_accrued"] = round(max(0.0, (ledger["collected"] - ledger["refunded"]) * (1 - DEFAULT_PLATFORM_FEE_RATE)), 2)
    audit(
        state,
        actor,
        "change_order.applied",
        "Active Service",
        active["id"],
        change_order["summary"],
        {
            "change_order": change_order,
            "contract_before": contract_before,
            "contract": contract,
            "ledger_before": ledger_before,
            "payment_ledger": deepcopy(ledger),
            "payment_events": payment_events,
            "playbook_version": buyer_agent.get("playbook_version"),
            "playbook_rule": "Change Orders are signed Service Contract/SOW amendments and must pass contract/payment authority.",
            "authority_check": authority_check,
            "source": source,
        },
    )
    return {
        "blocked": False,
        "contract": contract,
        "payment_ledger": ledger,
        "payment_events": payment_events,
        "authority_check": authority_check,
    }


def command_active_action(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    active = get_active(state, args.active_service_id)
    action = args.action
    actor = args.actor or "Belong Agent"
    as_human = bool(getattr(args, "as_human", False))
    ensure_active_actor_can_act(state, active, actor, action, args.payment_type, as_human=as_human)
    if not as_human:
        _, allowed_roles = active_required_roles(action, args.payment_type)
        for role in ("buyer", "seller"):
            if role not in allowed_roles:
                continue
            token = active_action_human_token(action, role)
            if not token:
                continue
            role_agent = state["agents"][active["buyer_agent_id"] if role == "buyer" else active["selling_agent_id"]]
            if token in playbook_human_actions(role_agent["playbook"]):
                return route_action_to_human(state, role, token, "Active Service", active["id"], role_agent.get("playbook_version"))
    details = args.details or ""
    created: dict[str, Any] = {}
    if action == "fulfillment-task":
        task = {
            "id": next_id(state, "task"),
            "action": details or "Provider human action required",
            "owner": args.owner or "Service Provider human/team",
            "due": args.due or "next business day",
            "context": args.context or "Created by Selling Agent to deliver the Service.",
            "evidence_required": split_list(args.evidence_required) or ["completion note"],
            "status": "open",
            "created_at": now(),
        }
        active["delivery"]["tasks"].append(task)
        created["fulfillment_task"] = task
        add_inbox(state, "seller", "instruction_execution", "Complete Fulfillment Task", task["action"], "Active Service", active["id"], assigned_to=task["owner"])
        audit(state, actor, "fulfillment_task.created", "Active Service", active["id"], task["action"], task)
    elif action == "deliver":
        evidence = {
            "id": next_id(state, "evidence"),
            "deliverable": args.deliverable or "Service deliverable",
            "files": split_list(args.files),
            "links": split_list(args.links),
            "notes": details or "Delivered with mocked evidence.",
            "acceptance_mapping": split_list(args.acceptance_mapping),
            "submitter": actor,
            "timestamp": now(),
        }
        active["delivery"]["deliverables"].append(
            {
                "id": next_id(state, "deliverable"),
                "name": evidence["deliverable"],
                "status": "submitted_for_acceptance",
                "evidence_package_id": evidence["id"],
                "submitted_at": evidence["timestamp"],
            }
        )
        active["delivery"]["evidence_packages"].append(evidence)
        active["status"] = "acceptance_review"
        created["deliverable_evidence_package"] = evidence
        resolve_matching_inbox(
            state,
            "Active Service",
            active["id"],
            "Start Active Service delivery",
            actor,
            "Deliverable evidence has been submitted for acceptance review.",
        )
        resolve_matching_inbox(
            state,
            "Active Service",
            active["id"],
            "Complete Fulfillment Task",
            actor,
            "Fulfillment task completed through deliverable evidence submission.",
        )
        add_inbox(state, "buyer", "authorization", "Review Deliverable Evidence Package", f"Evidence {evidence['id']} is ready for acceptance review.", "Active Service", active["id"])
        audit(
            state,
            actor,
            "evidence.submitted",
            "Active Service",
            active["id"],
            f"Submitted evidence {evidence['id']}",
            {
                "evidence": evidence,
                "contract": state["contracts"][active["contract_id"]],
                "playbook_rule": "Selling Agent submits Deliverable Evidence Package mapped to SOW acceptance criteria.",
                "authority_check": {"result": "submitted_for_buyer_acceptance", "rule": "SOW evidence requirements"},
            },
        )
    elif action in {"accept", "reject", "revise", "dispute"}:
        ensure_delivery_acceptance_ready(active, action)
        acceptance = {
            "id": next_id(state, "acceptance"),
            "decision": action,
            "notes": details,
            "actor": actor,
            "timestamp": now(),
        }
        active["delivery"]["acceptance"].append(acceptance)
        if action == "accept":
            active["status"] = "accepted"
            payment = payment_for_active(
                state,
                active["id"],
                "release",
                details or "Acceptance released payment",
                {"result": "buyer_acceptance_release", "rule": state["agents"][active["buyer_agent_id"]]["playbook"].get("payment_rules"), "human_approved": False},
            )
            created["payment_event"] = payment
            add_reputation_event(state, active["selling_agent_id"], 2.0, "Delivery accepted", "Active Service", active["id"])
            add_reputation_event(state, active["buyer_agent_id"], 1.0, "Timely acceptance completed", "Active Service", active["id"])
            resolve_matching_inbox(
                state,
                "Active Service",
                active["id"],
                "Review Deliverable Evidence Package",
                actor,
                "Delivery evidence accepted and payment release processed.",
            )
        elif action == "dispute":
            active["status"] = "disputed"
            dispute = create_dispute(state, active["id"], "buyer", details or "Acceptance contested", "Acceptance decision opened dispute")
            created["dispute"] = dispute
        else:
            active["status"] = "revision_requested"
            add_inbox(state, "seller", "instruction_execution", "Resolve delivery acceptance issue", f"Buyer requested {action}: {details}", "Active Service", active["id"])
        created["delivery_acceptance"] = acceptance
        audit(
            state,
            actor,
            f"delivery.{action}",
            "Active Service",
            active["id"],
            f"Delivery decision: {action}",
            {
                "delivery_acceptance": acceptance,
                "evidence_packages": active["delivery"]["evidence_packages"],
                "contract": state["contracts"][active["contract_id"]],
                "payment_ledger": active.get("payment_ledger"),
                "playbook_rule": state["agents"][active["buyer_agent_id"]]["playbook"].get("acceptance_criteria"),
                "authority_check": {"result": "within_buying_playbook" if action != "dispute" else "dispute_opened", "rule": "Delivery Acceptance criteria"},
            },
        )
    elif action == "payment":
        payment_type = canonical_payment_type(args.payment_type)
        ensure_payment_lifecycle_ready(active, payment_type, bool(args.human_approved))
        authority_check = {
            "result": "human_approved_exception" if args.human_approved else "payment_lifecycle_passed",
            "rule": state["agents"][active["buyer_agent_id"]]["playbook"].get("payment_rules"),
            "human_approved": bool(args.human_approved),
            "actor": actor,
            "payment_type": payment_type,
            "exception_reason": details if args.human_approved else None,
            "evidence_present": active_has_evidence(active),
            "buyer_acceptance_present": active_has_buyer_acceptance(active),
        }
        payment = payment_for_active(state, active["id"], payment_type, details, authority_check)
        created["payment_event"] = payment
    elif action == "change-order":
        contract = state["contracts"][active["contract_id"]]
        change_order = {
            "id": next_id(state, "change"),
            "summary": details or "Change order requested",
            "scope_delta": details or "Change order requested",
            "price_change": float(args.price_change or 0),
            "timeline_change": args.timeline_change,
            "deliverable_delta": split_list(args.deliverable),
            "acceptance_evidence_delta": split_list(args.acceptance_mapping) or split_list(args.evidence_required),
            "payment_impact": {
                "price_change": float(args.price_change or 0),
                "currency": state["contracts"][active["contract_id"]]["commercial_terms"].get("currency", "USD"),
                "requires_ledger_update": bool(args.signed),
            },
            "signature_state": {
                "buyer": "signed" if args.signed else "pending",
                "seller": "signed" if args.signed else "pending",
                "provider": "Mock Signing Provider (provider choice open for production)",
            },
            "status": "signed" if args.signed else "awaiting_signature",
            "signing_provider": "Mock Signing Provider (provider choice open for production)",
            "created_at": now(),
        }
        active["change_orders"].append(change_order)
        created["change_order"] = change_order
        if args.signed:
            applied = apply_signed_change_order(state, active, change_order, actor, bool(args.human_approved), "direct-signed", as_human=as_human)
            created.update(applied)
            if applied.get("blocked"):
                created["change_order"] = change_order
                return output(
                    "Change Order was not applied because it exceeds Standing Authorization.",
                    {"active_service": active, **created},
                    [
                        "Resolve the authorization inbox item as the buyer-side human or lower the Change Order amount.",
                        "Paused agents still cannot initiate contract or payment changes.",
                    ],
                )
            resolve_matching_inbox(
                state,
                "Active Service",
                active["id"],
                "Approve Change Order",
                actor,
                f"Change Order {change_order['id']} signed and applied to contract/payment terms.",
            )
        else:
            add_inbox(state, "both", "authorization", "Approve Change Order", change_order["summary"], "Active Service", active["id"], urgency="high")
        audit(
            state,
            actor,
            "change_order.created",
            "Active Service",
            active["id"],
            change_order["summary"],
            {
                "change_order": change_order,
                "contract": contract,
                "payment_ledger": active.get("payment_ledger"),
                "playbook_rule": "Change Orders are signed Service Contract/SOW amendments.",
                "authority_check": {"result": "signed" if args.signed else "pending_authorization", "rule": "Change Order signature/approval required"},
            },
        )
    elif action == "meeting":
        meeting = {
            "id": next_id(state, "meeting"),
            "mode": args.meeting_mode or "video",
            "purpose": details or "Human-to-Human Meeting",
            "requested_by": actor,
            "prep": "Agent prep: summarize context, goals, risks, open decisions, and recommended asks before the meeting.",
            "follow_up": "Agent follow-up: capture outcomes, update tasks, send contract/change-order/dispute actions if needed.",
            "status": "scheduled",
            "urgency": getattr(args, "urgency", None) or "normal",
            "created_at": now(),
        }
        active["meetings"].append(meeting)
        created["human_to_human_meeting"] = meeting
        add_inbox(state, "both", "meeting", "Prepare for Human-to-Human Meeting", meeting["purpose"], "Active Service", active["id"], urgency=getattr(args, "urgency", None) or "normal")
        audit(state, actor, "meeting.scheduled", "Active Service", active["id"], meeting["purpose"], meeting)
    elif action == "message":
        message = {"id": next_id(state, "msg"), "from": actor, "body": details, "timestamp": now()}
        active["messages"].append(message)
        created["message"] = message
        audit(state, actor, "message.sent", "Active Service", active["id"], details, message)
    else:
        raise ValueError(f"Unsupported Active Service action: {action}")
    return output(
        f"Applied Active Service action {action} to {active['id']}.",
        {"active_service": active, **created},
        [
            "Inspect the Marketplace Inbox for new requests.",
            "Continue delivery, acceptance, payment, meeting, change-order, or dispute work as needed.",
            "Ask for an Audit Log or Decision Explanation if the human wants to understand what changed.",
        ],
    )


def command_propose_meeting(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    proposal = state["proposals"].get(args.proposal_id)
    if not proposal:
        raise ValueError(f"Unknown Proposal: {args.proposal_id}")
    actor = args.actor or "Belong Agent"
    meeting = {
        "id": next_id(state, "meeting"),
        "mode": args.meeting_mode or "video",
        "purpose": args.details or "Pre-contract Human-to-Human Meeting",
        "requested_by": actor,
        "stage": "pre_contract",
        "prep": "Agent prep: summarize context, goals, risks, open decisions, and recommended asks before the meeting.",
        "follow_up": "Agent follow-up: capture outcomes, update the proposal/negotiation, and send next steps if needed.",
        "status": "scheduled",
        "urgency": getattr(args, "urgency", None) or "normal",
        "created_at": now(),
    }
    proposal.setdefault("meetings", []).append(meeting)
    add_inbox(state, "both", "meeting", "Prepare for Human-to-Human Meeting", meeting["purpose"], "Proposal", args.proposal_id, urgency=getattr(args, "urgency", None) or "normal")
    audit(state, actor, "meeting.scheduled", "Proposal", args.proposal_id, meeting["purpose"], meeting)
    return output(
        f"Scheduled pre-contract Human-to-Human Meeting on proposal {args.proposal_id}.",
        {"human_to_human_meeting": meeting, "proposal": proposal},
        [
            "Acceptance always shares the human's Calendly link; the proposing agent books a slot that fits both humans' calendars.",
            "Booking auto-creates the video join link; record time, timezone, and link in the meeting purpose/details.",
            "Escalate through belong-inbox if scheduling would exceed the playbook's meeting authority.",
        ],
    )


def payment_for_active(
    state: dict[str, Any],
    active_service_id: str,
    payment_type: str,
    notes: str = "",
    authority_check: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active = get_active(state, active_service_id)
    contract = state["contracts"][active["contract_id"]]
    active.setdefault("payment_ledger", payment_ledger_for_contract(contract))
    ledger = active["payment_ledger"]
    schedule = ledger["payment_schedule"]
    if payment_type == "authorization":
        amount = ledger["contract_amount"]
    elif payment_type in {"release", "collection"}:
        amount = max(0.0, float(schedule.get("acceptance_due", 0)) or (ledger["contract_amount"] - ledger["released"]))
    elif payment_type == "refund":
        amount = max(0.0, ledger["collected"] - ledger["refunded"])
    elif payment_type == "hold":
        amount = max(0.0, ledger["contract_amount"] - ledger["held"])
    else:
        amount = max(0.0, ledger["contract_amount"] - ledger["charged"])
    return record_payment_event(state, active, payment_type, amount, notes, authority_check)


def create_dispute(state: dict[str, Any], active_service_id: str, opened_by: str, reason: str, evidence: str) -> dict[str, Any]:
    active = get_active(state, active_service_id)
    dispute_id = next_id(state, "dispute")
    dispute = {
        "id": dispute_id,
        "active_service_id": active_service_id,
        "opened_by": opened_by,
        "status": "agent_negotiation",
        "reason": reason,
        "evidence": split_list(evidence) or [evidence],
        "responses": [],
        "judge_decision": None,
        "human_judge_escalation": None,
        "created_at": now(),
    }
    state["disputes"][dispute_id] = dispute
    active["status"] = "disputed"
    add_inbox(state, "both", "dispute", "Respond to Dispute", reason, "Dispute", dispute_id, urgency="high")
    audit(state, opened_by, "dispute.opened", "Dispute", dispute_id, reason, dispute)
    return dispute


def command_dispute_open(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    dispute = create_dispute(state, args.active_service_id, args.opened_by, args.reason, args.evidence)
    return output(
        f"Opened Dispute {dispute['id']}.",
        {"dispute": dispute},
        [
            "Let agents negotiate or respond inside Playbooks.",
            "Run Belong Judge if agent negotiation cannot resolve the dispute.",
            "Escalate to a Belong human judge if the autonomous decision is unsatisfactory.",
        ],
    )


def command_dispute_respond(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    dispute = state["disputes"].get(args.dispute_id)
    if not dispute:
        raise ValueError(f"Unknown Dispute: {args.dispute_id}")
    response = {"actor": args.actor, "response": args.response, "timestamp": now()}
    dispute["responses"].append(response)
    resolve_matching_inbox(
        state,
        "Dispute",
        args.dispute_id,
        "Respond to Dispute",
        args.actor,
        "Dispute response recorded.",
    )
    audit(state, args.actor, "dispute.responded", "Dispute", args.dispute_id, args.response, response)
    return output(
        f"Recorded response on Dispute {args.dispute_id}.",
        {"dispute": dispute},
        ["Run Belong Judge, negotiate a settlement, or escalate to the human if authority is exceeded."],
    )


def command_judge(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    dispute = state["disputes"].get(args.dispute_id)
    if not dispute:
        raise ValueError(f"Unknown Dispute: {args.dispute_id}")
    if args.escalate_human:
        dispute["human_judge_escalation"] = {
            "status": "requested",
            "reason": args.reason or "Human requested Belong human judge review.",
            "timestamp": now(),
        }
        dispute["status"] = "human_judge_requested"
        audit(state, "Belong Judge", "dispute.escalated_human_judge", "Dispute", args.dispute_id, dispute["human_judge_escalation"]["reason"], dispute)
        return output(
            f"Escalated Dispute {args.dispute_id} to a Belong human judge.",
            {"dispute": dispute},
            ["Keep evidence and payment holds visible in the inbox until the human judge outcome is mocked."],
        )
    decision = {
        "status": "decided",
        "decision": args.decision or "partial_credit_to_buyer_revision_required",
        "rationale": "Mocked autonomous Belong Judge reviewed the executed contract/SOW version, evidence packages, acceptance criteria, payment ledger, messages, dispute responses, and reputation history.",
        "timestamp": now(),
    }
    dispute["judge_decision"] = decision
    dispute["status"] = "judge_decided"
    active = get_active(state, dispute["active_service_id"])
    add_reputation_event(state, active["buyer_agent_id"], -0.5, "Dispute required Belong Judge review", "Dispute", args.dispute_id)
    add_reputation_event(state, active["selling_agent_id"], -1.0, "Dispute outcome affected delivery trust", "Dispute", args.dispute_id)
    audit(
        state,
        "Belong Judge",
        "dispute.judge_decision",
        "Dispute",
        args.dispute_id,
        decision["decision"],
        {
            "judge_decision": decision,
            "active_service": active,
            "contract": state["contracts"].get(active.get("contract_id")),
            "payment_ledger": active.get("payment_ledger"),
            "evidence_packages": active.get("delivery", {}).get("evidence_packages", []),
            "dispute_responses": dispute.get("responses", []),
            "playbook_rule": "Belong Judge reviews dispute evidence after agents cannot resolve contested delivery, payment, contract compliance, acceptance, evidence, or conduct.",
            "authority_check": {"result": "belong_judge_autonomous_decision", "rule": "first-layer Belong Judge"},
        },
    )
    resolve_matching_inbox(
        state,
        "Dispute",
        args.dispute_id,
        "Respond to Dispute",
        "Belong Judge",
        "Belong Judge decision issued after dispute response window.",
    )
    add_inbox(state, "both", "authorization", "Review Belong Judge decision", decision["decision"], "Dispute", args.dispute_id, urgency="high")
    return output(
        f"Belong Judge issued a mocked autonomous decision for {args.dispute_id}.",
        {"dispute": dispute, "judge_decision": decision},
        [
            "Accept the Judge decision, negotiate settlement, or escalate to a Belong human judge.",
            "Review reputation impact.",
            "Inspect the audit trail for the evidence used in the decision.",
        ],
    )


def command_inbox(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    items = list(state["inbox"].values())
    if args.owner_role != "all":
        items = [item for item in items if item["owner_role"] in {args.owner_role, "both"}]
    if args.status != "all":
        items = [item for item in items if item["status"] == args.status]
    items.sort(key=lambda item: item["created_at"])
    return output(
        f"Found {len(items)} Marketplace Inbox item(s).",
        {"inbox": items},
        [
            "Resolve information, authorization, instruction/execution, fulfillment, meeting, dispute, payment exception, Change Order, pause/resume, or operational intervention requests.",
            "Notifications are mocked as reminders to return to the agentic application and open this inbox.",
            "Agents should resolve what they can autonomously and escalate only when their Playbook or Standing Authorization requires it.",
        ],
    )


def command_resolve_inbox(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    item = state["inbox"].get(args.item_id)
    if not item:
        raise ValueError(f"Unknown Inbox item: {args.item_id}")
    item["status"] = "resolved"
    item["updated_at"] = now()
    item["resolution"] = {
        "decision": args.decision,
        "notes": args.notes,
        "actor": args.actor,
        "timestamp": now(),
    }
    linked_type = item.get("linked_object_type")
    linked_id = item.get("linked_object_id")
    resolution_details: dict[str, Any] = {
        "inbox_item": item,
        "playbook_rule": "Marketplace Inbox resolution applies day-to-day human information, authorization, instruction, fulfillment, meeting, dispute, payment exception, Change Order, pause/resume, or operational intervention decisions.",
        "authority_check": {"result": "resolved", "rule": item.get("request_type")},
    }
    if linked_type == "Active Service" and linked_id in state["active_services"]:
        active = state["active_services"][linked_id]
        resolution_details["active_service"] = active
        if item["title"] == "Complete Fulfillment Task":
            for task in active["delivery"].get("tasks", []):
                if task.get("status") == "open" and (task.get("action") == item.get("summary") or not args.notes):
                    task["status"] = "completed"
                    task["completed_at"] = now()
                    task["completion_notes"] = args.notes
                    break
        elif item["title"] == "Prepare for Human-to-Human Meeting":
            for meeting in reversed(active.get("meetings", [])):
                if meeting.get("status") == "scheduled":
                    meeting["status"] = "prepared"
                    meeting["prep_completed_at"] = now()
                    meeting["prep_notes"] = args.notes
                    meeting["follow_up_status"] = "pending_after_meeting"
                    resolution_details["meeting"] = meeting
                    break
        elif item["title"] == "Approve Change Order" and args.decision.lower() in {"approve", "approved", "sign", "signed"}:
            for change_order in reversed(active.get("change_orders", [])):
                if change_order.get("status") == "awaiting_signature":
                    applied = apply_signed_change_order(state, active, change_order, args.actor, True, f"inbox:{args.item_id}")
                    resolution_details.update(applied)
                    resolution_details["playbook_rule"] = "Human approved a Change Order as a signed Service Contract/SOW amendment."
                    resolution_details["authority_check"] = applied.get("authority_check")
                    break
    elif linked_type == "Dispute" and linked_id in state["disputes"]:
        dispute = state["disputes"][linked_id]
        if item["title"] == "Respond to Dispute":
            dispute["responses"].append({"actor": args.actor, "response": args.notes or args.decision, "timestamp": now(), "source": "inbox_resolution"})
        elif item["title"] == "Review Belong Judge decision":
            dispute["judge_review_resolution"] = {"decision": args.decision, "notes": args.notes, "actor": args.actor, "timestamp": now()}
        resolution_details["dispute"] = dispute
    audit(state, args.actor, "inbox.resolved", "Marketplace Inbox", args.item_id, f"Resolved inbox item with {args.decision}", resolution_details)
    return output(
        f"Resolved Inbox item {args.item_id}.",
        {"inbox_item": item},
        [
            "Continue the linked marketplace flow.",
            "Ask for status to see remaining pending work.",
            "Review audit if this approval or instruction changed agent behavior.",
        ],
    )


def command_override(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    agent = state["agents"].get(args.agent_id)
    if not agent:
        raise ValueError(f"Unknown agent: {args.agent_id}")
    if args.action == "pause":
        agent["paused"] = True
        agent["status"] = "paused"
        if agent.get("type") == "Selling Agent" and agent.get("service_id") in state["services"]:
            state["services"][agent["service_id"]]["status"] = "paused"
            resolve_matching_inbox(
                state,
                "Service",
                agent["service_id"],
                "Selling Agent ready for marketplace",
                args.actor,
                "Selling Agent was paused, so the Service is no longer ready for marketplace engagement.",
            )
    elif args.action == "resume":
        agent["paused"] = False
        agent["status"] = "production"
        if agent.get("type") == "Selling Agent" and agent.get("service_id") in state["services"]:
            state["services"][agent["service_id"]]["status"] = "listed"
    elif args.action == "intervene" and getattr(args, "flow_id", None):
        flow, flow_type = find_flow(state, args.flow_id)
        previous = set_flow_control(
            state,
            flow,
            flow_type,
            "human_controlled",
            args.actor,
            "intervene",
            args.details or f"Human intervened to take manual control of {flow_type} {flow['id']}.",
        )
        skill = "belong-operate-buying-flow" if flow_type == "Buying Request" else "belong-operate-selling-flow"
        return output(
            f"Human intervened on {flow_type} {flow['id']}; control is now human_controlled (was {previous}).",
            {"flow": flow},
            [
                f"Use {skill} to perform actions on this flow with --as-human.",
                "Use flow-control --action release to hand the flow back to the agent when done.",
                "Per-flow control does not change the agent-wide pause; other flows are unaffected.",
            ],
        )
    else:
        agent.setdefault("human_overrides", []).append({"action": args.action, "details": args.details, "timestamp": now()})
    audit(
        state,
        args.actor,
        f"human_override.{args.action}",
        "Belong Agent",
        args.agent_id,
        args.details or args.action,
        {
            "agent": agent,
            "playbook_rule": "Human Override can pause/resume agents or provide operational direct instructions. Durable Playbook changes happen through training/retraining skills.",
            "authority_check": {"result": "human_override_logged", "rule": args.action},
        },
    )
    return output(
        f"Applied human override {args.action} to {args.agent_id}.",
        {"agent": agent},
        [
            "Paused agents stop new autonomous actions but preserve obligations, deadlines, disputes, and notices.",
            "Use belong-train-buying-agent or belong-train-selling-agent for durable Playbook changes.",
            "Inspect audit and inbox for downstream effects.",
        ],
    )


FLOW_CONTROL_TRANSITIONS = {
    "take": "human_controlled",
    "release": "agent_controlled",
    "pause": "paused",
    "resume": "agent_controlled",
}


def find_flow(state: dict[str, Any], flow_id: str) -> tuple[dict[str, Any], str]:
    if flow_id in state.get("buying_requests", {}):
        return state["buying_requests"][flow_id], "Buying Request"
    if flow_id in state.get("active_services", {}):
        return state["active_services"][flow_id], "Active Service"
    raise ValueError(f"Unknown flow: {flow_id}. Provide a Buying Request or Active Service id.")


def set_flow_control(
    state: dict[str, Any],
    flow: dict[str, Any],
    flow_type: str,
    new_state: str,
    actor: str,
    event_label: str,
    details: str = "",
) -> str:
    previous = flow.get("control_state", "agent_controlled")
    flow["control_state"] = new_state
    summary = details or f"{flow_type} {flow['id']} control changed from {previous} to {new_state}."
    audit(
        state,
        actor,
        f"flow_control.{event_label}",
        flow_type,
        flow["id"],
        summary,
        {"previous_control_state": previous, "control_state": new_state},
    )
    add_inbox(
        state,
        "both",
        "operational_intervention",
        f"{flow_type} {flow['id']} is now {new_state}",
        summary,
        flow_type,
        flow["id"],
    )
    return previous


def command_flow_control(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    flow, flow_type = find_flow(state, args.flow_id)
    new_state = FLOW_CONTROL_TRANSITIONS[args.action]
    previous = set_flow_control(state, flow, flow_type, new_state, args.actor, args.action, args.details)
    hints = {
        "human_controlled": "The agent will not act on this flow; the human drives it directly. Use flow-control --action release to return it to the agent.",
        "agent_controlled": "The agent resumes autonomous work on this flow.",
        "paused": "The flow is frozen; nobody acts until it is resumed. Obligations, deadlines, disputes, and notices remain visible in the inbox.",
    }
    return output(
        f"Flow {flow['id']} ({flow_type}) control set to {new_state} (was {previous}).",
        {"flow": flow},
        [
            hints[new_state],
            "Per-flow control does not change the agent-wide pause; other flows are unaffected.",
            "Inspect audit and inbox for downstream effects.",
        ],
    )


def command_reputation(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    agents = [
        {
            "agent_id": agent_id,
            "name": agent["name"],
            "type": agent["type"],
            "score": agent.get("reputation", {}).get("score"),
            "events": [state["reputation_events"][event_id] for event_id in agent.get("reputation", {}).get("events", []) if event_id in state["reputation_events"]],
        }
        for agent_id, agent in state["agents"].items()
    ]
    return output(
        f"Loaded reputation for {len(agents)} agent(s).",
        {"agents": agents},
        [
            "Use ratings after delivery, dispute, or cancellation outcomes.",
            "Selling Agent reputation affects search, engagement, and buyer trust.",
            "Reputation is agent-level because all marketplace interactions happen through Belong agents.",
        ],
    )


def command_rate(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    delta = max(-5, min(5, float(args.score) - 3))
    event = add_reputation_event(state, args.agent_id, delta, f"Human rating {args.score}/5: {args.notes}", args.linked_object_type, args.linked_object_id)
    return output(
        f"Recorded rating for {args.agent_id}.",
        {"reputation_event": event, "agent": state["agents"][args.agent_id]},
        ["Review search ranking impact and audit history."],
    )


def command_audit(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    events = list(state["audit"].values())
    if args.object_id:
        events = [event for event in events if event["object_id"] == args.object_id]
    events.sort(key=lambda event: event["timestamp"])
    events = events[-args.limit :]
    return output(
        f"Loaded {len(events)} Audit Log event(s).",
        {"audit": events},
        [
            "Use explain for a Decision Explanation grounded in audit evidence.",
            "Audit should include identities, timestamps, instructions, Playbook versions, authority checks, decisions, messages, contracts, payments, evidence, acceptance, disputes, Judge decisions, and reputation changes.",
        ],
    )


def command_explain(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    event = state["audit"].get(args.audit_id)
    if not event:
        raise ValueError(f"Unknown Audit event: {args.audit_id}")
    related: dict[str, Any] = {}
    object_type = event.get("object_type")
    object_id = event.get("object_id")
    if object_type == "Active Service" and object_id in state["active_services"]:
        active = state["active_services"][object_id]
        related = {
            "active_service": active,
            "contract": state["contracts"].get(active.get("contract_id")),
            "payment_ledger": active.get("payment_ledger"),
            "buyer_agent_playbook_version": state["agents"].get(active.get("buyer_agent_id"), {}).get("playbook_version"),
            "selling_agent_playbook_version": state["agents"].get(active.get("selling_agent_id"), {}).get("playbook_version"),
        }
    elif object_type == "Proposal" and object_id in state["proposals"]:
        proposal = state["proposals"][object_id]
        related = {
            "proposal": proposal,
            "contract": state["contracts"].get(proposal.get("contract_id")),
            "selling_agent": state["agents"].get(proposal.get("selling_agent_id")),
        }
    elif object_type == "Dispute" and object_id in state["disputes"]:
        dispute = state["disputes"][object_id]
        active = state["active_services"].get(dispute.get("active_service_id"))
        related = {"dispute": dispute, "active_service": active}
        if active:
            related["contract"] = state["contracts"].get(active.get("contract_id"))
            related["payment_ledger"] = active.get("payment_ledger")
            related["buyer_agent_playbook_version"] = state["agents"].get(active.get("buyer_agent_id"), {}).get("playbook_version")
            related["selling_agent_playbook_version"] = state["agents"].get(active.get("selling_agent_id"), {}).get("playbook_version")
    elif object_type == "Buying Request" and object_id in state["buying_requests"]:
        request = state["buying_requests"][object_id]
        related = {"buying_request": request, "buying_agent": state["agents"].get(request.get("buying_agent_id"))}
    elif object_type == "Marketplace Inbox" and object_id in state["inbox"]:
        inbox_item = state["inbox"][object_id]
        related = {"inbox_item": inbox_item}
        linked_type = inbox_item.get("linked_object_type")
        linked_id = inbox_item.get("linked_object_id")
        if linked_type == "Active Service" and linked_id in state["active_services"]:
            active = state["active_services"][linked_id]
            related.update(
                {
                    "active_service": active,
                    "contract": state["contracts"].get(active.get("contract_id")),
                    "payment_ledger": active.get("payment_ledger"),
                    "buyer_agent_playbook_version": state["agents"].get(active.get("buyer_agent_id"), {}).get("playbook_version"),
                    "selling_agent_playbook_version": state["agents"].get(active.get("selling_agent_id"), {}).get("playbook_version"),
                }
            )
        elif linked_type == "Dispute" and linked_id in state["disputes"]:
            dispute = state["disputes"][linked_id]
            active = state["active_services"].get(dispute.get("active_service_id"))
            related.update({"dispute": dispute, "active_service": active})
            if active:
                related["contract"] = state["contracts"].get(active.get("contract_id"))
                related["payment_ledger"] = active.get("payment_ledger")
                related["buyer_agent_playbook_version"] = state["agents"].get(active.get("buyer_agent_id"), {}).get("playbook_version")
                related["selling_agent_playbook_version"] = state["agents"].get(active.get("selling_agent_id"), {}).get("playbook_version")
        elif linked_type == "Belong Agent" and linked_id in state["agents"]:
            agent = state["agents"][linked_id]
            related["agent"] = agent
            related["linked_agent_playbook_version"] = agent.get("playbook_version")
    details = event.get("details", {})
    explanation = {
        "audit_id": args.audit_id,
        "instruction_or_event": event["summary"],
        "timestamp": event["timestamp"],
        "actor": event["actor"],
        "object": {"type": object_type, "id": object_id},
        "playbook_version": details.get("playbook_version") or related.get("buyer_agent_playbook_version") or related.get("selling_agent_playbook_version") or related.get("linked_agent_playbook_version"),
        "relevant_playbook_rule": details.get("playbook_rule", "See linked Playbook and Standing Authorization for this object."),
        "authority_check": details.get("authority_check", "Mocked authority check recorded when applicable."),
        "contract_or_payment_evidence": {
            "contract": details.get("contract") or related.get("contract"),
            "payment_ledger": details.get("payment_ledger") or related.get("payment_ledger"),
        },
        "marketplace_evidence": details,
        "linked_objects": related,
        "outcome": event["event_type"],
        "raw_model_reasoning_exposed": False,
    }
    return output(
        f"Decision Explanation for {args.audit_id}.",
        {"decision_explanation": explanation},
        ["Use the explanation to decide whether to approve, override, pause, dispute, steer temporarily, or retrain through a training skill."],
    )


def command_optimization(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    agent = state["agents"].get(args.agent_id)
    if not agent:
        raise ValueError(f"Unknown agent: {args.agent_id}")
    ensure_agent_can_act(agent, "optimization recommendation")
    if agent["type"] == "Buying Agent":
        recommendation = {
            "type": "Provider Optimization",
            "summary": "Run a new semantic search/RFP for better price, higher reputation, or complementary Services.",
            "signals": ["accepted delivery", "price benchmark", "reputation trend", "new matching Services"],
        }
    else:
        recommendation = {
            "type": "Selling Optimization",
            "summary": "Improve pricing, discovery questions, scope packaging, contract terms, or offer positioning based on marketplace outcomes.",
            "signals": ["search impressions", "won/lost proposals", "negotiation patterns", "delivery outcomes", "buyer feedback"],
        }
    recommendation_id = next_id(state, "training_rec")
    state["training_recommendations"][recommendation_id] = {
        "id": recommendation_id,
        "agent_id": args.agent_id,
        "status": "pending_training_review",
        "recommendation": recommendation,
        "created_at": now(),
    }
    audit(state, agent["name"], "optimization.recommended", "Belong Agent", args.agent_id, recommendation["summary"], recommendation)
    return output(
        f"Created {recommendation['type']} recommendation for {args.agent_id}.",
        {"training_recommendation": state["training_recommendations"][recommendation_id]},
        [
            "Review and apply durable behavior changes through the relevant training skill.",
            "Provider Optimization can execute or escalate depending on Buying Agent autonomy.",
            "Selling Optimization should improve conversion and revenue while preserving authority limits.",
        ],
    )


def command_payments(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    payments = list(state["payments"].values())
    if args.active_service_id:
        if args.active_service_id not in state["active_services"]:
            raise ValueError(f"Unknown Active Service: {args.active_service_id}")
        payments = [payment for payment in payments if payment.get("active_service_id") == args.active_service_id]
    if args.owner_role != "all":
        filtered = []
        for payment in payments:
            active = state["active_services"].get(payment.get("active_service_id"))
            if not active:
                continue
            if args.owner_role == "buyer" and active.get("buyer_agent_id") in state["agents"]:
                filtered.append(payment)
            elif args.owner_role == "seller" and active.get("selling_agent_id") in state["agents"]:
                filtered.append(payment)
        payments = filtered
    ledgers = {
        active_id: active.get("payment_ledger")
        for active_id, active in state["active_services"].items()
        if active.get("payment_ledger") and (not args.active_service_id or active_id == args.active_service_id)
    }
    totals = {
        "authorized": round(sum(float(ledger.get("authorized", 0)) for ledger in ledgers.values()), 2),
        "charged": round(sum(float(ledger.get("charged", 0)) for ledger in ledgers.values()), 2),
        "held": round(sum(float(ledger.get("held", 0)) for ledger in ledgers.values()), 2),
        "released": round(sum(float(ledger.get("released", 0)) for ledger in ledgers.values()), 2),
        "refunded": round(sum(float(ledger.get("refunded", 0)) for ledger in ledgers.values()), 2),
        "collected": round(sum(float(ledger.get("collected", 0)) for ledger in ledgers.values()), 2),
        "platform_fee_accrued": round(sum(float(ledger.get("platform_fee_accrued", 0)) for ledger in ledgers.values()), 2),
        "seller_net_accrued": round(sum(float(ledger.get("seller_net_accrued", 0)) for ledger in ledgers.values()), 2),
    }
    bank_readiness = [
        {
            "organization_id": org_id,
            "organization_name": org.get("name"),
            "payment_setup": org.get("payment_setup", "mocked_ready"),
            "legal_setup": org.get("legal_setup", "mocked_ready"),
            "provider": "Stripe Payment Stack mock",
        }
        for org_id, org in state["organizations"].items()
    ]
    return output(
        f"Found {len(payments)} payment transaction(s).",
        {"payments": payments, "payment_ledgers": ledgers, "totals": totals, "bank_readiness": bank_readiness},
        [
            "This is a read/check view; payment movement happens through agent authority or Inbox approval.",
            "Use belong-inbox for payment exceptions and belong-check-active-services for linked delivery obligations.",
        ],
    )


def command_active_services(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    active_services = list(state["active_services"].values())
    if args.owner_role == "buyer":
        active_services = [active for active in active_services if active.get("buyer_agent_id") in state["agents"]]
    elif args.owner_role == "seller":
        active_services = [active for active in active_services if active.get("selling_agent_id") in state["agents"]]
    if args.status == "active":
        active_services = [active for active in active_services if active.get("status") not in {"accepted", "completed", "cancelled"}]
    elif args.status == "completed":
        active_services = [active for active in active_services if active.get("status") in {"accepted", "completed", "cancelled"}]
    summaries = []
    for active in active_services:
        linked_inbox = [
            item
            for item in state["inbox"].values()
            if item.get("linked_object_type") == "Active Service" and item.get("linked_object_id") == active["id"] and item.get("status") == "pending"
        ]
        linked_disputes = [dispute for dispute in state["disputes"].values() if dispute.get("active_service_id") == active["id"]]
        contract = state["contracts"].get(active.get("contract_id"), {})
        summaries.append(
            {
                "active_service": active,
                "contract_status": contract.get("status"),
                "obligations": contract.get("obligations", []),
                "pending_inbox_items": linked_inbox,
                "disputes": linked_disputes,
                "delivery_summary": {
                    "tasks": len(active.get("delivery", {}).get("tasks", [])),
                    "evidence_packages": len(active.get("delivery", {}).get("evidence_packages", [])),
                    "acceptance_events": len(active.get("delivery", {}).get("acceptance", [])),
                    "meetings": len(active.get("meetings", [])),
                    "change_orders": len(active.get("change_orders", [])),
                },
                "payment_ledger": active.get("payment_ledger"),
            }
        )
    return output(
        f"Found {len(summaries)} Active Service(s).",
        {"active_services": summaries},
        [
            "This is a read/check view; operational intervention goes through belong-inbox.",
            "Use belong-steer-buying-agent or belong-steer-selling-agent for temporary guidance and training skills for durable Playbook changes.",
        ],
    )


def request_has_active_service(state: dict[str, Any], request_id: str) -> bool:
    return any(active.get("buying_request_id") == request_id for active in state["active_services"].values())


def proposal_stage(state: dict[str, Any], proposal: dict[str, Any]) -> str:
    if proposal.get("status") == "signed_executed" or any(active.get("proposal_id") == proposal["id"] for active in state["active_services"].values()):
        return "signed"
    if proposal.get("status") == "seller_signed_revised_waiting_buyer_signature":
        return "negotiating"
    return "proposed"


def command_buying_requests(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    buyer_agent_id = best_buying_agent(state, args.buyer_agent_id)
    requests = [
        request
        for request in state["buying_requests"].values()
        if request.get("buying_agent_id") == buyer_agent_id and request.get("mode") != "composite"
    ]
    if args.status == "open":
        requests = [request for request in requests if not request_has_active_service(state, request["id"])]
    elif args.status == "signed":
        requests = [request for request in requests if request_has_active_service(state, request["id"])]
    summaries = []
    for request in requests:
        feeds = [state["engagement_feeds"][feed_id] for feed_id in request.get("engagement_feeds", []) if feed_id in state["engagement_feeds"]]
        proposals = [proposal for proposal in state["proposals"].values() if proposal.get("buying_request_id") == request["id"]]
        pending_inbox = [
            item
            for item in state["inbox"].values()
            if item.get("status") == "pending"
            and (
                item.get("linked_object_id") == request["id"]
                or item.get("linked_object_id") in {feed["id"] for feed in feeds}
                or item.get("linked_object_id") in {proposal["id"] for proposal in proposals}
            )
        ]
        summaries.append(
            {
                "buying_request": request,
                "search_results": request.get("search_results", []),
                "engagement_feeds": feeds,
                "discovery_questionnaires": [
                    questionnaire
                    for questionnaire in state["discovery_questionnaires"].values()
                    if questionnaire.get("feed_id") in {feed["id"] for feed in feeds}
                ],
                "proposals": [
                    {
                        "proposal": proposal,
                        "contract": state["contracts"].get(proposal.get("contract_id")),
                        "stage": proposal_stage(state, proposal),
                    }
                    for proposal in proposals
                ],
                "active_services": [
                    active
                    for active in state["active_services"].values()
                    if active.get("buying_request_id") == request["id"]
                ],
                "pending_inbox_items": pending_inbox,
            }
        )
    return output(
        f"Found {len(summaries)} Buying Request(s) for {buyer_agent_id}.",
        {"buying_requests": summaries},
        [
            "This is a read/check view of the buyer pre-contract pipeline.",
            "Use belong-start-buying-request for new buyer intent, belong-inbox for escalations, and belong-steer-buying-agent for temporary guidance.",
        ],
    )


def command_selling_pipeline(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    seller_agent = state["agents"].get(args.seller_agent_id)
    if not seller_agent:
        raise ValueError(f"Unknown Selling Agent: {args.seller_agent_id}")
    if seller_agent.get("type") != "Selling Agent":
        raise ValueError(f"{args.seller_agent_id} is not a Selling Agent.")
    service_ids = [service_id for service_id, service in state["services"].items() if service.get("selling_agent_id") == args.seller_agent_id]
    if args.service_id:
        if args.service_id not in state["services"]:
            raise ValueError(f"Unknown Service: {args.service_id}")
        if args.service_id not in service_ids:
            raise ValueError(f"Service {args.service_id} is not represented by {args.seller_agent_id}.")
        service_ids = [args.service_id]
    rows = []
    for service_id in service_ids:
        service = state["services"][service_id]
        feeds = [feed for feed in state["engagement_feeds"].values() if service_id in feed.get("service_ids", [])]
        proposals = [proposal for proposal in state["proposals"].values() if proposal.get("service_id") == service_id and proposal.get("selling_agent_id") == args.seller_agent_id]
        stages = {proposal_stage(state, proposal) for proposal in proposals}
        has_open_feed = any(feed.get("status") in {"discovery", "discovery_answered", "proposals_received"} for feed in feeds)
        stage = "signed" if "signed" in stages else "negotiating" if "negotiating" in stages else "proposed" if proposals else "open" if has_open_feed else "open"
        if args.status != "all" and stage != args.status:
            continue
        linked_ids = {service_id, *[feed["id"] for feed in feeds], *[proposal["id"] for proposal in proposals]}
        pending_inbox = [
            item
            for item in state["inbox"].values()
            if item.get("status") == "pending" and item.get("linked_object_id") in linked_ids
        ]
        rows.append(
            {
                "service": service,
                "stage": stage,
                "engagement_feeds": feeds,
                "discovery_questionnaires": [
                    questionnaire
                    for questionnaire in state["discovery_questionnaires"].values()
                    if questionnaire.get("feed_id") in {feed["id"] for feed in feeds}
                ],
                "proposals": [
                    {
                        "proposal": proposal,
                        "contract": state["contracts"].get(proposal.get("contract_id")),
                        "stage": proposal_stage(state, proposal),
                    }
                    for proposal in proposals
                ],
                "active_services": [
                    active
                    for active in state["active_services"].values()
                    if active.get("selling_agent_id") == args.seller_agent_id and active.get("proposal_id") in {proposal["id"] for proposal in proposals}
                ],
                "billing_readiness": service.get("price_signal"),
                "pending_inbox_items": pending_inbox,
            }
        )
    return output(
        f"Found {len(rows)} Selling Pipeline item(s) for {args.seller_agent_id}.",
        {"selling_pipeline": rows},
        [
            "This is a read/check view of seller inbound work before Active Service.",
            "Use belong-inbox for seller escalations, belong-steer-selling-agent for temporary guidance, and belong-train-selling-agent for durable Service Playbook changes.",
        ],
    )


def latest_request_for_buying_agent(state: dict[str, Any], buyer_agent_id: str, request_id: str | None) -> dict[str, Any] | None:
    if request_id:
        request = state["buying_requests"].get(request_id)
        if not request:
            raise ValueError(f"Unknown Buying Request: {request_id}")
        if request.get("buying_agent_id") != buyer_agent_id:
            raise ValueError(f"Buying Request {request_id} does not belong to {buyer_agent_id}.")
        return request
    requests = [
        request
        for request in state["buying_requests"].values()
        if request.get("buying_agent_id") == buyer_agent_id and not request_has_active_service(state, request["id"])
    ]
    return requests[-1] if requests else None


def latest_active_for_agent(state: dict[str, Any], agent_id: str, role_key: str, active_service_id: str | None) -> dict[str, Any] | None:
    if active_service_id:
        active = get_active(state, active_service_id)
        if active.get(role_key) != agent_id:
            raise ValueError(f"Active Service {active_service_id} is not linked to {agent_id}.")
        return active
    active_services = [
        active
        for active in state["active_services"].values()
        if active.get(role_key) == agent_id and active.get("status") not in {"completed", "cancelled"}
    ]
    return active_services[-1] if active_services else None


def proposal_ids_for_request(state: dict[str, Any], request_id: str) -> list[str]:
    return [
        proposal["id"]
        for proposal in state["proposals"].values()
        if proposal.get("buying_request_id") == request_id
        and proposal.get("status") in {"seller_signed_waiting_buyer_signature", "seller_signed_revised_waiting_buyer_signature"}
    ]


def preferred_proposal_id(state: dict[str, Any], request_id: str) -> str | None:
    comparison = command_compare_proposals(argparse.Namespace(request_id=request_id), state)["objects"]["comparison"]
    if not comparison:
        return None
    shortlisted = [item for item in comparison if item.get("recommendation") == "shortlist"]
    candidate = (shortlisted or comparison)[0]
    return candidate["proposal_id"]


def command_run_buying_agent(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    buyer_agent_id = best_buying_agent(state, args.buyer_agent_id)
    buyer_agent = state["agents"][buyer_agent_id]
    ensure_agent_can_act(buyer_agent, "Buying Agent autonomous work")

    if args.mode == "optimization":
        return command_optimization(argparse.Namespace(agent_id=buyer_agent_id), state)

    if args.mode == "composite":
        active_ids = args.active_service_ids
        if not active_ids:
            active_ids = ",".join(
                active["id"]
                for active in state["active_services"].values()
                if active.get("buyer_agent_id") == buyer_agent_id
            )
        if not active_ids:
            raise ValueError("Composite Buying Request needs at least one Active Service or --active-service-ids.")
        return command_composite(
            argparse.Namespace(
                buyer_agent_id=buyer_agent_id,
                goal=args.goal or "Coordinate multiple Services under one buyer goal.",
                budget=args.budget or "0",
                timeline=args.timeline or "",
                constraints=args.constraints or "",
                active_service_ids=active_ids,
                dependencies=args.dependencies or "",
                sequencing=args.sequencing or "",
                shared_context=args.shared_context or "",
                risks=args.risks or "",
                handoffs=args.handoffs or "",
                acceptance=args.acceptance or "",
                escalation=args.escalation or "Escalate cross-service blockers to the buyer-side human.",
            ),
            state,
        )

    if args.mode == "active-service" or args.active_service_id:
        active = latest_active_for_agent(state, buyer_agent_id, "buyer_agent_id", args.active_service_id)
        if not active:
            return output(
                "No buyer-side Active Service is ready for the Buying Agent.",
                {"agent": buyer_agent},
                [
                    "Use belong-check-buying-requests for pre-contract pipeline.",
                    "Use belong-start-buying-request to create new buyer demand.",
                ],
            )
        if active_has_evidence(active) and not active_has_buyer_acceptance(active):
            return command_active_action(
                argparse.Namespace(
                    active_service_id=active["id"],
                    action="accept",
                    actor="Buying Agent",
                    details=args.details or "Buying Agent accepted deliverable evidence against SOW acceptance criteria.",
                    owner=None,
                    due=None,
                    context=None,
                    evidence_required=None,
                    files=None,
                    links=None,
                    acceptance_mapping=None,
                    deliverable=None,
                    payment_type=None,
                    price_change=None,
                    timeline_change=None,
                    signed=False,
                    human_approved=False,
                    meeting_mode=None,
                ),
                state,
            )
        if active_has_buyer_acceptance(active):
            return command_optimization(argparse.Namespace(agent_id=buyer_agent_id), state)
        return output(
            f"Buying Agent is waiting for seller-side delivery evidence on Active Service {active['id']}.",
            {"active_service": active},
            [
                "Use belong-check-active-services to inspect obligations and pending evidence.",
                "Use belong-inbox if the buyer-side human needs to authorize a meeting, Change Order, dispute, or payment exception.",
            ],
        )

    request = latest_request_for_buying_agent(state, buyer_agent_id, args.request_id)
    if not request:
        return output(
            "No open Buying Request is ready for the Buying Agent.",
            {"agent": buyer_agent},
            ["Use belong-start-buying-request when the buyer-side human has a new need."],
        )
    if not request.get("search_results"):
        return command_search(
            argparse.Namespace(
                request_id=request["id"],
                query=args.search_query or request.get("need", ""),
                tags=args.tags or "",
                limit=args.limit,
            ),
            state,
        )
    feeds = [state["engagement_feeds"][feed_id] for feed_id in request.get("engagement_feeds", []) if feed_id in state["engagement_feeds"]]
    if not feeds:
        return command_engage(
            argparse.Namespace(
                request_id=request["id"],
                service_ids=None,
                count=args.engage_count or (1 if request.get("mode") == "direct" else 2),
            ),
            state,
        )
    feed = feeds[-1]
    questionnaires = [
        questionnaire
        for questionnaire in state["discovery_questionnaires"].values()
        if questionnaire.get("feed_id") == feed["id"]
    ]
    if any(questionnaire.get("status") == "pending_answer" for questionnaire in questionnaires):
        answers = args.discovery_answers or (
            f"Need: {request.get('need')}. Budget: {request.get('budget')}. "
            f"Timeline: {request.get('timeline')}. Constraints: {', '.join(request.get('constraints', [])) or 'none provided'}."
        )
        return command_answer_discovery(argparse.Namespace(feed_id=feed["id"], answers=answers), state)
    proposals = proposal_ids_for_request(state, request["id"])
    if not proposals:
        return output(
            f"Buying Agent is waiting for Selling Agents to send seller-signed Service Contract/SOW proposals in Engagement Feed {feed['id']}.",
            {"buying_request": request, "engagement_feed": feed, "discovery_questionnaires": questionnaires},
            [
                "The relevant Selling Agent should continue autonomously and create seller-side proposals when inside its Service Playbook.",
                "Use belong-inbox if a seller-side human must approve discovery, scope, or contract behavior.",
            ],
        )
    preferred_id = preferred_proposal_id(state, request["id"])
    if args.sign_best and preferred_id:
        return command_sign(argparse.Namespace(proposal_id=preferred_id, human_approved=False), state)
    return output(
        f"Buying Agent compared proposals for Buying Request {request['id']}.",
        {"buying_request": request, "preferred_proposal_id": preferred_id},
        [
            "The Buying Agent can sign autonomously when the preferred seller-signed Service Contract/SOW fits Standing Authorization.",
            "Use belong-inbox for buyer-side authorization if the proposal exceeds budget, legal, or payment limits.",
        ],
    )


def best_selling_agent(state: dict[str, Any], explicit_id: str | None = None) -> str:
    if explicit_id:
        if explicit_id not in state["agents"]:
            raise ValueError(f"Unknown Selling Agent: {explicit_id}")
        if state["agents"][explicit_id].get("type") != "Selling Agent":
            raise ValueError(f"{explicit_id} is not a Selling Agent.")
        return explicit_id
    selling_agents = [agent_id for agent_id, agent in state["agents"].items() if agent.get("type") == "Selling Agent"]
    if not selling_agents:
        raise ValueError("No Selling Agent exists. Train one with belong-train-selling-agent first.")
    if len(selling_agents) > 1:
        raise ValueError("Multiple Selling Agents exist. Pass --seller-agent-id so the Service Provider human stays oriented to one Service.")
    return selling_agents[0]


def command_run_selling_agent(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    seller_agent_id = best_selling_agent(state, args.seller_agent_id)
    seller_agent = state["agents"][seller_agent_id]
    ensure_agent_can_act(seller_agent, "Selling Agent autonomous work")

    if args.mode == "optimization":
        return command_optimization(argparse.Namespace(agent_id=seller_agent_id), state)

    if args.mode == "active-service" or args.active_service_id:
        active = latest_active_for_agent(state, seller_agent_id, "selling_agent_id", args.active_service_id)
        if not active:
            return output(
                "No seller-side Active Service is ready for the Selling Agent.",
                {"agent": seller_agent},
                [
                    "Use belong-check-selling-pipeline to inspect inbound pre-contract work.",
                    "Use belong-inbox for seller-side escalations or fulfillment tasks.",
                ],
            )
        if not active.get("delivery", {}).get("tasks"):
            return command_active_action(
                argparse.Namespace(
                    active_service_id=active["id"],
                    action="fulfillment-task",
                    actor="Selling Agent",
                    details=args.details or "Prepare kickoff, gather provider inputs, and execute the signed SOW delivery workflow.",
                    owner=args.owner or "Service Provider human/team",
                    due=args.due or "next business day",
                    context=args.context or "Selling Agent created this task to deliver the Active Service.",
                    evidence_required=args.evidence_required or "completion note,deliverable evidence",
                    files=None,
                    links=None,
                    acceptance_mapping=None,
                    deliverable=None,
                    payment_type=None,
                    price_change=None,
                    timeline_change=None,
                    signed=False,
                    human_approved=False,
                    meeting_mode=None,
                ),
                state,
            )
        if not active_has_evidence(active):
            contract = state["contracts"][active["contract_id"]]
            deliverables = contract.get("sow", {}).get("deliverables", [])
            evidence = contract.get("sow", {}).get("evidence_requirements", [])
            return command_active_action(
                argparse.Namespace(
                    active_service_id=active["id"],
                    action="deliver",
                    actor="Selling Agent",
                    details=args.details or "Selling Agent submitted mocked deliverable evidence for buyer acceptance.",
                    owner=None,
                    due=None,
                    context=None,
                    evidence_required=None,
                    files=args.files or "mock-deliverable.pdf",
                    links=args.links or "https://mock.belong/evidence/package",
                    acceptance_mapping=args.acceptance_mapping or ",".join(evidence or deliverables),
                    deliverable=args.deliverable or (deliverables[0] if deliverables else "Service deliverable"),
                    payment_type=None,
                    price_change=None,
                    timeline_change=None,
                    signed=False,
                    human_approved=False,
                    meeting_mode=None,
                ),
                state,
            )
        if active_has_buyer_acceptance(active):
            return command_optimization(argparse.Namespace(agent_id=seller_agent_id), state)
        return output(
            f"Selling Agent is waiting for buyer-side acceptance on Active Service {active['id']}.",
            {"active_service": active},
            [
                "Use belong-check-active-services to inspect evidence and acceptance state.",
                "Use belong-inbox for seller-side dispute, meeting, Change Order, or payment exceptions.",
            ],
        )

    service_ids = [service_id for service_id, service in state["services"].items() if service.get("selling_agent_id") == seller_agent_id]
    if args.service_id:
        if args.service_id not in service_ids:
            raise ValueError(f"Service {args.service_id} is not represented by {seller_agent_id}.")
        service_ids = [args.service_id]
    feeds = [
        feed
        for feed in state["engagement_feeds"].values()
        if set(feed.get("service_ids", [])) & set(service_ids)
    ]
    if not feeds:
        return output(
            f"No inbound Engagement Feed is ready for Selling Agent {seller_agent_id}.",
            {"agent": seller_agent, "service_ids": service_ids},
            [
                "Use belong-check-selling-pipeline to inspect listed Service state.",
                "The Selling Agent waits for Buying Agents to engage the Service after semantic search.",
            ],
        )
    feed = feeds[-1]
    questionnaires = [
        questionnaire
        for questionnaire in state["discovery_questionnaires"].values()
        if questionnaire.get("feed_id") == feed["id"] and questionnaire.get("selling_agent_id") == seller_agent_id
    ]
    if any(questionnaire.get("status") != "answered" for questionnaire in questionnaires):
        return output(
            f"Selling Agent is waiting for buyer discovery answers in Engagement Feed {feed['id']}.",
            {"engagement_feed": feed, "discovery_questionnaires": questionnaires},
            [
                "The Buying Agent should answer seller-led discovery autonomously when inside its Buying Playbook.",
                "Use belong-inbox if seller-side human context is required before proposal creation.",
            ],
        )
    existing = [
        proposal
        for proposal in state["proposals"].values()
        if proposal.get("feed_id") == feed["id"] and proposal.get("selling_agent_id") == seller_agent_id
    ]
    if not existing:
        return command_create_proposals(argparse.Namespace(feed_id=feed["id"]), state)
    if any(proposal.get("status") in {"seller_signed_waiting_buyer_signature", "seller_signed_revised_waiting_buyer_signature"} for proposal in existing):
        return output(
            f"Selling Agent has seller-signed Service Contract/SOW proposal(s) waiting for buyer action in Engagement Feed {feed['id']}.",
            {"engagement_feed": feed, "proposals": existing},
            [
                "Use belong-check-selling-pipeline for seller visibility.",
                "The Buying Agent should compare, negotiate, or sign autonomously when inside its Buying Playbook and Standing Authorization.",
            ],
        )
    return command_optimization(argparse.Namespace(agent_id=seller_agent_id), state)


FORBIDDEN_STEERING_PATTERNS = re.compile(
    r"\b("
    r"permanent|permanently|durable|update playbook|change playbook|retrain|"
    r"increase authority|increase budget|max spend|spend limit|legal terms?|payment rules?|"
    r"sign contract|sign the contract|move money|release payment|charge payment|refund|"
    r"bypass pause|ignore authority|ignore standing authorization"
    r")\b",
    re.IGNORECASE,
)


def record_steering(args: argparse.Namespace, state: dict[str, Any], expected_type: str | None = None, allowed_scopes: set[str] | None = None) -> dict[str, Any]:
    agent = state["agents"].get(args.agent_id)
    if not agent:
        raise ValueError(f"Unknown agent: {args.agent_id}")
    if expected_type and agent.get("type") != expected_type:
        raise ValueError(f"{args.agent_id} is not a {expected_type}.")
    if allowed_scopes and args.scope not in allowed_scopes:
        allowed = ", ".join(sorted(allowed_scopes))
        raise ValueError(f"{expected_type or 'Agent'} steering supports only these scopes: {allowed}.")
    ensure_agent_can_act(agent, "temporary steering")
    if args.scope != "general" and not args.object_id:
        raise ValueError(f"Steering scope {args.scope} requires --object-id.")
    if FORBIDDEN_STEERING_PATTERNS.search(args.instruction):
        raise ValueError(
            "Steering cannot expand authority, change legal/payment limits, move money, sign contracts, bypass pause, or permanently alter a Playbook. Use Inbox for operational approval or training for durable changes."
        )
    if args.object_id:
        scoped_collections = {
            "service": "services",
            "buying_request": "buying_requests",
            "engagement_feed": "engagement_feeds",
            "proposal": "proposals",
            "active_service": "active_services",
        }
        collection_name = scoped_collections.get(args.scope)
        if collection_name and args.object_id not in state[collection_name]:
            raise ValueError(f"Unknown {args.scope}: {args.object_id}")
        if args.scope == "service":
            service = state["services"][args.object_id]
            if service.get("selling_agent_id") != args.agent_id:
                raise ValueError(f"Service {args.object_id} does not belong to {args.agent_id}.")
        if args.scope == "buying_request":
            request = state["buying_requests"][args.object_id]
            if request.get("buying_agent_id") != args.agent_id:
                raise ValueError(f"Buying Request {args.object_id} does not belong to {args.agent_id}.")
        if args.scope == "engagement_feed":
            feed = state["engagement_feeds"][args.object_id]
            request = state["buying_requests"].get(feed.get("buying_request_id"), {})
            linked_agents = set(feed.get("selling_agent_ids", [])) | {request.get("buying_agent_id")}
            if args.agent_id not in linked_agents:
                raise ValueError(f"Engagement Feed {args.object_id} is not linked to {args.agent_id}.")
        if args.scope == "proposal":
            proposal = state["proposals"][args.object_id]
            request = state["buying_requests"].get(proposal.get("buying_request_id"), {})
            linked_agents = {proposal.get("selling_agent_id"), request.get("buying_agent_id")}
            if args.agent_id not in linked_agents:
                raise ValueError(f"Proposal {args.object_id} is not linked to {args.agent_id}.")
        if args.scope == "active_service":
            active = state["active_services"][args.object_id]
            if args.agent_id not in {active.get("buyer_agent_id"), active.get("selling_agent_id")}:
                raise ValueError(f"Active Service {args.object_id} is not linked to {args.agent_id}.")
    steering_id = next_id(state, "steer")
    steering = {
        "id": steering_id,
        "agent_id": args.agent_id,
        "instruction": args.instruction,
        "scope": args.scope,
        "object_id": args.object_id,
        "expires": args.expires,
        "status": "active",
        "created_at": now(),
        "non_durable": True,
    }
    state["steering_instructions"][steering_id] = steering
    agent.setdefault("steering_instructions", []).append(steering_id)
    audit(
        state,
        args.actor,
        "agent.steered",
        "Belong Agent",
        args.agent_id,
        args.instruction,
        {
            "steering_instruction": steering,
            "playbook_version": agent.get("playbook_version"),
            "playbook_rule": "Steering is temporary guidance inside existing Playbook and Standing Authorization.",
            "authority_check": {"result": "temporary_guidance_recorded", "rule": "no_authority_expansion"},
        },
    )
    return output(
        f"Recorded temporary steering instruction {steering_id} for {args.agent_id}.",
        {"steering_instruction": steering, "agent": agent},
        [
            "The instruction is auditable and non-durable.",
            "Use the relevant training skill for durable Playbook changes.",
            "Use belong-inbox for operational approvals or exceptions.",
        ],
    )


def command_steer_agent(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    return record_steering(args, state)


def command_steer_buying_agent(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    return record_steering(args, state, "Buying Agent", {"general", "buying_request", "active_service"})


def command_steer_selling_agent(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    return record_steering(args, state, "Selling Agent", {"general", "service", "engagement_feed", "proposal", "active_service"})


def apply_training_update(
    state: dict[str, Any],
    agent: dict[str, Any],
    actor: str,
    changes: str,
    reason: str,
    event_type: str,
) -> dict[str, Any]:
    previous_version = int(agent.get("playbook_version", 0))
    update_id = next_id(state, "training")
    training_update = {
        "id": update_id,
        "agent_id": agent["id"],
        "previous_playbook_version": previous_version,
        "new_playbook_version": previous_version + 1,
        "changes": changes,
        "reason": reason,
        "created_at": now(),
        "source": "human_training_skill",
    }
    agent["playbook_version"] = previous_version + 1
    agent.setdefault("playbook", {}).setdefault("training_history", []).append(training_update)
    for recommendation in state["training_recommendations"].values():
        if recommendation.get("agent_id") == agent["id"] and recommendation.get("status") == "pending_training_review":
            recommendation["status"] = "reviewed_in_training"
            recommendation["reviewed_at"] = now()
            recommendation["reviewed_by"] = actor
            recommendation["review_notes"] = reason
    audit(
        state,
        actor,
        event_type,
        "Belong Agent",
        agent["id"],
        changes,
        {
            "training_update": training_update,
            "playbook_version": agent.get("playbook_version"),
            "playbook_rule": "Durable Playbook changes happen through training/retraining skills.",
            "authority_check": {"result": "durable_training_update_applied", "rule": "human_training_skill"},
        },
    )
    return training_update


def command_update_buying_playbook(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    agent = state["agents"].get(args.agent_id)
    if not agent:
        raise ValueError(f"Unknown agent: {args.agent_id}")
    if agent.get("type") != "Buying Agent":
        raise ValueError(f"{args.agent_id} is not a Buying Agent.")
    training_update = apply_training_update(state, agent, args.actor, args.changes, args.reason, "buying_agent.retrained")
    return output(
        f"Updated Buying Playbook for {args.agent_id}.",
        {"agent": agent, "training_update": training_update},
        [
            "The durable Buying Playbook change is versioned.",
            "Pause state is preserved; resume through belong-inbox only when the human wants new autonomous work.",
            "Use belong-steer-buying-agent for temporary guidance that should not become durable.",
        ],
    )


def command_update_selling_playbook(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    agent = state["agents"].get(args.agent_id)
    if not agent:
        raise ValueError(f"Unknown agent: {args.agent_id}")
    if agent.get("type") != "Selling Agent":
        raise ValueError(f"{args.agent_id} is not a Selling Agent.")
    if args.service_id not in state["services"]:
        raise ValueError(f"Unknown Service: {args.service_id}")
    if agent.get("service_id") != args.service_id:
        raise ValueError(f"Service {args.service_id} is not represented by {args.agent_id}.")
    training_update = apply_training_update(state, agent, args.actor, args.changes, args.reason, "selling_agent.retrained")
    service = state["services"][args.service_id]
    service.setdefault("training_history", []).append(training_update["id"])
    return output(
        f"Updated Selling Playbook for {args.agent_id}.",
        {"agent": agent, "service": service, "training_update": training_update},
        [
            "The durable Service Playbook change is versioned.",
            "Pause state and Service listing state are preserved.",
            "Use belong-steer-selling-agent for temporary guidance that should not become durable.",
        ],
    )


def command_composite(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    buyer_agent_id = best_buying_agent(state, args.buyer_agent_id)
    ensure_agent_can_act(state["agents"][buyer_agent_id], "Composite Buying Request")
    request_id = next_id(state, "buy_req")
    active_ids = split_list(args.active_service_ids)
    unknown_active = [active_id for active_id in active_ids if active_id not in state["active_services"]]
    if unknown_active:
        raise ValueError(f"Unknown Active Service IDs for Composite Buying Request: {', '.join(unknown_active)}")
    foreign_active = [
        active_id
        for active_id in active_ids
        if state["active_services"][active_id].get("buyer_agent_id") != buyer_agent_id
    ]
    if foreign_active:
        raise ValueError(f"Active Service IDs must belong to Buying Agent {buyer_agent_id}: {', '.join(foreign_active)}")
    max_spend = float(state["agents"][buyer_agent_id]["playbook"]["standing_authorization"].get("max_spend", 0))
    existing_spend = buyer_agent_exposure(state, buyer_agent_id)
    composite_budget = float(args.budget or 0)
    if max_spend and existing_spend + composite_budget > max_spend:
        inbox = add_inbox(
            state,
            "buyer",
            "authorization",
            "Approve Composite Buying Request budget above Standing Authorization",
            f"Composite budget {composite_budget} plus current spend {existing_spend} exceeds max spend {max_spend}.",
            "Buying Agent",
            buyer_agent_id,
            urgency="high",
        )
        audit(
            state,
            "Buying Agent",
            "composite_buying_request.blocked_authority",
            "Buying Agent",
            buyer_agent_id,
            args.goal,
            {
                "playbook_rule": state["agents"][buyer_agent_id]["playbook"].get("contract_authority"),
                "authority_check": {
                    "result": "blocked_requires_buyer_human_authorization",
                    "current_spend": existing_spend,
                    "composite_budget": composite_budget,
                    "threshold": max_spend,
                },
                "inbox_item_id": inbox["id"],
            },
        )
        return output(
            "Composite Buying Request was not created because it exceeds Standing Authorization.",
            {"inbox_item": inbox},
            ["Resolve the authorization inbox item or lower the composite budget."],
        )
    request = {
        "id": request_id,
        "buying_agent_id": buyer_agent_id,
        "need": args.goal,
        "budget": float(args.budget or 0),
        "timeline": args.timeline,
        "constraints": split_list(args.constraints),
        "mode": "composite",
        "is_composite": True,
        "status": "coordinating_active_services",
        "control_state": "agent_controlled",
        "active_service_ids": active_ids,
        "coordination": {
            "dependencies": split_list(args.dependencies),
            "sequencing": args.sequencing,
            "shared_context": args.shared_context,
            "risks": split_list(args.risks),
            "handoffs": split_list(args.handoffs),
            "acceptance": args.acceptance,
            "escalation": args.escalation,
        },
        "created_at": now(),
        "search_results": [],
        "engagement_feeds": [],
    }
    state["buying_requests"][request_id] = request
    audit(state, "Buying Agent", "composite_buying_request.created", "Composite Buying Request", request_id, args.goal, request)
    return output(
        f"Created Composite Buying Request {request_id}.",
        {"composite_buying_request": request},
        [
            "Coordinate dependencies, sequencing, shared context, risks, handoffs, timelines, acceptance, and escalation across Active Services.",
            "Use Provider Optimization to search for better or complementary providers.",
            "Open inbox items for any cross-service human decisions.",
        ],
    )


def command_status(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    pending = [item for item in state["inbox"].values() if item["status"] == "pending"]
    status = {
        "state_path": str(args.state_path),
        "accounts": len(state["accounts"]),
        "organizations": len(state["organizations"]),
        "agents": {
            "buying": len([agent for agent in state["agents"].values() if agent["type"] == "Buying Agent"]),
            "selling": len([agent for agent in state["agents"].values() if agent["type"] == "Selling Agent"]),
            "production": len([agent for agent in state["agents"].values() if agent.get("status") == "production"]),
            "paused": len([agent for agent in state["agents"].values() if agent.get("paused")]),
        },
        "services": len(state["services"]),
        "buying_requests": len(state["buying_requests"]),
        "engagement_feeds": len(state["engagement_feeds"]),
        "proposals": len(state["proposals"]),
        "active_services": len(state["active_services"]),
        "payments": len(state["payments"]),
        "payment_ledgers": {
            active_id: active.get("payment_ledger")
            for active_id, active in state["active_services"].items()
            if active.get("payment_ledger")
        },
        "disputes": len(state["disputes"]),
        "pending_inbox_items": len(pending),
        "notification_events": len(state.get("notification_events", {})),
        "training_recommendations": len(state["training_recommendations"]),
        "steering_instructions": len(state["steering_instructions"]),
        "audit_events": len(state["audit"]),
        "next_attention": pending[:5],
        "privacy_promise": state["marketplace_signals"]["privacy_promise"],
    }
    return output(
        "Loaded Belong mocked marketplace status.",
        {"status": status},
        [
            "If no account exists, run belong-setup-account.",
            "If agents are not in Production, complete buying or selling training.",
            "If Production objects exist, agents continue autonomously inside their Playbooks; humans open Inbox, check buyer/seller pipeline, check Active Services, check Payments, check Reputation, steer temporarily, or retrain as needed.",
        ],
    )


def command_reset(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    state.clear()
    state.update(default_state())
    if args.seed_catalog:
        seed_marketplace_catalog(state)
    return output(
        "Reset mocked Belong marketplace state.",
        {"state": {"version": state["version"], "seeded_services": len(state["services"])}},
        ["Start with account setup or run the full-lifecycle demo scenario."],
    )


def run_full_lifecycle(state: dict[str, Any]) -> dict[str, Any]:
    setup_seller = argparse.Namespace(human_name="Maya Seller", role="seller", org_name="Atlas Automation", org_kind="company", notifications="email,Slack")
    command_setup_account(setup_seller, state)
    selling_args = argparse.Namespace(
        human_name="Maya Seller",
        org_name="Atlas Automation",
        notifications="email,Slack",
        service_name="Customer Success Onboarding Sprint",
        description="A two-week service that designs onboarding journeys, playbooks, and customer success handoffs.",
        tags="customer-success,onboarding,cs-playbook",
        availability="24/7 Selling Agent; human workshops weekdays",
        buyer_personas="Head of CS, founder, operations leader",
        use_cases="new customer onboarding, churn reduction, implementation process",
        discovery_questions="What product and customer segment are we onboarding?;What churn or activation target matters?;What systems and stakeholders are involved?",
        pricing_model="fixed_fee",
        starting_price="9000",
        currency="USD",
        billing_cycle="milestone",
        collections="50% at signature, 50% after accepted deliverables",
        contract_terms="Standard Service Contract/SOW with one revision window and milestone payment.",
        discount_limit="10%",
        scope_limits="No custom software development beyond workflow templates",
        negotiation_limits="Escalate indemnity, discounts above 10%, or timelines under one week.",
        delivery_workflow="Kickoff, discovery, draft journey, review workshop, evidence package, acceptance.",
        deliverables="onboarding journey map,CS handoff playbook,activation metrics dashboard",
        evidence_requirements="links,files,meeting notes,acceptance criteria mapping",
        escalation_paths="workshop scheduling,scope expansion,custom legal terms",
        meeting_rules="Video meeting for kickoff or review workshop.",
        dispute_rules="Agent negotiation first, then Belong Judge.",
        reputation_rules="Accepted delivery improves score; late evidence or poor escalation lowers score.",
        activate=True,
    )
    command_train_selling(selling_args, state)
    setup_buyer = argparse.Namespace(human_name="Nia Buyer", role="buyer", org_name="Quill Health", org_kind="company", notifications="email,WhatsApp")
    command_setup_account(setup_buyer, state)
    buying_args = argparse.Namespace(
        human_name="Nia Buyer",
        org_name="Quill Health",
        org_kind="company",
        notifications="email,WhatsApp",
        goals="improve customer onboarding,reduce implementation delays",
        needed_services="customer success onboarding,operations design",
        provider_preferences="strong reputation,healthcare startup experience",
        blocked_providers="",
        budget="50000",
        max_spend="50000",
        timeline="30 days",
        selection_rules="Prefer best evidence quality and reputation, then price.",
        rfp_rules="Engage at least two providers for competitive work above $5000.",
        negotiation_limits="Seek discount or shorter timeline, escalate legal exceptions.",
        proposal_comparison_rules="Compare scope, price, timing, terms, reputation, and fit.",
        contract_authority="May sign standard SOWs up to $50000.",
        payment_rules="Authorize at signature, release final payment on accepted evidence.",
        acceptance_criteria="journey map delivered,playbook delivered,dashboard delivered,stakeholder review complete",
        escalation_rules="Escalate spend above $50000, unusual legal terms, low-confidence acceptance, or disputes.",
        dispute_posture="Try revision first; open dispute for missed acceptance criteria.",
        rating_rules="Rate after accepted delivery or dispute resolution.",
        optimization_goals="Continuously search for better onboarding and CS providers.",
        activate=True,
    )
    command_train_buying(buying_args, state)
    seed_marketplace_catalog(state)
    buyer_agent_id = best_buying_agent(state)
    request = command_buying_request(
        argparse.Namespace(
            buyer_agent_id=buyer_agent_id,
            need="Find a provider to improve customer onboarding and CS handoffs in 30 days.",
            budget="12000",
            timeline="30 days",
            constraints="healthcare startup,needs evidence package",
            mode="competitive",
            composite=False,
        ),
        state,
    )["objects"]["buying_request"]
    command_search(argparse.Namespace(request_id=request["id"], query="customer success onboarding implementation playbook", tags="customer-success,onboarding", limit=5), state)
    feed = command_engage(argparse.Namespace(request_id=request["id"], service_ids=None, count=2), state)["objects"]["engagement_feed"]
    command_answer_discovery(argparse.Namespace(feed_id=feed["id"], answers="We need a 30-day onboarding redesign for healthcare SMB customers with a concrete evidence package and stakeholder review."), state)
    proposals = command_create_proposals(argparse.Namespace(feed_id=feed["id"]), state)["objects"]["proposals"]
    preferred = proposals[0]["proposal"]["id"]
    command_compare_proposals(argparse.Namespace(request_id=request["id"]), state)
    command_negotiate(argparse.Namespace(proposal_id=preferred, instruction="Ask for a small discount and explicit evidence mapping.", price_delta=None, seller_approved=False), state)
    active = command_sign(argparse.Namespace(proposal_id=preferred, human_approved=False), state)["objects"]["active_service"]
    command_active_action(argparse.Namespace(active_service_id=active["id"], action="fulfillment-task", actor="Selling Agent", details="Schedule kickoff workshop and collect existing onboarding materials.", owner="Maya Seller", due="tomorrow", context="Kickoff prep", evidence_required="calendar invite,source files", files=None, links=None, acceptance_mapping=None, deliverable=None, payment_type=None, price_change=None, timeline_change=None, signed=False, meeting_mode=None, human_approved=False), state)
    command_active_action(argparse.Namespace(active_service_id=active["id"], action="meeting", actor="Buying Agent", details="Kickoff workshop for customer onboarding sprint.", owner=None, due=None, context=None, evidence_required=None, files=None, links=None, acceptance_mapping=None, deliverable=None, payment_type=None, price_change=None, timeline_change=None, signed=False, meeting_mode="video", human_approved=False), state)
    command_active_action(argparse.Namespace(active_service_id=active["id"], action="change-order", actor="Buying Agent and Selling Agent", details="Add one stakeholder enablement session.", owner=None, due=None, context=None, evidence_required=None, files=None, links=None, acceptance_mapping=None, deliverable=None, payment_type=None, price_change="750", timeline_change="extend by 3 days", signed=True, meeting_mode=None, human_approved=False), state)
    command_active_action(argparse.Namespace(active_service_id=active["id"], action="deliver", actor="Selling Agent", details="Delivered onboarding journey, handoff playbook, and dashboard evidence.", owner=None, due=None, context=None, evidence_required=None, files="journey-map.pdf,playbook.docx", links="https://mock.belong/evidence/dashboard", acceptance_mapping="journey map delivered,playbook delivered,dashboard delivered", deliverable="CS Onboarding Sprint Evidence Package", payment_type=None, price_change=None, timeline_change=None, signed=False, meeting_mode=None, human_approved=False), state)
    command_active_action(argparse.Namespace(active_service_id=active["id"], action="accept", actor="Buying Agent", details="Evidence matches SOW acceptance criteria.", owner=None, due=None, context=None, evidence_required=None, files=None, links=None, acceptance_mapping=None, deliverable=None, payment_type=None, price_change=None, timeline_change=None, signed=False, meeting_mode=None, human_approved=False), state)
    command_rate(argparse.Namespace(agent_id=active["selling_agent_id"], score="5", notes="Strong evidence and fast escalation.", linked_object_type="Active Service", linked_object_id=active["id"]), state)
    dispute = command_dispute_open(argparse.Namespace(active_service_id=active["id"], opened_by="seller", reason="Mock post-acceptance dispute over a late extra request outside scope.", evidence="contract scope,change order,meeting notes"), state)["objects"]["dispute"]
    command_dispute_respond(argparse.Namespace(dispute_id=dispute["id"], actor="Buying Agent", response="Buyer acknowledges extra request requires separate Change Order."), state)
    command_judge(argparse.Namespace(dispute_id=dispute["id"], decision="extra_request_requires_new_change_order_no_refund", escalate_human=False, reason=None), state)
    command_judge(argparse.Namespace(dispute_id=dispute["id"], decision=None, escalate_human=True, reason="Seller wants Belong human judge review for pricing precedent."), state)
    command_optimization(argparse.Namespace(agent_id=active["buyer_agent_id"]), state)
    command_optimization(argparse.Namespace(agent_id=active["selling_agent_id"]), state)
    command_composite(
        argparse.Namespace(
            buyer_agent_id=active["buyer_agent_id"],
            goal="Coordinate onboarding redesign with analytics and support enablement.",
            budget="25000",
            timeline="45 days",
            constraints="healthcare,customer data privacy",
            active_service_ids=active["id"],
            dependencies="analytics dashboard before final acceptance,support macros before handoff",
            sequencing="Discovery first, then analytics, then enablement.",
            shared_context="Customer onboarding goals and evidence requirements.",
            risks="scope creep,legal review,timeline conflicts",
            handoffs="dashboard to CS team,playbook to support team",
            acceptance="All Active Services accepted against their SOWs.",
            escalation="Escalate cross-service blockers to buyer-side human.",
        ),
        state,
    )
    command_override(argparse.Namespace(agent_id=active["buyer_agent_id"], action="pause", details="Pause new autonomous provider changes during executive review.", actor="Nia Buyer", approved=False), state)
    return command_status(argparse.Namespace(state_path=state_path(None)), state)


def command_scenario(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    if args.name != "full-lifecycle":
        raise ValueError("Only scenario supported now: full-lifecycle")
    if args.reset:
        state.clear()
        state.update(default_state())
    result = run_full_lifecycle(state)
    result["objects"]["status"]["state_path"] = str(args.state_path)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mock Belong Agent-to-Agent Marketplace backend")
    parser.add_argument("--state", dest="state", default=None, help="Optional explicit JSON state path")
    sub = parser.add_subparsers(dest="command", required=True)

    reset = sub.add_parser("reset")
    reset.add_argument("--seed-catalog", action="store_true")

    sub.add_parser("status")

    setup = sub.add_parser("setup-account")
    setup.add_argument("--human-name", required=True)
    setup.add_argument("--role", choices=["buyer", "seller", "both"], required=True)
    setup.add_argument("--org-name", required=True)
    setup.add_argument("--org-kind", choices=["individual", "company"], default="company")
    setup.add_argument("--notifications", default="email")
    setup.add_argument(
        "--invite",
        action="append",
        default=None,
        metavar="NAME|EMAIL|ROLE",
        help="Invite another human to this account. Repeatable. ROLE one of owner, admin, developer, finance, support, buyer, approver.",
    )

    update_account = sub.add_parser("update-account")
    update_account.add_argument("--account-id")
    update_account.add_argument("--human-name")
    update_account.add_argument("--set-notifications")
    update_account.add_argument("--rename-org")
    update_account.add_argument("--org-id")
    update_account.add_argument("--remove-role", choices=["buyer", "seller"])

    sell = sub.add_parser("train-selling")
    sell.add_argument("--human-name", required=True)
    sell.add_argument("--org-name", required=True)
    sell.add_argument("--notifications", default="email")
    sell.add_argument("--service-name", required=True)
    sell.add_argument("--description", required=True)
    sell.add_argument("--tags", default="")
    sell.add_argument("--availability", default="24/7 Selling Agent availability")
    sell.add_argument("--buyer-personas", default="")
    sell.add_argument("--use-cases", default="")
    sell.add_argument("--discovery-questions", default="")
    sell.add_argument("--pricing-model", default="fixed_fee")
    sell.add_argument("--starting-price", default="5000")
    sell.add_argument("--currency", default="USD")
    sell.add_argument("--billing-cycle", default="milestone")
    sell.add_argument("--collections", default="Collected according to signed Service Contract/SOW")
    sell.add_argument("--contract-terms", default="")
    sell.add_argument("--discount-limit", default="0%")
    sell.add_argument("--scope-limits", default="")
    sell.add_argument("--negotiation-limits", default="")
    sell.add_argument("--delivery-workflow", default="")
    sell.add_argument("--deliverables", default="")
    sell.add_argument("--evidence-requirements", default="")
    sell.add_argument("--escalation-paths", default="")
    sell.add_argument("--meeting-rules", default="")
    sell.add_argument("--dispute-rules", default="")
    sell.add_argument("--reputation-rules", default="")
    sell.add_argument("--human-controlled-actions", default="")
    sell.add_argument("--activate", action="store_true")

    buy = sub.add_parser("train-buying")
    buy.add_argument("--human-name", required=True)
    buy.add_argument("--org-name", required=True)
    buy.add_argument("--org-kind", choices=["individual", "company"], default="company")
    buy.add_argument("--notifications", default="email")
    buy.add_argument("--goals", required=True)
    buy.add_argument("--needed-services", default="")
    buy.add_argument("--provider-preferences", default="")
    buy.add_argument("--blocked-providers", default="")
    buy.add_argument("--budget", default="10000")
    buy.add_argument("--max-spend", default=None)
    buy.add_argument("--timeline", required=True)
    buy.add_argument("--selection-rules", required=True)
    buy.add_argument("--rfp-rules", default="")
    buy.add_argument("--negotiation-limits", default="")
    buy.add_argument("--proposal-comparison-rules", default="")
    buy.add_argument("--contract-authority", required=True)
    buy.add_argument("--payment-rules", required=True)
    buy.add_argument("--acceptance-criteria", required=True)
    buy.add_argument("--escalation-rules", required=True)
    buy.add_argument("--dispute-posture", default="")
    buy.add_argument("--rating-rules", default="")
    buy.add_argument("--optimization-goals", default="")
    buy.add_argument("--human-controlled-actions", default="")
    buy.add_argument("--activate", action="store_true")

    req = sub.add_parser("buying-request")
    req.add_argument("--buyer-agent-id", default=None)
    req.add_argument("--need", required=True)
    req.add_argument("--budget", default=None)
    req.add_argument("--timeline", default=None)
    req.add_argument("--constraints", default="")
    req.add_argument("--mode", choices=["direct", "competitive"], default="competitive")
    req.add_argument("--composite", action="store_true")

    start_req = sub.add_parser("start-buying-request")
    start_req.add_argument("--buyer-agent-id", default=None)
    start_req.add_argument("--need", required=True)
    start_req.add_argument("--budget", default=None)
    start_req.add_argument("--timeline", default=None)
    start_req.add_argument("--constraints", default="")
    start_req.add_argument("--mode", choices=["direct", "competitive"], default="competitive")
    start_req.add_argument("--composite", action="store_true")
    start_req.add_argument("--search-query", default="")
    start_req.add_argument("--tags", default="")
    start_req.add_argument("--limit", type=int, default=5)
    start_req.add_argument("--auto-engage-count", type=int, default=0)

    search = sub.add_parser("search")
    search.add_argument("--request-id", required=True)
    search.add_argument("--query", default="")
    search.add_argument("--tags", default="")
    search.add_argument("--limit", type=int, default=5)

    engage = sub.add_parser("engage")
    engage.add_argument("--request-id", required=True)
    engage.add_argument("--service-ids", default=None)
    engage.add_argument("--count", type=int, default=3)

    answer = sub.add_parser("answer-discovery")
    answer.add_argument("--feed-id", required=True)
    answer.add_argument("--answers", required=True)
    answer.add_argument("--as-human", action="store_true")

    proposals = sub.add_parser("create-proposals")
    proposals.add_argument("--feed-id", required=True)
    proposals.add_argument("--as-human", action="store_true")

    compare = sub.add_parser("compare-proposals")
    compare.add_argument("--request-id", required=True)

    negotiate = sub.add_parser("negotiate")
    negotiate.add_argument("--proposal-id", required=True)
    negotiate.add_argument("--instruction", required=True)
    negotiate.add_argument("--price-delta", default=None)
    negotiate.add_argument("--seller-approved", action="store_true")
    negotiate.add_argument("--as-human", action="store_true")

    sign = sub.add_parser("sign")
    sign.add_argument("--proposal-id", required=True)
    sign.add_argument("--human-approved", action="store_true")
    sign.add_argument("--as-human", action="store_true")

    active = sub.add_parser("active-action")
    active.add_argument("--active-service-id", required=True)
    active.add_argument("--action", choices=["fulfillment-task", "deliver", "accept", "reject", "revise", "dispute", "payment", "change-order", "meeting", "message"], required=True)
    active.add_argument("--actor", default=None)
    active.add_argument("--details", default="")
    active.add_argument("--owner", default=None)
    active.add_argument("--due", default=None)
    active.add_argument("--context", default=None)
    active.add_argument("--evidence-required", default=None)
    active.add_argument("--files", default=None)
    active.add_argument("--links", default=None)
    active.add_argument("--acceptance-mapping", default=None)
    active.add_argument("--deliverable", default=None)
    active.add_argument("--payment-type", default=None)
    active.add_argument("--price-change", default=None)
    active.add_argument("--timeline-change", default=None)
    active.add_argument("--signed", action="store_true")
    active.add_argument("--human-approved", action="store_true")
    active.add_argument("--as-human", action="store_true")
    active.add_argument("--meeting-mode", default=None)
    active.add_argument("--urgency", choices=["normal", "high"], default="normal")

    pmeeting = sub.add_parser("propose-meeting")
    pmeeting.add_argument("--proposal-id", required=True)
    pmeeting.add_argument("--actor", default=None)
    pmeeting.add_argument("--details", default="")
    pmeeting.add_argument("--meeting-mode", default=None)
    pmeeting.add_argument("--urgency", choices=["normal", "high"], default="normal")

    inbox = sub.add_parser("inbox")
    inbox.add_argument("--owner-role", choices=["buyer", "seller", "both", "all"], default="all")
    inbox.add_argument("--status", choices=["pending", "resolved", "all"], default="pending")

    payments = sub.add_parser("payments")
    payments.add_argument("--owner-role", choices=["buyer", "seller", "all"], default="all")
    payments.add_argument("--active-service-id", default=None)

    active_services = sub.add_parser("active-services")
    active_services.add_argument("--owner-role", choices=["buyer", "seller", "all"], default="all")
    active_services.add_argument("--status", choices=["active", "completed", "all"], default="all")

    buying_requests = sub.add_parser("buying-requests")
    buying_requests.add_argument("--buyer-agent-id", default=None)
    buying_requests.add_argument("--status", choices=["open", "signed", "all"], default="all")

    selling_pipeline = sub.add_parser("selling-pipeline")
    selling_pipeline.add_argument("--seller-agent-id", required=True)
    selling_pipeline.add_argument("--service-id", default=None)
    selling_pipeline.add_argument("--status", choices=["open", "proposed", "negotiating", "signed", "all"], default="all")

    run_buying = sub.add_parser("run-buying-agent")
    run_buying.add_argument("--buyer-agent-id", default=None)
    run_buying.add_argument("--request-id", default=None)
    run_buying.add_argument("--active-service-id", default=None)
    run_buying.add_argument("--mode", choices=["next", "pre-contract", "active-service", "optimization", "composite"], default="next")
    run_buying.add_argument("--search-query", default="")
    run_buying.add_argument("--tags", default="")
    run_buying.add_argument("--limit", type=int, default=5)
    run_buying.add_argument("--engage-count", type=int, default=0)
    run_buying.add_argument("--discovery-answers", default="")
    run_buying.add_argument("--sign-best", action="store_true")
    run_buying.add_argument("--goal", default="")
    run_buying.add_argument("--budget", default="0")
    run_buying.add_argument("--timeline", default="")
    run_buying.add_argument("--constraints", default="")
    run_buying.add_argument("--active-service-ids", default="")
    run_buying.add_argument("--dependencies", default="")
    run_buying.add_argument("--sequencing", default="")
    run_buying.add_argument("--shared-context", default="")
    run_buying.add_argument("--risks", default="")
    run_buying.add_argument("--handoffs", default="")
    run_buying.add_argument("--acceptance", default="")
    run_buying.add_argument("--escalation", default="")
    run_buying.add_argument("--details", default="")

    run_selling = sub.add_parser("run-selling-agent")
    run_selling.add_argument("--seller-agent-id", default=None)
    run_selling.add_argument("--service-id", default=None)
    run_selling.add_argument("--active-service-id", default=None)
    run_selling.add_argument("--mode", choices=["next", "pipeline", "active-service", "optimization"], default="next")
    run_selling.add_argument("--details", default="")
    run_selling.add_argument("--owner", default="")
    run_selling.add_argument("--due", default="")
    run_selling.add_argument("--context", default="")
    run_selling.add_argument("--evidence-required", default="")
    run_selling.add_argument("--files", default="")
    run_selling.add_argument("--links", default="")
    run_selling.add_argument("--acceptance-mapping", default="")
    run_selling.add_argument("--deliverable", default="")

    resolve = sub.add_parser("resolve-inbox")
    resolve.add_argument("--item-id", required=True)
    resolve.add_argument("--decision", required=True)
    resolve.add_argument("--notes", default="")
    resolve.add_argument("--actor", default="human")

    flow_control = sub.add_parser("flow-control")
    flow_control.add_argument("--flow-id", required=True)
    flow_control.add_argument("--action", choices=["take", "release", "pause", "resume"], required=True)
    flow_control.add_argument("--details", default="")
    flow_control.add_argument("--actor", default="human")

    override = sub.add_parser("override")
    override.add_argument("--agent-id", required=True)
    override.add_argument("--action", choices=["pause", "resume", "direct-instruction", "cancel-negotiation", "request-meeting", "intervene"], required=True)
    override.add_argument("--flow-id", default=None)
    override.add_argument("--details", default="")
    override.add_argument("--actor", default="human")

    steer = sub.add_parser("steer-agent")
    steer.add_argument("--agent-id", required=True)
    steer.add_argument("--instruction", required=True)
    steer.add_argument("--scope", choices=["general", "service", "buying_request", "engagement_feed", "proposal", "active_service"], default="general")
    steer.add_argument("--object-id", default=None)
    steer.add_argument("--expires", default=None)
    steer.add_argument("--actor", default="human")

    steer_buying = sub.add_parser("steer-buying-agent")
    steer_buying.add_argument("--agent-id", required=True)
    steer_buying.add_argument("--instruction", required=True)
    steer_buying.add_argument("--scope", choices=["general", "buying_request", "active_service"], default="general")
    steer_buying.add_argument("--object-id", default=None)
    steer_buying.add_argument("--expires", default=None)
    steer_buying.add_argument("--actor", default="human")

    steer_selling = sub.add_parser("steer-selling-agent")
    steer_selling.add_argument("--agent-id", required=True)
    steer_selling.add_argument("--instruction", required=True)
    steer_selling.add_argument("--scope", choices=["general", "service", "engagement_feed", "proposal", "active_service"], default="general")
    steer_selling.add_argument("--object-id", default=None)
    steer_selling.add_argument("--expires", default=None)
    steer_selling.add_argument("--actor", default="human")

    update_buying = sub.add_parser("update-buying-playbook")
    update_buying.add_argument("--agent-id", required=True)
    update_buying.add_argument("--changes", required=True)
    update_buying.add_argument("--reason", required=True)
    update_buying.add_argument("--actor", default="human")

    update_selling = sub.add_parser("update-selling-playbook")
    update_selling.add_argument("--agent-id", required=True)
    update_selling.add_argument("--service-id", required=True)
    update_selling.add_argument("--changes", required=True)
    update_selling.add_argument("--reason", required=True)
    update_selling.add_argument("--actor", default="human")

    dispute = sub.add_parser("dispute-open")
    dispute.add_argument("--active-service-id", required=True)
    dispute.add_argument("--opened-by", choices=["buyer", "seller"], required=True)
    dispute.add_argument("--reason", required=True)
    dispute.add_argument("--evidence", default="")

    dispute_response = sub.add_parser("dispute-respond")
    dispute_response.add_argument("--dispute-id", required=True)
    dispute_response.add_argument("--actor", required=True)
    dispute_response.add_argument("--response", required=True)

    judge = sub.add_parser("judge")
    judge.add_argument("--dispute-id", required=True)
    judge.add_argument("--decision", default=None)
    judge.add_argument("--escalate-human", action="store_true")
    judge.add_argument("--reason", default=None)

    sub.add_parser("reputation")

    rate = sub.add_parser("rate")
    rate.add_argument("--agent-id", required=True)
    rate.add_argument("--score", required=True)
    rate.add_argument("--notes", default="")
    rate.add_argument("--linked-object-type", default="manual_rating")
    rate.add_argument("--linked-object-id", default="manual")

    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("--object-id", default=None)
    audit_parser.add_argument("--limit", type=int, default=50)

    explain = sub.add_parser("explain")
    explain.add_argument("--audit-id", required=True)

    optimize = sub.add_parser("optimization")
    optimize.add_argument("--agent-id", required=True)

    composite = sub.add_parser("composite-request")
    composite.add_argument("--buyer-agent-id", default=None)
    composite.add_argument("--goal", required=True)
    composite.add_argument("--budget", default="0")
    composite.add_argument("--timeline", default="")
    composite.add_argument("--constraints", default="")
    composite.add_argument("--active-service-ids", default="")
    composite.add_argument("--dependencies", default="")
    composite.add_argument("--sequencing", default="")
    composite.add_argument("--shared-context", default="")
    composite.add_argument("--risks", default="")
    composite.add_argument("--handoffs", default="")
    composite.add_argument("--acceptance", default="")
    composite.add_argument("--escalation", default="")

    scenario = sub.add_parser("scenario")
    scenario.add_argument("name", choices=["full-lifecycle"])
    scenario.add_argument("--reset", action="store_true")

    return parser


COMMANDS = {
    "reset": command_reset,
    "status": command_status,
    "setup-account": command_setup_account,
    "update-account": command_update_account,
    "train-selling": command_train_selling,
    "train-buying": command_train_buying,
    "buying-request": command_buying_request,
    "start-buying-request": command_start_buying_request,
    "search": command_search,
    "engage": command_engage,
    "answer-discovery": command_answer_discovery,
    "create-proposals": command_create_proposals,
    "compare-proposals": command_compare_proposals,
    "negotiate": command_negotiate,
    "sign": command_sign,
    "active-action": command_active_action,
    "propose-meeting": command_propose_meeting,
    "inbox": command_inbox,
    "payments": command_payments,
    "active-services": command_active_services,
    "buying-requests": command_buying_requests,
    "selling-pipeline": command_selling_pipeline,
    "run-buying-agent": command_run_buying_agent,
    "run-selling-agent": command_run_selling_agent,
    "resolve-inbox": command_resolve_inbox,
    "flow-control": command_flow_control,
    "override": command_override,
    "steer-agent": command_steer_agent,
    "steer-buying-agent": command_steer_buying_agent,
    "steer-selling-agent": command_steer_selling_agent,
    "update-buying-playbook": command_update_buying_playbook,
    "update-selling-playbook": command_update_selling_playbook,
    "dispute-open": command_dispute_open,
    "dispute-respond": command_dispute_respond,
    "judge": command_judge,
    "reputation": command_reputation,
    "rate": command_rate,
    "audit": command_audit,
    "explain": command_explain,
    "optimization": command_optimization,
    "composite-request": command_composite,
    "scenario": command_scenario,
}


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    path = state_path(args.state)
    args.state_path = path
    state = load_state(path)
    try:
        result = COMMANDS[args.command](args, state)
        save_state(path, state)
    except Exception as exc:  # noqa: BLE001 - CLI should return JSON errors for skills.
        error = output(
            f"Belong mock command failed: {exc}",
            {"error": {"type": exc.__class__.__name__, "message": str(exc), "state_path": str(path)}},
            ["Check the lifecycle order and existing object IDs, then continue guided work from status or inbox."],
        )
        print(json.dumps(error, indent=2, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
