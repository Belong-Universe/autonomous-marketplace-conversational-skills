import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "skills" / "marketplace" / "belong-marketplace-runtime" / "scripts" / "belong_mock.py"
SKILLS = ROOT / "skills"


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


def train_ready_buyer(state_path, name="Nia Buyer", org="Quill Health", budget="20000", max_spend="20000", human_controlled_actions=""):
    run_belong(state_path, "setup-account", "--human-name", name, "--role", "buyer", "--org-name", org)
    extra = ["--human-controlled-actions", human_controlled_actions] if human_controlled_actions else []
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
        *extra,
    )


def train_ready_seller(state_path, name="Maya Seller", org="Atlas Automation", service="CS Onboarding Sprint", price="9000", human_controlled_actions=""):
    run_belong(state_path, "setup-account", "--human-name", name, "--role", "seller", "--org-name", org)
    extra = ["--human-controlled-actions", human_controlled_actions] if human_controlled_actions else []
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
        "--category",
        "customer-success",
        "--buyer-personas",
        "Head of Customer Success,COO,founder",
        "--use-cases",
        "customer onboarding,implementation operations,activation improvement",
        "--discovery-questions",
        "What customer segment is in scope?,What systems are involved?,What evidence proves acceptance?",
        "--price",
        price,
        "--contract-terms",
        "Standard Service Contract/SOW with one revision window.",
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
        "Try agent-led revision first; if delivery stays contested, open a Dispute for a Belong admin verdict.",
        "--reputation-rules",
        "Accepted delivery, strong evidence, and fast escalation improve reputation; missed obligations reduce it.",
        "--activate",
        *extra,
    )


def buy_to_proposal(state_path, budget="25000"):
    request = run_belong(state_path, "buying-request", "--need", "customer success onboarding help", "--budget", budget, "--timeline", "30 days")["objects"]["buying_request"]
    run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success onboarding")
    feed = run_belong(state_path, "engage", "--request-id", request["id"], "--count", "1")["objects"]["engagement_feed"]
    run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need onboarding journey and evidence.")
    proposal = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"][0]["proposal"]
    return request, proposal


def execute_basic_active_service(state_path, buyer_budget="25000", buyer_max_spend="25000"):
    train_ready_seller(state_path, price="9000")
    train_ready_buyer(state_path, budget=buyer_budget, max_spend=buyer_max_spend)
    _, proposal = buy_to_proposal(state_path, budget=buyer_budget)
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
            self.assertTrue(state["training_recommendations"])
            self.assertTrue(any(item.get("status") == "resolved" for item in state["disputes"].values()))
            self.assertTrue(any((item.get("resolution") or {}).get("direction") in {"refund_buyer", "release_provider"} for item in state["disputes"].values()))
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
                "--category",
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
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "SOC2 readiness")
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
            results = run_belong(state_path, "search", "--request-id", request["id"], "--query", "SOC2 compliance controls evidence readiness")["objects"]["search_results"]

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
                "--category",
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
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success onboarding")
            feed = run_belong(state_path, "engage", "--request-id", request["id"], "--count", "1")["objects"]["engagement_feed"]
            code, payload = run_belong_raw(state_path, "create-proposals", "--feed-id", feed["id"])
            self.assertNotEqual(code, 0)
            self.assertIn("Discovery must be answered", payload["summary"])

            run_belong(state_path, "answer-discovery", "--feed-id", feed["id"], "--answers", "Need onboarding journey and evidence.")
            first = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"]
            second = run_belong(state_path, "create-proposals", "--feed-id", feed["id"])["objects"]["proposals"]
            self.assertEqual(first[0]["proposal"]["id"], second[0]["proposal"]["id"])

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
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success automation")
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

    def test_decision_explanations_include_playbook_version_for_inbox_and_dispute(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "meeting",
                "--actor",
                "Buying Agent",
                "--details",
                "Kickoff alignment meeting.",
            )
            state = json.loads(state_path.read_text())
            inbox_id = next(item_id for item_id, item in state["inbox"].items() if item["title"] == "Prepare for Human-to-Human Meeting" and item["status"] == "pending")
            run_belong(state_path, "resolve-inbox", "--item-id", inbox_id, "--decision", "approve", "--actor", "Nia Buyer", "--notes", "Meeting prepared.")
            state = json.loads(state_path.read_text())
            inbox_audit_id = next(
                event_id
                for event_id, event in state["audit"].items()
                if event["event_type"] == "inbox.resolved" and event["object_id"] == inbox_id
            )
            explanation = run_belong(state_path, "explain", "--audit-id", inbox_audit_id)["objects"]["decision_explanation"]
            self.assertIsNotNone(explanation["playbook_version"])

            run_belong(state_path, "dispute-open", "--active-service-id", active["id"], "--opened-by", "buyer", "--kind", "deliverable_rejection", "--reason", "Evidence missed acceptance criteria.")
            state = json.loads(state_path.read_text())
            dispute_id = next(iter(state["disputes"]))
            run_belong(state_path, "dispute-review", "--dispute-id", dispute_id)
            run_belong(state_path, "dispute-resolve", "--dispute-id", dispute_id, "--resolution", "refund_buyer")
            state = json.loads(state_path.read_text())
            resolve_audit_id = next(
                event_id
                for event_id, event in state["audit"].items()
                if event["event_type"] == "dispute.resolved"
            )
            resolve_explanation = run_belong(state_path, "explain", "--audit-id", resolve_audit_id)["objects"]["decision_explanation"]
            self.assertIsNotNone(resolve_explanation["playbook_version"])

    def test_dispute_admin_binary_verdict_releases_to_provider(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            opened = run_belong(state_path, "dispute-open", "--active-service-id", active["id"], "--opened-by", "seller", "--kind", "charge_disagreement", "--reason", "Extra request outside the signed scope.", "--evidence", "contract scope,meeting notes")["objects"]["dispute"]
            self.assertEqual(opened["status"], "opened")
            self.assertEqual(opened["kind"], "charge_disagreement")
            state = json.loads(state_path.read_text())
            self.assertEqual(state["active_services"][active["id"]]["status"], "disputed")
            run_belong(state_path, "dispute-review", "--dispute-id", opened["id"])
            state = json.loads(state_path.read_text())
            self.assertEqual(state["disputes"][opened["id"]]["status"], "under_review")
            resolved = run_belong(state_path, "dispute-resolve", "--dispute-id", opened["id"], "--resolution", "release_provider")
            dispute = resolved["objects"]["dispute"]
            self.assertEqual(dispute["status"], "resolved")
            self.assertEqual(dispute["resolution"]["direction"], "release_provider")
            self.assertEqual(dispute["resolution"]["decided_by"], "Belong Admin")
            self.assertEqual(resolved["objects"]["payment_event"]["type"], "release")
            state = json.loads(state_path.read_text())
            self.assertEqual(state["active_services"][active["id"]]["status"], "completed")
            self.assertTrue(any(event["event_type"] == "dispute.resolved" for event in state["audit"].values()))

    def test_dispute_withdraw_restores_prior_active_status(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            prior_status = json.loads(state_path.read_text())["active_services"][active["id"]]["status"]
            opened = run_belong(state_path, "dispute-open", "--active-service-id", active["id"], "--opened-by", "buyer", "--kind", "deliverable_rejection", "--reason", "Deliverable missed acceptance criteria.")["objects"]["dispute"]
            run_belong(state_path, "dispute-withdraw", "--dispute-id", opened["id"], "--reason", "Resolved directly with the provider.")
            state = json.loads(state_path.read_text())
            self.assertEqual(state["disputes"][opened["id"]]["status"], "withdrawn")
            self.assertEqual(state["active_services"][active["id"]]["status"], prior_status)

    def test_paused_agent_blocks_optimization_and_payment(self):
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

    def test_readme_uses_host_resolved_installer_contract(self):
        readme = (ROOT / "README.md").read_text()
        installer = (ROOT / "scripts" / "install-local-skills.sh").read_text()

        self.assertIn("BELONG_SKILLS_DEST", readme)
        self.assertIn("--dest \"$BELONG_SKILLS_DEST\"", readme)
        self.assertIn("current host application", readme)
        self.assertIn("Missing skill destination.", installer)
        self.assertIn("BELONG_SKILLS_DEST", installer)
        self.assertNotIn('${CODEX_HOME:-$HOME/.codex}/skills', readme)
        self.assertNotIn('DEST_DIR="${CODEX_HOME:-$HOME/.codex}/skills"', installer)

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
            "Dispute",
            "Belong admin",
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

    def test_flow_control_cycle_sets_control_state_and_audits(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            flow_id = active["id"]
            taken = run_belong(state_path, "flow-control", "--flow-id", flow_id, "--action", "take", "--actor", "Nia Buyer")
            self.assertEqual(taken["objects"]["flow"]["control_state"], "human_controlled")
            paused = run_belong(state_path, "flow-control", "--flow-id", flow_id, "--action", "pause", "--actor", "Nia Buyer")
            self.assertEqual(paused["objects"]["flow"]["control_state"], "paused")
            resumed = run_belong(state_path, "flow-control", "--flow-id", flow_id, "--action", "resume", "--actor", "Nia Buyer")
            self.assertEqual(resumed["objects"]["flow"]["control_state"], "agent_controlled")
            run_belong(state_path, "flow-control", "--flow-id", flow_id, "--action", "take", "--actor", "Nia Buyer")
            released = run_belong(state_path, "flow-control", "--flow-id", flow_id, "--action", "release", "--actor", "Nia Buyer")
            self.assertEqual(released["objects"]["flow"]["control_state"], "agent_controlled")
            state = json.loads(state_path.read_text())
            self.assertTrue(any(event["event_type"].startswith("flow_control.") for event in state["audit"].values()))

    def test_paused_flow_blocks_agent_action(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path, price="9000")
            train_ready_buyer(state_path, budget="25000", max_spend="25000")
            request = run_belong(state_path, "buying-request", "--need", "customer success onboarding help", "--budget", "25000", "--timeline", "30 days")["objects"]["buying_request"]
            run_belong(state_path, "search", "--request-id", request["id"], "--query", "customer success onboarding")
            run_belong(state_path, "flow-control", "--flow-id", request["id"], "--action", "pause", "--actor", "Nia Buyer")
            code, payload = run_belong_raw(state_path, "engage", "--request-id", request["id"], "--count", "1")
            self.assertNotEqual(code, 0)
            self.assertIn("is paused", payload["summary"])

    def test_human_controlled_flow_blocks_agent_and_requires_take_for_human(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
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
                "Nia Buyer",
                "--as-human",
                "--details",
                "Human accepts before taking control.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("Take control first", payload["summary"])

            run_belong(state_path, "flow-control", "--flow-id", active["id"], "--action", "take", "--actor", "Nia Buyer")
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
                "Agent tries to act on a human-controlled flow.",
            )
            self.assertNotEqual(code, 0)
            self.assertIn("under human control", payload["summary"])

            accepted = run_belong(
                state_path,
                "active-action",
                "--active-service-id",
                active["id"],
                "--action",
                "accept",
                "--actor",
                "Nia Buyer",
                "--as-human",
                "--details",
                "Human accepts after taking control.",
            )["objects"]
            self.assertEqual(accepted["active_service"]["status"], "accepted")

    def test_intervene_override_takes_flow_control(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            active = execute_basic_active_service(state_path)
            buyer_agent_id = active["buyer_agent_id"]
            result = run_belong(
                state_path,
                "override",
                "--agent-id",
                buyer_agent_id,
                "--action",
                "intervene",
                "--flow-id",
                active["id"],
                "--actor",
                "Nia Buyer",
            )
            self.assertIn("control is now human_controlled", result["summary"])
            self.assertEqual(result["objects"]["flow"]["control_state"], "human_controlled")
            state = json.loads(state_path.read_text())
            self.assertEqual(state["active_services"][active["id"]]["control_state"], "human_controlled")

    def test_ineligible_human_controlled_action_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            with self.assertRaises(AssertionError) as ctx:
                train_ready_buyer(state_path, human_controlled_actions="meeting")
            self.assertIn("Ineligible human-controlled action", str(ctx.exception))

    def test_scenario_b_reserved_buyer_sign_routes_to_human_then_human_signs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path, price="9000")
            train_ready_buyer(state_path, budget="25000", max_spend="25000", human_controlled_actions="sign")
            request, proposal = buy_to_proposal(state_path)
            routed = run_belong(state_path, "sign", "--proposal-id", proposal["id"])
            self.assertIn("routed to the buyer-side human", routed["summary"])
            self.assertEqual(routed["objects"]["inbox_item"]["request_type"], "human_performed_action")

            run_belong(state_path, "flow-control", "--flow-id", request["id"], "--action", "take", "--actor", "Nia Buyer")
            active = run_belong(state_path, "sign", "--proposal-id", proposal["id"], "--as-human")["objects"]["active_service"]
            self.assertTrue(active["id"])
            state = json.loads(state_path.read_text())
            self.assertTrue(any(event["event_type"] == "authority.routed_to_human" for event in state["audit"].values()))

    def test_scenario_b_reserved_seller_deliver_routes_to_human(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path, price="9000", human_controlled_actions="deliver")
            train_ready_buyer(state_path, budget="25000", max_spend="25000")
            _, proposal = buy_to_proposal(state_path)
            active = run_belong(state_path, "sign", "--proposal-id", proposal["id"])["objects"]["active_service"]
            routed = run_belong(
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
            self.assertIn("routed to the seller-side human", routed["summary"])
            self.assertEqual(routed["objects"]["inbox_item"]["request_type"], "human_performed_action")

    def test_active_service_inherits_human_control_from_buying_request(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path, price="9000")
            train_ready_buyer(state_path, budget="25000", max_spend="25000")
            request, proposal = buy_to_proposal(state_path)
            run_belong(state_path, "flow-control", "--flow-id", request["id"], "--action", "take", "--actor", "Nia Buyer")
            signed = run_belong(state_path, "sign", "--proposal-id", proposal["id"], "--as-human")
            active = signed["objects"]["active_service"]
            self.assertEqual(active["control_state"], "human_controlled")
            self.assertIn("the human is in control and it will stay that way", signed["summary"])
            state = json.loads(state_path.read_text())
            self.assertTrue(any(event["event_type"] == "flow_control.inherited" for event in state["audit"].values()))

    def test_active_service_stays_agent_controlled_when_agent_signs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            train_ready_seller(state_path, price="9000")
            train_ready_buyer(state_path, budget="25000", max_spend="25000")
            _, proposal = buy_to_proposal(state_path)
            active = run_belong(state_path, "sign", "--proposal-id", proposal["id"])["objects"]["active_service"]
            self.assertEqual(active["control_state"], "agent_controlled")


if __name__ == "__main__":
    unittest.main()
