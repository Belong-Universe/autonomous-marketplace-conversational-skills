import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "skills" / "marketplace" / "belong-marketplace-runtime" / "scripts" / "belong_mock.py"
SKILLS = ROOT / "skills"
INSTALLER = ROOT / "scripts" / "install-local-skills.sh"
SYNC_MIRRORS = ROOT / "scripts" / "sync-skill-mirrors.sh"
MIRROR_ROOTS = [
    ROOT / ".agents" / "skills",
    ROOT / ".claude" / "skills",
]


def skill_path(name):
    matches = [path for path in SKILLS.rglob("SKILL.md") if path.parent.name == name]
    if not matches:
        raise AssertionError(f"Missing skill: {name}")
    if len(matches) > 1:
        raise AssertionError(f"Duplicate skill folder for {name}: {matches}")
    return matches[0]


def run_belong(state_path, *args):
    completed = subprocess.run(
        ["python3", str(RUNTIME), "--state", str(state_path), *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON output:\nSTDOUT={completed.stdout}\nSTDERR={completed.stderr}") from exc
    if completed.returncode != 0:
        raise AssertionError(f"Command failed: {args}\n{json.dumps(payload, indent=2)}\n{completed.stderr}")
    return payload


def run_belong_raw(state_path, *args):
    completed = subprocess.run(
        ["python3", str(RUNTIME), "--state", str(state_path), *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    payload = json.loads(completed.stdout)
    return completed.returncode, payload


def run_installer(*args):
    return subprocess.run(
        [str(INSTALLER), *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def source_skill_dirs():
    return sorted(path.parent for path in SKILLS.rglob("SKILL.md"))


def files_under(path):
    return sorted(candidate.relative_to(path) for candidate in path.rglob("*") if candidate.is_file())


def train_ready_buyer(state_path, name="Nia Buyer", org="Quill Health", budget="20000", max_spend="20000"):
    run_belong(state_path, "setup-account", "--human-name", name, "--role", "buyer", "--org-name", org)
    run_belong(
        state_path,
        "train-buying",
        "--human-name",
        name,
        "--org-name",
        org,
        "--goals",
        "buy reliable expert services",
        "--needed-services",
        "security compliance customer success operations",
        "--budget",
        budget,
        "--max-spend",
        max_spend,
        "--timeline",
        "30 days",
        "--selection-rules",
        "Prefer SOW fit, then reputation, then price.",
        "--rfp-rules",
        "Engage multiple providers for material work.",
        "--proposal-comparison-rules",
        "Compare SOW fit, price, timing, reputation, and evidence.",
        "--contract-authority",
        f"May sign standard SOWs up to {max_spend}.",
        "--payment-rules",
        "Authorize at signature, release final payment on acceptance.",
        "--acceptance-criteria",
        "report delivered,evidence mapped,stakeholder review complete",
        "--escalation-rules",
        f"Escalate spend above {max_spend}, unusual legal terms, and low-confidence acceptance.",
        "--dispute-posture",
        "Request revision first, then open dispute.",
        "--rating-rules",
        "Rate after delivery, dispute, or cancellation.",
        "--optimization-goals",
        "Continuously search for better providers and value.",
        "--activate",
    )


def train_ready_seller(state_path, name="Maya Seller", org="Atlas Automation", service="CS Onboarding Sprint", price="9000"):
    run_belong(state_path, "setup-account", "--human-name", name, "--role", "seller", "--org-name", org)
    return run_belong(
        state_path,
        "train-selling",
        "--human-name",
        name,
        "--org-name",
        org,
        "--service-name",
        service,
        "--description",
        "Customer success onboarding service with journey maps, handoff playbooks, and dashboard evidence.",
        "--tags",
        "customer-success,onboarding,operations",
        "--buyer-personas",
        "Head of Customer Success,COO,founder",
        "--use-cases",
        "customer onboarding,implementation operations,activation improvement",
        "--discovery-questions",
        "What customer segment is in scope?,What systems are involved?,What evidence proves acceptance?",
        "--starting-price",
        price,
        "--billing-cycle",
        "milestone",
        "--collections",
        "50% at signature, 50% on acceptance",
        "--contract-terms",
        "Standard Service Contract/SOW with one revision window.",
        "--discount-limit",
        "10%",
        "--scope-limits",
        "No custom software development",
        "--delivery-workflow",
        "Kickoff, discovery, delivery, evidence, acceptance.",
        "--deliverables",
        "journey map,handoff playbook,dashboard",
        "--evidence-requirements",
        "files,links,acceptance criteria mapping",
        "--escalation-paths",
        "scope expansion,legal exceptions,human workshop",
        "--meeting-rules",
        "Video kickoff and review workshops are allowed when the Service needs human context.",
        "--dispute-rules",
        "Try agent-led revision first, then Belong Judge if delivery remains contested.",
        "--reputation-rules",
        "Accepted delivery, strong evidence, and fast escalation improve reputation; missed obligations reduce it.",
        "--activate",
    )


def execute_basic_active_service(state_path, buyer_budget="25000", buyer_max_spend="25000"):
    train_ready_seller(state_path, price="9000")
    train_ready_buyer(state_path, budget=buyer_budget, max_spend=buyer_max_spend)
    request = run_belong(state_path, "buying-request", "--need", "customer success onboarding help", "--budget", buyer_budget, "--timeline", "30 days")["objects"]["buying_request"]
    run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success onboarding", "--tags", "customer-success")
    feed = run_belong(state_path, "engage", "--request-id", request["id"], "--count", "1")["objects"]["engagement_feed"]
    run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need onboarding journey and evidence.")
    proposal = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"][0]["proposal"]
    return run_belong(state_path, "sign", "--proposal-id", proposal["id"])["objects"]["active_service"]


class BelongSkillPackTests(unittest.TestCase):
    def test_full_lifecycle_scenario_covers_marketplace_surface(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            result = run_belong(state_path, "scenario", "full-lifecycle", "--reset")
            status = result["objects"]["status"]

            self.assertGreaterEqual(status["accounts"], 2)
            self.assertGreaterEqual(status["agents"]["buying"], 1)
            self.assertGreaterEqual(status["agents"]["selling"], 2)
            self.assertGreaterEqual(status["services"], 2)
            self.assertGreaterEqual(status["proposals"], 2)
            self.assertGreaterEqual(status["active_services"], 1)
            self.assertGreaterEqual(status["payments"], 2)
            self.assertGreaterEqual(status["disputes"], 1)
            self.assertGreaterEqual(status["audit_events"], 40)
            self.assertGreaterEqual(status["pending_inbox_items"], 1)

            state = json.loads(state_path.read_text())
            active = next(iter(state["active_services"].values()))
            self.assertTrue(active["delivery"]["tasks"])
            self.assertTrue(active["delivery"]["evidence_packages"])
            self.assertTrue(active["delivery"]["acceptance"])
            self.assertTrue(active["meetings"])
            self.assertTrue(active["change_orders"])
            self.assertTrue(state["training_recommendations"])
            self.assertTrue(any(item.get("judge_decision") for item in state["disputes"].values()))
            self.assertTrue(any(item.get("human_judge_escalation") for item in state["disputes"].values()))
            self.assertTrue(any(req.get("is_composite") for req in state["buying_requests"].values()))
            self.assertTrue(state["notification_events"])

    def test_internal_agent_ticks_advance_marketplace_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path)
            train_ready_buyer(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Buying Agent")
            seller_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Selling Agent")

            started = run_belong(
                state_path,
                "start-buying-request",
                "--buyer-agent-id",
                buyer_agent_id,
                "--need",
                "customer success onboarding help",
                "--budget",
                "20000",
                "--timeline",
                "30 days",
                "--search-query",
                "customer success onboarding",
                "--tags",
                "customer-success",
            )["objects"]["buying_request"]
            feed = run_belong(state_path, "run-buying-agent", "--buyer-agent-id", buyer_agent_id, "--request-id", started["id"])["objects"]["engagement_feed"]
            run_belong(state_path, "run-buying-agent", "--buyer-agent-id", buyer_agent_id, "--request-id", started["id"])
            proposals = run_belong(state_path, "run-selling-agent", "--seller-agent-id", seller_agent_id)["objects"]["proposals"]
            compared = run_belong(state_path, "run-buying-agent", "--buyer-agent-id", buyer_agent_id, "--request-id", started["id"])
            active = run_belong(state_path, "run-buying-agent", "--buyer-agent-id", buyer_agent_id, "--request-id", started["id"], "--sign-best")["objects"]["active_service"]
            run_belong(state_path, "run-selling-agent", "--seller-agent-id", seller_agent_id, "--active-service-id", active["id"], "--mode", "active-service")
            evidence = run_belong(state_path, "run-selling-agent", "--seller-agent-id", seller_agent_id, "--active-service-id", active["id"], "--mode", "active-service")["objects"]["deliverable_evidence_package"]
            acceptance = run_belong(state_path, "run-buying-agent", "--buyer-agent-id", buyer_agent_id, "--active-service-id", active["id"], "--mode", "active-service")["objects"]["delivery_acceptance"]
            state = json.loads(state_path.read_text())

            self.assertEqual(feed["id"], next(iter(state["engagement_feeds"])))
            self.assertTrue(proposals)
            self.assertIn("preferred_proposal_id", compared["objects"])
            self.assertIn(active["id"], state["active_services"])
            self.assertTrue(evidence["id"])
            self.assertEqual(acceptance["decision"], "accept")
            self.assertTrue(any(event["event_type"] == "delivery.accept" for event in state["audit"].values()))

    def test_authority_exception_creates_authorization_inbox_item(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            run_belong(state_path, "setup-account", "--human-name", "Budget Buyer", "--role", "buyer", "--org-name", "Budget Co")
            run_belong(
                state_path,
                "train-buying",
                "--human-name",
                "Budget Buyer",
                "--org-name",
                "Budget Co",
                "--goals",
                "buy compliance help",
                "--budget",
                "1000",
                "--max-spend",
                "1000",
                "--timeline",
                "30 days",
                "--selection-rules",
                "Prefer best fit",
                "--rfp-rules",
                "Engage at least one qualified provider.",
                "--proposal-comparison-rules",
                "Compare SOW fit, price, reputation, and timeline.",
                "--contract-authority",
                "May sign only up to 1000",
                "--payment-rules",
                "Authorize at signature",
                "--acceptance-criteria",
                "report delivered",
                "--escalation-rules",
                "Escalate spend above 1000",
                "--dispute-posture",
                "Open dispute if acceptance criteria are missed.",
                "--rating-rules",
                "Rate after delivery or dispute.",
                "--optimization-goals",
                "Search for better providers after each outcome.",
                "--activate",
            )
            request = run_belong(state_path, "buying-request", "--need", "SOC2 readiness", "--budget", "1000", "--timeline", "30 days")["objects"]["buying_request"]
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "SOC2 readiness", "--tags", "soc2")
            feed = run_belong(state_path, "engage", "--request-id", request["id"], "--count", "1")["objects"]["engagement_feed"]
            run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need SOC2 readiness under a very small budget.")
            proposal = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"][0]["proposal"]
            blocked = run_belong(state_path, "sign", "--proposal-id", proposal["id"])

            self.assertIn("exceeds Standing Authorization", blocked["summary"])
            inbox_item = blocked["objects"]["inbox_item"]
            self.assertEqual(inbox_item["request_type"], "authorization")
            self.assertEqual(inbox_item["owner_role"], "buyer")

    def test_semantic_search_ranks_soc2_service_first(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            run_belong(state_path, "reset", "--seed-catalog")
            train_ready_buyer(state_path, budget="25000", max_spend="25000")
            request = run_belong(state_path, "buying-request", "--need", "Need SOC2 readiness and evidence collection", "--budget", "25000", "--timeline", "45 days")["objects"]["buying_request"]
            results = run_belong(state_path, "search", "--request-id", request["id"], "--query", "SOC2 compliance controls evidence readiness", "--tags", "soc2,security,evidence")["objects"]["search_results"]

            self.assertIn("SOC2", results[0]["service_name"])
            self.assertGreater(results[0]["ranking"]["semantic_fit"], results[-1]["ranking"]["semantic_fit"])

    def test_pause_blocks_new_autonomous_buying_request(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_buyer(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Buying Agent")
            run_belong(state_path, "override", "--agent-id", buyer_agent_id, "--action", "pause", "--actor", "Nia Buyer", "--details", "Pause new autonomous work.")
            code, payload = run_belong_raw(
                state_path,
                "steer-buying-agent",
                "--agent-id",
                buyer_agent_id,
                "--instruction",
                "Prefer lower-cost providers for the current search.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("is paused", payload["summary"])

            train_ready_buyer(state_path)
            state = json.loads(state_path.read_text())
            self.assertTrue(state["agents"][buyer_agent_id]["paused"])
            self.assertEqual(state["agents"][buyer_agent_id]["status"], "paused")

            code, payload = run_belong_raw(state_path, "buying-request", "--buyer-agent-id", buyer_agent_id, "--need", "Find a new provider")

            self.assertNotEqual(code, 0)
            self.assertIn("is paused", payload["summary"])

            code, payload = run_belong_raw(state_path, "start-buying-request", "--buyer-agent-id", buyer_agent_id, "--need", "Find a new provider")

            self.assertNotEqual(code, 0)
            self.assertIn("is paused", payload["summary"])

    def test_start_buying_request_creates_search_and_optional_engagement(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path)
            train_ready_buyer(state_path)
            result = run_belong(
                state_path,
                "start-buying-request",
                "--need",
                "Need customer success onboarding help",
                "--budget",
                "20000",
                "--timeline",
                "30 days",
                "--search-query",
                "customer success onboarding",
                "--tags",
                "customer-success",
                "--auto-engage-count",
                "1",
            )["objects"]
            state = json.loads(state_path.read_text())

            self.assertIn("buying_request", result)
            self.assertTrue(result["search_results"])
            self.assertIn("engagement_feed", result)
            self.assertIn(result["buying_request"]["id"], state["buying_requests"])
            self.assertIn(result["engagement_feed"]["id"], state["engagement_feeds"])
            self.assertTrue(any(event["event_type"] == "buying_request.started_by_human_intent" for event in state["audit"].values()))

    def test_incomplete_selling_playbook_cannot_activate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            run_belong(state_path, "setup-account", "--human-name", "Maya Seller", "--role", "seller", "--org-name", "Atlas Automation")
            result = run_belong(
                state_path,
                "train-selling",
                "--human-name",
                "Maya Seller",
                "--org-name",
                "Atlas Automation",
                "--service-name",
                "Thin Service",
                "--description",
                "A thin service with missing operating rules.",
                "--contract-terms",
                "Standard SOW.",
                "--delivery-workflow",
                "Deliver work.",
                "--deliverables",
                "report",
                "--evidence-requirements",
                "file",
                "--activate",
            )

            self.assertEqual(result["objects"]["agent"]["status"], "validation")
            self.assertEqual(result["objects"]["service"]["status"], "draft")
            self.assertIn("buyer_personas", result["objects"]["validation"]["missing"])
            self.assertIn("meeting_rules", result["objects"]["validation"]["missing"])
            self.assertIn("dispute_rules", result["objects"]["validation"]["missing"])
            self.assertIn("reputation_rules", result["objects"]["validation"]["missing"])

    def test_engagement_requires_prior_search_result(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path)
            train_ready_buyer(state_path)
            request = run_belong(state_path, "buying-request", "--need", "customer success onboarding help", "--budget", "20000", "--timeline", "30 days")["objects"]["buying_request"]
            state = json.loads(state_path.read_text())
            service_id = next(iter(state["services"]))
            code, payload = run_belong_raw(state_path, "engage", "--request-id", request["id"], "--service-ids", service_id)

            self.assertNotEqual(code, 0)
            self.assertIn("Run semantic search", payload["summary"])

    def test_discovery_required_and_proposals_are_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path)
            train_ready_buyer(state_path)
            request = run_belong(state_path, "buying-request", "--need", "customer success onboarding help", "--budget", "20000", "--timeline", "30 days")["objects"]["buying_request"]
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success onboarding", "--tags", "customer-success")
            feed = run_belong(state_path, "engage", "--request-id", request["id"], "--count", "1")["objects"]["engagement_feed"]
            code, payload = run_belong_raw(state_path, "create-proposals", "--feed-id", feed["id"])
            self.assertNotEqual(code, 0)
            self.assertIn("Discovery must be answered", payload["summary"])

            run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need onboarding journey and evidence.")
            first = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"]
            second = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"]
            self.assertEqual(first[0]["proposal"]["id"], second[0]["proposal"]["id"])

    def test_seller_discount_authority_blocks_excess_discount(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path, price="9000")
            train_ready_buyer(state_path)
            request = run_belong(state_path, "buying-request", "--need", "customer success onboarding help", "--budget", "20000", "--timeline", "30 days")["objects"]["buying_request"]
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success onboarding", "--tags", "customer-success")
            feed = run_belong(state_path, "engage", "--request-id", request["id"], "--count", "1")["objects"]["engagement_feed"]
            run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need onboarding journey and evidence.")
            proposal = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"][0]["proposal"]
            blocked = run_belong(state_path, "negotiate", "--proposal-id", proposal["id"], "--instruction", "Apply a large discount.", "--price-delta", "-2000")

            self.assertIn("exceeds Selling Agent Standing Authorization", blocked["summary"])
            self.assertEqual(blocked["objects"]["inbox_item"]["owner_role"], "seller")

    def test_inbox_approved_change_order_preserves_payment_ledger(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "change-order",
                "--actor",
                "Buying Agent and Selling Agent",
                "--details",
                "Add an enablement workshop.",
                "--price-change",
                "3000",
            )
            state = json.loads(state_path.read_text())
            inbox_id = next(item_id for item_id, item in state["inbox"].items() if item["title"] == "Approve Change Order" and item["status"] == "pending")
            run_belong(state_path, "resolve-inbox", "--item-id", inbox_id, "--decision", "approve", "--actor", "Nia Buyer", "--notes", "Approved workshop amendment.")
            state = json.loads(state_path.read_text())
            active_after = state["active_services"][active["id"]]
            ledger = active_after["payment_ledger"]

            self.assertEqual(ledger["contract_amount"], 12000.0)
            self.assertEqual(ledger["authorized"], 12000.0)
            self.assertEqual(ledger["collected"], 6000.0)
            self.assertEqual(ledger["platform_fee_accrued"], 480.0)
            self.assertTrue(any(payment["type"] == "authorization_delta" for payment in state["payments"].values()))

    def test_pending_change_order_counts_against_signature_authority(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path, buyer_budget="15000", buyer_max_spend="15000")
            run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "change-order",
                "--actor",
                "Buying Agent and Selling Agent",
                "--details",
                "Large scope expansion.",
                "--price-change",
                "7000",
            )
            train_ready_seller(state_path, service="CS Evidence Review", price="6000")
            request = run_belong(state_path, "buying-request", "--need", "customer success evidence review", "--budget", "15000", "--timeline", "30 days")["objects"]["buying_request"]
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success evidence review", "--tags", "customer-success")
            state = json.loads(state_path.read_text())
            service_id = next(service_id for service_id, service in state["services"].items() if service["name"] == "CS Evidence Review")
            feed = run_belong(state_path, "engage", "--request-id", request["id"], "--service-ids", service_id)["objects"]["engagement_feed"]
            run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need additional evidence review.")
            proposal = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"][0]["proposal"]
            blocked = run_belong(state_path, "sign", "--proposal-id", proposal["id"])

            self.assertIn("exceeds Standing Authorization", blocked["summary"])
            authority = blocked["objects"]["inbox_item"]["metadata"]["authority_check"]
            self.assertEqual(authority["current_spend"], 16000.0)

    def test_composite_budget_and_active_ownership_are_enforced(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path, buyer_budget="20000", buyer_max_spend="20000")
            run_belong(
                state_path,
                "composite-request",
                "--buyer-agent-id",
                active["buyer_agent_id"],
                "--goal",
                "Coordinate providers for onboarding launch.",
                "--budget",
                "5000",
                "--active-service-ids",
                active["id"],
                "--dependencies",
                "handoff data",
                "--acceptance",
                "launch accepted",
            )
            train_ready_seller(state_path, service="CS Automation Sprint", price="10000")
            request = run_belong(state_path, "buying-request", "--need", "customer success automation sprint", "--budget", "20000", "--timeline", "30 days")["objects"]["buying_request"]
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success automation", "--tags", "customer-success")
            state = json.loads(state_path.read_text())
            service_id = next(service_id for service_id, service in state["services"].items() if service["name"] == "CS Automation Sprint")
            feed = run_belong(state_path, "engage", "--request-id", request["id"], "--service-ids", service_id)["objects"]["engagement_feed"]
            run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need automation sprint.")
            proposal = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"][0]["proposal"]
            blocked = run_belong(state_path, "sign", "--proposal-id", proposal["id"])
            self.assertIn("exceeds Standing Authorization", blocked["summary"])

            train_ready_buyer(state_path, name="Omar Buyer", org="Other Co", budget="20000", max_spend="20000")
            state = json.loads(state_path.read_text())
            other_buyer_agent_id = next(
                agent_id
                for agent_id, agent in state["agents"].items()
                if agent["type"] == "Buying Agent" and agent["name"] == "Omar Buyer Buying Agent"
            )
            code, payload = run_belong_raw(
                state_path,
                "composite-request",
                "--buyer-agent-id",
                other_buyer_agent_id,
                "--goal",
                "Use another buyer active service.",
                "--budget",
                "1000",
                "--active-service-ids",
                active["id"],
            )
            self.assertNotEqual(code, 0)
            self.assertIn("must belong to Buying Agent", payload["summary"])

    def test_decision_explanations_include_playbook_version_for_inbox_and_judge(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "change-order",
                "--actor",
                "Buying Agent and Selling Agent",
                "--details",
                "Add manager training.",
                "--price-change",
                "1000",
            )
            state = json.loads(state_path.read_text())
            inbox_id = next(item_id for item_id, item in state["inbox"].items() if item["title"] == "Approve Change Order" and item["status"] == "pending")
            run_belong(state_path, "resolve-inbox", "--item-id", inbox_id, "--decision", "approve", "--actor", "Nia Buyer", "--notes", "Approved amendment.")
            state = json.loads(state_path.read_text())
            inbox_audit_id = next(
                event_id
                for event_id, event in state["audit"].items()
                if event["event_type"] == "inbox.resolved" and event["object_id"] == inbox_id
            )
            explanation = run_belong(state_path, "explain", "--audit-id", inbox_audit_id)["objects"]["decision_explanation"]
            self.assertIsNotNone(explanation["playbook_version"])

            run_belong(state_path, "dispute-open", "--active-service-id", active["id"], "--opened-by", "buyer", "--reason", "Evidence missed acceptance criteria.")
            state = json.loads(state_path.read_text())
            dispute_id = next(iter(state["disputes"]))
            run_belong(state_path, "judge", "--dispute-id", dispute_id, "--decision", "seller_revision_required")
            state = json.loads(state_path.read_text())
            judge_audit_id = next(
                event_id
                for event_id, event in state["audit"].items()
                if event["event_type"] == "dispute.judge_decision"
            )
            judge_explanation = run_belong(state_path, "explain", "--audit-id", judge_audit_id)["objects"]["decision_explanation"]
            self.assertIsNotNone(judge_explanation["playbook_version"])

    def test_paused_agent_blocks_optimization_payment_and_change_order(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = active["buyer_agent_id"]
            seller_agent_id = active["selling_agent_id"]
            run_belong(state_path, "override", "--agent-id", buyer_agent_id, "--action", "pause", "--actor", "Nia Buyer", "--details", "Pause buyer.")
            for command in [
                ("optimization", "--agent-id", buyer_agent_id),
                ("active-action", "--active-service-id", active["id"], "--action", "payment", "--payment-type", "hold"),
                ("active-action", "--active-service-id", active["id"], "--action", "change-order", "--price-change", "1000", "--signed"),
            ]:
                code, payload = run_belong_raw(state_path, *command)
                self.assertNotEqual(code, 0)
                self.assertIn("is paused", payload["summary"])

            run_belong(state_path, "override", "--agent-id", buyer_agent_id, "--action", "resume", "--actor", "Nia Buyer")
            run_belong(state_path, "override", "--agent-id", seller_agent_id, "--action", "pause", "--actor", "Maya Seller", "--details", "Pause seller.")
            code, payload = run_belong_raw(state_path, "optimization", "--agent-id", seller_agent_id)
            self.assertNotEqual(code, 0)
            self.assertIn("is paused", payload["summary"])

    def test_active_service_role_permissions_block_wrong_side_actions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            code, payload = run_belong_raw(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "accept",
                "--actor",
                "Nia Buyer",
                "--details",
                "Buyer tries to accept before evidence exists.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("requires a Deliverable Evidence Package", payload["summary"])

            code, payload = run_belong_raw(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "deliver",
                "--actor",
                "Nia Buyer",
                "--deliverable",
                "Buyer-submitted evidence",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("requires seller authority", payload["summary"])

            run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "deliver",
                "--actor",
                "Maya Seller",
                "--deliverable",
                "Seller evidence package",
                "--files",
                "evidence.pdf",
                "--acceptance-mapping",
                "report delivered",
            )
            code, payload = run_belong_raw(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "accept",
                "--actor",
                "Maya Seller",
                "--details",
                "Seller tries to accept its own work.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("requires buyer authority", payload["summary"])

            accepted = run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "accept",
                "--actor",
                "Nia Buyer",
                "--details",
                "Buyer accepts mapped evidence.",
            )["objects"]
            self.assertEqual(accepted["active_service"]["status"], "accepted")
            self.assertEqual(accepted["payment_event"]["type"], "release")

    def test_direct_payment_release_requires_evidence_and_acceptance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            alias_payment = run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "payment",
                "--actor",
                "Nia Buyer",
                "--payment-type",
                "authorize",
                "--details",
                "Friendly alias for authorization.",
            )["objects"]["payment_event"]
            self.assertEqual(alias_payment["type"], "authorization")

            code, payload = run_belong_raw(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "payment",
                "--actor",
                "Nia Buyer",
                "--payment-type",
                "release",
                "--details",
                "Try to release before delivery.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("requires deliverable evidence", payload["summary"])

            run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "deliver",
                "--actor",
                "Maya Seller",
                "--deliverable",
                "Seller evidence package",
                "--files",
                "evidence.pdf",
                "--acceptance-mapping",
                "report delivered",
            )
            code, payload = run_belong_raw(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "payment",
                "--actor",
                "Nia Buyer",
                "--payment-type",
                "release",
                "--details",
                "Try to release before acceptance.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("requires buyer acceptance", payload["summary"])

            run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "payment",
                "--actor",
                "Nia Buyer",
                "--payment-type",
                "release",
                "--details",
                "Human-approved exception for manual release.",
                "--human-approved",
            )
            state = json.loads(state_path.read_text())
            payment_audit = next(
                event
                for event in reversed(list(state["audit"].values()))
                if event["event_type"] == "payment.release"
            )
            authority = payment_audit["details"]["authority_check"]
            self.assertEqual(authority["result"], "human_approved_exception")
            self.assertTrue(authority["human_approved"])

    def test_retraining_paused_seller_preserves_pause_and_unlists_service(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path)
            state = json.loads(state_path.read_text())
            seller_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Selling Agent")
            service_id = state["agents"][seller_agent_id]["service_id"]
            run_belong(state_path, "override", "--agent-id", seller_agent_id, "--action", "pause", "--actor", "Maya Seller", "--details", "Pause seller.")
            train_ready_seller(state_path)
            state = json.loads(state_path.read_text())

            self.assertTrue(state["agents"][seller_agent_id]["paused"])
            self.assertEqual(state["agents"][seller_agent_id]["status"], "paused")
            self.assertEqual(state["services"][service_id]["status"], "paused")
            ready_items = [
                item
                for item in state["inbox"].values()
                if item["title"] == "Selling Agent ready for marketplace" and item["linked_object_id"] == service_id and item["status"] == "pending"
            ]
            self.assertFalse(ready_items)

    def test_optimization_creates_training_recommendation_not_inbox_work(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_buyer(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Buying Agent")
            result = run_belong(state_path, "optimization", "--agent-id", buyer_agent_id)
            state = json.loads(state_path.read_text())

            self.assertIn("training_recommendation", result["objects"])
            self.assertTrue(state["training_recommendations"])
            self.assertFalse(any(item["request_type"].startswith("playbook") for item in state["inbox"].values()))

    def test_read_only_payment_and_active_service_commands_do_not_change_objects(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = active["buyer_agent_id"]
            seller_agent_id = active["selling_agent_id"]
            before = json.loads(state_path.read_text())
            payments = run_belong(state_path, "payments", "--owner-role", "all", "--active-service-id", active["id"])["objects"]
            active_services = run_belong(state_path, "active-services", "--owner-role", "all", "--status", "all")["objects"]
            buying_requests = run_belong(state_path, "buying-requests", "--buyer-agent-id", buyer_agent_id, "--status", "all")["objects"]
            selling_pipeline = run_belong(state_path, "selling-pipeline", "--seller-agent-id", seller_agent_id, "--status", "all")["objects"]
            after = json.loads(state_path.read_text())
            before.pop("updated_at", None)
            after.pop("updated_at", None)

            self.assertTrue(payments["payments"])
            self.assertTrue(active_services["active_services"])
            self.assertTrue(buying_requests["buying_requests"])
            self.assertTrue(selling_pipeline["selling_pipeline"])
            self.assertEqual(before, after)

    def test_steer_agent_records_temporary_guidance_without_playbook_change(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_buyer(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Buying Agent")
            version_before = state["agents"][buyer_agent_id]["playbook_version"]
            playbook_before = state["agents"][buyer_agent_id]["playbook"]
            steering = run_belong(
                state_path,
                "steer-buying-agent",
                "--agent-id",
                buyer_agent_id,
                "--instruction",
                "Prefer faster providers for the next search.",
                "--scope",
                "general",
                "--expires",
                "tomorrow",
            )["objects"]["steering_instruction"]
            state = json.loads(state_path.read_text())

            self.assertTrue(steering["non_durable"])
            self.assertEqual(state["agents"][buyer_agent_id]["playbook_version"], version_before)
            self.assertEqual(state["agents"][buyer_agent_id]["playbook"], playbook_before)
            self.assertIn(steering["id"], state["agents"][buyer_agent_id]["steering_instructions"])

            code, payload = run_belong_raw(
                state_path,
                "steer-buying-agent",
                "--agent-id",
                buyer_agent_id,
                "--instruction",
                "Increase max spend and change payment rules.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("Steering cannot expand authority", payload["summary"])

    def test_role_specific_steering_rejects_wrong_agent_type(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_buyer(state_path)
            train_ready_seller(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Buying Agent")
            seller_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Selling Agent")

            code, payload = run_belong_raw(
                state_path,
                "steer-buying-agent",
                "--agent-id",
                seller_agent_id,
                "--instruction",
                "Prefer faster responses.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("is not a Buying Agent", payload["summary"])

            code, payload = run_belong_raw(
                state_path,
                "steer-selling-agent",
                "--agent-id",
                buyer_agent_id,
                "--instruction",
                "Prefer faster responses.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("is not a Selling Agent", payload["summary"])

    def test_retraining_commands_version_playbooks_and_preserve_pause(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_buyer(state_path)
            train_ready_seller(state_path)
            state = json.loads(state_path.read_text())
            buyer_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Buying Agent")
            seller_agent_id = next(agent_id for agent_id, agent in state["agents"].items() if agent["type"] == "Selling Agent")
            service_id = state["agents"][seller_agent_id]["service_id"]
            buyer_version = state["agents"][buyer_agent_id]["playbook_version"]
            seller_version = state["agents"][seller_agent_id]["playbook_version"]

            run_belong(state_path, "override", "--agent-id", buyer_agent_id, "--action", "pause", "--actor", "Nia Buyer", "--details", "Pause buyer.")
            run_belong(state_path, "override", "--agent-id", seller_agent_id, "--action", "pause", "--actor", "Maya Seller", "--details", "Pause seller.")
            run_belong(
                state_path,
                "update-buying-playbook",
                "--agent-id",
                buyer_agent_id,
                "--changes",
                "Prefer shorter timelines for onboarding providers.",
                "--reason",
                "Buyer retraining request.",
                "--actor",
                "Nia Buyer",
            )
            run_belong(
                state_path,
                "update-selling-playbook",
                "--agent-id",
                seller_agent_id,
                "--service-id",
                service_id,
                "--changes",
                "Tighten evidence requirements for dashboard deliverables.",
                "--reason",
                "Seller retraining request.",
                "--actor",
                "Maya Seller",
            )
            state = json.loads(state_path.read_text())

            self.assertTrue(state["agents"][buyer_agent_id]["paused"])
            self.assertTrue(state["agents"][seller_agent_id]["paused"])
            self.assertEqual(state["services"][service_id]["status"], "paused")
            self.assertEqual(state["agents"][buyer_agent_id]["playbook_version"], buyer_version + 1)
            self.assertEqual(state["agents"][seller_agent_id]["playbook_version"], seller_version + 1)
            self.assertTrue(state["agents"][buyer_agent_id]["playbook"]["training_history"])
            self.assertTrue(state["agents"][seller_agent_id]["playbook"]["training_history"])

    def test_repeated_selling_training_does_not_duplicate_ready_inbox(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path)
            train_ready_seller(state_path)
            state = json.loads(state_path.read_text())
            ready_items = [
                item
                for item in state["inbox"].values()
                if item["title"] == "Selling Agent ready for marketplace" and item["status"] == "pending"
            ]
            self.assertEqual(len(ready_items), 1)

    def test_installer_and_docs_use_host_native_destinations(self):
        readme = (ROOT / "README.md").read_text()
        llms = (ROOT / "llms.txt").read_text()
        llms_full = (ROOT / "llms-full.txt").read_text()
        handoff = (ROOT / "AGENT_HANDOFF.md").read_text()
        manifest = json.loads((ROOT / "agent-manifest.json").read_text())
        installer = INSTALLER.read_text()

        self.assertIn("BELONG_SKILLS_DEST", readme)
        self.assertIn("--host codex --scope repo", readme)
        self.assertIn("--host cursor --scope repo", readme)
        self.assertIn("--host claude-code --scope repo", readme)
        self.assertIn("--host other-ai", readme)
        self.assertIn("Other AI Hosts", readme)
        self.assertIn("--host other-ai", llms)
        self.assertIn("Other AI Hosts", llms_full)
        self.assertIn("Other AI Hosts", handoff)
        self.assertIn(".agents/skills", readme)
        self.assertIn(".claude/skills", readme)
        self.assertIn("Missing skill destination.", installer)
        self.assertIn("--host codex|cursor|claude-code|other-ai|custom", installer)
        self.assertIn("Other AI hosts are welcome", installer)
        self.assertIn("BELONG_SKILLS_DEST", installer)
        self.assertTrue(manifest["other_ai_hosts_supported"])
        self.assertTrue(manifest["other_ai_requires_explicit_destination"])
        self.assertIn("--host other-ai", manifest["other_ai_command"])
        self.assertNotIn('${CODEX_HOME:-$HOME/.codex}/skills', readme)
        self.assertNotIn('DEST_DIR="${CODEX_HOME:-$HOME/.codex}/skills"', installer)

    def test_skill_mirrors_exist_and_match_source(self):
        sources = source_skill_dirs()
        self.assertEqual(len(sources), 18)

        for mirror_root in MIRROR_ROOTS:
            self.assertTrue(mirror_root.exists(), f"Missing mirror root: {mirror_root}")
            mirrored_names = sorted(path.parent.name for path in mirror_root.rglob("SKILL.md"))
            source_names = sorted(path.name for path in sources)
            self.assertEqual(mirrored_names, source_names)

            for source in sources:
                mirror = mirror_root / source.name
                self.assertTrue((mirror / "SKILL.md").exists(), f"Missing mirrored SKILL.md: {mirror}")
                self.assertEqual(files_under(mirror), files_under(source), f"Mirror file drift: {mirror}")
                for relative_file in files_under(source):
                    self.assertEqual(
                        (mirror / relative_file).read_bytes(),
                        (source / relative_file).read_bytes(),
                        f"Mirror content drift: {mirror / relative_file}",
                    )

    def test_sync_skill_mirrors_script_is_present(self):
        text = SYNC_MIRRORS.read_text()
        self.assertIn(".agents/skills", text)
        self.assertIn(".claude/skills", text)
        self.assertIn("Missing skill folder", text)

    def test_installer_host_repo_dry_runs(self):
        cases = [
            ("codex", ".agents/skills"),
            ("cursor", ".agents/skills"),
            ("claude-code", ".claude/skills"),
        ]
        for host, expected_destination in cases:
            completed = run_installer("--host", host, "--scope", "repo", "--dry-run")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn(expected_destination, completed.stdout)
            self.assertIn("Installing/updating Belong skills", completed.stdout)

    def test_installer_custom_host_requires_destination(self):
        completed = run_installer("--host", "custom", "--dry-run")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Missing skill destination.", completed.stderr)

    def test_installer_other_ai_requires_explicit_destination(self):
        missing_destination = run_installer("--host", "other-ai", "--dry-run")
        self.assertNotEqual(missing_destination.returncode, 0)
        self.assertIn("Missing skill destination.", missing_destination.stderr)
        self.assertIn("Other AI Hosts", missing_destination.stderr)

        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "other-ai-skills"
            completed = run_installer("--host", "other-ai", "--dest", str(dest), "--dry-run")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn(str(dest), completed.stdout)
            self.assertIn("Installing/updating Belong skills", completed.stdout)

    def test_installer_backs_up_existing_destination_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "skills"
            first = run_installer("--dest", str(dest))
            second = run_installer("--dest", str(dest))

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("Backed up replaced skills to", second.stdout)
            backup_root = dest / ".belong-skill-backups"
            self.assertTrue(any(backup_root.iterdir()))

    def test_public_copy_avoids_agent_command_phrasing(self):
        public_files = [
            ROOT / "README.md",
            ROOT / "llms.txt",
            ROOT / "llms-full.txt",
            ROOT / "AGENT_HANDOFF.md",
            ROOT / "agent-manifest.json",
            ROOT / "index.html",
        ]
        banned_patterns = [
            r"Do not stop at summary",
            r"Do not stop at summarizing",
            r"Act when your host permits",
            r"execution contract",
            r"Treat it as an instruction surface",
            r"This page is meant for you, agent, to read and execute",
            r"Welcome, agent\. This .* execute",
        ]
        for path in public_files:
            text = path.read_text()
            for pattern in banned_patterns:
                self.assertIsNone(re.search(pattern, text), f"{path} contains banned copy: {pattern}")

    def test_public_and_internal_skill_docs_mark_their_surfaces(self):
        public_read_check = [
            skill_path("belong-check-active-services"),
            skill_path("belong-check-payments"),
            skill_path("belong-check-reputation"),
            skill_path("belong-check-buying-requests"),
            skill_path("belong-check-selling-pipeline"),
        ]
        for path in public_read_check:
            text = path.read_text()
            self.assertIn("read/check", text)
            self.assertNotIn("Run runtime `active-action`", text)
            self.assertNotIn("Run runtime `sign`", text)
            self.assertNotIn("Run runtime `negotiate`", text)

        internal_skills = [
            skill_path("belong-internal-buying-workflow"),
            skill_path("belong-internal-selling-workflow"),
            skill_path("belong-internal-active-service-actions"),
            skill_path("belong-internal-disputes"),
        ]
        for path in internal_skills:
            self.assertIn("internal", path.read_text().lower())

        guide = skill_path("belong-marketplace-guide").read_text()
        runtime_docs = (SKILLS / "marketplace" / "belong-marketplace-runtime" / "references" / "runtime-commands.md").read_text()
        self.assertNotIn("$belong-steer-agent", guide)
        self.assertNotIn("skills/belong-steer-agent", (ROOT / "README.md").read_text())
        self.assertIn("$belong-steer-buying-agent", guide)
        self.assertIn("$belong-steer-selling-agent", guide)
        self.assertNotIn("$belong-run-buying-agent", guide)
        self.assertNotIn("$belong-run-selling-agent", guide)
        self.assertIn("start-buying-request", runtime_docs)
        self.assertIn("run-buying-agent", runtime_docs)
        self.assertIn("run-selling-agent", runtime_docs)
        self.assertIn("internal mock agent tick commands", runtime_docs)
        self.assertIn("selling-pipeline", runtime_docs)

    def test_skill_docs_have_required_coverage_terms_and_no_todos(self):
        text = "\n".join(path.read_text() for path in SKILLS.rglob("*.md"))
        self.assertNotIn("TODO", text)
        required_terms = [
            "OAuth",
            "Buying Agent",
            "Selling Agent",
            "Service Playbook",
            "Buying Playbook",
            "Standing Authorization",
            "Buying Request",
            "semantic",
            "Engagement Feed",
            "Discovery Questionnaire",
            "seller-signed Service Contract/SOW",
            "Active Service",
            "Marketplace Inbox",
            "Fulfillment Task",
            "Human-to-Human Meeting",
            "Deliverable Evidence Package",
            "Delivery Acceptance",
            "Change Order",
            "Dispute",
            "Belong Judge",
            "Agent Reputation",
            "Audit Log",
            "Decision Explanation",
            "Composite Buying Request",
            "Provider Optimization",
            "Selling Optimization",
            "Marketplace Privacy Promise",
            "Marketplace Learning Boundary",
            "Steering Instruction",
            "Training Recommendation",
            "autonomously",
            "internal mock agent tick commands",
        ]
        missing = [term for term in required_terms if term not in text]
        self.assertFalse(missing, f"Missing coverage terms: {missing}")


if __name__ == "__main__":
    unittest.main()
